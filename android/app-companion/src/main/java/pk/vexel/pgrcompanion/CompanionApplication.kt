package pk.vexel.pgrcompanion

import android.app.Application

class CompanionApplication : Application() {
    val institutional: InstitutionalRepository by lazy { InstitutionalRepository(this) }
}
