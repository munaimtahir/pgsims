package fmu.pg.sims.feature.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
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
import fmu.pg.sims.core.designsystem.FmuStatusAmber
import fmu.pg.sims.core.designsystem.FmuStatusAmberBg
import fmu.pg.sims.core.designsystem.FmuStatusGreen
import fmu.pg.sims.core.designsystem.FmuStatusGreenBg
import fmu.pg.sims.ui.TestTags
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading

@Composable
fun HomeScreen(
    viewModelFactory: ViewModelFactory,
    onGoToDocuments: () -> Unit,
    viewModel: HomeViewModel = viewModel(factory = viewModelFactory),
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.error != null -> ErrorRetryView(message = uiState.error!!, onRetry = viewModel::refresh)
        else -> {
            val me = uiState.me
            val onboarding = uiState.onboarding
            val outstandingCount = maxOf(me?.pendingUploadCount ?: 0, onboarding?.pendingUploadCount ?: 0)

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text(text = "Welcome back, ${me?.username ?: ""}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)

                if (outstandingCount > 0) {
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = FmuStatusAmberBg,
                        modifier = Modifier.fillMaxWidth().testTag(TestTags.HOME_OUTSTANDING_BANNER),
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(text = "ACTION REQUIRED", color = FmuStatusAmber, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelLarge)
                            Text(
                                text = "$outstandingCount document(s) outstanding",
                                color = FmuStatusAmber,
                                style = MaterialTheme.typography.bodyMedium,
                            )
                            Button(
                                onClick = onGoToDocuments,
                                modifier = Modifier.padding(top = 8.dp).testTag(TestTags.HOME_UPLOAD_DOCUMENTS_BUTTON),
                            ) {
                                Text("Upload Documents")
                            }
                        }
                    }
                } else {
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = FmuStatusGreenBg,
                        modifier = Modifier.fillMaxWidth().testTag(TestTags.HOME_ALL_COMPLETE_BANNER),
                    ) {
                        Text(
                            text = "All required documents are complete.",
                            color = FmuStatusGreen,
                            modifier = Modifier.padding(16.dp),
                        )
                    }
                }

                InfoCard(title = "Training", value = uiState.trainingProgram.ifBlank { "Not set" }, subtitle = uiState.trainingLevel)
                InfoCard(
                    title = "Supervisor",
                    value = when (onboarding?.supervisorStatus) {
                        "ASSIGNED" -> "Assigned"
                        "PENDING" -> "Pending confirmation"
                        else -> "Not yet linked"
                    },
                    subtitle = "",
                )
                InfoCard(title = "Onboarding status", value = "Approved", subtitle = "")
            }
        }
    }
}

@Composable
private fun InfoCard(title: String, value: String, subtitle: String) {
    Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = title, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(text = value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            if (subtitle.isNotBlank()) {
                Text(text = subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}
