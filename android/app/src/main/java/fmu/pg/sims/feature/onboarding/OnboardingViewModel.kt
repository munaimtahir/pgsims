package fmu.pg.sims.feature.onboarding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.model.IdentityOptionsResponse
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.OnboardingStateResponse
import fmu.pg.sims.core.model.ResidentDocumentDto
import fmu.pg.sims.core.model.ResidentDocumentRequirementDto
import fmu.pg.sims.core.model.SupervisorOption
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.supervision.SupervisionRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.io.File

data class OnboardingUiState(
    val loading: Boolean = true,
    val loadError: String? = null,
    val state: OnboardingStateResponse? = null,
    val identityOptions: IdentityOptionsResponse? = null,
    val fieldValues: Map<String, String> = emptyMap(),
    val saving: Boolean = false,
    val saveError: String? = null,
    val submitting: Boolean = false,
    val submitError: String? = null,
    val requirements: List<ResidentDocumentRequirementDto> = emptyList(),
    val documents: List<ResidentDocumentDto> = emptyList(),
    val documentBusyIds: Set<Int> = emptySet(),
    val documentActionError: String? = null,
    val allSupervisors: List<SupervisorOption> = emptyList(),
    val supervisorSearchLoading: Boolean = false,
    val supervisorRequestSubmitting: Boolean = false,
    val supervisorRequestError: String? = null,
    val supervisorRequestSuccess: Boolean = false,
)

class OnboardingViewModel(
    private val onboardingRepository: OnboardingRepository,
    private val supervisionRepository: SupervisionRepository,
    private val documentsRepository: DocumentsRepository,
    private val authRepository: AuthRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(OnboardingUiState())
    val uiState: StateFlow<OnboardingUiState> = _uiState.asStateFlow()

    fun load() {
        viewModelScope.launch {
            _uiState.update { it.copy(loading = true, loadError = null) }

            val stateResult = onboardingRepository.getState()
            val optionsResult = onboardingRepository.getIdentityOptions()
            val requirementsResult = documentsRepository.getRequirements()
            val documentsResult = documentsRepository.getDocuments()

            val state = (stateResult as? NetworkResult.Success)?.data
            if (state == null) {
                val message = (stateResult as? NetworkResult.Error)?.message ?: "Could not load onboarding status."
                _uiState.update { it.copy(loading = false, loadError = message) }
                return@launch
            }

            _uiState.update {
                it.copy(
                    loading = false,
                    loadError = null,
                    state = state,
                    fieldValues = fieldValuesFrom(state),
                    identityOptions = (optionsResult as? NetworkResult.Success)?.data,
                    requirements = (requirementsResult as? NetworkResult.Success)?.data ?: emptyList(),
                    documents = (documentsResult as? NetworkResult.Success)?.data ?: emptyList(),
                )
            }
        }
    }

    private fun fieldValuesFrom(state: OnboardingStateResponse): Map<String, String> =
        state.sections.flatMap { it.fields }.associate { it.field to (it.value ?: "") }

    fun setFieldValue(field: String, value: String) {
        _uiState.update { it.copy(fieldValues = it.fieldValues + (field to value)) }
    }

    /** Persists every field in [fields] (present in the local draft buffer) in one call. */
    fun saveFields(fields: List<String>, onDone: (Boolean) -> Unit = {}) {
        val current = _uiState.value
        val payload = fields.associateWith { current.fieldValues[it] ?: "" }
        _uiState.update { it.copy(saving = true, saveError = null) }
        viewModelScope.launch {
            when (val result = onboardingRepository.saveFields(payload)) {
                is NetworkResult.Success -> {
                    _uiState.update {
                        it.copy(saving = false, state = result.data, fieldValues = fieldValuesFrom(result.data))
                    }
                    onDone(true)
                }
                is NetworkResult.Error -> {
                    _uiState.update { it.copy(saving = false, saveError = result.message) }
                    onDone(false)
                }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun submit() {
        _uiState.update { it.copy(submitting = true, submitError = null) }
        viewModelScope.launch {
            when (val result = onboardingRepository.submit()) {
                is NetworkResult.Success -> {
                    _uiState.update { it.copy(submitting = false, state = result.data) }
                    authRepository.fetchCurrentUser()
                }
                is NetworkResult.Error -> _uiState.update { it.copy(submitting = false, submitError = result.message) }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun loadSupervisorOptions() {
        _uiState.update { it.copy(supervisorSearchLoading = true) }
        viewModelScope.launch {
            when (val result = supervisionRepository.searchSupervisors()) {
                is NetworkResult.Success -> _uiState.update {
                    it.copy(supervisorSearchLoading = false, allSupervisors = result.data.supervisors)
                }
                is NetworkResult.Error -> _uiState.update {
                    it.copy(supervisorSearchLoading = false, supervisorRequestError = result.message)
                }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun requestSupervisor(residentProfileId: Int, option: SupervisorOption) {
        submitSupervisorRequest(
            residentProfileId = residentProfileId,
            name = option.name,
            department = option.department,
            institution = option.trainingSite,
        )
    }

    fun requestSupervisorNotListed(
        residentProfileId: Int,
        name: String,
        department: String,
        institution: String,
        pmdcNumber: String,
        email: String,
        phone: String,
    ) {
        submitSupervisorRequest(residentProfileId, name, department, institution, pmdcNumber, email, phone)
    }

    private fun submitSupervisorRequest(
        residentProfileId: Int,
        name: String,
        department: String = "",
        institution: String = "",
        pmdcNumber: String = "",
        email: String = "",
        phone: String = "",
    ) {
        if (name.isBlank()) {
            _uiState.update { it.copy(supervisorRequestError = "Supervisor name is required.") }
            return
        }
        _uiState.update { it.copy(supervisorRequestSubmitting = true, supervisorRequestError = null) }
        viewModelScope.launch {
            when (
                val result = supervisionRepository.requestSupervisorLink(
                    residentProfileId = residentProfileId,
                    supervisorName = name,
                    department = department,
                    institution = institution,
                    pmdcNumber = pmdcNumber,
                    email = email,
                    phone = phone,
                )
            ) {
                is NetworkResult.Success -> {
                    _uiState.update { it.copy(supervisorRequestSubmitting = false, supervisorRequestSuccess = true) }
                    refreshStateOnly()
                }
                is NetworkResult.Error -> _uiState.update {
                    it.copy(supervisorRequestSubmitting = false, supervisorRequestError = result.message)
                }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun deferDocument(documentId: Int) {
        withDocumentBusy(documentId) { documentsRepository.defer(documentId) }
    }

    fun uploadDocument(documentId: Int, file: File, mimeType: String) {
        withDocumentBusy(documentId) { documentsRepository.upload(documentId, file, mimeType) }
    }

    private fun withDocumentBusy(documentId: Int, action: suspend () -> NetworkResult<ResidentDocumentDto>) {
        _uiState.update { it.copy(documentBusyIds = it.documentBusyIds + documentId, documentActionError = null) }
        viewModelScope.launch {
            when (val result = action()) {
                is NetworkResult.Success -> {
                    _uiState.update { current ->
                        current.copy(
                            documentBusyIds = current.documentBusyIds - documentId,
                            documents = current.documents.map { if (it.id == documentId) result.data else it },
                        )
                    }
                    refreshStateOnly()
                }
                is NetworkResult.Error -> _uiState.update {
                    it.copy(documentBusyIds = it.documentBusyIds - documentId, documentActionError = result.message)
                }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    private suspend fun refreshStateOnly() {
        when (val result = onboardingRepository.getState()) {
            is NetworkResult.Success -> _uiState.update { it.copy(state = result.data) }
            else -> Unit
        }
    }
}
