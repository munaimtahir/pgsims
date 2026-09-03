package fmu.pg.sims.feature.onboarding

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import fmu.pg.sims.core.model.IdentityOptionsResponse
import fmu.pg.sims.ui.components.DateField
import fmu.pg.sims.ui.components.DropdownField
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading
import fmu.pg.sims.ui.components.InlineErrorBanner
import fmu.pg.sims.ui.components.LabeledTextField
import fmu.pg.sims.ui.components.OnboardingStepScaffold

private val TRAINING_FIELDS = listOf(
    "hospital", "department_ref", "program_ref", "academic_session_ref", "specialty_ref",
    "training_start_date", "expected_end_date", "current_level", "notes",
)

@Composable
fun OnboardingTrainingScreen(
    viewModel: OnboardingViewModel,
    onBack: () -> Unit,
    onNext: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.loadError != null -> ErrorRetryView(message = uiState.loadError!!, onRetry = viewModel::load)
        else -> {
            val section = uiState.state?.sections?.firstOrNull { it.key == "enrollment" }
            val fieldMeta = section?.fields.orEmpty().associateBy { it.field }
            val options: IdentityOptionsResponse = uiState.identityOptions ?: IdentityOptionsResponse()

            OnboardingStepScaffold(
                title = "Training & Enrollment",
                stepIndex = 2,
                stepCount = 6,
                onBack = onBack,
                primaryLabel = "Save & Continue",
                primaryEnabled = true,
                primaryLoading = uiState.saving,
                onPrimaryClick = { viewModel.saveFields(TRAINING_FIELDS) { success -> if (success) onNext() } },
            ) {
                DropdownField(
                    label = fieldMeta["hospital"]?.label ?: "Hospital / training site",
                    options = options.hospitals,
                    selectedId = uiState.fieldValues["hospital"] ?: "",
                    onSelect = { viewModel.setFieldValue("hospital", it.id) },
                    required = fieldMeta["hospital"]?.required ?: true,
                )
                DropdownField(
                    label = fieldMeta["department_ref"]?.label ?: "Department",
                    options = options.departments,
                    selectedId = uiState.fieldValues["department_ref"] ?: "",
                    onSelect = { viewModel.setFieldValue("department_ref", it.id) },
                    required = fieldMeta["department_ref"]?.required ?: true,
                )
                DropdownField(
                    label = fieldMeta["program_ref"]?.label ?: "Training program",
                    options = options.programs,
                    selectedId = uiState.fieldValues["program_ref"] ?: "",
                    onSelect = { viewModel.setFieldValue("program_ref", it.id) },
                    required = fieldMeta["program_ref"]?.required ?: true,
                )
                DropdownField(
                    label = fieldMeta["academic_session_ref"]?.label ?: "Academic session",
                    options = options.academicSessions,
                    selectedId = uiState.fieldValues["academic_session_ref"] ?: "",
                    onSelect = { viewModel.setFieldValue("academic_session_ref", it.id) },
                    required = fieldMeta["academic_session_ref"]?.required ?: true,
                )
                DropdownField(
                    label = fieldMeta["specialty_ref"]?.label ?: "Specialty",
                    options = options.specialties,
                    selectedId = uiState.fieldValues["specialty_ref"] ?: "",
                    onSelect = { viewModel.setFieldValue("specialty_ref", it.id) },
                    required = fieldMeta["specialty_ref"]?.required ?: true,
                )
                DateField(
                    label = fieldMeta["training_start_date"]?.label ?: "Training start date",
                    value = uiState.fieldValues["training_start_date"] ?: "",
                    onValueChange = { viewModel.setFieldValue("training_start_date", it) },
                    required = fieldMeta["training_start_date"]?.required ?: true,
                )
                DateField(
                    label = fieldMeta["expected_end_date"]?.label ?: "Expected end date",
                    value = uiState.fieldValues["expected_end_date"] ?: "",
                    onValueChange = { viewModel.setFieldValue("expected_end_date", it) },
                    required = fieldMeta["expected_end_date"]?.required ?: false,
                )
                LabeledTextField(
                    label = fieldMeta["current_level"]?.label ?: "Current year / level",
                    value = uiState.fieldValues["current_level"] ?: "",
                    onValueChange = { viewModel.setFieldValue("current_level", it) },
                    required = fieldMeta["current_level"]?.required ?: true,
                )
                LabeledTextField(
                    label = fieldMeta["notes"]?.label ?: "Training notes",
                    value = uiState.fieldValues["notes"] ?: "",
                    onValueChange = { viewModel.setFieldValue("notes", it) },
                    required = false,
                )
                if (uiState.saveError != null) {
                    InlineErrorBanner(message = uiState.saveError!!)
                }
            }
        }
    }
}
