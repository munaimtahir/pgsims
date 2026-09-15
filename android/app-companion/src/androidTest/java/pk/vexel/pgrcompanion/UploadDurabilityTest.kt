package pk.vexel.pgrcompanion

import android.os.Bundle
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.io.IOException
import java.io.InputStream
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import org.junit.Assert.*
import org.junit.Assume.assumeTrue
import org.junit.Test
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import okhttp3.mockwebserver.MockWebServer
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.SocketPolicy

/** Synthetic, app-private fixtures only. Host terminates instrumentation at an explicit ack. */
class UploadDurabilityTest {
    private val instrumentation = InstrumentationRegistry.getInstrumentation()
    private val context get() = instrumentation.targetContext
    private val name = "ANDROID-CLOSURE-DURABILITY.pdf"
    private val bytes = "%PDF-1.4 synthetic durability fixture".toByteArray()
    private fun authorize() {
        assumeTrue(InstrumentationRegistry.getArguments().getString("storageAcceptance") == "synthetic-only")
        check(BuildConfig.DEBUG)
        check(!InstitutionalRepository(context).isConnected()) { "Sign out before synthetic storage tests." }
    }
    private fun signal(value: String) = instrumentation.sendStatus(0, Bundle().apply { putString("storage_gate", value) })

    @Test fun stageAndWaitForHostKill() {
        authorize()
        val store = OfflineUploadStore(context)
        check(store.all().isEmpty())
        bytes.inputStream().use { store.stage(-9001, name, "application/pdf", 9001, it) }
        signal("STAGE_ACK")
        CountDownLatch(1).await(2, TimeUnit.MINUTES)
        fail("Host must terminate this process immediately after STAGE_ACK")
    }

    @Test fun uploadAndWaitForHostKill(): Unit = runBlocking {
        authorize()
        val store = OfflineUploadStore(context)
        check(store.all().isEmpty())
        val upload = store.stage(-9001, name, "application/pdf", 9001, bytes.inputStream())
        store.update(upload.copy(state = OfflineUpload.UPLOADING, attempts = 1))
        val server = MockWebServer()
        server.enqueue(MockResponse().setSocketPolicy(SocketPolicy.NO_RESPONSE))
        server.start()
        val repo = InstitutionalRepository(server.url("/").toString(), InMemoryTokenStore().apply { save("synthetic", "synthetic") })
        val job = launch(Dispatchers.IO) { repo.upload(upload, store) }
        checkNotNull(server.takeRequest(15, TimeUnit.SECONDS))
        signal("UPLOAD_IN_FLIGHT")
        CountDownLatch(1).await(2, TimeUnit.MINUTES)
        job.cancel()
        server.shutdown()
        fail("Host must terminate the process with the upload awaiting confirmation")
    }

    @Test fun verifyAfterHostKill() {
        authorize()
        val store = OfflineUploadStore(context)
        val item = store.all().single { it.displayName == name }
        assertEquals(9001, item.ownerUserId)
        assertArrayEquals(bytes, store.open(item).use { it.readBytes() })
        assertFalse(File(context.filesDir, "institutional_upload_queue/${item.id}").readBytes().contentEquals(bytes))
        store.remove(item)
        signal("POST_KILL_VERIFIED")
    }

    @Test fun interruptBeforeAcknowledgment() {
        authorize()
        val store = OfflineUploadStore(context)
        check(store.all().isEmpty())
        store.stage(-9001, name, "application/pdf", 9001, object : InputStream() {
            override fun read(): Int {
                signal("PRE_ACK")
                CountDownLatch(1).await(2, TimeUnit.MINUTES)
                throw IOException("host did not terminate")
            }
        })
    }

    @Test fun verifyPreAckCleanup() {
        authorize()
        assertTrue(OfflineUploadStore(context).all().isEmpty())
        assertTrue(File(context.filesDir, "institutional_upload_queue").listFiles().orEmpty().isEmpty())
        signal("PRE_ACK_CLEANUP_VERIFIED")
    }

    @Test fun metadataCommitFailureDoesNotAcknowledgeOrRetainSource() {
        authorize()
        check(OfflineUploadStore(context).all().isEmpty())
        val store = OfflineUploadStore(context, commitMetadata = { false })
        try {
            store.stage(-9001, name, "application/pdf", 9001, bytes.inputStream())
            fail("Failed metadata commit must not acknowledge staging")
        } catch (_: IllegalStateException) { }
        assertTrue(OfflineUploadStore(context).all().isEmpty())
        assertTrue(File(context.filesDir, "institutional_upload_queue").listFiles().orEmpty().isEmpty())
    }

    @Test fun sourceFailureCleansUpAndReconciliationWaitsForStaging() {
        authorize()
        val store = OfflineUploadStore(context)
        check(store.all().isEmpty())
        try {
            store.stage(-9001, name, "application/pdf", 9001, object : InputStream() {
                override fun read(): Int = throw IOException("synthetic read failure")
            })
            fail("Expected source failure")
        } catch (_: IOException) { }
        assertTrue(store.all().isEmpty())
        assertTrue(File(context.filesDir, "institutional_upload_queue").listFiles().orEmpty().isEmpty())
        val entered = CountDownLatch(1)
        val release = CountDownLatch(1)
        val pool = Executors.newFixedThreadPool(2)
        try {
            val staging = pool.submit<OfflineUpload> {
                store.stage(-9001, name, "application/pdf", 9001, object : InputStream() {
                    var readOnce = false
                    override fun read(): Int {
                        if (readOnce) return -1
                        entered.countDown()
                        check(release.await(10, TimeUnit.SECONDS))
                        readOnce = true
                        return 42
                    }
                })
            }
            check(entered.await(10, TimeUnit.SECONDS))
            val reconciling = pool.submit<OfflineUploadStore> { OfflineUploadStore(context) }
            release.countDown()
            val item = staging.get(10, TimeUnit.SECONDS)
            val recovered = reconciling.get(10, TimeUnit.SECONDS)
            assertEquals(item.id, recovered.all().single().id)
            assertArrayEquals(byteArrayOf(42), recovered.open(item).use { it.readBytes() })
            recovered.remove(item)
        } finally { release.countDown(); pool.shutdownNow() }
    }
}
