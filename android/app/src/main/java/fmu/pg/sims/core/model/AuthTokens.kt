package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class AuthTokens(
    @SerialName("access") val access: String,
    @SerialName("refresh") val refresh: String,
)

@Serializable
data class LoginRequest(
    @SerialName("username") val username: String,
    @SerialName("password") val password: String,
)

@Serializable
data class LoginResponse(
    @SerialName("access") val access: String,
    @SerialName("refresh") val refresh: String,
    @SerialName("user") val user: User? = null,
    @SerialName("role") val role: Role? = null,
    @SerialName("must_change_password") val mustChangePassword: Boolean = false,
    @SerialName("is_profile_complete") val isProfileComplete: Boolean = false,
)

@Serializable
data class RefreshTokenRequest(
    @SerialName("refresh") val refresh: String,
)

@Serializable
data class RefreshTokenResponse(
    @SerialName("access") val access: String,
    @SerialName("refresh") val refresh: String? = null,
)

@Serializable
data class LogoutRequest(
    @SerialName("refresh") val refresh: String,
)

@Serializable
data class SimpleMessageResponse(
    @SerialName("message") val message: String = "",
    @SerialName("allowed_next_route") val allowedNextRoute: String? = null,
    @SerialName("error") val error: String? = null,
)
