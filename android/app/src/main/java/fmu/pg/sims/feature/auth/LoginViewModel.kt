package fmu.pg.sims.feature.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.NetworkResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class LoginUiState {
    data object Idle : LoginUiState()
    data object Loading : LoginUiState()
    data class Error(val message: String) : LoginUiState()
}

class LoginViewModel(private val authRepository: AuthRepository) : ViewModel() {
    private val _uiState = MutableStateFlow<LoginUiState>(LoginUiState.Idle)
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    fun login(username: String, password: String, onSuccess: (AuthMeResponse) -> Unit) {
        if (username.isBlank() || password.isBlank()) {
            _uiState.value = LoginUiState.Error("Enter your username and password.")
            return
        }
        _uiState.value = LoginUiState.Loading
        viewModelScope.launch {
            when (val result = authRepository.login(username.trim(), password)) {
                is NetworkResult.Success -> {
                    _uiState.value = LoginUiState.Idle
                    onSuccess(result.data)
                }
                is NetworkResult.Error -> _uiState.value = LoginUiState.Error(result.message)
                is NetworkResult.Loading -> Unit
            }
        }
    }
}
