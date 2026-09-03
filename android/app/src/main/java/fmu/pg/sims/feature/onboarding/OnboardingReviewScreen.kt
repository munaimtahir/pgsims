package fmu.pg.sims.feature.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import fmu.pg.sims.core.designsystem.FmuStatusAmber
import fmu.pg.sims.core.designsystem.FmuStatusGreen
import fmu.pg.sims.core.model.ReviewStatus
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading
import fmu.pg.sims.ui.components.InlineErrorBanner
import fmu.pg.sims.ui.components.OnboardingStepScaffold

@Composable
fun OnboardingReviewScreen(
    viewModel: OnboardingViewModel,
    onBack: () -> Unit,
    onSubmitted: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(uiState.state?.reviewStatus) {
        if (uiState.state?.reviewStatus == ReviewStatus.PENDING_REVIEW) onSubmitted()
    }

    when {
        uiState.loading -> FullScreenLoading()
        uiState.loadError != null -> ErrorRetryView(message = uiState.loadError!!, onRetry = viewModel::load)
        else -> {
            val state = uiState.state
            val profileComplete = state?.profileComplete ?: false
            val missing = state?.requiredOnboardingFields.orEmpty()
            val outstandingDocs = uiState.documents.filter { it.isOutstanding }
            val supervisorLinked = state?.supervisorStatus != "NOT_STARTED"

            OnboardingStepScaffold(
                title = "Review & Submit",
                stepIndex = 5,
                stepCount = 6,
                onBack = onBack,
                primaryLabel = "Submit for Review",
                primaryEnabled = profileComplete,
                primaryLoading = uiState.submitting,
                onPrimaryClick = viewModel::submit,
            ) {
                ReviewRow(
                    ok = profileComplete,
                    okText = "Required profile fields complete",
                    warnText = "${missing.size} required field(s) missing",
                )
                ReviewRow(
                    ok = supervisorLinked,
                    okText = "Supervisor identified",
                    warnText = "No supervisor selected yet",
                )
                ReviewRow(
                    ok = outstandingDocs.isEmpty(),
                    okText = "All documents uploaded",
                    warnText = "${outstandingDocs.size} document(s) outstanding (deferred documents are allowed)",
                )

                if (!profileComplete) {
                    InlineErrorBanner(message = "Complete all required fields before submitting. Missing: ${missing.joinToString(", ")}")
                }
                if (uiState.submitError != null) {
                    InlineErrorBanner(message = uiState.submitError!!)
                }

                Text(
                    text = "By submitting, you confirm the information provided is correct and the documents " +
                        "you uploaded are authentic. Your profile will be sent for administrative review.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun ReviewRow(ok: Boolean, okText: String, warnText: String) {
    Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), modifier = Modifier.fillMaxWidth()) {
        Row(modifier = Modifier.padding(12.dp)) {
            Icon(
                imageVector = if (ok) Icons.Default.CheckCircle else Icons.Default.Warning,
                contentDescription = null,
                tint = if (ok) FmuStatusGreen else FmuStatusAmber,
            )
            Text(
                text = if (ok) okText else warnText,
                modifier = Modifier.padding(start = 8.dp),
                fontWeight = FontWeight.Medium,
            )
        }
    }
}
