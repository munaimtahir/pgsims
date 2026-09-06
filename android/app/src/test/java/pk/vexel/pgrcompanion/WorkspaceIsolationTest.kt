package pk.vexel.pgrcompanion

import kotlinx.coroutines.runBlocking
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

/**
 * The two rules the product cannot break (spec §17):
 *
 *   institutional authentication failure MUST NOT break the Personal Workspace, and
 *   institution logout MUST NOT delete unrelated local companion data.
 *
 * These run against the real [LocalStore] and the real [InstitutionalRepository], sharing nothing
 * but the process — which is exactly the claim being tested.
 */
class WorkspaceIsolationTest {

    private lateinit var server: MockWebServer
    private lateinit var storage: InMemoryStorage
    private lateinit var store: LocalStore
    private lateinit var tokens: InMemoryTokenStore
    private lateinit var institution: InstitutionalRepository

    private val personalRecords = AppData(
        profile = ResidentProfile("A Resident", institution = "Some Other Hospital", programme = "FCPS"),
        rotations = listOf(Rotation(title = "Medicine")),
        milestones = listOf(Milestone(title = "Synopsis submitted")),
        reminders = listOf(ReminderRecord(title = "Supervisor meeting", dueDate = "12 Sep 2026", dueAtMillis = 4_000_000_000_000L)),
    )

    @Before fun setUp() {
        server = MockWebServer().also { it.start() }
        storage = InMemoryStorage()
        store = LocalStore(storage)
        store.save(personalRecords)
        tokens = InMemoryTokenStore()
        institution = InstitutionalRepository(server.url("/").toString(), tokens)
    }

    @After fun tearDown() = server.shutdown()

    @Test fun `a failed institutional login leaves every personal record readable`() = runBlocking {
        server.enqueue(MockResponse().setResponseCode(401).setBody("""{"detail":"no"}"""))

        val result = institution.login("someone", "wrong")

        assertTrue(result.isFailure)
        assertFalse(institution.isConnected())
        // The Personal Workspace is reconstructed from storage, as it would be on the next launch.
        assertEquals(personalRecords, LocalStore(storage).read())
    }

    @Test fun `an institutional outage leaves every personal record readable`() = runBlocking {
        tokens.save("access", "refresh")
        server.shutdown()

        assertTrue(institution.snapshot().isFailure)

        assertEquals(personalRecords, LocalStore(storage).read())
        assertNotNull(LocalStore(storage).read().profile)
    }

    @Test fun `institution sign-out clears the session and nothing else`() = runBlocking {
        tokens.save("access", "refresh")
        server.enqueue(MockResponse().setResponseCode(205))

        institution.logout()

        assertNull(tokens.access)
        assertNull(tokens.refresh)
        assertFalse(institution.isConnected())
        assertEquals(personalRecords, LocalStore(storage).read())
    }

    @Test fun `deleting all personal data does not sign the user out of their institution`() {
        tokens.save("access", "refresh")

        store.clear()

        assertEquals(AppData(), LocalStore(storage).read())
        assertTrue(institution.isConnected()) // the two boundaries are independent in both directions
    }

    @Test fun `a corrupt personal blob degrades to an empty workspace instead of crashing`() {
        val corrupt = InMemoryStorage("{ this is not json")
        assertEquals(AppData(), LocalStore(corrupt).read())
    }

    @Test fun `records written by the approved 1_0_0 baseline still load`() {
        // 1.0.0 had no dueAtMillis on reminders; that data must survive the upgrade untouched.
        val legacy = InMemoryStorage(
            """{"profile":{"fullName":"Old User"},"reminders":[{"id":"r1","title":"Old reminder","dueDate":"01 Jan 2026","kind":"Task","completed":false}]}"""
        )
        val restored = LocalStore(legacy).read()
        assertEquals("Old User", restored.profile?.fullName)
        assertEquals(1, restored.reminders.size)
        assertNull(restored.reminders.first().dueAtMillis)
    }
}
