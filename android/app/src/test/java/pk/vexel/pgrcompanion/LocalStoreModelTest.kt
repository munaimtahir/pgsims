package pk.vexel.pgrcompanion

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class LocalStoreModelTest {
    private val json = Json { ignoreUnknownKeys = true }

    @Test fun appData_roundTripsProfileAndRecords() {
        val original = AppData(
            profile = ResidentProfile("A Resident", institution = "City Hospital", programme = "FCPS"),
            rotations = listOf(Rotation(title = "Medicine", status = "Ongoing")),
            activities = listOf(ActivityRecord(type = "Workshop", title = "Research methods")),
            milestones = listOf(Milestone(title = "Synopsis submitted")),
            reminders = listOf(ReminderRecord(title = "Supervisor meeting", dueDate = "12 Sep 2026")),
        )
        val restored = json.decodeFromString<AppData>(json.encodeToString(original))
        assertEquals(original, restored)
    }

    @Test fun patientData_isNotPartOfTheLocalModel() {
        val serialized = json.encodeToString(AppData(profile = ResidentProfile("Resident")))
        assertTrue(serialized.contains("Resident"))
        assertTrue(!serialized.contains("patient", ignoreCase = true))
        assertTrue(!serialized.contains("mrNumber", ignoreCase = true))
    }
}
