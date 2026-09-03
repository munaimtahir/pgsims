package fmu.pg.sims

import android.app.Application
import fmu.pg.sims.core.AppContainer

class PgsimsApplication : Application() {
    lateinit var appContainer: AppContainer
        private set

    override fun onCreate() {
        super.onCreate()
        appContainer = AppContainer(this)
    }
}
