package fmu.pg.sims.core.network

import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.HealthStatus
import fmu.pg.sims.core.model.LoginRequest
import fmu.pg.sims.core.model.LoginResponse
import fmu.pg.sims.core.model.LogoutRequest
import fmu.pg.sims.core.model.RefreshTokenRequest
import fmu.pg.sims.core.model.RefreshTokenResponse
import fmu.pg.sims.core.model.SimpleMessageResponse
import fmu.pg.sims.core.model.User
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
