package fmu.pg.sims.feature.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.OnboardingStateResponse
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.training.TrainingRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class HomeUiState(
    val loading: Boolean = true,
    val error: String? = null,
    val me: AuthMeResponse? = null,
    val onboarding: OnboardingStateResponse? = null,
    val trainingLevel: String = "",
    val trainingProgram: String = "",
)

class HomeViewModel(
    private val authRepository: AuthRepository,
    private val onboardingRepository: OnboardingRepository,
    private val trainingRepository: TrainingRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(loading = true, error = null) }
            val meResult = authRepository.fetchCurrentUser()
            val onboardingResult = onboardingRepository.getState()
            val trainingResult = trainingRepository.getMyTrainingRecords()

            val me = (meResult as? NetworkResult.Success)?.data
            if (me == null) {
                _uiState.update {
                    it.copy(loading = false, error = (meResult as? NetworkResult.Error)?.message ?: "Could not load your dashboard.")
                }
                return@launch
            }
            val activeRecord = (trainingResult as? NetworkResult.Success)?.data?.firstOrNull { it.active }

            _uiState.update {
                it.copy(
                    loading = false,
                    error = null,
                    me = me,
                    onboarding = (onboardingResult as? NetworkResult.Success)?.data,
                    trainingLevel = activeRecord?.currentLevel ?: "",
                    trainingProgram = activeRecord?.programName ?: "",
                )
            }
        }
    }
}
