package fmu.pg.sims.feature.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import fmu.pg.sims.ui.TestTags
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading

@Composable
fun OnboardingWelcomeScreen(
    viewModel: OnboardingViewModel,
    onStart: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.loadError != null -> ErrorRetryView(message = uiState.loadError!!, onRetry = viewModel::load)
        else -> {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
            ) {
                Text(text = "Welcome to PGR SIMS", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "Before you can access your resident dashboard, complete your onboarding profile: " +
                        "personal information, training details, supervisor, and required documents.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(modifier = Modifier.height(8.dp))
                val missing = uiState.state?.requiredOnboardingFields.orEmpty()
                if (missing.isNotEmpty()) {
                    Text(
                        text = "${missing.size} required item(s) remaining.",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary,
                    )
                }
                Spacer(modifier = Modifier.height(32.dp))
                Button(
                    onClick = onStart,
                    modifier = Modifier.fillMaxWidth().testTag(TestTags.ONBOARDING_WELCOME_START_BUTTON),
                ) {
                    Text(if (missing.isEmpty()) "Continue" else "Get Started")
                }
            }
        }
    }
}
