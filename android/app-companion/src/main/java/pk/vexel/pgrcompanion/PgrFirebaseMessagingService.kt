package pk.vexel.pgrcompanion

import com.google.firebase.messaging.FirebaseMessagingService
import kotlinx.coroutines.launch

/** Token registration is best effort; no token is transmitted without an authenticated session. */
class PgrFirebaseMessagingService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Firebase may refresh before login.  Registration is also attempted after sign-in.
        if (BuildConfig.FCM_ENABLED && (application as CompanionApplication).institutional.isConnected()) {
            kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                (application as CompanionApplication).institutional.registerPushToken(token)
            }
        }
    }
}
