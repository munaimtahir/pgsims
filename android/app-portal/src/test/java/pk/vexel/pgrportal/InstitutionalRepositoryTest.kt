package pk.vexel.pgrportal

import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
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
private const val LOGBOOK_BODY = """{"count":1,"results":[{"id":4,"title":"Synthetic activity","entry_date":"2026-09-01","status":"DRAFT"}]}"""
private const val CATEGORIES_BODY = """{"count":1,"results":[{"id":2,"name":"Clinical activity"}]}"""
private const val ASSESSMENTS_BODY = """{"count":0,"results":[]}"""
private const val RESEARCH_BODY = """{"status":"DRAFT"}"""
private const val WORKSHOPS_BODY = """{"count":0,"results":[]}"""
private const val RESIDENT_SUMMARY_BODY = """{"current_rotation":{"id":8,"department":"Medicine","status":"ACTIVE"}}"""

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
        assertTrue(snapshot.unavailable.isEmpty())
        assertEquals("Bearer access-1", bearerOf(server.takeRequest()))
    }

    /** A SUPERVISOR or ADMIN account gets 403 from the resident-only endpoints. */
    @Test fun `snapshot still succeeds when resident-only sections are forbidden`() = runBlocking {
        tokens.save("access-1", "refresh-1")
        server.enqueue(json("""{"id":2,"username":"demo.supervisor","role":"SUPERVISOR"}"""))
        server.enqueue(json("""{"detail":"Resident onboarding is only available to residents."}""", 403))
        server.enqueue(json("""[]"""))
        server.enqueue(json("""{"count":0,"results":[]}"""))
        server.enqueue(json("""{"count":0,"results":[]}"""))
        enqueueResidentWorkflowBodies()

        val snapshot = repository.snapshot().getOrThrow()

        assertEquals("SUPERVISOR", snapshot.me.string("role"))
        assertNull(snapshot.onboarding)
        assertEquals(listOf("Onboarding"), snapshot.unavailable)
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

    private fun enqueueResidentWorkflowBodies() {
        server.enqueue(json(ROTATIONS_BODY))
        server.enqueue(json(LOGBOOK_BODY))
        server.enqueue(json(CATEGORIES_BODY))
        server.enqueue(json(ASSESSMENTS_BODY))
        server.enqueue(json(RESEARCH_BODY))
        server.enqueue(json(WORKSHOPS_BODY))
        server.enqueue(json(RESIDENT_SUMMARY_BODY))
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
    }
}

class InstitutionalTokenStoreTest {
    @Test fun `in-memory store round-trips and clears`() {
        val store = InMemoryTokenStore()
        assertNull(store.access)
        store.save("a", "r")
        assertEquals("a", store.access)
        assertEquals("r", store.refresh)
        store.clear()
        assertNull(store.access)
        assertNull(store.refresh)
    }
}
