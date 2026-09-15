package pk.vexel.pgrcompanion

import androidx.test.platform.app.InstrumentationRegistry
import androidx.work.WorkManager
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.*
import org.junit.Assert.*
import org.junit.Assume.assumeTrue
import org.junit.Test
import java.io.File

/** Explicit opt-in, authorized demo records only. No credentials or clinical data in fixtures. */
class AuthenticatedParityRecoveryTest {
    private val instrumentation = InstrumentationRegistry.getInstrumentation()
    private val context get() = instrumentation.targetContext
    private val file get() = File(context.cacheDir, "parity-acceptance-fixture.json")
    private val json = Json { ignoreUnknownKeys = true }
    private val marker = "ANDROID-PARITY-20260915-RECOVERY"
    private val pdf = "%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 0/Kids[]>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n".toByteArray()
    private fun authorize() {
        assumeTrue(InstrumentationRegistry.getArguments().getString("parityAcceptance") == "authorized-demo")
        check(BuildConfig.DEBUG && !BuildConfig.FCM_ENABLED)
    }
    private fun fixture() = json.parseToJsonElement(file.readText()).jsonObject
    private fun save(value: JsonObject) = file.writeText(value.toString())
    private fun report(value: String) = instrumentation.sendStatus(0, android.os.Bundle().apply { putString("parity_gate", value) })
    private fun drafts(): Pair<LeaveRequestPayload, AcademicLogbookPayload> {
        val data = fixture()
        return json.decodeFromJsonElement<LeaveRequestPayload>(data.getValue("leave")) to
            json.decodeFromJsonElement<AcademicLogbookPayload>(data.getValue("logbook"))
    }

    @Test fun prepare(): Unit = runBlocking {
        authorize()
        check(!file.exists()) { "Existing acceptance fixture must be reviewed before a new run" }
        val repo = InstitutionalRepository(context)
        assertEquals("RESIDENT", repo.me().getOrThrow().string("role"))
        assertTrue(OfflineDraftStore(context).all().isEmpty())
        assertTrue(OfflineUploadStore(context).all().isEmpty())
        val seedLeave = repo.notificationTarget("leave", 20).getOrThrow()
        val seedLogbook = repo.notificationTarget("logbook", 32).getOrThrow()
        check(seedLeave.string("reason").orEmpty().startsWith("ANDROID-ACCEPTANCE-"))
        check(seedLogbook.string("title").orEmpty().startsWith("ANDROID-ACCEPTANCE-"))
        val doc = repo.snapshot().getOrThrow().documents.single { it.string("id") == "2" }
        check(doc.string("title").orEmpty().startsWith("ANDROID-CLOSURE-"))
        val leave = LeaveRequestPayload(seedLeave.string("resident_training")!!.toInt(), seedLeave.string("leave_type")!!,
            "2026-11-10", "2026-11-11", marker).withOfflineId()
        val logbook = AcademicLogbookPayload(seedLogbook.string("category")!!.toInt(), "2026-09-15", marker,
            description = "Synthetic acceptance record; no patient information.", resident_reflection = "Synthetic reflection").withOfflineId()
        save(buildJsonObject { put("leave", json.encodeToJsonElement(leave)); put("logbook", json.encodeToJsonElement(logbook)) })
        val manager = WorkManager.getInstance(context)
        manager.cancelUniqueWork("institutional-offline-recovery-now").result.get()
        manager.cancelUniqueWork("institutional-offline-draft-sync").result.get()
        report("prepared synthetic fixture; no server writes")
    }

    @Test fun stageOffline() {
        authorize()
        val owner = EncryptedTokenStore.create(context).userId ?: error("Authenticated session required")
        val (leave, logbook) = drafts()
        assertTrue(OfflineDraftStore(context).all().isEmpty())
        OfflineDraftStore(context).saveLeave(leave, owner)
        OfflineDraftStore(context).saveLogbook(logbook, owner)
        OfflineUploadStore(context).stage(2, "$marker.pdf", "application/pdf", owner, pdf.inputStream())
        report("offline staging acknowledged: two drafts and encrypted PDF")
    }

    @Test fun verifyAfterRestart() {
        authorize()
        val (leave, logbook) = drafts()
        val stored = OfflineDraftStore(context).all()
        assertEquals(2, stored.size)
        assertEquals(setOf(leave.client_request_id, logbook.client_request_id), stored.map { it.leave?.client_request_id ?: it.logbook?.client_request_id }.toSet())
        val uploads = OfflineUploadStore(context)
        assertArrayEquals(pdf, uploads.open(uploads.all().single()).use { it.readBytes() })
        report("fresh process retained exact keys and decrypted PDF bytes")
    }

    @Test fun replayAndSubmit(): Unit = runBlocking {
        authorize()
        val repo = InstitutionalRepository(context)
        assertEquals("RESIDENT", repo.me().getOrThrow().string("role"))
        replayOffline(context, repo)
        assertTrue(OfflineDraftStore(context).all().isEmpty())
        assertTrue(OfflineUploadStore(context).all().isEmpty())
        val (leave, logbook) = drafts()
        val firstLeave = repo.createLeave(leave).getOrThrow()
        val firstLog = repo.createLogbook(logbook).getOrThrow()
        assertEquals(firstLeave.string("id"), repo.createLeave(leave).getOrThrow().string("id"))
        assertEquals(firstLog.string("id"), repo.createLogbook(logbook).getOrThrow().string("id"))
        val leaveId = firstLeave.string("id")!!.toInt()
        val logId = firstLog.string("id")!!.toInt()
        save(JsonObject(fixture() + mapOf("leave_id" to JsonPrimitive(leaveId), "logbook_id" to JsonPrimitive(logId))))
        assertEquals("SUBMITTED", repo.submitLeave(leaveId).getOrThrow().string("status"))
        assertEquals("SUBMITTED", repo.submitLogbook(logId).getOrThrow().string("status"))
        report("replayed twice to same IDs; submitted leave=$leaveId logbook=$logId; leave_key=${leave.client_request_id}; logbook_key=${logbook.client_request_id}")
    }

    @Test fun supervisorReturn(): Unit = runBlocking {
        authorize()
        val repo = InstitutionalRepository(context)
        assertEquals("SUPERVISOR", repo.me().getOrThrow().string("role"))
        val id = fixture().string("logbook_id")!!.toInt()
        val entry = repo.notificationTarget("logbook", id).getOrThrow()
        assertEquals(marker, entry.string("title"))
        val returned = repo.returnLogbook(id, "$marker: synthetic correction requested").getOrThrow()
        assertEquals("RETURNED", canonicalLogbookBucket(returned.string("status").orEmpty()))
        report("assigned supervisor returned synthetic logbook=$id")
    }

    @Test fun residentCorrectAndResubmit(): Unit = runBlocking {
        authorize()
        val repo = InstitutionalRepository(context)
        assertEquals("RESIDENT", repo.me().getOrThrow().string("role"))
        val id = fixture().string("logbook_id")!!.toInt()
        val corrected = drafts().second.copy(resident_reflection = "$marker corrected synthetic reflection")
        val result = repo.updateLogbook(id, corrected).getOrThrow()
        assertEquals(corrected.resident_reflection, result.string("resident_reflection"))
        assertEquals("SUBMITTED", repo.submitLogbook(id).getOrThrow().string("status"))
        report("resident corrected and resubmitted logbook=$id")
    }
    @Test fun discardAndLogoutOffline(): Unit = runBlocking {
        authorize()
        check(file.exists())
        val owner = EncryptedTokenStore.create(context).userId ?: error("Authenticated session required")
        val (leave, logbook) = drafts()
        val manager = WorkManager.getInstance(context)
        manager.cancelUniqueWork("institutional-offline-recovery-now").result.get()
        manager.cancelUniqueWork("institutional-offline-draft-sync").result.get()
        val store = OfflineUploadStore(context)
        val disposable = store.stage(2, "$marker-DISCARD.pdf", "application/pdf", owner, pdf.inputStream())
        store.remove(disposable)
        assertTrue(store.all().isEmpty())
        store.stage(2, "$marker-PURGE.pdf", "application/pdf", owner, pdf.inputStream())
        OfflineDraftStore(context).saveLeave(leave.copy(reason = "$marker-PURGE", client_request_id = null).withOfflineId(), owner)
        OfflineDraftStore(context).saveLogbook(logbook.copy(title = "$marker-PURGE", client_request_id = null).withOfflineId(), owner)
        (context.applicationContext as CompanionApplication).signOutInstitutional()
        assertTrue(OfflineDraftStore(context).all().isEmpty())
        assertTrue(OfflineUploadStore(context).all().isEmpty())
        assertNull(EncryptedTokenStore.create(context).access)
        assertNull(EncryptedTokenStore.create(context).refresh)
        report("explicit discard and offline logout purge PASS: two drafts, encrypted PDF and tokens removed")
    }

}
