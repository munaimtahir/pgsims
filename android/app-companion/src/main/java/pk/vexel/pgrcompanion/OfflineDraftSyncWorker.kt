package pk.vexel.pgrcompanion

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import java.io.File

/** Replays only idempotency-keyed drafts; a server success is the only deletion condition. */
class OfflineDraftSyncWorker(context: Context, parameters: WorkerParameters) : CoroutineWorker(context, parameters) {
    override suspend fun doWork(): Result {
        val drafts = OfflineDraftStore(applicationContext)
        val repository = (applicationContext as CompanionApplication).institutional
        if (!repository.isConnected()) return Result.success()
        for (draft in drafts.all()) {
            val result = when (draft.kind) {
                "leave" -> draft.leave?.let { repository.createLeave(it) }
                "logbook" -> draft.logbook?.let { repository.createLogbook(it) }
                else -> null
            } ?: continue
            if (result.isSuccess) drafts.remove(draft.id) else return Result.retry()
        }
        val uploads = OfflineUploadStore(applicationContext)
        for (upload in uploads.all()) {
            val result = runCatching {
                uploads.update(upload.copy(state = OfflineUpload.UPLOADING, attempts = upload.attempts + 1, lastError = null))
                val temporary = File.createTempFile("pgr-upload-", ".tmp", applicationContext.cacheDir)
                try {
                    uploads.open(upload).use { input -> temporary.outputStream().use(input::copyTo) }
                    repository.upload(upload.documentId, temporary, upload.displayName).getOrThrow()
                } finally {
                    temporary.delete()
                }
            }
            result.fold(
                { uploads.remove(upload) },
                { uploads.update(upload.copy(state = OfflineUpload.FAILED, attempts = upload.attempts + 1, lastError = it.message)) },
            )
            // Retain every failed source and let WorkManager backoff retry it.  It is never
            // discarded or replaced without an explicit user action.
            if (result.isFailure) return Result.retry()
        }
        return Result.success()
    }
}
