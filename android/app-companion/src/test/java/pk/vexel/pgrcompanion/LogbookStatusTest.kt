package pk.vexel.pgrcompanion

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import org.junit.Assert.assertEquals
import org.junit.Test

class LogbookStatusTest {
    @Test fun aliasesAreSummedWithoutLosingOtherStates() {
        val statuses = listOf("VERIFIED", " approved ", "verified", "RETURNED", " returned_for_revision ", "REJECTED", "CANCELLED", "new_status", "")
        val rows = statuses.map { Json.parseToJsonElement("""{"status":"$it"}""").jsonObject }
        assertEquals(mapOf("APPROVED" to 3, "RETURNED" to 2, "REJECTED" to 1, "CANCELLED" to 1, "NEW_STATUS" to 1, "" to 1), logbookCounts(rows))
        assertEquals(emptyMap<String, Int>(), logbookCounts(emptyList()))
    }
}
