package fmu.pg.sims.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.auth.SecureTokenStorage
import fmu.pg.sims.core.designsystem.PgsimsTheme
import fmu.pg.sims.core.network.ApiClient

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
