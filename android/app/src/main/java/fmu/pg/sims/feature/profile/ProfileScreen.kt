package fmu.pg.sims.feature.profile

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import fmu.pg.sims.core.ViewModelFactory
import fmu.pg.sims.feature.home.HomeViewModel
import fmu.pg.sims.ui.TestTags
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading

@Composable
fun ProfileScreen(
    viewModelFactory: ViewModelFactory,
    onLogout: () -> Unit,
    viewModel: HomeViewModel = viewModel(factory = viewModelFactory),
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.error != null -> ErrorRetryView(message = uiState.error!!, onRetry = viewModel::refresh)
        else -> {
            val me = uiState.me
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Text(text = "Profile", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        ProfileRow(label = "Username", value = me?.username ?: "")
                        ProfileRow(label = "Role", value = me?.role?.displayName ?: "")
                        ProfileRow(label = "Onboarding status", value = me?.effectiveReviewStatus ?: "")
                    }
                }
                Button(
                    onClick = onLogout,
                    modifier = Modifier.fillMaxWidth().testTag(TestTags.PROFILE_SIGN_OUT_BUTTON),
                ) { Text("Sign Out") }
            }
        }
    }
}

@Composable
private fun ProfileRow(label: String, value: String) {
    Column {
        Text(text = label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(text = value.ifBlank { "—" }, style = MaterialTheme.typography.bodyLarge)
    }
}
