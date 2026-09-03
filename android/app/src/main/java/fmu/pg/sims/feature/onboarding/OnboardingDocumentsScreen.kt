package fmu.pg.sims.feature.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.unit.dp
import fmu.pg.sims.ui.components.DocumentRow
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading
import fmu.pg.sims.ui.components.InlineErrorBanner
import fmu.pg.sims.ui.components.OnboardingStepScaffold

@Composable
fun OnboardingDocumentsScreen(
    viewModel: OnboardingViewModel,
    onBack: () -> Unit,
    onNext: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.loadError != null -> ErrorRetryView(message = uiState.loadError!!, onRetry = viewModel::load)
        else -> {
            OnboardingStepScaffold(
                title = "Documents",
                stepIndex = 4,
                stepCount = 6,
                onBack = onBack,
                primaryLabel = "Continue",
                primaryEnabled = true,
                primaryLoading = false,
                onPrimaryClick = onNext,
            ) {
                if (uiState.documents.isEmpty()) {
                    Text(
                        text = "No documents are required for onboarding right now.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                } else {
                    Text(
                        text = "Upload required documents now, or defer eligible ones for later. " +
                            "Deferred documents remain outstanding until uploaded.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        uiState.documents.forEach { document ->
                            DocumentRow(
                                document = document,
                                busy = document.id in uiState.documentBusyIds,
                                onUpload = { file, mime -> viewModel.uploadDocument(document.id, file, mime) },
                                onDefer = { viewModel.deferDocument(document.id) },
                            )
                        }
                    }
                }
                if (uiState.documentActionError != null) {
                    InlineErrorBanner(message = uiState.documentActionError!!)
                }
            }
        }
    }
}
