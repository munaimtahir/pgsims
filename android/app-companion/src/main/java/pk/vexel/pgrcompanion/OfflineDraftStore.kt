package pk.vexel.pgrcompanion

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.util.UUID

/**
 * Small encrypted, app-private holding area for work created while PGR SIMS is unreachable.
 * Drafts are never mixed with the personal workspace and are only removed after explicit user
 * action or confirmed server persistence. Replay uses stable backend idempotency keys.
 */
@Serializable
internal data class OfflineDraft(
    val id: String = UUID.randomUUID().toString(),
    val kind: String,
    val leave: LeaveRequestPayload? = null,
    val logbook: AcademicLogbookPayload? = null,
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

internal class OfflineDraftStore(context: Context) {
    private val json = Json { ignoreUnknownKeys = true }
    private val preferences = EncryptedSharedPreferences.create(
        context.applicationContext,
        "institutional_offline_drafts",
        MasterKey.Builder(context.applicationContext).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
    )

    fun all(): List<OfflineDraft> = preferences.all.values.mapNotNull { raw ->
        (raw as? String)?.let { runCatching { json.decodeFromString<OfflineDraft>(it) }.getOrNull() }
    }.sortedByDescending { it.createdAtMillis }

    fun saveLeave(payload: LeaveRequestPayload, ownerUserId: Int) = save(OfflineDraft(kind = "leave", leave = payload, ownerUserId = ownerUserId))
    fun saveLogbook(payload: AcademicLogbookPayload, ownerUserId: Int) = save(OfflineDraft(kind = "logbook", logbook = payload, ownerUserId = ownerUserId))
    fun update(draft: OfflineDraft) = save(draft)
    fun remove(id: String) { check(preferences.edit().remove(id).commit()) }
    /** Logout is a hard ownership boundary for recoverable institutional work. */
    fun clear() { check(preferences.edit().clear().commit()) }

    private fun save(draft: OfflineDraft) {
        check(preferences.edit().putString(draft.id, json.encodeToString(draft)).commit()) {
            "Could not durably retain the offline draft."
        }
    }
}
