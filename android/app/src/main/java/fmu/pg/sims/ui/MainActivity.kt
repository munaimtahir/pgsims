package fmu.pg.sims.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import fmu.pg.sims.PgsimsApplication
import fmu.pg.sims.core.ViewModelFactory
import fmu.pg.sims.core.designsystem.PgsimsTheme
import fmu.pg.sims.ui.navigation.PgsimsNavHost

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val appContainer = (application as PgsimsApplication).appContainer
        val viewModelFactory = ViewModelFactory(appContainer)

        setContent {
            PgsimsTheme {
                PgsimsNavHost(viewModelFactory = viewModelFactory)
            }
        }
    }
}
