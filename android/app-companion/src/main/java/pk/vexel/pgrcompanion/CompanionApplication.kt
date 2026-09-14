package pk.vexel.pgrcompanion

import android.app.Application
import androidx.work.*
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.sync.withLock

class CompanionApplication : Application() {
    val institutional: InstitutionalRepository by lazy { InstitutionalRepository(this) }

    override fun onCreate() {
        super.onCreate()
        val request = PeriodicWorkRequestBuilder<OfflineDraftSyncWorker>(15, TimeUnit.MINUTES)
            .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
            .build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "institutional-offline-draft-sync", ExistingPeriodicWorkPolicy.KEEP, request,
        )
    }

    fun enqueueOfflineRecovery() {
        val request = OneTimeWorkRequestBuilder<OfflineDraftSyncWorker>()
            .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 15, TimeUnit.MINUTES)
            .build()
        WorkManager.getInstance(this).enqueueUniqueWork(
            "institutional-offline-recovery-now", ExistingWorkPolicy.KEEP, request,
        )
    }

    suspend fun signOutInstitutional() = withContext(Dispatchers.IO) {
        cancelRecovery()
        RecoveryCoordinator.mutex.withLock {
            institutional.logout()
            clearRecovery()
        }
    }

    suspend fun purgeInstitutionalRecoveryMaterial() = withContext(Dispatchers.IO) {
        cancelRecovery()
        RecoveryCoordinator.mutex.withLock { clearRecovery() }
    }

    private fun cancelRecovery() {
        val manager = WorkManager.getInstance(this)
        manager.cancelUniqueWork("institutional-offline-recovery-now").result.get()
        manager.cancelUniqueWork("institutional-offline-draft-sync").result.get()
    }

    private fun clearRecovery() {
        OfflineDraftStore(this).clear()
        OfflineUploadStore(this).clear()
    }
}
