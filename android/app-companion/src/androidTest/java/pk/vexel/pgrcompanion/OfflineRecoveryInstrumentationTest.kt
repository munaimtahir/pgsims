package pk.vexel.pgrcompanion

import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import java.util.UUID

/** Noncredentialed process-recovery checks; uses only synthetic app-private material. */
class OfflineRecoveryInstrumentationTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext

    @Test fun uploadMetadataIsDurableWhenStageReturns() {
        val store = OfflineUploadStore(context)
        store.clear()
        val payload = "%PDF-1.4\nSYNTHETIC-NONCREDENTIALLED\n%%EOF".toByteArray()
        val staged = payload.inputStream().use {
            store.stage(-1001, "synthetic.pdf", "application/pdf", ownerUserId = 1001, input = it)
        }

        val restored = OfflineUploadStore(context).all().single { it.id == staged.id }
        assertEquals(1001, restored.ownerUserId)
        assertEquals(payload.size.toLong(), restored.sizeBytes)
        assertTrue(OfflineUploadStore(context).open(restored).use { it.readBytes().contentEquals(payload) })
        OfflineUploadStore(context).clear()
    }

    @Test fun startupReconciliationRemovesEncryptedFileWithoutMetadata() {
        val store = OfflineUploadStore(context)
        store.clear()
        val directory = File(context.filesDir, "institutional_upload_queue").also(File::mkdirs)
        val orphan = File(directory, "orphan-${UUID.randomUUID()}").apply { writeBytes(byteArrayOf(1, 2, 3)) }
        assertTrue(orphan.exists())

        OfflineUploadStore(context)

        assertFalse(orphan.exists())
        store.clear()
    }
}
