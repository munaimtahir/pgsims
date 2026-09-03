package fmu.pg.sims.core.network

import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.ChangePasswordRequest
import fmu.pg.sims.core.model.CreatePendingSupervisorLinkRequest
import fmu.pg.sims.core.model.HealthStatus
import fmu.pg.sims.core.model.IdentityOptionsResponse
import fmu.pg.sims.core.model.LoginRequest
import fmu.pg.sims.core.model.LoginResponse
import fmu.pg.sims.core.model.LogoutRequest
import fmu.pg.sims.core.model.OnboardingFieldUpdateRequest
import fmu.pg.sims.core.model.OnboardingStateResponse
import fmu.pg.sims.core.model.PaginatedResponse
import fmu.pg.sims.core.model.PendingSupervisorLinkDto
import fmu.pg.sims.core.model.RefreshTokenRequest
import fmu.pg.sims.core.model.RefreshTokenResponse
import fmu.pg.sims.core.model.ResidentDocumentDto
import fmu.pg.sims.core.model.ResidentDocumentRequirementDto
import fmu.pg.sims.core.model.ResidentSupervisorAssignmentDto
import fmu.pg.sims.core.model.ResidentTrainingRecordDto
import fmu.pg.sims.core.model.SimpleMessageResponse
import fmu.pg.sims.core.model.SubmitOnboardingRequest
import fmu.pg.sims.core.model.SupervisionOptionsResponse
import fmu.pg.sims.core.model.User
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Part
import retrofit2.http.Path
import retrofit2.http.Query
import retrofit2.http.Streaming

interface ApiService {

    // ---- Auth / bootstrap ----

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

    @POST("api/auth/change-password/")
    suspend fun changePassword(@Body request: ChangePasswordRequest): Response<SimpleMessageResponse>

    @GET("api/identity/options/")
    suspend fun getIdentityOptions(): Response<IdentityOptionsResponse>

    // ---- Onboarding ----

    @GET("api/auth/onboarding/")
    suspend fun getOnboardingState(): Response<OnboardingStateResponse>

    @PATCH("api/auth/onboarding/")
    suspend fun updateOnboardingFields(@Body request: OnboardingFieldUpdateRequest): Response<OnboardingStateResponse>

    @GET("api/resident-onboarding/state/")
    suspend fun getOnboardingReviewState(): Response<OnboardingStateResponse>

    @POST("api/resident-onboarding/state/")
    suspend fun submitOnboarding(@Body request: SubmitOnboardingRequest): Response<OnboardingStateResponse>

    // ---- Documents ----

    // Paginated (DRF default PageNumberPagination) — unlike /resident-documents/ below.
    @GET("api/resident-document-requirements/")
    suspend fun getDocumentRequirements(): Response<PaginatedResponse<ResidentDocumentRequirementDto>>

    @GET("api/resident-documents/")
    suspend fun getResidentDocuments(): Response<List<ResidentDocumentDto>>

    @POST("api/resident-documents/{id}/defer/")
    suspend fun deferDocument(@Path("id") id: Int): Response<ResidentDocumentDto>

    @Multipart
    @POST("api/resident-documents/{id}/upload/")
    suspend fun uploadDocument(
        @Path("id") id: Int,
        @Part file: MultipartBody.Part,
    ): Response<ResidentDocumentDto>

    @Streaming
    @GET("api/resident-documents/{id}/file/")
    suspend fun getDocumentFile(@Path("id") id: Int): Response<ResponseBody>

    // ---- Supervision ----

    @GET("api/supervision/options/")
    suspend fun getSupervisionOptions(
        @Query("training_site_id") trainingSiteId: Int? = null,
        @Query("department_id") departmentId: Int? = null,
    ): Response<SupervisionOptionsResponse>

    // Paginated (DRF default PageNumberPagination).
    @GET("api/supervision/assignments/")
    suspend fun getSupervisorAssignments(
        @Query("resident_id") residentId: Int? = null,
    ): Response<PaginatedResponse<ResidentSupervisorAssignmentDto>>

    @POST("api/pending-supervisor-links/")
    suspend fun createPendingSupervisorLink(
        @Body request: CreatePendingSupervisorLinkRequest,
    ): Response<PendingSupervisorLinkDto>

    // ---- Training ----

    // Paginated (DRF default PageNumberPagination).
    @GET("api/resident-training/")
    suspend fun getResidentTrainingRecords(): Response<PaginatedResponse<ResidentTrainingRecordDto>>
}
