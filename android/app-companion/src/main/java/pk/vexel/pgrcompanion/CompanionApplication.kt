package pk.vexel.pgrcompanion

import android.app.Application
import androidx.work.*
import java.util.concurrent.TimeUnit

class CompanionApplication : Application() {
    val institutional: InstitutionalRepository by lazy { InstitutionalRepository(this) }

    override fun onCreate() {
        super.onCreate()
        // Construction reconciles encrypted queue metadata with app-private files, removing
        // process-death orphans before any worker can attempt recovery.
        runCatching { OfflineUploadStore(this) }
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

    fun purgeInstitutionalRecoveryMaterial() {
        OfflineDraftStore(this).clear()
        OfflineUploadStore(this).clear()
        WorkManager.getInstance(this).cancelUniqueWork("institutional-offline-recovery-now")
    }
}
