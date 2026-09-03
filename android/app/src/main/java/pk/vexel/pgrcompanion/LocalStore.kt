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
@Serializable data class ReminderRecord(val id: String = UUID.randomUUID().toString(), val title: String, val dueDate: String, val kind: String = "Task", val completed: Boolean = false)
@Serializable data class AppData(val profile: ResidentProfile? = null, val rotations: List<Rotation> = emptyList(), val activities: List<ActivityRecord> = emptyList(), val milestones: List<Milestone> = emptyList(), val documents: List<StoredDocument> = emptyList(), val reminders: List<ReminderRecord> = emptyList())

class LocalStore(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences("pgr_companion_local", Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }
    private var data: AppData = runCatching { json.decodeFromString<AppData>(prefs.getString(KEY, "") ?: "") }.getOrDefault(AppData())
    fun read(): AppData = data
    fun save(value: AppData) { data = value; prefs.edit().putString(KEY, json.encodeToString(value)).apply() }
    fun clear(context: Context) {
        data.documents.forEach { File(it.path).delete() }
        data = AppData(); prefs.edit().clear().apply()
        context.filesDir.resolve("documents").deleteRecursively()
    }
    companion object { private const val KEY = "app_data" }
}
