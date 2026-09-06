package pk.vexel.pgrcompanion

import android.app.Application

class CompanionApplication : Application() {
    lateinit var store: LocalStore
        private set

    /**
     * Institutional Workspace boundary. Built lazily so that no networking, keystore or
     * institution-specific work happens on the startup path of the offline Personal Workspace.
     */
    val institutional: InstitutionalRepository by lazy { InstitutionalRepository(this) }

    override fun onCreate() {
        super.onCreate()
        store = LocalStore(this)
    }
}
