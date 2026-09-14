package pk.vexel.pgrcompanion

import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class RecoveryOwnershipTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private fun requireEmptySession() {
        check(!InstitutionalRepository(context).isConnected())
        check(OfflineUploadStore(context).all().isEmpty())
        check(OfflineDraftStore(context).all().isEmpty())
    }
    private fun repository(server: MockWebServer) = InstitutionalRepository(server.url("/").toString(), InMemoryTokenStore().apply { save("synthetic", "synthetic") })

    @Test fun unownedAndOtherOwnerUploadsAreNeverAdopted(): Unit = runBlocking {
        requireEmptySession()
        val server = MockWebServer()
        server.enqueue(MockResponse().setBody("""{"id":9001,"role":"RESIDENT"}"""))
        server.start()
        val store = OfflineUploadStore(context)
        try {
            val unowned = store.stage(-9001, "ANDROID-CLOSURE-UNOWNED.pdf", "application/pdf", 9002, byteArrayOf(1).inputStream())
            store.update(unowned.copy(ownerUserId = null))
            val other = store.stage(-9002, "ANDROID-CLOSURE-OTHER.pdf", "application/pdf", 9002, byteArrayOf(2).inputStream())
            replayOffline(context, repository(server))
            assertEquals(1, server.requestCount)
            assertEquals("/api/auth/me/", server.takeRequest().path)
            assertEquals(2, store.all().size)
            assertTrue(store.all().all { it.state == OfflineUpload.FAILED })
            assertNull(store.all().single { it.id == unowned.id }.ownerUserId)
            assertEquals(9002, store.all().single { it.id == other.id }.ownerUserId)
        } finally { store.clear(); server.shutdown() }
    }

    @Test fun purgeWaitsForActiveRecoveryAndLeavesNoResurrectedMetadata(): Unit = runBlocking {
        requireEmptySession()
        val reachedUpload = CountDownLatch(1)
        val releaseUpload = CountDownLatch(1)
        val server = MockWebServer()
        server.dispatcher = object : Dispatcher() {
            override fun dispatch(request: RecordedRequest): MockResponse {
                if (request.path == "/api/auth/me/") return MockResponse().setBody("""{"id":9001,"role":"RESIDENT"}""")
                reachedUpload.countDown()
                check(releaseUpload.await(20, TimeUnit.SECONDS))
                return MockResponse().setBody("""{"id":9001,"status":"PENDING_REVIEW"}""")
            }
        }
        server.start()
        val store = OfflineUploadStore(context)
        try {
            store.stage(-9001, "ANDROID-CLOSURE-PURGE.pdf", "application/pdf", 9001, byteArrayOf(1).inputStream())
            val recovery = async(Dispatchers.IO) { replayOffline(context, repository(server)) }
            check(reachedUpload.await(15, TimeUnit.SECONDS))
            val purgeStarted = CompletableDeferred<Unit>()
            val purge = async(Dispatchers.IO) {
                purgeStarted.complete(Unit)
                (context.applicationContext as CompanionApplication).purgeInstitutionalRecoveryMaterial()
            }
            purgeStarted.await()
            assertFalse(purge.isCompleted)
            releaseUpload.countDown()
            withTimeout(15000) { recovery.await(); purge.await() }
            assertTrue(OfflineUploadStore(context).all().isEmpty())
            assertTrue(OfflineDraftStore(context).all().isEmpty())
            assertTrue(context.cacheDir.listFiles().orEmpty().none { it.name.startsWith("pgr-upload-") })
        } finally { releaseUpload.countDown(); store.clear(); server.shutdown() }
    }
}
