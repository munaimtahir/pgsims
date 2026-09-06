package pk.vexel.pgrcompanion

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

private fun obj(raw: String) = Json.parseToJsonElement(raw) as JsonObject

/** Fixture shaped exactly like `get_resident_onboarding_state` in sims/users/onboarding_api.py. */
private val INCOMPLETE = obj(
    """
    {"profile_complete":false,"onboarding_complete":false,"declaration_accepted":false,
     "review_status":"CORRECTION_REQUIRED","review_note":"CNIC scan is unreadable.",
     "supervisor_status":"PENDING",
     "required_onboarding_fields":["phone","department_ref"],
     "documents":[{"id":1,"title":"CNIC Copy","status":"REUPLOAD_REQUIRED"},
                  {"id":2,"title":"Degree","status":"VERIFIED"}],
     "sections":[{"key":"identity","title":"Identity","fields":[
        {"field":"full_name","label":"Full name","value":"A Resident","required":true},
        {"field":"phone","label":"Contact number","value":"","required":true}]},
       {"key":"enrollment","title":"Enrollment","fields":[
        {"field":"department_ref","label":"Department","value":3,"required":true},
        {"field":"training_start_date","label":"Training start date","value":"2026-01-01","required":true}]}]}
    """
)

private val COMPLETE = obj(
    """
    {"profile_complete":true,"onboarding_complete":true,"declaration_accepted":true,
     "review_status":"APPROVED","review_note":"","supervisor_status":"ASSIGNED",
     "required_onboarding_fields":[],
     "documents":[{"id":1,"title":"CNIC Copy","status":"VERIFIED"}],"sections":[]}
    """
)

class InstitutionalLabelsTest {

    @Test fun `every backend document status has a plain-English label`() {
        assertEquals("Not uploaded", InstitutionalLabels.documentStatus("NOT_STARTED"))
        assertEquals("Deferred", InstitutionalLabels.documentStatus("DEFERRED"))
        assertEquals("Uploaded", InstitutionalLabels.documentStatus("UPLOADED"))
        assertEquals("Under review", InstitutionalLabels.documentStatus("PENDING_REVIEW"))
        assertEquals("Approved", InstitutionalLabels.documentStatus("VERIFIED"))
        assertEquals("Rejected", InstitutionalLabels.documentStatus("REJECTED"))
        assertEquals("Correction required", InstitutionalLabels.documentStatus("REUPLOAD_REQUIRED"))
    }

    @Test fun `an unrecognised status is humanised rather than hidden`() {
        assertEquals("Awaiting countersign", InstitutionalLabels.documentStatus("AWAITING_COUNTERSIGN"))
        assertEquals("Unknown", InstitutionalLabels.documentStatus(""))
    }

    @Test fun `every review status maps to the institution's own wording`() {
        assertEquals("Not submitted", InstitutionalLabels.reviewStatus("NOT_SUBMITTED"))
        assertEquals("Under review", InstitutionalLabels.reviewStatus("PENDING_REVIEW"))
        assertEquals("Approved", InstitutionalLabels.reviewStatus("APPROVED"))
        assertEquals("Correction required", InstitutionalLabels.reviewStatus("CORRECTION_REQUIRED"))
    }

    @Test fun `only outstanding documents are flagged as needing action`() {
        listOf("NOT_STARTED", "DEFERRED", "REUPLOAD_REQUIRED", "REJECTED").forEach {
            assertTrue(it, InstitutionalLabels.documentNeedsAction(it))
        }
        listOf("UPLOADED", "PENDING_REVIEW", "VERIFIED").forEach {
            assertFalse(it, InstitutionalLabels.documentNeedsAction(it))
        }
    }

    @Test fun `replacing an already-submitted document must be confirmed, uploading a missing one need not be`() {
        assertTrue(InstitutionalLabels.replacementNeedsConfirmation("VERIFIED"))
        assertTrue(InstitutionalLabels.replacementNeedsConfirmation("PENDING_REVIEW"))
        assertFalse(InstitutionalLabels.replacementNeedsConfirmation("NOT_STARTED"))
        assertFalse(InstitutionalLabels.replacementNeedsConfirmation("REUPLOAD_REQUIRED"))
        assertEquals("Upload", InstitutionalLabels.documentAction("NOT_STARTED"))
        assertEquals("Replace", InstitutionalLabels.documentAction("REUPLOAD_REQUIRED"))
    }
}

class OnboardingFieldPolicyTest {

    @Test fun `only the fields the backend accepts as free text are editable`() {
        listOf("full_name", "phone", "email", "registration_no", "cnic", "notes").forEach {
            assertTrue(it, OnboardingFieldPolicy.isEditable(it))
            assertNull(it, OnboardingFieldPolicy.readOnlyReason(it))
        }
    }

    @Test fun `reference and administrative fields are never editable from the phone`() {
        // These resolve server-side to a row by pk or code; a text box would show a database id.
        listOf("hospital", "department_ref", "program_ref", "academic_session_ref", "specialty_ref").forEach {
            assertFalse(it, OnboardingFieldPolicy.isEditable(it))
            assertEquals("Set by your institution.", OnboardingFieldPolicy.readOnlyReason(it))
        }
        listOf("training_start_date", "expected_end_date", "current_level").forEach {
            assertFalse(it, OnboardingFieldPolicy.isEditable(it))
        }
        assertFalse(OnboardingFieldPolicy.isEditable("supervisor_status"))
    }

    @Test fun `a raw reference id is never shown to the resident`() {
        assertEquals("Recorded", OnboardingFieldPolicy.displayValue("department_ref", "3"))
        assertEquals("Not set", OnboardingFieldPolicy.displayValue("department_ref", ""))
        assertEquals("Medicine", OnboardingFieldPolicy.displayValue("department_ref", "3", "Medicine"))
        assertEquals("2026-01-01", OnboardingFieldPolicy.displayValue("training_start_date", "2026-01-01"))
    }
}

class OnboardingSummaryTest {

    @Test fun `an incomplete record lists every outstanding item using the institution's labels`() {
        val summary = OnboardingSummary.from(INCOMPLETE)

        assertEquals("CORRECTION_REQUIRED", summary.reviewStatus)
        assertEquals("CNIC scan is unreadable.", summary.reviewNote)
        assertFalse(summary.profileComplete)
        assertFalse(summary.onboardingComplete)
        assertTrue(summary.hasOutstanding)
        assertTrue(summary.outstanding.contains("Complete Contact number"))
        assertTrue(summary.outstanding.contains("Complete Department"))
        assertTrue(summary.outstanding.any { it.startsWith("Replace CNIC Copy") })
        // An approved document is not an outstanding requirement.
        assertFalse(summary.outstanding.any { it.contains("Degree") })
        assertTrue(summary.outstanding.any { it.startsWith("Supervisor assignment") })
        assertTrue(summary.outstanding.any { it.contains("declaration") })
    }

    @Test fun `a complete record has nothing outstanding`() {
        val summary = OnboardingSummary.from(COMPLETE)
        assertTrue(summary.onboardingComplete)
        assertTrue(summary.declarationAccepted)
        assertFalse(summary.hasOutstanding)
    }

    @Test fun `a missing onboarding payload yields an empty summary rather than an exception`() {
        val summary = OnboardingSummary.from(null)
        assertEquals("", summary.reviewStatus)
        assertFalse(summary.hasOutstanding)
    }

    @Test fun `document list falls back to the resident-documents endpoint when onboarding omits it`() {
        val withoutDocuments = obj("""{"declaration_accepted":true,"supervisor_status":"ASSIGNED","sections":[]}""")
        val summary = OnboardingSummary.from(
            withoutDocuments,
            listOf(obj("""{"id":9,"title":"Domicile","status":"NOT_STARTED"}""")),
        )
        assertEquals(listOf("Upload Domicile (Not uploaded)"), summary.outstanding)
    }

    @Test fun `field labels are read from the institution's declared sections`() {
        val labels = OnboardingSummary.fieldLabels(INCOMPLETE)
        assertEquals("Contact number", labels["phone"])
        assertEquals("Department", labels["department_ref"])
        assertNull(labels["not_a_field"])
    }
}
