package fmu.pg.sims.feature.training

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.ResidentTrainingRecordDto
import fmu.pg.sims.core.training.TrainingRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class TrainingUiState(
    val loading: Boolean = true,
    val error: String? = null,
    val records: List<ResidentTrainingRecordDto> = emptyList(),
)

class TrainingViewModel(private val trainingRepository: TrainingRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(TrainingUiState())
    val uiState: StateFlow<TrainingUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(loading = true, error = null) }
            when (val result = trainingRepository.getMyTrainingRecords()) {
                is NetworkResult.Success -> _uiState.update { it.copy(loading = false, records = result.data) }
                is NetworkResult.Error -> _uiState.update { it.copy(loading = false, error = result.message) }
                is NetworkResult.Loading -> Unit
            }
        }
    }
}
