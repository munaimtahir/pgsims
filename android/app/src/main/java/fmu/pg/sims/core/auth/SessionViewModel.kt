package fmu.pg.sims.core.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.ReviewStatus
import fmu.pg.sims.core.model.Role
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/** Where the app should route to, entirely derived from backend-declared state. */
sealed class SessionDestination {
    data object Loading : SessionDestination()
    data object LoggedOut : SessionDestination()
    data object ChangePassword : SessionDestination()
    data object Onboarding : SessionDestination()
    data object PendingReview : SessionDestination()
    data object CorrectionRequired : SessionDestination()
    data object Home : SessionDestination()
}

class SessionViewModel(private val authRepository: AuthRepository) : ViewModel() {

    private val _me = MutableStateFlow<AuthMeResponse?>(null)
    val me: StateFlow<AuthMeResponse?> = _me.asStateFlow()

    private val _destination = MutableStateFlow<SessionDestination>(SessionDestination.Loading)
    val destination: StateFlow<SessionDestination> = _destination.asStateFlow()

    private val _lastError = MutableStateFlow<String?>(null)
    val lastError: StateFlow<String?> = _lastError.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _destination.value = SessionDestination.Loading
            when (val result = authRepository.fetchCurrentUser()) {
                is NetworkResult.Success -> applyUser(result.data)
                is NetworkResult.Error -> {
                    _me.value = null
                    _lastError.value = result.message
                    _destination.value = SessionDestination.LoggedOut
                }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun onLoginSuccess(user: AuthMeResponse) {
        applyUser(user)
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
            _me.value = null
            _destination.value = SessionDestination.LoggedOut
        }
    }

    private fun applyUser(user: AuthMeResponse) {
        _me.value = user
        _destination.value = routeFor(user)
    }

    private fun routeFor(user: AuthMeResponse): SessionDestination {
        if (user.mustChangePassword) return SessionDestination.ChangePassword
        if (user.role != Role.RESIDENT) return SessionDestination.Home
        return when (user.effectiveReviewStatus) {
            ReviewStatus.APPROVED -> SessionDestination.Home
            ReviewStatus.PENDING_REVIEW -> SessionDestination.PendingReview
            ReviewStatus.CORRECTION_REQUIRED -> SessionDestination.CorrectionRequired
            else -> SessionDestination.Onboarding
        }
    }
}
