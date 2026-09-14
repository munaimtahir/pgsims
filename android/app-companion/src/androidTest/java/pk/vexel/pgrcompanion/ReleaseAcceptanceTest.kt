package pk.vexel.pgrcompanion

import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.junit.Assert.*
import org.junit.Assume.assumeTrue
import org.junit.Test
import java.io.File

/** Manual device gates. Never logs credentials, tokens, or institutional content.
 * Explicit opt-in prevents normal connected tests from touching an authenticated demo session.
 */
class ReleaseAcceptanceTest {
    private val instrumentation = InstrumentationRegistry.getInstrumentation()
    private val context get() = instrumentation.targetContext
    private fun authorize() {
        assumeTrue(InstrumentationRegistry.getArguments().getString("releaseAcceptance") == "authorized-demo")
        check(BuildConfig.DEBUG && !BuildConfig.FCM_ENABLED)
    }

    @Test fun forceRefresh(): Unit = runBlocking {
        authorize()
        val expected = InstrumentationRegistry.getArguments().getString("expectedRole")
        check(expected in listOf("RESIDENT", "SUPERVISOR"))
        val tokens = EncryptedTokenStore.create(context)
        check(tokens.access != null && tokens.refresh != null)
        val refresh = tokens.refresh!!
        // Invalid access triggers the real 401 -> refresh -> retried request path.
        tokens.save("release-acceptance-invalid-access", refresh)
        val repository = InstitutionalRepository(context)
        val snapshot = repository.snapshot().getOrThrow()
        assertEquals(expected, snapshot.me.string("role"))
        assertNotEquals("release-acceptance-invalid-access", tokens.access)
        assertNotNull(tokens.refresh)
        repository.notifications().getOrThrow()
        repository.unreadNotificationCount().getOrThrow()
        repository.notificationPreferences().getOrThrow()
    }

    @Test fun inspectEncryptedRecovery() {
        authorize()
        val drafts = OfflineDraftStore(context).all()
        val uploads = OfflineUploadStore(context).all()
        assertTrue("Expected at least one queued draft or upload", drafts.isNotEmpty() || uploads.isNotEmpty())
        for (upload in uploads) {
            val encrypted = File(context.filesDir, "institutional_upload_queue/${upload.id}").readBytes()
            val plain = OfflineUploadStore(context).open(upload).use { it.readBytes() }
            assertEquals(upload.sizeBytes, plain.size.toLong())
            assertFalse("Source must be encrypted at rest", plain.contentEquals(encrypted))
        }
        val result = android.os.Bundle()
        result.putString("recovery_counts", "leave=${drafts.count { it.kind == "leave" }},logbook=${drafts.count { it.kind == "logbook" }},upload=${uploads.size}")
        instrumentation.sendStatus(0, result)
    }

    @Test fun retainSyntheticDraftsForReplay() {
        authorize()
        val drafts = OfflineDraftStore(context).all()
        assertEquals(2, drafts.size)
        assertTrue(drafts.any { it.leave?.reason?.startsWith("ANDROID-ACCEPTANCE-") == true })
        assertTrue(drafts.any { it.logbook?.title?.startsWith("ANDROID-ACCEPTANCE-") == true })
        // Only explicitly labeled synthetic test payloads; remove this fixture after the run.
        File(context.cacheDir, "release-acceptance-drafts.json").writeText(Json.encodeToString(drafts))
        val result = android.os.Bundle()
        result.putString("idempotency_keys", drafts.joinToString { it.leave?.client_request_id ?: it.logbook?.client_request_id ?: error("Missing key") })
        instrumentation.sendStatus(0, result)
    }

    @Test fun replaySyntheticDrafts(): Unit = runBlocking {
        authorize()
        val repository = InstitutionalRepository(context)
        assertEquals("RESIDENT", repository.snapshot().getOrThrow().me.string("role"))
        assertTrue("Worker must finish before replay", OfflineDraftStore(context).all().isEmpty())
        val drafts = Json.decodeFromString<List<OfflineDraft>>(File(context.cacheDir, "release-acceptance-drafts.json").readText())
        for (draft in drafts) {
            val first = if (draft.leave != null) repository.createLeave(draft.leave).getOrThrow()
                else repository.createLogbook(draft.logbook!!).getOrThrow()
            val second = if (draft.leave != null) repository.createLeave(draft.leave).getOrThrow()
                else repository.createLogbook(draft.logbook!!).getOrThrow()
            assertNotNull(first.string("id"))
            assertEquals(first.string("id"), second.string("id"))
            val result = android.os.Bundle()
            result.putString("replayed_record", "${draft.kind}:${first.string("id")}")
            instrumentation.sendStatus(0, result)
        }
    }

    @Test fun stageSyntheticUpload() {
        authorize()
        // A deliberately nonexistent target permits retry/discard testing without replacing
        // any institutional document. It can never succeed against an unrelated document.
        val source = "%PDF-1.4\nANDROID-ACCEPTANCE-20260915-SYNTHETIC-ONLY\n%%EOF".byteInputStream()
        val owner = EncryptedTokenStore.create(context).userId ?: error("Run forceRefresh before staging")
        source.use { OfflineUploadStore(context).stage(-1, "ANDROID-ACCEPTANCE-20260915.pdf", "application/pdf", owner, it) }
    }

    @Test fun enqueueRecovery() {
        authorize()
        (context.applicationContext as CompanionApplication).enqueueOfflineRecovery()
    }

    @Test fun stageSyntheticDraftsForLogout() {
        authorize()
        val drafts = Json.decodeFromString<List<OfflineDraft>>(File(context.cacheDir, "release-acceptance-drafts.json").readText())
        val store = OfflineDraftStore(context)
        val owner = EncryptedTokenStore.create(context).userId ?: error("Run forceRefresh before staging")
        drafts.forEach { draft ->
            draft.leave?.let { store.saveLeave(it, owner) }
            draft.logbook?.let { store.saveLogbook(it, owner) }
        }
    }

    @Test fun assertLogoutPurge() {
        authorize()
        val tokens = EncryptedTokenStore.create(context)
        assertNull(tokens.access)
        assertNull(tokens.refresh)
        assertTrue(OfflineDraftStore(context).all().isEmpty())
        assertTrue(OfflineUploadStore(context).all().isEmpty())
        assertTrue(File(context.filesDir, "institutional_upload_queue").listFiles().orEmpty().isEmpty())
    }
}
