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
 * action or confirmed server persistence.  Automatic replay is intentionally not implemented
 * until the backend accepts idempotency keys for these create operations.
 */
@Serializable
internal data class OfflineDraft(
    val id: String = UUID.randomUUID().toString(),
    val kind: String,
    val leave: LeaveRequestPayload? = null,
    val logbook: AcademicLogbookPayload? = null,
    val createdAtMillis: Long = System.currentTimeMillis(),
)

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

    fun saveLeave(payload: LeaveRequestPayload) = save(OfflineDraft(kind = "leave", leave = payload))
    fun saveLogbook(payload: AcademicLogbookPayload) = save(OfflineDraft(kind = "logbook", logbook = payload))
    fun remove(id: String) { preferences.edit().remove(id).apply() }
    /** Logout is a hard ownership boundary for recoverable institutional work. */
    fun clear() { preferences.edit().clear().apply() }

    private fun save(draft: OfflineDraft) {
        preferences.edit().putString(draft.id, json.encodeToString(draft)).apply()
    }
}
