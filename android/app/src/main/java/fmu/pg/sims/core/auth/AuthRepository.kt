package fmu.pg.sims.core.auth

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.HealthStatus
import fmu.pg.sims.core.model.LoginRequest
import fmu.pg.sims.core.model.LogoutRequest
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.RefreshTokenRequest
import fmu.pg.sims.core.network.ApiService

sealed class AuthState {
    data object Initial : AuthState()
    data object Loading : AuthState()
    data class Authenticated(val user: AuthMeResponse) : AuthState()
    data object Unauthenticated : AuthState()
    data class Error(val message: String) : AuthState()
}

class AuthRepository(
    private val apiService: ApiService,
    private val tokenStorage: TokenStorage
) {
    private val _authState = MutableStateFlow<AuthState>(AuthState.Initial)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()

    suspend fun checkHealth(): NetworkResult<HealthStatus> {
        return try {
            val response = apiService.getHealthStatus()
            if (response.isSuccessful && response.body() != null) {
                NetworkResult.Success(response.body()!!)
            } else {
                NetworkResult.Error(response.code(), response.message())
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.localizedMessage ?: "Health check connection failed", cause = e)
        }
    }

    suspend fun login(username: String, password: String): NetworkResult<AuthMeResponse> {
        _authState.value = AuthState.Loading
        return try {
            val loginResp = apiService.login(LoginRequest(username = username, password = password))
            if (loginResp.isSuccessful && loginResp.body() != null) {
                val tokens = loginResp.body()!!
                tokenStorage.saveTokens(tokens.access, tokens.refresh)
                if (tokens.role != null) {
                    tokenStorage.saveUserRole(tokens.role)
                }

                // Fetch current user onboarding / profile state
                val meResp = apiService.getAuthMe()
                if (meResp.isSuccessful && meResp.body() != null) {
                    val me = meResp.body()!!
                    _authState.value = AuthState.Authenticated(me)
                    NetworkResult.Success(me)
                } else {
                    _authState.value = AuthState.Unauthenticated
                    NetworkResult.Error(meResp.code(), "Failed to fetch identity profile")
                }
            } else {
                val errorMsg = loginResp.errorBody()?.string() ?: "Invalid credentials"
                _authState.value = AuthState.Error(errorMsg)
                NetworkResult.Error(loginResp.code(), errorMsg)
            }
        } catch (e: Exception) {
            val msg = e.localizedMessage ?: "Login failed"
            _authState.value = AuthState.Error(msg)
            NetworkResult.Error(message = msg, cause = e)
        }
    }

    suspend fun logout(): NetworkResult<Unit> {
        val refreshToken = tokenStorage.getRefreshToken()
        if (!refreshToken.isNullOrBlank()) {
            try {
                apiService.logout(LogoutRequest(refresh = refreshToken))
            } catch (_: Exception) {
                // Ignore network errors on logout
            }
        }
        tokenStorage.clear()
        _authState.value = AuthState.Unauthenticated
        return NetworkResult.Success(Unit)
    }

    suspend fun refreshSession(): Boolean {
        val refreshToken = tokenStorage.getRefreshToken() ?: return false
        return try {
            val resp = apiService.refreshToken(RefreshTokenRequest(refresh = refreshToken))
            if (resp.isSuccessful && resp.body() != null) {
                val body = resp.body()!!
                tokenStorage.saveTokens(body.access, body.refresh ?: refreshToken)
                true
            } else {
                tokenStorage.clear()
                _authState.value = AuthState.Unauthenticated
                false
            }
        } catch (e: Exception) {
            false
        }
    }
}
