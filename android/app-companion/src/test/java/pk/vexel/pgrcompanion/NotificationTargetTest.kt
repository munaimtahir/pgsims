package pk.vexel.pgrcompanion

import kotlinx.coroutines.runBlocking
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.Assert.*
import org.junit.Test

class NotificationTargetTest {
    @Test fun exactIdsAndRecoverableErrors(): Unit = runBlocking {
        val server = MockWebServer()
        server.start()
        try {
            val repository = InstitutionalRepository(server.url("/").toString(), InMemoryTokenStore().apply { save("synthetic", "synthetic") })
            for ((kind, path) in mapOf("leave" to "leaves", "logbook" to "academics/logbook-entries", "evaluation" to "academics/evaluation-submissions", "rotation" to "rotations")) {
                server.enqueue(MockResponse().setBody("""{"id":42,"status":"DRAFT"}"""))
                assertEquals("42", repository.notificationTarget(kind, 42).getOrThrow().string("id"))
                assertEquals("/api/$path/42/", server.takeRequest().path)
            }
            for (code in listOf(403, 404)) {
                server.enqueue(MockResponse().setResponseCode(code).setBody("{}"))
                assertTrue(repository.notificationTarget("leave", 404).isFailure)
                server.takeRequest()
            }
            val before = server.requestCount
            assertTrue(repository.notificationTarget("unsupported", 1).isFailure)
            assertEquals(before, server.requestCount)
        } finally { server.shutdown() }
    }
}
