package fmu.pg.sims.testutil

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
import fmu.pg.sims.core.model.Role
import fmu.pg.sims.core.model.SimpleMessageResponse
import fmu.pg.sims.core.model.SubmitOnboardingRequest
import fmu.pg.sims.core.model.SupervisionOptionsResponse
import fmu.pg.sims.core.model.User
import fmu.pg.sims.core.network.ApiService
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import okhttp3.ResponseBody.Companion.toResponseBody
import retrofit2.Response

/**
 * In-memory [ApiService] test double. Every endpoint has a deterministic default response
 * (matching real payload shapes captured from the live backend, see
 * SerializationContractTest and docs/implementation/20260903_resident_onboarding_android_mvp)
 * and can be overridden per-test via the mutable fields/lambdas below — no real network, no
 * flaky timing.
 */
class FakeApiService(
    var loginResult: (LoginRequest) -> Response<LoginResponse> = { req ->
        if (req.username == TestFixtures.VALID_USERNAME && req.password == TestFixtures.VALID_PASSWORD) {
            Response.success(TestFixtures.loginResponse())
        } else {
            Response.error(401, errorBody("""{"detail":"Incorrect username or password."}"""))
        }
    },
    var authMeResult: () -> Response<AuthMeResponse> = { Response.success(TestFixtures.authMe()) },
    var changePasswordResult: (ChangePasswordRequest) -> Response<SimpleMessageResponse> = {
        Response.success(SimpleMessageResponse(message = "Password changed."))
    },
    var onboardingStateResult: () -> Response<OnboardingStateResponse> = { Response.success(TestFixtures.onboardingState()) },
    var updateOnboardingFieldsResult: (OnboardingFieldUpdateRequest) -> Response<OnboardingStateResponse> = { req ->
        val updates = req.fields ?: req.field?.let { mapOf(it to req.value) } ?: emptyMap()
        Response.success(TestFixtures.onboardingState(fieldOverrides = updates))
    },
    var submitOnboardingResult: (SubmitOnboardingRequest) -> Response<OnboardingStateResponse> = {
        Response.success(TestFixtures.onboardingState(reviewStatus = "PENDING_REVIEW"))
    },
    var documentRequirementsResult: () -> Response<PaginatedResponse<ResidentDocumentRequirementDto>> = {
        Response.success(PaginatedResponse(count = 0, results = emptyList()))
    },
    var residentDocumentsResult: () -> Response<List<ResidentDocumentDto>> = { Response.success(TestFixtures.documents()) },
    var deferDocumentResult: (Int) -> Response<ResidentDocumentDto> = { id ->
        Response.success(TestFixtures.documents().first { it.id == id }.copy(status = "DEFERRED"))
    },
    var uploadDocumentResult: (Int) -> Response<ResidentDocumentDto> = { id ->
        Response.success(TestFixtures.documents().first { it.id == id }.copy(status = "PENDING_REVIEW"))
    },
    var supervisionOptionsResult: () -> Response<SupervisionOptionsResponse> = { Response.success(TestFixtures.supervisionOptions()) },
    var createPendingSupervisorLinkResult: (CreatePendingSupervisorLinkRequest) -> Response<PendingSupervisorLinkDto> = { req ->
        Response.success(PendingSupervisorLinkDto(id = 501, resident = req.resident, supervisorNameText = req.supervisorNameText, status = "PENDING"))
    },
    var trainingRecordsResult: () -> Response<PaginatedResponse<ResidentTrainingRecordDto>> = {
        Response.success(PaginatedResponse(count = 1, results = listOf(TestFixtures.trainingRecord())))
    },
    var identityOptionsResult: () -> Response<IdentityOptionsResponse> = { Response.success(IdentityOptionsResponse()) },
) : ApiService {

    override suspend fun getHealthStatus(): Response<HealthStatus> = Response.success(HealthStatus(status = "ok"))

    override suspend fun login(request: LoginRequest): Response<LoginResponse> = loginResult(request)

    override suspend fun refreshToken(request: RefreshTokenRequest): Response<RefreshTokenResponse> =
        Response.success(RefreshTokenResponse(access = "fake-access-refreshed", refresh = request.refresh))

    override suspend fun logout(request: LogoutRequest): Response<SimpleMessageResponse> =
        Response.success(SimpleMessageResponse(message = "Logged out."))

    override suspend fun getAuthMe(): Response<AuthMeResponse> = authMeResult()

    override suspend fun getUserProfile(): Response<User> = Response.success(TestFixtures.user())

    override suspend fun changePassword(request: ChangePasswordRequest): Response<SimpleMessageResponse> =
        changePasswordResult(request)

    override suspend fun getIdentityOptions(): Response<IdentityOptionsResponse> = identityOptionsResult()

    override suspend fun getOnboardingState(): Response<OnboardingStateResponse> = onboardingStateResult()

    override suspend fun updateOnboardingFields(request: OnboardingFieldUpdateRequest): Response<OnboardingStateResponse> =
        updateOnboardingFieldsResult(request)

    override suspend fun getOnboardingReviewState(): Response<OnboardingStateResponse> = onboardingStateResult()

    override suspend fun submitOnboarding(request: SubmitOnboardingRequest): Response<OnboardingStateResponse> =
        submitOnboardingResult(request)

    override suspend fun getDocumentRequirements(): Response<PaginatedResponse<ResidentDocumentRequirementDto>> =
        documentRequirementsResult()

    override suspend fun getResidentDocuments(): Response<List<ResidentDocumentDto>> = residentDocumentsResult()

    override suspend fun deferDocument(id: Int): Response<ResidentDocumentDto> = deferDocumentResult(id)

    override suspend fun uploadDocument(id: Int, file: MultipartBody.Part): Response<ResidentDocumentDto> =
        uploadDocumentResult(id)

    override suspend fun getDocumentFile(id: Int): Response<ResponseBody> =
        Response.success("fake-file-bytes".toResponseBody())

    override suspend fun getSupervisionOptions(trainingSiteId: Int?, departmentId: Int?): Response<SupervisionOptionsResponse> =
        supervisionOptionsResult()

    override suspend fun getSupervisorAssignments(residentId: Int?): Response<PaginatedResponse<ResidentSupervisorAssignmentDto>> =
        Response.success(PaginatedResponse(count = 0, results = emptyList()))

    override suspend fun createPendingSupervisorLink(request: CreatePendingSupervisorLinkRequest): Response<PendingSupervisorLinkDto> =
        createPendingSupervisorLinkResult(request)

    override suspend fun getResidentTrainingRecords(): Response<PaginatedResponse<ResidentTrainingRecordDto>> =
        trainingRecordsResult()
}

private fun errorBody(json: String): ResponseBody =
    json.toResponseBody("application/json".toMediaTypeOrNull())
