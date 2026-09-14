package pk.vexel.pgrcompanion

import android.content.Context
import androidx.security.crypto.EncryptedFile
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.io.File
import java.io.InputStream
import java.util.UUID

/**
 * Encrypted, app-private upload queue.  A selected document is staged before any network work,
 * so an interrupted foreground upload never loses the source material.  The document id is the
 * server-owned target; the UUID identifies this local retry record and is useful in support logs
 * without exposing a filename or content.
 */
@Serializable
internal data class OfflineUpload(
    val id: String = UUID.randomUUID().toString(),
    val documentId: Int,
    val displayName: String,
    val mimeType: String,
    val sizeBytes: Long,
    val ownerUserId: Int? = null,
    val state: String = QUEUED,
    val attempts: Int = 0,
    val lastError: String? = null,
    val createdAtMillis: Long = System.currentTimeMillis(),
) {
    companion object {
        const val QUEUED = "queued"
        const val UPLOADING = "uploading"
        const val FAILED = "failed"
    }
}

internal class OfflineUploadStore(context: Context) {
    private val app = context.applicationContext
    private val json = Json { ignoreUnknownKeys = true }
    private val key = MasterKey.Builder(app).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
    private val preferences = EncryptedSharedPreferences.create(
        app, "institutional_offline_uploads", key,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
    )
    private val directory = File(app.filesDir, "institutional_upload_queue").also { it.mkdirs() }

    init {
        val metadataIds = preferences.all.keys
        directory.listFiles()?.filterNot { it.name in metadataIds }?.forEach(File::delete)
        preferences.all.forEach { (id, raw) ->
            if (raw !is String || runCatching { json.decodeFromString<OfflineUpload>(raw) }.isFailure) {
                preferences.edit().remove(id).commit()
                File(directory, id).delete()
            }
        }
    }

    fun all(): List<OfflineUpload> = preferences.all.values.mapNotNull { raw ->
        (raw as? String)?.let { runCatching { json.decodeFromString<OfflineUpload>(it) }.getOrNull() }
    }.sortedBy { it.createdAtMillis }

    fun stage(documentId: Int, displayName: String, mimeType: String, ownerUserId: Int, input: InputStream): OfflineUpload {
        val id = UUID.randomUUID().toString()
        val encrypted = encryptedFile(id)
        val size = encrypted.openFileOutput().use { output -> input.copyTo(output) }
        val upload = OfflineUpload(id, documentId, displayName, mimeType, size, ownerUserId)
        try {
            save(upload)
        } catch (failure: Throwable) {
            File(directory, id).delete()
            throw failure
        }
        return upload
    }

    fun open(upload: OfflineUpload): InputStream = encryptedFile(upload.id).openFileInput()
    fun update(upload: OfflineUpload) = save(upload)
    fun remove(upload: OfflineUpload) {
        preferences.edit().remove(upload.id).commit()
        File(directory, upload.id).delete()
    }

    /** Logout is a hard ownership boundary: no queued institutional material survives it. */
    fun clear() {
        all().forEach(::remove)
        directory.listFiles()?.forEach { it.delete() }
    }

    private fun save(upload: OfflineUpload) {
        check(preferences.edit().putString(upload.id, json.encodeToString(upload)).commit()) {
            "Could not durably retain the upload queue record."
        }
    }
    private fun encryptedFile(id: String) = EncryptedFile.Builder(
        app, File(directory, id), key, EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB,
    ).build()
}
