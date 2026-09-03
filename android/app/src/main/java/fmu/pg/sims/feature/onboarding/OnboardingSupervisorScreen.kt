package fmu.pg.sims.feature.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import fmu.pg.sims.core.designsystem.FmuStatusGreen
import fmu.pg.sims.core.designsystem.FmuStatusGreenBg
import fmu.pg.sims.core.model.SupervisorOption
import fmu.pg.sims.ui.TestTags
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading
import fmu.pg.sims.ui.components.InlineErrorBanner
import fmu.pg.sims.ui.components.LabeledTextField
import fmu.pg.sims.ui.components.OnboardingStepScaffold

@Composable
fun OnboardingSupervisorScreen(
    viewModel: OnboardingViewModel,
    residentProfileId: Int?,
    onBack: () -> Unit,
    onNext: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()
    var query by remember { mutableStateOf("") }
    var showNotListedForm by remember { mutableStateOf(false) }
    var manualName by remember { mutableStateOf("") }
    var manualDepartment by remember { mutableStateOf("") }
    var manualInstitution by remember { mutableStateOf("") }
    var manualPmdc by remember { mutableStateOf("") }
    var manualEmail by remember { mutableStateOf("") }
    var manualPhone by remember { mutableStateOf("") }

    LaunchedEffect(Unit) { viewModel.loadSupervisorOptions() }

    when {
        uiState.loading -> FullScreenLoading()
        uiState.loadError != null -> ErrorRetryView(message = uiState.loadError!!, onRetry = viewModel::load)
        else -> {
            val supervisorStatus = uiState.state?.supervisorStatus ?: "NOT_STARTED"
            val pendingLink = uiState.state?.pendingSupervisorLink

            OnboardingStepScaffold(
                title = "Supervisor",
                stepIndex = 3,
                stepCount = 6,
                onBack = onBack,
                primaryLabel = "Continue",
                primaryEnabled = true,
                primaryLoading = false,
                onPrimaryClick = onNext,
                primaryTestTag = TestTags.ONBOARDING_SUPERVISOR_PRIMARY_BUTTON,
            ) {
                when {
                    supervisorStatus == "ASSIGNED" -> Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = FmuStatusGreenBg,
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Text(
                            text = "A primary supervisor is assigned to your record.",
                            color = FmuStatusGreen,
                            modifier = Modifier.padding(12.dp),
                        )
                    }
                    pendingLink != null || uiState.supervisorRequestSuccess -> Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Text(
                            text = "Supervisor request pending administrator confirmation" +
                                (pendingLink?.name?.takeIf { it.isNotBlank() }?.let { ": $it" } ?: "."),
                            modifier = Modifier.padding(12.dp),
                        )
                    }
                    else -> {
                        Text(
                            text = "Search for your supervisor by name, department, or training site.",
                            style = MaterialTheme.typography.bodyMedium,
                        )
                        LabeledTextField(
                            label = "Search supervisors",
                            value = query,
                            onValueChange = { query = it },
                            modifier = Modifier.testTag(TestTags.ONBOARDING_SUPERVISOR_SEARCH_FIELD),
                        )

                        val filtered = uiState.allSupervisors.filter {
                            query.isBlank() ||
                                it.name.contains(query, ignoreCase = true) ||
                                it.department.contains(query, ignoreCase = true) ||
                                it.trainingSite.contains(query, ignoreCase = true)
                        }
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            filtered.take(20).forEach { option ->
                                SupervisorCard(
                                    option = option,
                                    submitting = uiState.supervisorRequestSubmitting,
                                    onSelect = {
                                        if (residentProfileId != null) {
                                            viewModel.requestSupervisor(residentProfileId, option)
                                        }
                                    },
                                )
                            }
                            if (!uiState.supervisorSearchLoading && filtered.isEmpty()) {
                                Text(
                                    text = "No matching supervisors found.",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                )
                            }
                        }

                        TextButton(
                            onClick = { showNotListedForm = !showNotListedForm },
                            modifier = Modifier.testTag(TestTags.ONBOARDING_SUPERVISOR_NOT_LISTED_TOGGLE),
                        ) {
                            Text(if (showNotListedForm) "Cancel" else "My supervisor is not listed")
                        }

                        if (showNotListedForm) {
                            LabeledTextField(
                                label = "Supervisor's full name",
                                value = manualName,
                                onValueChange = { manualName = it },
                                required = true,
                                modifier = Modifier.testTag(TestTags.ONBOARDING_SUPERVISOR_MANUAL_NAME_FIELD),
                            )
                            LabeledTextField(label = "Department", value = manualDepartment, onValueChange = { manualDepartment = it })
                            LabeledTextField(label = "Institution", value = manualInstitution, onValueChange = { manualInstitution = it })
                            LabeledTextField(label = "PMDC number", value = manualPmdc, onValueChange = { manualPmdc = it })
                            LabeledTextField(label = "Email", value = manualEmail, onValueChange = { manualEmail = it })
                            LabeledTextField(label = "Phone", value = manualPhone, onValueChange = { manualPhone = it })
                            Button(
                                onClick = {
                                    if (residentProfileId != null) {
                                        viewModel.requestSupervisorNotListed(
                                            residentProfileId, manualName, manualDepartment,
                                            manualInstitution, manualPmdc, manualEmail, manualPhone,
                                        )
                                    }
                                },
                                enabled = !uiState.supervisorRequestSubmitting,
                                modifier = Modifier.fillMaxWidth().testTag(TestTags.ONBOARDING_SUPERVISOR_SUBMIT_REQUEST_BUTTON),
                            ) { Text("Submit Request") }
                        }

                        if (uiState.supervisorRequestError != null) {
                            InlineErrorBanner(message = uiState.supervisorRequestError!!)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SupervisorCard(option: SupervisorOption, submitting: Boolean, onSelect: () -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Column {
                Text(text = option.name, fontWeight = FontWeight.SemiBold)
                Text(
                    text = listOf(option.designation, option.department, option.trainingSite).filter { it.isNotBlank() }.joinToString(" · "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            OutlinedButton(
                onClick = onSelect,
                enabled = !submitting,
                modifier = Modifier.testTag(TestTags.supervisorSelectButton(option.id)),
            ) { Text("Select") }
        }
    }
}
