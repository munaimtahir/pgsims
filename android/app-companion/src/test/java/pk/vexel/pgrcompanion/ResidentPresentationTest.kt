package pk.vexel.pgrcompanion

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ResidentPresentationTest {
    private fun objectOf(raw: String) = Json.parseToJsonElement(raw) as JsonObject

    @Test fun `onboarding summary retains backend outstanding requirements and document correction`() {
        val onboarding = objectOf(
            """{
              "review_status":"CORRECTION_REQUIRED",
              "supervisor_status":"PENDING",
              "profile_complete":false,
              "declaration_accepted":true,
              "onboarding_complete":false,
              "required_onboarding_fields":["phone"],
              "sections":[{"fields":[{"field":"phone","label":"Contact number"}]}],
              "documents":[{"title":"CNIC Copy","status":"REUPLOAD_REQUIRED"}]
            }""".trimIndent(),
        )

        val summary = OnboardingSummary.from(onboarding)

        assertEquals("Correction required", InstitutionalLabels.reviewStatus(summary.reviewStatus))
        assertTrue(summary.outstanding.contains("Complete Contact number"))
        assertTrue(summary.outstanding.any { it.contains("Replace CNIC Copy") })
        assertTrue(summary.outstanding.any { it.contains("Supervisor assignment") })
    }

    @Test fun `document state copy makes resident action unambiguous`() {
        assertEquals("Upload", InstitutionalLabels.documentAction("NOT_STARTED"))
        assertEquals("Replace", InstitutionalLabels.documentAction("REUPLOAD_REQUIRED"))
        assertEquals("Correction required", InstitutionalLabels.documentStatus("REUPLOAD_REQUIRED"))
        assertTrue(InstitutionalLabels.documentNeedsAction("REJECTED"))
        assertFalse(InstitutionalLabels.documentNeedsAction("VERIFIED"))
        assertTrue(InstitutionalLabels.replacementNeedsConfirmation("PENDING_REVIEW"))
    }

    @Test fun `workflow statuses use resident language rather than backend enum names`() {
        assertEquals("Correction required", residentStatus("RETURNED"))
        assertEquals("Under review", residentStatus("UNDER_REVIEW"))
        assertEquals("Approved", residentStatus("VERIFIED"))
        assertEquals("In progress", residentStatus("IN_PROGRESS"))
    }
}
