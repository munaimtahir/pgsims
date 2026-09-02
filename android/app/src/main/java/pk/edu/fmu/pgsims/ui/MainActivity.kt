package pk.edu.fmu.pgsims.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import pk.edu.fmu.pgsims.core.auth.AuthRepository
import pk.edu.fmu.pgsims.core.auth.SecureTokenStorage
import pk.edu.fmu.pgsims.core.designsystem.PgsimsTheme
import pk.edu.fmu.pgsims.core.network.ApiClient

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val tokenStorage = SecureTokenStorage(applicationContext)
        val apiService = ApiClient.create(tokenStorage = tokenStorage)
        val authRepository = AuthRepository(apiService, tokenStorage)

        setContent {
            PgsimsTheme {
                FoundationScreen(authRepository = authRepository)
            }
        }
    }
}
