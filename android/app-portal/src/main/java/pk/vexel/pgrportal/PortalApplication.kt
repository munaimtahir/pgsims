package pk.vexel.pgrportal

import android.app.Application

class PortalApplication : Application() {
    val institutional: InstitutionalRepository by lazy { InstitutionalRepository(this) }
}
