package fmu.pg.sims.core.model

import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * These are not synthetic fixtures — every JSON blob below was captured verbatim from the real
 * local Django dev server (sims_project.settings, sqlite) during the resident onboarding MVP
 * build, via a logged-in resident test account, and is byte-for-byte what Android actually
 * receives. This substitutes for on-device network testing in an environment where the Android
 * emulator cannot boot (no /dev/kvm, no CPU virtualization extensions available in this sandbox).
 */
class SerializationContractTest {

    private val json = Json {
        ignoreUnknownKeys = true
        coerceInputValues = true
        isLenient = true
        encodeDefaults = true
    }

    @Test
    fun `login response nests role under user, not top-level`() {
        val raw = """{"refresh":"r.jwt","access":"a.jwt","user":{"id":4,"username":"pgr002","email":"android.mvp.resident@example.com","role":"RESIDENT","first_name":"Android","last_name":"MVP Resident","full_name":"Android MVP Resident"}}"""
        val response = json.decodeFromString<LoginResponse>(raw)
        assertEquals("a.jwt", response.access)
        assertEquals("r.jwt", response.refresh)
        assertNull("backend never actually sends a top-level role", response.role)
        assertEquals(Role.RESIDENT, response.user?.role)
        assertEquals("pgr002", response.user?.username)
    }

    @Test
    fun `auth me response carries full onboarding review surface`() {
        val raw = """{"id":4,"username":"pgr002","role":"RESIDENT","must_change_password":false,"is_profile_complete":false,"profile_type":"ResidentProfile","profile_id":2,"profile_status":"INCOMPLETE","profile_schema_version":1,"completed_schema_version":0,"missing_required_fields":["hospital","department_ref","program_ref","academic_session_ref"],"allowed_next_route":"/complete-profile","required_onboarding_fields":["hospital","department_ref","program_ref","academic_session_ref","specialty_ref","training_start_date","current_level"],"pending_upload_count":0,"pending_uploads":[],"pending_supervisor_link":{"id":1,"name":"Dr Test Supervisor","status":"PENDING"},"onboarding_complete":false,"onboarding_review_status":"NOT_SUBMITTED","onboarding_review_note":"","onboarding_submitted_at":null,"onboarding_reviewed_at":null}"""
        val me = json.decodeFromString<AuthMeResponse>(raw)
        assertEquals(4, me.id)
        assertEquals(Role.RESIDENT, me.role)
        assertEquals(2, me.profileId)
        assertEquals(4, me.missingRequiredFields.size)
        assertEquals(ReviewStatus.NOT_SUBMITTED, me.effectiveReviewStatus)
        assertEquals("Dr Test Supervisor", me.pendingSupervisorLink?.name)
        assertEquals("PENDING", me.pendingSupervisorLink?.status)
        assertEquals("/complete-profile", me.allowedNextRoute)
    }

    @Test
    fun `onboarding state sections and field metadata round-trip`() {
        val raw = """{"password_change_required":false,"profile_complete":false,"onboarding_complete":false,"required_onboarding_fields":["hospital"],"training_record_id":null,"supervisor_status":"NOT_STARTED","declaration_accepted":false,"review_status":"NOT_SUBMITTED","review_note":"","submitted_at":null,"reviewed_at":null,"documents":[],"baseline":{"research":{"title":"","topic_area":"","status":"DRAFT"},"thesis":{"status":"NOT_STARTED","notes":""}},"workshops":[],"sections":[{"key":"identity","title":"Identity","fields":[{"field":"full_name","label":"Full name","value":"Android MVP Resident","required":true},{"field":"cnic","label":"CNIC","value":null,"required":false}]},{"key":"enrollment","title":"Enrollment","fields":[{"field":"hospital","label":"Hospital / training site","value":null,"required":true}]}],"pending_upload_count":0,"pending_uploads":[],"pending_supervisor_link":null}"""
        val state = json.decodeFromString<OnboardingStateResponse>(raw)
        assertEquals(2, state.sections.size)
        val identity = state.sections.first { it.key == "identity" }
        assertEquals("Android MVP Resident", identity.fields.first { it.field == "full_name" }.value)
        assertNull(identity.fields.first { it.field == "cnic" }.value)
        assertFalse(state.onboardingComplete)
        assertEquals(ReviewStatus.NOT_SUBMITTED, state.reviewStatus)
    }

    @Test
    fun `identity options coerce numeric ids and code-as-id values into strings`() {
        // hospitals/departments/programs carry a raw JSON number "id"; academic_sessions and
        // specialties already carry their "code" as "id" (a JSON string). Both must deserialize
        // into OptionItem.id: String without throwing, since the field value that must be sent
        // back to PATCH /api/auth/onboarding/ has to be a plain string either way.
        val raw = """{"institutions":[],"training_sites":[],"hospitals":[{"id":1,"name":"Allied Hospital","code":"ALLIED"},{"id":4,"name":"Children Hospital","code":"CHILD"}],"departments":[{"id":4,"name":"Cardiology","code":"CARD"}],"programs":[{"id":3,"name":"Doctor of Medicine","code":"MD"}],"academic_sessions":[{"id":"JAN-2026","name":"JAN-2026 Induction","code":"JAN-2026"}],"designations":[],"specialties":[{"id":"anesthesia","name":"Anesthesia","code":"anesthesia"}]}"""
        val options = json.decodeFromString<IdentityOptionsResponse>(raw)
        assertEquals("1", options.hospitals.first().id)
        assertEquals("Allied Hospital", options.hospitals.first().name)
        assertEquals("4", options.departments.first().id)
        assertEquals("3", options.programs.first().id)
        assertEquals("JAN-2026", options.academicSessions.first().id)
        assertEquals("anesthesia", options.specialties.first().id)
    }

    @Test
    fun `resident documents list is a bare array, not paginated`() {
        val raw = """[{"id":1,"resident_id":2,"requirement_id":1,"document_type":"cnic_copy","title":"CNIC Copy","stage":"ONBOARDING","status":"NOT_STARTED","original_filename":"","verification_remarks":"","file":null,"file_url":null}]"""
        val documents = json.decodeFromString<List<ResidentDocumentDto>>(raw)
        assertEquals(1, documents.size)
        assertTrue(documents.first().isOutstanding)
        assertEquals(DocumentStatus.NOT_STARTED, documents.first().status)
    }

    @Test
    fun `document requirements and training records are DRF-paginated envelopes`() {
        val requirementsRaw = """{"count":1,"next":null,"previous":null,"results":[{"id":1,"document_type":"cnic_copy","display_name":"CNIC Copy","stage":"ONBOARDING","is_required":true,"is_active":true,"display_order":1}]}"""
        val requirements = json.decodeFromString<PaginatedResponse<ResidentDocumentRequirementDto>>(requirementsRaw)
        assertEquals(1, requirements.count)
        assertEquals("CNIC Copy", requirements.results.first().displayName)

        val trainingRaw = """{"count":0,"next":null,"previous":null,"results":[]}"""
        val training = json.decodeFromString<PaginatedResponse<ResidentTrainingRecordDto>>(trainingRaw)
        assertEquals(0, training.count)
        assertTrue(training.results.isEmpty())
    }

    @Test
    fun `supervision options is a bare object keyed by supervisors and residents`() {
        val raw = """{"residents":[{"id":2,"name":"Android MVP Resident","username":"pgr002","training_site":"","department":"","program":"","academic_session":"","has_active_primary":false}],"supervisors":[{"id":1,"name":"Brand New Person","training_site":"","department":"","designation":"","active_primary_count":0,"active_total_count":0}]}"""
        val options = json.decodeFromString<SupervisionOptionsResponse>(raw)
        assertEquals(1, options.supervisors.size)
        assertEquals("Brand New Person", options.supervisors.first().name)
    }

    @Test
    fun `pending supervisor link create response round-trips`() {
        val raw = """{"id":1,"supervisor_name_text":"Dr Test Supervisor","department_text":"Medicine","institution_text":"","pmdc_number_text":"","email_text":"","phone_text":"","notes":"","status":"PENDING","resolved_at":null,"created_at":"2026-09-03T00:12:47.570381Z","updated_at":"2026-09-03T00:12:47.570415Z","resident":2,"resolved_supervisor":null,"resolved_by":null}"""
        val link = json.decodeFromString<PendingSupervisorLinkDto>(raw)
        assertEquals(2, link.resident)
        assertEquals("PENDING", link.status)
        assertNotNull(link.supervisorNameText)
    }
}
