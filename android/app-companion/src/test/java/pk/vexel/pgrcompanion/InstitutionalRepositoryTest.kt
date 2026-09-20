package pk.vexel.pgrcompanion

import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonPrimitive
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import okhttp3.mockwebserver.RecordedRequest
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test
import java.io.File

/**
 * These fixtures are the real payloads observed against the canonical PGR SIMS backend on
 * 2026-09-06 (see PGR_SIMS_ANDROID_API_INTEGRATION.md), reduced to the fields the client reads.
 */
private const val LOGIN_BODY = """
{"access":"access-1","refresh":"refresh-1",
 "user":{"id":9,"username":"demo.resident","role":"RESIDENT","full_name":"Demo Resident"}}
"""
private const val ME_BODY = """
{"id":9,"username":"demo.resident","role":"RESIDENT","must_change_password":false,
 "is_profile_complete":true,"allowed_next_route":"/dashboard/resident",
 "onboarding_review_status":"APPROVED","pending_upload_count":1,"pending_uploads":[]}
"""
private const val ONBOARDING_BODY = """
{"review_status":"APPROVED","supervisor_status":"PENDING","declaration_accepted":true,
 "sections":[{"key":"identity","title":"Identity","fields":[
   {"field":"full_name","label":"Full name","value":"Demo Resident","required":true},
   {"field":"cnic","label":"CNIC","value":"","required":false}]}],
 "documents":[{"id":1,"requirement_id":1,"title":"CNIC Copy","status":"PENDING_REVIEW","stage":"ONBOARDING"}]}
"""
private const val DOCUMENTS_BODY = """
[{"id":1,"resident_id":4,"requirement_id":1,"document_type":"CNIC","title":"CNIC Copy",
  "stage":"ONBOARDING","status":"PENDING_REVIEW","original_filename":"cnic.pdf",
  "verification_remarks":"","file":"/api/resident-documents/1/file/","file_url":"/api/resident-documents/1/file/"}]
"""
private const val TRAINING_BODY = """
{"count":1,"next":null,"previous":null,"results":[
 {"id":3,"program_name":"Active Surface Baseline Programme","program_code":"ASBP",
  "current_level":"YEAR_1","start_date":"2026-01-01","expected_end_date":"2029-12-31","active":true}]}
"""
private const val ASSIGNMENTS_BODY = """
{"count":1,"next":null,"previous":null,"results":[
 {"id":7,"assignment_type":"PRIMARY","status":"ACTIVE","is_active":true,
  "supervisor":{"id":2,"name":"Ayesha Malik","department":"Medicine","training_site":"Allied","designation":"HOD"}}]}
"""
private const val ROTATIONS_BODY = """{"count":1,"results":[{"id":8,"department":"Medicine","hospital":"Allied","start_date":"2026-01-01","end_date":"2026-03-31","status":"ACTIVE"}]}"""
private const val LEAVES_BODY = """{"count":0,"results":[]}"""
private const val LOGBOOK_BODY = """{"count":1,"results":[{"id":4,"title":"Synthetic activity","entry_date":"2026-09-01","status":"DRAFT"}]}"""
private const val CATEGORIES_BODY = """{"count":1,"results":[{"id":2,"name":"Clinical activity"}]}"""
private const val ACADEMIC_OPTIONS_BODY = """{"supervisors":[{"id":2,"name":"Ayesha Malik"}],"periods":[{"id":4,"name":"Year 2"}]}"""
private const val ASSESSMENTS_BODY = """{"count":0,"results":[]}"""
private const val EVALUATION_TEMPLATES_BODY = """{"count":1,"results":[{"id":5,"name":"Mini-CEX","form_type":"MINI_CEX","schema":{}}]}"""
private const val RESEARCH_BODY = """{"status":"DRAFT"}"""
private const val WORKSHOPS_BODY = """{"count":0,"results":[]}"""
private const val RESIDENT_SUMMARY_BODY = """{"rotation":{"current":{"id":8,"department":"Medicine","status":"ACTIVE"}}}"""
private const val ACADEMIC_PROGRESS_BODY = """{"training_record_status":"ACTIVE","training_year":2,"evaluations_total":3,"evaluations_approved":2,"logbooks_total":12,"logbooks_verified":9}"""
private const val PROGRESS_MONITORING_BODY = """{"training_record_status":"ACTIVE","overall_status":"ON_TRACK"}"""
private const val SUPERVISOR_ME_BODY = """{"id":2,"username":"demo.supervisor","role":"SUPERVISOR"}"""
private const val ADMIN_ME_BODY = """{"id":1,"username":"demo.admin","role":"ADMIN"}"""
private const val SUPERVISOR_SUMMARY_BODY = """
{"pending":{"rotation_approvals":1,"leave_approvals":0,"research_approvals":2},
 "residents":[{"id":9,"rtr_id":3,"name":"Demo Resident","program":"MS Urology",
   "current_rotation":"Urology @ Allied Hospital-I","imm_status":"ON_TRACK","final_status":null,"research_status":"SUBMITTED_TO_SUPERVISOR"}],
 "supervision":{"active_primary_residents":[],"active_co_supervised_residents":[],"past_assigned_residents":[]}}
"""
private const val SUPERVISOR_DASHBOARD_BODY = """
{"assigned_residents_count":1,"pending_evaluation_reviews_count":0,"pending_logbook_reviews_count":3,
 "overdue_reviews_count":0,"returned_items_count":0,"recently_approved_evaluations":[],
 "recently_verified_logbooks":[],"residents_below_req":[],"assigned_residents":[],"review_queue":[]}
"""
private const val SUPERVISOR_RESIDENT_PROGRESS_BODY = """
{"RESIDENT":{"id":9,"name":"Demo Resident","username":"demo.resident"},
 "training_record":{"program_code":"MS-URO","program_name":"MS Urology","degree_type":"MS",
   "start_date":"2024-01-15","current_month_index":20},
 "current_rotation":{"department":"Urology","hospital":"Allied Hospital-I Faisalabad",
   "start_date":"2026-07-01","end_date":"2026-12-31","status":"ACTIVE"},
 "research":{"status":"SUBMITTED_TO_SUPERVISOR","title":"Outcomes of PCNL"},
 "thesis":{"status":"IN_PROGRESS"},
 "workshops":{"total_completed":4},
 "eligibility":{"IMM":{"status":"ON_TRACK","reasons":[]},"FINAL":{"status":"NOT_ELIGIBLE","reasons":["Logbook incomplete"]}}}
"""

class InstitutionalRepositoryTest {
    private lateinit var server: MockWebServer
    private lateinit var tokens: InMemoryTokenStore
    private lateinit var repository: InstitutionalRepository

    @Before fun setUp() {
        server = MockWebServer().also { it.start() }
        tokens = InMemoryTokenStore()
        repository = InstitutionalRepository(server.url("/").toString(), tokens)
    }

    @After fun tearDown() = server.shutdown()

    private fun json(body: String, code: Int = 200) =
        MockResponse().setResponseCode(code).setHeader("Content-Type", "application/json").setBody(body.trim())

    private fun bearerOf(request: RecordedRequest) = request.getHeader("Authorization")

    // --- session ---------------------------------------------------------------------------

    @Test fun `login stores both tokens and reports connected`() = runBlocking {
        server.enqueue(json(LOGIN_BODY))
        assertFalse(repository.isConnected())

        val result = repository.login(" demo.resident ", "secret")

        assertTrue(result.isSuccess)
        assertEquals("access-1", tokens.access)
        assertEquals("refresh-1", tokens.refresh)
        assertTrue(repository.isConnected())

        val sent = Json.parseToJsonElement(server.takeRequest().body.readUtf8()) as JsonObject
        assertEquals("demo.resident", sent.string("username")) // trimmed
    }

    @Test fun `login rejects bad credentials with a plain message and stores nothing`() = runBlocking {
        server.enqueue(json("""{"detail":"No active account found with the given credentials"}""", 401))

        val result = repository.login("demo.resident", "wrong")

        assertTrue(result.isFailure)
        assertEquals("Incorrect username or password.", result.exceptionOrNull()?.message)
        assertNull(tokens.access)
        assertFalse(repository.isConnected())
    }

    @Test fun `login surfaces throttling distinctly`() = runBlocking {
        server.enqueue(json("""{"detail":"throttled"}""", 429))
        val result = repository.login("demo.resident", "secret")
        assertTrue(result.exceptionOrNull()?.message.orEmpty().contains("Too many sign-in attempts"))
    }

    @Test fun `login never echoes the password in the failure message`() = runBlocking {
        server.enqueue(json("""{"detail":"nope"}""", 401))
        val result = repository.login("demo.resident", "sup3rSecret!")
        assertFalse(result.exceptionOrNull()?.message.orEmpty().contains("sup3rSecret!"))
    }

    @Test fun `logout clears the session even when the server rejects the blacklist call`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"error":"Invalid token"}""", 400))

        repository.logout()

        assertFalse(repository.isConnected())
        assertNull(tokens.access)
        assertNull(tokens.refresh)
        assertEquals("Bearer access-1", bearerOf(server.takeRequest()))
    }

    // --- snapshot --------------------------------------------------------------------------

    @Test fun `snapshot reads every section and unwraps DRF pages`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json(ME_BODY))
        server.enqueue(json(ONBOARDING_BODY))
        server.enqueue(json(DOCUMENTS_BODY))
        server.enqueue(json(TRAINING_BODY))
        server.enqueue(json(ASSIGNMENTS_BODY))
        enqueueResidentWorkflowBodies()

        val snapshot = repository.snapshot().getOrThrow()

        assertEquals("demo.resident", snapshot.me.string("username"))
        assertNotNull(snapshot.onboarding)
        assertEquals(1, snapshot.documents.size)
        assertEquals(1, snapshot.training.size)
        assertEquals("Active Surface Baseline Programme", snapshot.training.first().string("program_name"))
        assertEquals(1, snapshot.assignments.size)
        assertEquals(1, snapshot.rotations.size)
        assertEquals(1, snapshot.logbook.size)
        assertEquals("DRAFT", snapshot.research?.string("status"))
        assertEquals(
            "Medicine",
            snapshot.residentSummary?.get("rotation")?.jsonObject?.get("current")?.jsonObject?.string("department"),
        )
        assertEquals("ACTIVE", snapshot.academicProgress?.string("training_record_status"))
        assertTrue(snapshot.unavailable.isEmpty())
        assertEquals("Bearer access-1", bearerOf(server.takeRequest()))
    }

    /** A SUPERVISOR account takes the supervisor branch of [InstitutionalRepository.snapshot]: it
     * never calls the resident-only endpoints at all, and reads its own two sections instead. */
    @Test fun `snapshot for a SUPERVISOR reads the supervisor sections, not the resident ones`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json(SUPERVISOR_ME_BODY))
        server.enqueue(json(SUPERVISOR_SUMMARY_BODY))
        server.enqueue(json(SUPERVISOR_DASHBOARD_BODY))

        val snapshot = repository.snapshot().getOrThrow()

        assertEquals("SUPERVISOR", snapshot.me.string("role"))
        assertNull(snapshot.onboarding)
        assertTrue(snapshot.training.isEmpty())
        assertEquals(1, snapshot.supervisorSummary?.objectList("residents")?.size)
        assertEquals("Demo Resident", snapshot.supervisorSummary?.objectList("residents")?.first()?.string("name"))
        assertEquals(3, snapshot.supervisorDashboard?.get("pending_logbook_reviews_count")?.jsonPrimitive?.intOrNull)
        assertTrue(snapshot.unavailable.isEmpty())
    }

    @Test fun `snapshot for ADMIN never falls through to resident workspace calls`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json(ADMIN_ME_BODY))

        val snapshot = repository.snapshot().getOrThrow()

        assertEquals("ADMIN", snapshot.me.string("role"))
        assertEquals(listOf("Mobile workspace"), snapshot.unavailable)
        assertEquals(1, server.requestCount)
    }

    @Test fun `snapshot for a SUPERVISOR tolerates the dashboard section being unavailable`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json(SUPERVISOR_ME_BODY))
        server.enqueue(json(SUPERVISOR_SUMMARY_BODY))
        server.enqueue(json("""{"detail":"Not found."}""", 404))

        val snapshot = repository.snapshot().getOrThrow()

        assertNull(snapshot.supervisorDashboard)
        assertEquals(listOf("Supervisor dashboard"), snapshot.unavailable)
    }

    @Test fun `supervisorResidentProgress returns the resident's training and eligibility snapshot`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json(SUPERVISOR_RESIDENT_PROGRESS_BODY))

        val progress = repository.supervisorResidentProgress(9).getOrThrow()

        assertEquals("Demo Resident", progress["RESIDENT"]?.jsonObject?.string("name"))
        assertEquals("MS Urology", progress["training_record"]?.jsonObject?.string("program_name"))
        assertEquals("Urology", progress["current_rotation"]?.jsonObject?.string("department"))
        assertEquals("NOT_ELIGIBLE", progress["eligibility"]?.jsonObject?.get("FINAL")?.jsonObject?.string("status"))
        val request = server.takeRequest()
        assertTrue(request.path.orEmpty().endsWith("/api/supervisors/residents/9/progress/"))
    }

    @Test fun `supervisorResidentProgress surfaces a denied assignment as a plain message`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"detail":"You do not have an active supervision assignment for this resident."}""", 403))

        val result = repository.supervisorResidentProgress(9)

        assertTrue(result.isFailure)
        assertEquals("This account is not permitted to view this resident's progress.", result.exceptionOrNull()?.message)
    }

    @Test fun `snapshot fails when identity itself cannot be read`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"detail":"boom"}""", 500))
        val result = repository.snapshot()
        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull()?.message.orEmpty().contains("unavailable right now"))
    }

    @Test fun `snapshot reports a network outage in words a trainee can act on`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.shutdown()

        val result = repository.snapshot()

        assertTrue(result.isFailure)
        assertEquals(
            "Cannot reach PGR SIMS. Check your connection and try again.",
            result.exceptionOrNull()?.message,
        )
    }

    // --- refresh ---------------------------------------------------------------------------

    @Test fun `a 401 triggers one refresh and replays the request with the rotated token`() = runBlocking {
        tokens.save("stale", "refresh-1")
        server.enqueue(json("""{"detail":"token_not_valid"}""", 401))
        server.enqueue(json("""{"access":"access-2","refresh":"refresh-2"}"""))
        server.enqueue(json(ME_BODY))
        server.enqueue(json(ONBOARDING_BODY))
        server.enqueue(json(DOCUMENTS_BODY))
        server.enqueue(json(TRAINING_BODY))
        server.enqueue(json(ASSIGNMENTS_BODY))
        enqueueResidentWorkflowBodies()

        val snapshot = repository.snapshot().getOrThrow()

        assertEquals("demo.resident", snapshot.me.string("username"))
        assertEquals("access-2", tokens.access)
        assertEquals("refresh-2", tokens.refresh) // rotation honoured
        assertEquals("Bearer stale", bearerOf(server.takeRequest()))
        assertNull(bearerOf(server.takeRequest()))  // refresh call is unauthenticated
        assertEquals("Bearer access-2", bearerOf(server.takeRequest()))
    }

    @Test fun `a spent refresh token drops the session instead of looping`() = runBlocking {
        tokens.save("stale", "spent")
        server.enqueue(json("""{"detail":"token_not_valid"}""", 401))
        server.enqueue(json("""{"detail":"Token is blacklisted"}""", 401))

        val result = repository.snapshot()

        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull()?.message.orEmpty().contains("session has expired"))
        assertFalse(repository.isConnected())
        assertEquals(2, server.requestCount) // no retry storm
    }

    // --- writes ----------------------------------------------------------------------------

    @Test fun `update sends the fields envelope the backend expects`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json(ONBOARDING_BODY))

        repository.update(mapOf("cnic" to "35201-1234567-1")).getOrThrow()

        val request = server.takeRequest()
        assertEquals("PATCH", request.method)
        assertEquals("/api/auth/onboarding/", request.path)
        val body = Json.parseToJsonElement(request.body.readUtf8()) as JsonObject
        assertNotNull(body["fields"]) // {"fields":{...}}, not a bare map
    }

    @Test fun `upload posts multipart to the document's upload action`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":1,"status":"PENDING_REVIEW"}"""))
        val file = File.createTempFile("cnic", ".pdf").apply { writeText("%PDF-1.4 test") }

        repository.upload(1, file, "cnic.pdf").getOrThrow()

        val request = server.takeRequest()
        assertEquals("/api/resident-documents/1/upload/", request.path)
        val body = request.body.readUtf8()
        assertTrue(body.contains("""name="file""""))
        assertTrue(body.contains("cnic.pdf"))
        file.delete()
        Unit
    }

    @Test fun `resident leave create and submit use canonical actions`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":12,"status":"DRAFT"}""", 201))
        server.enqueue(json("""{"id":12,"status":"SUBMITTED"}"""))

        val created = repository.createLeave(LeaveRequestPayload(3, "annual", "2026-09-20", "2026-09-22", "Conference" )).getOrThrow()
        assertEquals(12, created["id"]?.jsonPrimitive?.intOrNull)
        repository.submitLeave(12).getOrThrow()

        val create = server.takeRequest()
        assertEquals("POST", create.method)
        assertEquals("/api/leaves/", create.path)
        assertTrue(create.body.readUtf8().contains("resident_training"))
        assertEquals("/api/leaves/12/submit/", server.takeRequest().path)
    }

    @Test fun `evaluation review actions use supervisor comment payload`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":21,"status":"APPROVED"}"""))

        repository.approveEvaluation(21, "Good progress.").getOrThrow()

        val request = server.takeRequest()
        assertEquals("POST", request.method)
        assertEquals("/api/academics/evaluation-submissions/21/approve/", request.path)
        assertTrue(request.body.readUtf8().contains("supervisor_comments"))
    }

    @Test fun `password and dynamic completion contracts use canonical endpoints`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"message":"Password changed","allowed_next_route":"/complete-profile"}"""))
        server.enqueue(json("""{"profile_type":"AdminProfile","missing_fields":[{"field":"email","input_type":"email","required":true}]}"""))
        server.enqueue(json("""{"hospitals":[],"departments":[]}"""))
        server.enqueue(json("""{"id":1,"role":"ADMIN","allowed_next_route":"/dashboard/utrmc"}"""))

        repository.changePassword("old-secret", "new-secret", "new-secret").getOrThrow()
        repository.completeProfileForm().getOrThrow()
        repository.identityOptions().getOrThrow()
        repository.completeProfile(mapOf("email" to "admin@example.com")).getOrThrow()

        val passwordRequest = server.takeRequest()
        assertEquals("/api/auth/change-password/", passwordRequest.path)
        val passwordBody = passwordRequest.body.readUtf8()
        assertTrue(passwordBody.contains("old_password"))
        assertTrue(passwordBody.contains("new_password2"))
        assertEquals("/api/auth/complete-profile/", server.takeRequest().path)
        assertEquals("/api/identity/options/", server.takeRequest().path)
        val completion = server.takeRequest()
        assertEquals("POST", completion.method)
        assertEquals("/api/auth/complete-profile/", completion.path)
        assertTrue(completion.body.readUtf8().contains("admin@example.com"))
    }

    @Test fun `password reset confirmation is anonymous and preserves uid token contract`() = runBlocking {
        server.enqueue(json("""{"message":"Password reset successful"}"""))

        repository.confirmPasswordReset("uid-value", "reset-token", "new-secret", "new-secret").getOrThrow()

        val request = server.takeRequest()
        assertNull(request.getHeader("Authorization"))
        assertEquals("/api/auth/password-reset/confirm/", request.path)
        val body = request.body.readUtf8()
        assertTrue(body.contains("uid-value"))
        assertTrue(body.contains("reset-token"))
    }

    @Test fun `notification target fetches the exact authorized record`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":44,"title":"Exact logbook","status":"RETURNED"}"""))

        val target = repository.notificationTarget("logbook", 44).getOrThrow()

        assertEquals("44", target.string("id"))
        assertEquals("/api/academics/logbook-entries/44/", server.takeRequest().path)
    }

    @Test fun `rotation review uses the canonical review application action`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":8,"status":"RETURNED"}"""))

        repository.returnRotation(8, "More information required").getOrThrow()

        val request = server.takeRequest()
        assertEquals("/api/rotations/8/review-application/", request.path)
        val body = request.body.readUtf8()
        assertTrue(body.contains("\"action\":\"defer\""))
        assertTrue(body.contains("More information required"))
    }

    @Test fun `admin directory preserves server paging filters and four role creation`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"count":31,"next":"https://example/api/users/?page=3","previous":null,"results":[{"id":9,"username":"res9","role":"RESIDENT"}]}"""))
        server.enqueue(json("""{"user_id":40,"username":"staff040","role":"SUPPORT_STAFF","profile_type":"SupportStaffProfile"}""", 201))

        val page = repository.users(page = 2, role = "RESIDENT", search = "demo", active = true).getOrThrow()
        assertEquals(31, page.count)
        assertNotNull(page.next)
        assertEquals(1, page.results.size)
        repository.createUser(UniversalUserPayload("SUPPORT_STAFF", "Demo Staff", "staff@example.com", "03000000000")).getOrThrow()

        val list = server.takeRequest()
        assertTrue(list.path.orEmpty().contains("page=2"))
        assertTrue(list.path.orEmpty().contains("role=RESIDENT"))
        assertTrue(list.path.orEmpty().contains("search=demo"))
        assertTrue(list.path.orEmpty().contains("active=true"))
        val create = server.takeRequest()
        assertEquals("POST", create.method)
        assertEquals("/api/users/", create.path)
        val body = create.body.readUtf8()
        assertTrue(body.contains("SUPPORT_STAFF"))
        assertTrue(body.contains("Demo Staff"))
    }

    private fun enqueueResidentWorkflowBodies() {
        server.enqueue(json(ROTATIONS_BODY))
        server.enqueue(json(LEAVES_BODY))
        server.enqueue(json(LOGBOOK_BODY))
        server.enqueue(json(CATEGORIES_BODY))
        server.enqueue(json(ACADEMIC_OPTIONS_BODY))
        server.enqueue(json(ASSESSMENTS_BODY))
        server.enqueue(json(EVALUATION_TEMPLATES_BODY))
        server.enqueue(json(RESEARCH_BODY))
        server.enqueue(json(WORKSHOPS_BODY))
        server.enqueue(json(RESIDENT_SUMMARY_BODY))
        server.enqueue(json(ACADEMIC_PROGRESS_BODY))
        server.enqueue(json(PROGRESS_MONITORING_BODY))
    }

    @Test fun `upload is rejected client-side before any request when the file is unusable`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        val file = File.createTempFile("notes", ".txt").apply { writeText("hello") }

        val result = repository.upload(1, file, "notes.txt")

        assertTrue(result.isFailure)
        assertEquals(0, server.requestCount)
        file.delete()
        Unit
    }

    @Test fun `returned leave editor patches the existing record and preserves idempotency key`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":21,"status":"RETURNED"}"""))
        val result = repository.updateLeave(21, LeaveRequestPayload(11, "annual", "2026-11-10", "2026-11-11", "Corrected dates", "leave-key-21"))
        assertTrue(result.isSuccess)
        val request = server.takeRequest()
        assertEquals("PATCH", request.method)
        assertEquals("/api/leaves/21/", request.path)
        val body = Json.parseToJsonElement(request.body.readUtf8()) as JsonObject
        assertEquals("leave-key-21", body.string("client_request_id"))
        assertEquals("Corrected dates", body.string("reason"))
    }

    @Test fun `returned evaluation editor patches the same submission with response values`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":33,"status":"RETURNED"}"""))
        val result = repository.updateEvaluation(33, EvaluationSubmissionPayload(5, 4, 2, "Updated reflection", listOf(Json.parseToJsonElement("""{"field_key":"quality","value_text":"improved"}""") as JsonObject)))
        assertTrue(result.isSuccess)
        val request = server.takeRequest()
        assertEquals("PATCH", request.method)
        assertEquals("/api/academics/evaluation-submissions/33/", request.path)
        val body = Json.parseToJsonElement(request.body.readUtf8()) as JsonObject
        assertEquals("Updated reflection", body.string("resident_comments"))
        assertEquals("improved", body["responses"]!!.jsonArray[0].jsonObject.string("value_text"))
    }

    @Test fun `admin report export returns CSV text through the authenticated client`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(MockResponse().setResponseCode(200).setHeader("Content-Type", "text/csv").setBody("name,count\nDemo,2\n"))
        val result = repository.adminReportCsv("Data quality")
        assertEquals("name,count\nDemo,2\n", result.getOrThrow())
        val request = server.takeRequest()
        assertEquals("GET", request.method)
        assertEquals("/api/academics/reports/data-quality/export.csv", request.path)
        assertEquals("Bearer access-1", request.getHeader("Authorization"))
    }

    @Test fun `all displayed report labels resolve to their canonical CSV exports`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        val expected = mapOf(
            "Logbook" to "/api/academics/reports/logbook/export.csv",
            "Evaluations" to "/api/academics/reports/evaluations/export.csv",
            "Resident progress" to "/api/academics/reports/resident-progress/export.csv",
            "Supervisor workload" to "/api/academics/reports/supervisor-workload/export.csv",
        )
        expected.forEach { (label, path) ->
            server.enqueue(MockResponse().setResponseCode(200).setHeader("Content-Type", "text/csv").setBody("id\n1\n"))
            assertEquals("id\n1\n", repository.adminReportCsv(label).getOrThrow())
            assertEquals(path, server.takeRequest().path)
        }
    }

    @Test fun `admin authoring only posts to an allow-listed canonical collection`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":12,"name":"Rotation A"}""", 201))
        val payload = Json.parseToJsonElement("""{"name":"Rotation A","code":"ROT-A"}""") as JsonObject

        repository.adminCreate("academics/rotation-templates", payload, "rotation template").getOrThrow()

        val request = server.takeRequest()
        assertEquals("POST", request.method)
        assertEquals("/api/academics/rotation-templates/", request.path)
        assertEquals("Bearer access-1", request.getHeader("Authorization"))
        assertEquals("Rotation A", (Json.parseToJsonElement(request.body.readUtf8()) as JsonObject).string("name"))
        val requestsBeforeRejectedPath = server.requestCount
        val rejected = repository.adminCreate("auth/logout", payload, "logout")
        assertTrue(rejected.isFailure)
        assertEquals(requestsBeforeRejectedPath, server.requestCount)
    }

    @Test fun `pending supervisor links list and resolve through canonical admin endpoints`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""[{"id":18,"resident":"Demo Resident","supervisor_name":"Dr Requested"}]"""))
        server.enqueue(json("""{"pending_id":18,"assignment_id":4,"status":"RESOLVED"}"""))

        assertEquals(18, repository.pendingSupervisorLinks().getOrThrow().single().string("id")?.toInt())
        assertEquals("RESOLVED", repository.resolvePendingSupervisor(18, 7).getOrThrow().string("status"))

        assertEquals("/api/pending-supervisor-links/", server.takeRequest().path)
        val resolve = server.takeRequest()
        assertEquals("/api/pending-supervisor-links/18/resolve/", resolve.path)
        assertEquals(7, (Json.parseToJsonElement(resolve.body.readUtf8()) as JsonObject).string("supervisor_id")?.toInt())
    }

    @Test fun `admin lifecycle actions and primary change use canonical guarded endpoints`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":7,"status":"ENDED"}"""))
        server.enqueue(json("""{"id":8,"assignment_type":"PRIMARY","status":"ACTIVE"}"""))
        assertEquals("ENDED", repository.adminAction("supervision/assignments", 7, "end", Json.parseToJsonElement("""{"end_date":"2026-09-20","reason_for_change":"Synthetic"}""") as JsonObject, "assignment").getOrThrow().string("status"))
        assertEquals("ACTIVE", repository.changePrimarySupervisor(4, 2, "2026-09-21", "Synthetic").getOrThrow().string("status"))
        assertEquals("/api/supervision/assignments/7/end/", server.takeRequest().path)
        val change = server.takeRequest()
        assertEquals("/api/supervision/change-primary/", change.path)
        val body = Json.parseToJsonElement(change.body.readUtf8()) as JsonObject
        assertEquals(4, body.string("resident_id")?.toInt())
        assertEquals(2, body.string("new_supervisor_id")?.toInt())
        assertTrue(repository.changePrimarySupervisor(0, 2, "bad", "").isFailure)
        Unit
    }

    @Test fun `standard import requires a supported entity and uses dry-run before apply`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        val file = File.createTempFile("pgr-import", ".csv").apply { writeText("email,full_name\ndemo@example.com,Demo\n") }
        server.enqueue(json("""{"dry_run":true,"status":"COMPLETED"}"""))
        assertEquals("COMPLETED", repository.bulkImport("residents", "dry-run", file).getOrThrow().string("status"))
        val request = server.takeRequest()
        assertEquals("POST", request.method)
        assertEquals("/api/bulk/import/residents/dry-run/", request.path)
        assertTrue(request.body.readUtf8().contains("demo@example.com"))
        val requestsBeforeRejectedImport = server.requestCount
        assertTrue(repository.bulkImport("unknown", "apply", file).isFailure)
        assertEquals(requestsBeforeRejectedImport, server.requestCount)
        file.delete()
        Unit
    }

    @Test fun `flexible import detects headers validates mappings and posts a mapped dry run`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        val file = File.createTempFile("pgr-flexible", ".csv").apply { writeText("Full Name,Email\nDemo,demo@example.com\n") }
        val mapping = Json.parseToJsonElement("""{"full_name":"Full Name","email":"Email"}""") as JsonObject
        server.enqueue(json("""{"headers":["Full Name","Email"],"total_rows":1}"""))
        server.enqueue(json("""{"ready":true,"missing_required_fields":[]}"""))
        server.enqueue(json("""{"dry_run":true,"status":"COMPLETED"}"""))

        assertEquals(2, repository.detectFlexibleHeaders(file).getOrThrow()["headers"]!!.jsonArray.size)
        assertTrue(repository.validateFlexibleMapping("residents", mapping).getOrThrow().boolean("ready"))
        assertEquals("COMPLETED", repository.flexibleImport("residents", "dry-run", file, mapping).getOrThrow().string("status"))

        assertEquals("/api/bulk/flexible/detect-headers/", server.takeRequest().path)
        val validate = server.takeRequest()
        assertEquals("/api/bulk/flexible/validate-mapping/", validate.path)
        assertEquals("residents", (Json.parseToJsonElement(validate.body.readUtf8()) as JsonObject).string("entity"))
        val dryRun = server.takeRequest()
        assertEquals("/api/bulk/flexible/dry-run/", dryRun.path)
        assertTrue(dryRun.body.readUtf8().contains("full_name"))
        file.delete()
        Unit
    }

    @Test fun `bulk templates and exports use allow-listed canonical resources`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(MockResponse().setResponseCode(200).setHeader("Content-Type", "text/csv").setBody("code,name\nH1,Hospital\n"))
        server.enqueue(MockResponse().setResponseCode(200).setHeader("Content-Type", "text/csv").setBody("code,name\nH1,Hospital\n"))
        assertTrue(repository.bulkTemplate("hospitals").getOrThrow().contains("Hospital"))
        assertTrue(repository.bulkExport("hospitals").getOrThrow().contains("Hospital"))
        assertEquals("/api/bulk/templates/hospitals/", server.takeRequest().path)
        assertEquals("/api/bulk/exports/hospitals/?file_format=csv", server.takeRequest().path)
        assertTrue(repository.bulkExport("not-a-resource").isFailure)
        Unit
    }

    @Test fun `notification reads follow every server page`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"count":2,"next":"https://example/api/notifications/?page=2","results":[{"id":1,"title":"First"}]}"""))
        server.enqueue(json("""{"count":2,"next":null,"results":[{"id":2,"title":"Second"}]}"""))

        val rows = repository.notifications().getOrThrow()

        assertEquals(listOf(1, 2), rows.mapNotNull { it.string("id")?.toIntOrNull() })
        assertEquals("/api/notifications/?page=1", server.takeRequest().path)
        assertEquals("/api/notifications/?page=2", server.takeRequest().path)
    }
}

class InstitutionalValidationTest {
    @Test fun `upload validation mirrors the backend allowlist and size cap`() {
        assertNull(InstitutionalRepository.validateUpload("scan.pdf", 1_000))
        assertNull(InstitutionalRepository.validateUpload("SCAN.PDF", 1_000)) // case-insensitive
        assertNull(InstitutionalRepository.validateUpload("photo.JPEG", 1_000))
        assertNotNull(InstitutionalRepository.validateUpload("notes.txt", 1_000))
        assertNotNull(InstitutionalRepository.validateUpload("noextension", 1_000))
        assertNotNull(InstitutionalRepository.validateUpload("scan.pdf", 0))
        assertNotNull(InstitutionalRepository.validateUpload("scan.pdf", 10L * 1024 * 1024 + 1))
        assertNull(InstitutionalRepository.validateUpload("scan.pdf", 10L * 1024 * 1024))
    }

    @Test fun `mime types match the extensions the backend accepts`() {
        assertEquals("application/pdf", InstitutionalRepository.mimeTypeFor("a.pdf"))
        assertEquals("image/jpeg", InstitutionalRepository.mimeTypeFor("a.jpg"))
        assertEquals("image/jpeg", InstitutionalRepository.mimeTypeFor("a.jpeg"))
        assertEquals("image/png", InstitutionalRepository.mimeTypeFor("a.png"))
        assertEquals(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            InstitutionalRepository.mimeTypeFor("a.docx"),
        )
    }

    @Test fun `every user-facing error is a sentence with no protocol jargon or secrets`() {
        val messages = listOf(401, 403, 404, 429, 500, 418).map { InstitutionalRepository.errorFor(it, "training") } +
            listOf(400, 401, 403, 429, 500).map { InstitutionalRepository.loginErrorFor(it) }
        messages.forEach { message ->
            assertTrue(message, message.endsWith("."))
            assertFalse(message, message.contains("token", ignoreCase = true))
            assertFalse(message, message.contains("Bearer"))
        }
    }

    @Test fun `paged unwraps results, data and neither`() {
        fun obj(raw: String) = Json.parseToJsonElement(raw) as JsonObject
        assertEquals(2, obj("""{"count":2,"results":[{"a":1},{"a":2}]}""").paged().size)
        assertEquals(1, obj("""{"data":[{"a":1}]}""").paged().size)
        assertTrue(obj("""{"count":0}""").paged().isEmpty())
        assertTrue(obj("""{"results":null}""").paged().isEmpty())
        assertTrue((null as JsonObject?).paged().isEmpty())
    }

    @Test fun `string returns null rather than throwing on absent or structured values`() {
        val body = Json.parseToJsonElement("""{"a":"x","b":null,"c":{"d":1}}""") as JsonObject
        assertEquals("x", body.string("a"))
        assertNull(body.string("b"))
        assertNull(body.string("c"))
        assertNull(body.string("missing"))
    }

}

class CredentialRedactionTest {

    /** These generated strings ship in the release binary; they must not carry the secret. */
    @Test fun `credential payloads never stringify their secret`() {
        val login = LoginPayload("demo.resident", "sup3rSecret!").toString()
        assertTrue(login, login.contains("demo.resident")) // identifying the account is still useful
        assertFalse(login, login.contains("sup3rSecret!"))

        assertFalse(RefreshPayload("refresh-token-value").toString().contains("refresh-token-value"))
        assertFalse(LogoutPayload("refresh-token-value").toString().contains("refresh-token-value"))
        assertFalse(ChangePasswordPayload("old-secret", "new-secret", "new-secret").toString().contains("old-secret"))
        assertFalse(PasswordResetConfirmPayload("uid-secret", "token-secret", "new", "new").toString().contains("token-secret"))
    }
}

class InstitutionalTokenStoreTest {
    @Test fun `in-memory store round-trips and clears`() {
        val store = InMemoryTokenStore()
        assertNull(store.access)
        store.save("a", "r")
        assertEquals("a", store.access)
        assertEquals("r", store.refresh)
        store.saveUserId(42)
        assertEquals(42, store.userId)
        store.clear()
        assertNull(store.access)
        assertNull(store.refresh)
        assertNull(store.userId)
    }
}
