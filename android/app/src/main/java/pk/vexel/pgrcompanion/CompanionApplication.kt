package pk.vexel.pgrcompanion

import android.app.Application

class CompanionApplication : Application() {
    lateinit var store: LocalStore
        private set

    override fun onCreate() {
        super.onCreate()
        store = LocalStore(this)
    }
}
