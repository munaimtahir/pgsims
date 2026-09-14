package pk.vexel.pgrcompanion

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import androidx.work.ListenableWorker
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

internal object RecoveryCoordinator { val mutex = Mutex() }

/** Logout waits for this critical section before purging either encrypted store. */
class OfflineDraftSyncWorker(context: Context, parameters: WorkerParameters) : CoroutineWorker(context, parameters) {
    override suspend fun doWork(): Result = replayOffline(applicationContext, (applicationContext as CompanionApplication).institutional)
}

internal suspend fun replayOffline(applicationContext: Context, repository: InstitutionalRepository): ListenableWorker.Result =
    RecoveryCoordinator.mutex.withLock {
        if (!repository.isConnected()) return@withLock ListenableWorker.Result.success()
        val owner = repository.me().getOrNull()?.string("id")?.toIntOrNull()
            ?: return@withLock ListenableWorker.Result.retry()
        val drafts = OfflineDraftStore(applicationContext)
        var retry = false
        for (draft in drafts.all()) {
            currentCoroutineContext().ensureActive()
            if (draft.ownerUserId != owner) {
                drafts.update(draft.copy(state = "failed", lastError = "This draft belongs to another or unknown account. Discard it explicitly."))
                continue
            }
            val result = when (draft.kind) {
                "leave" -> draft.leave?.let { repository.createLeave(it) }
                "logbook" -> draft.logbook?.let { repository.createLogbook(it) }
                else -> null
            } ?: continue
            currentCoroutineContext().ensureActive()
            if (result.isSuccess) drafts.remove(draft.id) else {
                drafts.update(draft.copy(state = "failed", attempts = draft.attempts + 1, lastError = "Retry failed; draft retained."))
                retry = true
            }
        }
        val uploads = OfflineUploadStore(applicationContext)
        for (upload in uploads.all()) {
            currentCoroutineContext().ensureActive()
            if (upload.ownerUserId != owner) {
                uploads.update(upload.copy(state = OfflineUpload.FAILED, lastError = "This upload belongs to another or unknown account. Discard it explicitly."))
                continue
            }
            uploads.update(upload.copy(state = OfflineUpload.UPLOADING, attempts = upload.attempts + 1, lastError = null))
            val result = repository.upload(upload, uploads)
            currentCoroutineContext().ensureActive()
            result.fold(
                { uploads.remove(upload) },
                { uploads.update(upload.copy(state = OfflineUpload.FAILED, attempts = upload.attempts + 1, lastError = "Upload failed; encrypted source retained.")); retry = true },
            )
        }
        if (retry) ListenableWorker.Result.retry() else ListenableWorker.Result.success()
    }
