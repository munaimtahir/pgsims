package pk.vexel.pgrcompanion

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import org.junit.Assert.*
import org.junit.Test

class OnboardingPolicyTest {
    private fun body(raw: String) = Json.parseToJsonElement(raw) as JsonObject

    @Test fun documentStatesExposeTheCorrectActionAndConfirmation() {
        val labels = mapOf("NOT_STARTED" to "Not uploaded", "DEFERRED" to "Deferred", "UPLOADED" to "Uploaded", "PENDING_REVIEW" to "Under review", "VERIFIED" to "Approved", "REJECTED" to "Rejected", "REUPLOAD_REQUIRED" to "Correction required", "FUTURE_STATE" to "Future state", "" to "Unknown")
        for ((raw, label) in labels) {
            assertEquals(label, InstitutionalLabels.documentStatus(raw.lowercase()))
            assertEquals(raw in setOf("NOT_STARTED", "DEFERRED", "REUPLOAD_REQUIRED", "REJECTED"), InstitutionalLabels.documentNeedsAction(raw))
            assertEquals(raw in setOf("VERIFIED", "PENDING_REVIEW", "UPLOADED"), InstitutionalLabels.replacementNeedsConfirmation(raw))
            assertEquals(if (raw in setOf("NOT_STARTED", "DEFERRED")) "Upload" else "Replace", InstitutionalLabels.documentAction(raw))
        }
    }

    @Test fun reviewSupervisorAndWorkflowLabelsPreserveUnknownStates() {
        for ((value, expected) in mapOf("NOT_SUBMITTED" to "Not submitted", "PENDING_REVIEW" to "Under review", "APPROVED" to "Approved", "CORRECTION_REQUIRED" to "Correction required", "" to "Not available", "NEW_STATE" to "New state")) assertEquals(expected, InstitutionalLabels.reviewStatus(value))
        for ((value, expected) in mapOf("ASSIGNED" to "Assigned", "PENDING" to "Awaiting confirmation", "NOT_STARTED" to "Not assigned yet", "NOT_ASSIGNED" to "Not assigned yet", "" to "Not assigned yet", "NEW_STATE" to "New state")) assertEquals(expected, InstitutionalLabels.supervisorStatus(value))
        for ((value, expected) in mapOf("DRAFT" to "Draft", "SUBMITTED" to "Submitted", "UNDER_REVIEW" to "Under review", "RETURNED" to "Returned for revision", "APPROVED" to "Approved", "VERIFIED" to "Approved", "REJECTED" to "Rejected", "CANCELLED" to "Cancelled", "COMPLETED" to "Completed", "" to "Unknown", "NEW_STATE" to "New state")) assertEquals(expected, InstitutionalLabels.workflowStatus(value))
    }

    @Test fun editableFieldsAndAdministrativeValuesHaveExplicitPolicies() {
        for (field in OnboardingFieldPolicy.RESIDENT_EDITABLE) {
            assertTrue(OnboardingFieldPolicy.isEditable(field))
            assertNull(OnboardingFieldPolicy.readOnlyReason(field))
        }
        for (field in OnboardingFieldPolicy.REFERENCE) {
            assertFalse(OnboardingFieldPolicy.isEditable(field))
            assertEquals("Maintained in PGR SIMS.", OnboardingFieldPolicy.readOnlyReason(field))
            assertEquals("Recorded", OnboardingFieldPolicy.displayValue(field, "42"))
            assertEquals("Not set", OnboardingFieldPolicy.displayValue(field, ""))
            assertEquals("Hospital name", OnboardingFieldPolicy.displayValue(field, "42", "Hospital name"))
        }
        for (field in OnboardingFieldPolicy.ADMINISTRATIVE_DATE) assertEquals("Part of your training record, maintained in PGR SIMS.", OnboardingFieldPolicy.readOnlyReason(field))
        assertEquals("Maintained in PGR SIMS.", OnboardingFieldPolicy.readOnlyReason("future_field"))
        assertEquals("Not set", OnboardingFieldPolicy.displayValue("phone", " ", ""))
        assertEquals("123", OnboardingFieldPolicy.displayValue("phone", "123"))
    }

    @Test fun missingAndCompletedPayloadsDoNotInventMissingRequirements() {
        assertEquals(OnboardingSummary(), OnboardingSummary.from(null))
        val complete = OnboardingSummary.from(body("""{"supervisor_status":"ASSIGNED","declaration_accepted":true,"profile_complete":true,"onboarding_complete":true,"review_status":"APPROVED","review_note":"Reviewed"}"""))
        assertFalse(complete.hasOutstanding)
        assertTrue(complete.profileComplete)
        assertTrue(complete.onboardingComplete)
        assertEquals("Reviewed", complete.reviewNote)
        val empty = OnboardingSummary.from(body("{}"))
        assertTrue(empty.hasOutstanding)
        assertTrue(empty.outstanding.contains("Accept the required declaration to submit for review"))
    }

    @Test fun fallbackDocumentsAndFieldLabelsRetainActionableMissingData() {
        val source = body("""{"required_onboarding_fields":["future_field","phone"],"sections":[{"fields":[{"field":"phone","label":""},{"field":"","label":"Ignored"},{}]}]}""")
        val summary = OnboardingSummary.from(source, listOf(body("""{"status":"DEFERRED"}"""), body("""{"status":"VERIFIED","title":"Verified document"}""")))
        assertTrue(summary.outstanding.contains("Complete Future field"))
        assertTrue(summary.outstanding.contains("Complete Phone"))
        assertTrue(summary.outstanding.contains("Upload a required document (Deferred)"))
        assertFalse(summary.outstanding.any { it.contains("Verified document") })
        assertEquals(mapOf("phone" to "Phone"), OnboardingSummary.fieldLabels(source))
    }

    @Test fun embeddedDocumentsTakePrecedenceOverFallbackDocuments() {
        val source = body("""{"documents":[{"status":"REJECTED","title":"Current document"}]}""")
        val summary = OnboardingSummary.from(source, listOf(body("""{"status":"DEFERRED","title":"Stale document"}""")))
        assertTrue(summary.outstanding.any { it.contains("Current document") })
        assertFalse(summary.outstanding.any { it.contains("Stale document") })
    }

    @Test fun malformedOptionalJsonFieldsFallBackWithoutCrashing() {
        for (raw in listOf("{}", """{"items":null}""", """{"items":{}}""", """{"items":[42]}""")) assertEquals(emptyList<JsonObject>(), body(raw).objectList("items"))
        for (raw in listOf("{}", """{"items":null}""", """{"items":{}}""", """{"items":[{}]}""")) assertEquals(emptyList<String>(), body(raw).strings("items"))
        assertEquals(listOf("phone", "42"), body("""{"items":["phone",null,42]}""").strings("items"))
        for (raw in listOf("{}", """{"value":null}""", """{"value":{}}""", """{"value":"invalid"}""", """{"value":false}""")) assertFalse(body(raw).boolean("value"))
        assertTrue(body("""{"value":true}""").boolean("value"))
    }
}
