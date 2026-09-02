package pk.edu.fmu.pgsims.core.network

import pk.edu.fmu.pgsims.core.model.AuthMeResponse
import pk.edu.fmu.pgsims.core.model.HealthStatus
import pk.edu.fmu.pgsims.core.model.LoginRequest
import pk.edu.fmu.pgsims.core.model.LoginResponse
import pk.edu.fmu.pgsims.core.model.LogoutRequest
import pk.edu.fmu.pgsims.core.model.RefreshTokenRequest
import pk.edu.fmu.pgsims.core.model.RefreshTokenResponse
import pk.edu.fmu.pgsims.core.model.SimpleMessageResponse
import pk.edu.fmu.pgsims.core.model.User
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {

    @GET("api/health/")
    suspend fun getHealthStatus(): Response<HealthStatus>

    @POST("api/auth/login/")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @POST("api/auth/refresh/")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<RefreshTokenResponse>

    @POST("api/auth/logout/")
    suspend fun logout(@Body request: LogoutRequest): Response<SimpleMessageResponse>

    @GET("api/auth/me/")
    suspend fun getAuthMe(): Response<AuthMeResponse>

    @GET("api/auth/profile/")
    suspend fun getUserProfile(): Response<User>
}
