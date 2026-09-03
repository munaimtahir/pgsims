package fmu.pg.sims.feature.onboarding

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading
import fmu.pg.sims.ui.components.InlineErrorBanner
import fmu.pg.sims.ui.components.LabeledTextField
import fmu.pg.sims.ui.components.OnboardingStepScaffold

private val PERSONAL_FIELDS = listOf("full_name", "phone", "email", "registration_no", "cnic")

@Composable
fun OnboardingPersonalInfoScreen(
    viewModel: OnboardingViewModel,
    onBack: () -> Unit,
    onNext: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.loadError != null -> ErrorRetryView(message = uiState.loadError!!, onRetry = viewModel::load)
        else -> {
            val section = uiState.state?.sections?.firstOrNull { it.key == "identity" }
            val fieldMeta = section?.fields.orEmpty().associateBy { it.field }

            OnboardingStepScaffold(
                title = "Personal Information",
                stepIndex = 1,
                stepCount = 6,
                onBack = onBack,
                primaryLabel = "Save & Continue",
                primaryEnabled = true,
                primaryLoading = uiState.saving,
                onPrimaryClick = { viewModel.saveFields(PERSONAL_FIELDS) { success -> if (success) onNext() } },
            ) {
                LabeledTextField(
                    label = fieldMeta["full_name"]?.label ?: "Full name",
                    value = uiState.fieldValues["full_name"] ?: "",
                    onValueChange = { viewModel.setFieldValue("full_name", it) },
                    required = fieldMeta["full_name"]?.required ?: true,
                )
                LabeledTextField(
                    label = fieldMeta["phone"]?.label ?: "Contact number",
                    value = uiState.fieldValues["phone"] ?: "",
                    onValueChange = { viewModel.setFieldValue("phone", it) },
                    required = fieldMeta["phone"]?.required ?: true,
                )
                LabeledTextField(
                    label = fieldMeta["email"]?.label ?: "Email",
                    value = uiState.fieldValues["email"] ?: "",
                    onValueChange = { viewModel.setFieldValue("email", it) },
                    required = fieldMeta["email"]?.required ?: true,
                )
                LabeledTextField(
                    label = fieldMeta["registration_no"]?.label ?: "Registration number",
                    value = uiState.fieldValues["registration_no"] ?: "",
                    onValueChange = { viewModel.setFieldValue("registration_no", it) },
                    required = fieldMeta["registration_no"]?.required ?: false,
                )
                LabeledTextField(
                    label = fieldMeta["cnic"]?.label ?: "CNIC",
                    value = uiState.fieldValues["cnic"] ?: "",
                    onValueChange = { viewModel.setFieldValue("cnic", it) },
                    required = fieldMeta["cnic"]?.required ?: false,
                )
                if (uiState.saveError != null) {
                    InlineErrorBanner(message = uiState.saveError!!)
                }
            }
        }
    }
}
