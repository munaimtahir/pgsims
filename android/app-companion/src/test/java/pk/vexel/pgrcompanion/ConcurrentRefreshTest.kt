package pk.vexel.pgrcompanion

import kotlinx.coroutines.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

class ConcurrentRefreshTest {
    @Test fun simultaneousUnauthorizedRequestsRotateSharedSessionOnlyOnce(): Unit = runBlocking {
        val server = MockWebServer()
        val staleRequests = CountDownLatch(2)
        val refreshCount = AtomicInteger()
        server.dispatcher = object : Dispatcher() {
            override fun dispatch(request: RecordedRequest): MockResponse {
                if (request.path == "/api/auth/refresh/") {
                    refreshCount.incrementAndGet()
                    return MockResponse().setBody("""{"access":"new-access","refresh":"new-refresh"}""")
                }
                if (request.getHeader("Authorization") == "Bearer old-access") {
                    staleRequests.countDown()
                    check(staleRequests.await(10, TimeUnit.SECONDS))
                    return MockResponse().setResponseCode(401).setBody("{}")
                }
                return MockResponse().setBody("""{"id":42}""")
            }
        }
        server.start()
        try {
            val store = InMemoryTokenStore().apply { save("old-access", "old-refresh") }
            val repositories = List(2) { InstitutionalRepository(server.url("/").toString(), store) }
            repositories.map { repository -> async { repository.notificationTarget("leave", 42) } }.awaitAll().forEach {
                assertEquals("42", it.getOrThrow().string("id"))
            }
            assertEquals(1, refreshCount.get())
            assertEquals("new-refresh", store.refresh)
            assertEquals("new-access", store.access)
        } finally { server.shutdown() }
    }
}
