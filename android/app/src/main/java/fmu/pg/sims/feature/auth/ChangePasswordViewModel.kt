package fmu.pg.sims.feature.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.model.NetworkResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class ChangePasswordUiState {
    data object Idle : ChangePasswordUiState()
    data object Loading : ChangePasswordUiState()
    data object Success : ChangePasswordUiState()
    data class Error(val message: String) : ChangePasswordUiState()
}

class ChangePasswordViewModel(private val authRepository: AuthRepository) : ViewModel() {
    private val _uiState = MutableStateFlow<ChangePasswordUiState>(ChangePasswordUiState.Idle)
    val uiState: StateFlow<ChangePasswordUiState> = _uiState.asStateFlow()

    fun submit(oldPassword: String, newPassword: String, confirmPassword: String) {
        if (oldPassword.isBlank() || newPassword.isBlank() || confirmPassword.isBlank()) {
            _uiState.value = ChangePasswordUiState.Error("All fields are required.")
            return
        }
        if (newPassword != confirmPassword) {
            _uiState.value = ChangePasswordUiState.Error("New passwords do not match.")
            return
        }
        _uiState.value = ChangePasswordUiState.Loading
        viewModelScope.launch {
            when (val result = authRepository.changePassword(oldPassword, newPassword)) {
                is NetworkResult.Success -> _uiState.value = ChangePasswordUiState.Success
                is NetworkResult.Error -> _uiState.value = ChangePasswordUiState.Error(result.message)
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun resetError() {
        if (_uiState.value is ChangePasswordUiState.Error) {
            _uiState.value = ChangePasswordUiState.Idle
        }
    }
}
