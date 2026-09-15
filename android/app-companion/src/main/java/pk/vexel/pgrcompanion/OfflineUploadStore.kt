package pk.vexel.pgrcompanion

import android.content.Context
import android.system.Os
import android.system.OsConstants
import androidx.security.crypto.EncryptedFile
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.io.File
import java.io.InputStream
import java.io.RandomAccessFile
import java.util.UUID

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

/** All instances share a lock: reconciliation must never delete an in-flight stage. */
internal class OfflineUploadStore(
    context: Context,
    private val commitMetadata: (android.content.SharedPreferences.Editor) -> Boolean = { it.commit() },
) {
    private val app = context.applicationContext
    private val json = Json { ignoreUnknownKeys = true }
    private val key = MasterKey.Builder(app).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
    private val preferences = EncryptedSharedPreferences.create(
        app, "institutional_offline_uploads", key,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
    )
    private val directory = File(app.filesDir, "institutional_upload_queue").also { it.mkdirs() }

    init { synchronized(lock) {
        val valid = all().filter { File(directory, it.id).isFile }.map { it.id }.toSet()
        directory.listFiles()?.filter { it.name !in valid }?.forEach { check(it.delete()) }
        preferences.all.keys.filter { it !in valid }.forEach {
            check(preferences.edit().remove(it).commit()) { "Could not reconcile upload metadata." }
        }
        app.cacheDir.listFiles()?.filter { it.name.startsWith("pgr-upload-") }?.forEach { check(it.delete()) }
    } }

    fun all(): List<OfflineUpload> = synchronized(lock) {
        preferences.all.values.mapNotNull { raw ->
            (raw as? String)?.let { runCatching { json.decodeFromString<OfflineUpload>(it) }.getOrNull() }
        }.sortedBy { it.createdAtMillis }
    }

    fun stage(documentId: Int, displayName: String, mimeType: String, ownerUserId: Int, input: InputStream): OfflineUpload = synchronized(lock) {
        val id = UUID.randomUUID().toString()
        try {
            val size = encryptedFile(id).openFileOutput().use { output -> input.copyTo(output) }
            // Closing finalizes authenticated encryption; sync ciphertext and directory before
            // committing metadata. Returning from stage is the durable acknowledgment.
            RandomAccessFile(File(directory, id), "rw").use { it.fd.sync() }
            val fd = Os.open(directory.path, OsConstants.O_RDONLY, 0)
            try { Os.fsync(fd) } finally { Os.close(fd) }
            OfflineUpload(id, documentId, displayName, mimeType, size, ownerUserId).also(::save)
        } catch (failure: Throwable) {
            preferences.edit().remove(id).commit()
            File(directory, id).delete()
            throw failure
        }
    }

    fun open(upload: OfflineUpload): InputStream = synchronized(lock) { encryptedFile(upload.id).openFileInput() }
    fun update(upload: OfflineUpload) = synchronized(lock) {
        // A removed item may never be resurrected by a late retry callback.
        if (preferences.contains(upload.id)) save(upload)
    }
    fun remove(upload: OfflineUpload) = synchronized(lock) {
        check(preferences.edit().remove(upload.id).commit()) { "Could not remove upload metadata." }
        val file = File(directory, upload.id)
        check(!file.exists() || file.delete()) { "Could not remove encrypted document." }
    }
    fun clear() = synchronized(lock) {
        check(preferences.edit().clear().commit()) { "Could not clear upload metadata." }
        directory.listFiles()?.forEach { check(it.delete()) }
    }
    private fun save(upload: OfflineUpload) {
        check(commitMetadata(preferences.edit().putString(upload.id, json.encodeToString(upload)))) {
            "Could not persist encrypted upload metadata. Please select the document again."
        }
    }
    private fun encryptedFile(id: String) = EncryptedFile.Builder(
        app, File(directory, id), key, EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB,
    ).build()
    companion object { private val lock = Any() }
}
