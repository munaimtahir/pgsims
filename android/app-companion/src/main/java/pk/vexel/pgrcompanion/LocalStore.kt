package pk.vexel.pgrcompanion

import android.content.Context
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.io.File
import java.util.UUID

@Serializable data class ResidentProfile(val fullName: String, val institution: String = "", val programme: String = "", val specialty: String = "", val department: String = "", val startDate: String = "", val completionDate: String = "", val trainingYear: String = "", val supervisor: String = "", val coSupervisor: String = "", val registrationNumber: String = "", val email: String = "", val phone: String = "", val notes: String = "")
@Serializable data class Rotation(val id: String = UUID.randomUUID().toString(), val title: String, val unit: String = "", val institution: String = "", val startDate: String = "", val endDate: String = "", val supervisor: String = "", val status: String = "Planned", val notes: String = "")
@Serializable data class ActivityRecord(val id: String = UUID.randomUUID().toString(), val type: String, val title: String, val date: String = "", val location: String = "", val description: String = "")
@Serializable data class Milestone(val id: String = UUID.randomUUID().toString(), val title: String, val category: String = "General", val dueDate: String = "", val status: String = "Not Started", val completionDate: String = "", val notes: String = "")
@Serializable data class StoredDocument(val id: String = UUID.randomUUID().toString(), val title: String, val category: String, val filename: String, val path: String, val addedDate: String)

/**
 * [dueAtMillis] is the scheduled alarm time. It defaults to null so records written by 1.0.0, which
 * had no scheduling at all, still deserialize — those reminders simply stay unscheduled.
 */
@Serializable data class ReminderRecord(val id: String = UUID.randomUUID().toString(), val title: String, val dueDate: String, val kind: String = "Task", val completed: Boolean = false, val dueAtMillis: Long? = null)

@Serializable data class AppData(val profile: ResidentProfile? = null, val rotations: List<Rotation> = emptyList(), val activities: List<ActivityRecord> = emptyList(), val milestones: List<Milestone> = emptyList(), val documents: List<StoredDocument> = emptyList(), val reminders: List<ReminderRecord> = emptyList())

/**
 * The Personal Workspace's only persistence primitive. Deliberately narrow so the store can be
 * exercised in a plain JVM test with no Android framework, which is what lets the workspace
 * isolation tests assert that institutional code never reaches this data.
 */
interface LocalStorage {
    fun read(): String?
    fun write(value: String)
    fun clear()
}

private class PreferenceStorage(context: Context) : LocalStorage {
    private val prefs = context.applicationContext.getSharedPreferences("pgr_companion_local", Context.MODE_PRIVATE)
    override fun read(): String? = prefs.getString(KEY, null)
    override fun write(value: String) { prefs.edit().putString(KEY, value).apply() }
    override fun clear() { prefs.edit().clear().apply() }
    companion object { private const val KEY = "app_data" }
}

/** Test/in-memory backing. Also the safe fallback if preferences are unreadable. */
class InMemoryStorage(private var value: String? = null) : LocalStorage {
    override fun read(): String? = value
    override fun write(value: String) { this.value = value }
    override fun clear() { value = null }
}

/**
 * Local, device-only residency records. This is the source of truth for the Personal Workspace and
 * for nothing else: no institutional code reads or writes it, and signing out of an institution
 * leaves every record here untouched.
 */
class LocalStore(
    private val storage: LocalStorage,
    private val documentsDir: File? = null,
) {
    constructor(context: Context) : this(
        PreferenceStorage(context),
        context.applicationContext.filesDir.resolve(DOCUMENTS_DIR),
    )

    private val json = Json { ignoreUnknownKeys = true }

    // A corrupt or partially-written blob must not take the app down on launch; an empty workspace
    // is recoverable, a boot loop is not.
    private var data: AppData = runCatching { json.decodeFromString<AppData>(storage.read() ?: "") }
        .getOrDefault(AppData())

    fun read(): AppData = data

    fun save(value: AppData) {
        data = value
        runCatching { storage.write(json.encodeToString(value)) }
    }

    /** Removes every personal record and every stored file from this standalone app. */
    fun clear() {
        data.documents.forEach { runCatching { File(it.path).delete() } }
        data = AppData()
        storage.clear()
        documentsDir?.let { runCatching { it.deleteRecursively() } }
    }

    companion object { const val DOCUMENTS_DIR = "documents" }
}
