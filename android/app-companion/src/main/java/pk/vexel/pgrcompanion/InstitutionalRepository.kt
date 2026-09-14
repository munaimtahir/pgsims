package pk.vexel.pgrcompanion

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody.Companion.asRequestBody
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Part
import retrofit2.http.Path
import retrofit2.http.Query
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit
import java.util.UUID

/**
 * PGR SIMS networking boundary.
 *
 * Everything in this file is optional to the product: the Personal Workspace (see [LocalStore])
 * renders and functions with no session, no network and no institution. Nothing here writes into
 * [LocalStore], and [LocalStore] is never read from here — the two data boundaries stay disjoint.
 *
 * Endpoints below were verified against the canonical PGR SIMS backend; see
 * PGR_SIMS_ANDROID_API_INTEGRATION.md for the verified request/response shapes.
 */

/**
 * The credential-carrying payloads redact themselves.
 *
 * A Kotlin data class generates a `toString()` that prints every property, and that generated
 * string survives into the release binary. Nothing logs these today, but one future log line,
 * exception message or crash report that stringifies one of them would put a plaintext password or
 * a live refresh token where it must never be. Redacting at the type removes the possibility rather
 * than relying on nobody ever doing it.
 */
@Serializable data class LoginPayload(val username: String, val password: String) {
    override fun toString() = "LoginPayload(username=$username, password=***)"
}

@Serializable data class RefreshPayload(val refresh: String) {
    override fun toString() = "RefreshPayload(refresh=***)"
}

@Serializable data class LogoutPayload(val refresh: String) {
    override fun toString() = "LogoutPayload(refresh=***)"
}

@Serializable data class ChangePasswordPayload(
    val old_password: String,
    val new_password: String,
    val new_password2: String,
) {
    override fun toString() = "ChangePasswordPayload(old_password=***, new_password=***, new_password2=***)"
}

@Serializable data class PasswordResetPayload(val email: String)
@Serializable data class PasswordResetConfirmPayload(
    val uid: String,
    val token: String,
    val new_password: String,
    val new_password2: String,
) {
    override fun toString() = "PasswordResetConfirmPayload(uid=***, token=***, new_password=***, new_password2=***)"
}

@Serializable data class CompleteProfilePayload(val fields: Map<String, String>)
@Serializable data class DeclarationPayload(val accepted: Boolean = true)
@Serializable data class UniversalUserPayload(
    val role: String,
    val full_name: String,
    val email: String = "",
    val phone: String = "",
    val username: String? = null,
    val password: String? = null,
    val profile: JsonObject = JsonObject(emptyMap()),
)

data class PagedJsonResponse(
    val count: Int,
    val next: String?,
    val previous: String?,
    val results: List<JsonObject>,
)

@Serializable data class FieldPatch(val fields: Map<String, String?>)
@Serializable data class NotificationPreferencesPayload(
    val email_enabled: Boolean? = null,
    val in_app_enabled: Boolean? = null,
    val push_enabled: Boolean? = null,
)
@Serializable data class NotificationIdsPayload(val notification_ids: List<Int>)
@Serializable data class DeviceRegistrationPayload(val token: String, val platform: String = "android")

/** Reject/return payload shared by leave and rotation actions. */
@Serializable data class ReasonPayload(val reason: String = "")

/** Reject/return payload for logbook actions, which use `supervisor_comments` not `reason`. */
@Serializable data class SupervisorCommentPayload(val supervisor_comments: String = "")
@Serializable data class RotationReviewPayload(val action: String, val reason: String = "")

/** Approve/return payload for research submissions. */
@Serializable data class ResearchActionPayload(val project_id: Int, val feedback: String = "")

@Serializable data class LeaveRequestPayload(
    val resident_training: Int,
    val leave_type: String,
    val start_date: String,
    val end_date: String,
    val reason: String = "",
    val client_request_id: String? = null,
)

@Serializable data class EvaluationSubmissionPayload(
    val template: Int,
    val academic_period: Int? = null,
    val supervisor: Int? = null,
    val resident_comments: String = "",
    val responses: List<JsonObject> = emptyList(),
)

@Serializable data class EvaluationReviewPayload(
    val supervisor_comments: String = "",
    val score: Double? = null,
    val max_score: Double? = null,
)

@Serializable data class ProcedureRecordPayload(
    val procedure_name: String,
    val procedure_code: String = "",
    val role_performed: String = "",
    val complexity: String = "",
    val outcome: String = "",
    val complications: String = "",
)

/** Active academics-logbook contract. The server assigns resident/training ownership. */
@Serializable data class AcademicLogbookPayload(
    val category: Int,
    val entry_date: String,
    val title: String,
    val description: String = "",
    val case_identifier: String = "",
    val patient_age: String = "",
    val patient_gender: String = "",
    val resident_reflection: String = "",
    val supervisor: Int? = null,
    val academic_period: Int? = null,
    val procedure_record: ProcedureRecordPayload? = null,
    val client_request_id: String? = null,
)

internal fun LeaveRequestPayload.withOfflineId() = if (client_request_id != null) this else copy(client_request_id = UUID.randomUUID().toString())
internal fun AcademicLogbookPayload.withOfflineId() = if (client_request_id != null) this else copy(client_request_id = UUID.randomUUID().toString())

interface InstitutionalApi {
    @POST("api/auth/login/") suspend fun login(@Body body: LoginPayload): Response<JsonObject>
    @POST("api/auth/refresh/") suspend fun refresh(@Body body: RefreshPayload): Response<JsonObject>
    @POST("api/auth/logout/") suspend fun logout(@Body body: LogoutPayload): Response<JsonObject>
    @GET("api/auth/me/") suspend fun me(): Response<JsonObject>
    @GET("api/auth/profile/") suspend fun ownProfile(): Response<JsonObject>
    @PATCH("api/auth/profile/update/") suspend fun updateOwnProfile(@Body body: Map<String, String>): Response<JsonObject>
    @POST("api/auth/change-password/") suspend fun changePassword(@Body body: ChangePasswordPayload): Response<JsonObject>
    @POST("api/auth/password-reset/") suspend fun requestPasswordReset(@Body body: PasswordResetPayload): Response<JsonObject>
    @POST("api/auth/password-reset/confirm/") suspend fun confirmPasswordReset(@Body body: PasswordResetConfirmPayload): Response<JsonObject>
    @GET("api/auth/complete-profile/") suspend fun completeProfileForm(): Response<JsonObject>
    @POST("api/auth/complete-profile/") suspend fun completeProfile(@Body body: Map<String, String>): Response<JsonObject>
    @GET("api/identity/options/") suspend fun identityOptions(): Response<JsonObject>
    @GET("api/users/") suspend fun users(
        @Query("page") page: Int,
        @Query("role") role: String? = null,
        @Query("search") search: String? = null,
        @Query("active") active: Boolean? = null,
    ): Response<JsonObject>
    @POST("api/users/") suspend fun createUser(@Body body: UniversalUserPayload): Response<JsonObject>
    @GET("api/users/{id}/") suspend fun userDetail(@Path("id") id: Int): Response<JsonObject>
    @GET("api/auth/onboarding/") suspend fun onboarding(): Response<JsonObject>
    @GET("api/notifications/") suspend fun notifications(): Response<JsonObject>
    @GET("api/notifications/unread-count/") suspend fun notificationUnreadCount(): Response<JsonObject>
    @GET("api/notifications/preferences/") suspend fun notificationPreferences(): Response<JsonObject>
    @PATCH("api/notifications/preferences/") suspend fun updateNotificationPreferences(@Body body: NotificationPreferencesPayload): Response<JsonObject>
    @POST("api/notifications/mark-read/") suspend fun markNotificationsRead(@Body body: NotificationIdsPayload): Response<JsonObject>
    @POST("api/notifications/mark-unread/") suspend fun markNotificationsUnread(@Body body: NotificationIdsPayload): Response<JsonObject>
    @POST("api/notifications/devices/") suspend fun registerDevice(@Body body: DeviceRegistrationPayload): Response<JsonObject>
    @PATCH("api/auth/onboarding/") suspend fun updateOnboarding(@Body body: FieldPatch): Response<JsonObject>
    @POST("api/resident-onboarding/state/") suspend fun acceptDeclaration(@Body body: DeclarationPayload): Response<JsonObject>
    @GET("api/resident-documents/") suspend fun documents(): Response<JsonArray>
    @GET("api/resident-training/") suspend fun training(): Response<JsonObject>
    @GET("api/supervision/assignments/") suspend fun assignments(): Response<JsonObject>
    @GET("api/my/rotations/") suspend fun rotations(): Response<JsonObject>
    @GET("api/rotations/{id}/") suspend fun rotationDetail(@Path("id") id: Int): Response<JsonObject>
    @GET("api/my/leaves/") suspend fun leaves(): Response<JsonObject>
    @POST("api/leaves/") suspend fun createLeave(@Body body: LeaveRequestPayload): Response<JsonObject>
    @PATCH("api/leaves/{id}/") suspend fun updateLeave(@Path("id") id: Int, @Body body: LeaveRequestPayload): Response<JsonObject>
    @POST("api/leaves/{id}/submit/") suspend fun submitLeave(@Path("id") id: Int): Response<JsonObject>
    @GET("api/leaves/{id}/") suspend fun leaveDetail(@Path("id") id: Int): Response<JsonObject>
    @GET("api/academics/logbook-entries/") suspend fun logbook(): Response<JsonObject>
    @GET("api/academics/logbook-categories/") suspend fun logbookCategories(): Response<JsonObject>
    @GET("api/academics/options/") suspend fun academicOptions(): Response<JsonObject>
    @POST("api/academics/logbook-entries/") suspend fun createLogbook(@Body body: AcademicLogbookPayload): Response<JsonObject>
    @PATCH("api/academics/logbook-entries/{id}/") suspend fun updateLogbook(@Path("id") id: Int, @Body body: AcademicLogbookPayload): Response<JsonObject>
    @POST("api/academics/logbook-entries/{id}/submit/") suspend fun submitLogbook(@Path("id") id: Int): Response<JsonObject>
    @POST("api/academics/logbook-entries/{id}/cancel/") suspend fun cancelLogbook(@Path("id") id: Int): Response<JsonObject>
    @GET("api/academics/logbook-entries/{id}/") suspend fun logbookDetail(@Path("id") id: Int): Response<JsonObject>
    @GET("api/academics/evaluation-submissions/") suspend fun assessments(): Response<JsonObject>
    @GET("api/academics/evaluation-templates/") suspend fun evaluationTemplates(): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/") suspend fun createEvaluation(@Body body: EvaluationSubmissionPayload): Response<JsonObject>
    @PATCH("api/academics/evaluation-submissions/{id}/") suspend fun updateEvaluation(@Path("id") id: Int, @Body body: EvaluationSubmissionPayload): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/{id}/submit/") suspend fun submitEvaluation(@Path("id") id: Int): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/{id}/cancel/") suspend fun cancelEvaluation(@Path("id") id: Int): Response<JsonObject>
    @GET("api/academics/evaluation-submissions/{id}/") suspend fun evaluationDetail(@Path("id") id: Int): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/{id}/start_review/") suspend fun startEvaluationReview(@Path("id") id: Int): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/{id}/approve/") suspend fun approveEvaluation(@Path("id") id: Int, @Body body: EvaluationReviewPayload): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/{id}/return_revision/") suspend fun returnEvaluation(@Path("id") id: Int, @Body body: SupervisorCommentPayload): Response<JsonObject>
    @POST("api/academics/evaluation-submissions/{id}/reject/") suspend fun rejectEvaluation(@Path("id") id: Int, @Body body: SupervisorCommentPayload): Response<JsonObject>
    @GET("api/my/research/") suspend fun research(): Response<JsonObject>
    @GET("api/my/workshops/") suspend fun workshops(): Response<JsonObject>
    @GET("api/residents/me/summary/") suspend fun residentSummary(): Response<JsonObject>
    @GET("api/academics/my-progress/") suspend fun academicProgress(): Response<JsonObject>
    @GET("api/academics/monitoring/my-progress/") suspend fun progressMonitoring(): Response<JsonObject>
    @POST("api/resident-documents/{id}/defer/") suspend fun deferDocument(@Path("id") id: Int): Response<JsonObject>
    @Multipart @POST("api/resident-documents/{id}/upload/")
    suspend fun upload(@Path("id") id: Int, @Part file: MultipartBody.Part): Response<JsonObject>

    // Supervisor-role reads. Same auth/session plumbing as the resident endpoints above; the
    // backend itself scopes every one of these to the caller's own assigned residents.
    @GET("api/supervisors/me/summary/") suspend fun supervisorSummary(): Response<JsonObject>
    @GET("api/academics/monitoring/supervisor-dashboard/") suspend fun supervisorDashboard(): Response<JsonObject>
    @GET("api/supervisors/residents/{residentId}/progress/")
    suspend fun supervisorResidentProgress(@Path("residentId") residentId: Int): Response<JsonObject>

    // Supervisor-role workflow queues (on-demand, fetched only when a workflow is opened).
    // Logbook has no dedicated supervisor-pending endpoint: `logbook()` below (shared with the
    // resident flow) is already scoped to the supervisor's own residents by the backend, and the
    // repository filters it to SUBMITTED. The separate `review-queue` endpoint was tried first but
    // rejected — its item `id` is a queue-row id, not the actual logbook entry id the action
    // endpoints require, and it also mixes in EVALUATION_REVIEW rows with no action support.
    @GET("api/utrmc/approvals/leaves/") suspend fun supervisorLeaveQueue(): Response<JsonObject>
    @GET("api/supervisor/rotations/pending/") suspend fun supervisorRotationQueue(): Response<JsonObject>
    @GET("api/supervisor/research-approvals/") suspend fun supervisorResearchQueue(): Response<JsonObject>

    // Supervisor-role workflow actions.
    @POST("api/academics/logbook-entries/{id}/verify/")
    suspend fun verifyLogbook(@Path("id") id: Int, @Body body: SupervisorCommentPayload): Response<JsonObject>
    @POST("api/academics/logbook-entries/{id}/return_revision/")
    suspend fun returnLogbook(@Path("id") id: Int, @Body body: SupervisorCommentPayload): Response<JsonObject>
    @POST("api/academics/logbook-entries/{id}/reject/")
    suspend fun rejectLogbook(@Path("id") id: Int, @Body body: SupervisorCommentPayload): Response<JsonObject>

    @POST("api/leaves/{id}/approve/") suspend fun approveLeave(@Path("id") id: Int): Response<JsonObject>
    @POST("api/leaves/{id}/reject/")
    suspend fun rejectLeave(@Path("id") id: Int, @Body body: ReasonPayload): Response<JsonObject>

    @POST("api/rotations/{id}/review-application/")
    suspend fun reviewRotation(@Path("id") id: Int, @Body body: RotationReviewPayload): Response<JsonObject>

    @POST("api/my/research/action/supervisor-approve/")
    suspend fun approveResearch(@Body body: ResearchActionPayload): Response<JsonObject>
    @POST("api/my/research/action/supervisor-return/")
    suspend fun returnResearch(@Body body: ResearchActionPayload): Response<JsonObject>
}

/** A message that is safe to show a trainee. Never carries a token, password or raw stack trace. */
class InstitutionalException(message: String) : Exception(message)

/** Where the institutional session lives. Deliberately separate from the personal store. */
interface TokenStore {
    val access: String?
    val refresh: String?
    val userId: Int?
    fun save(access: String, refresh: String)
    fun saveUserId(userId: Int)
    fun clear()
}

/**
 * Keystore-backed token storage. If the device keystore is unusable (a known failure mode on some
 * OEM builds and on restored backups) we fall back to memory rather than crashing: losing the
 * institutional session is recoverable, taking down the offline Personal Workspace is not.
 */
class EncryptedTokenStore private constructor(private val prefs: android.content.SharedPreferences) : TokenStore {
    override val access: String? get() = prefs.getString(KEY_ACCESS, null)
    override val refresh: String? get() = prefs.getString(KEY_REFRESH, null)
    override val userId: Int? get() = prefs.getInt(KEY_USER_ID, -1).takeIf { it >= 0 }
    override fun save(access: String, refresh: String) {
        prefs.edit().putString(KEY_ACCESS, access).putString(KEY_REFRESH, refresh).commit()
    }
    override fun saveUserId(userId: Int) { prefs.edit().putInt(KEY_USER_ID, userId).commit() }
    override fun clear() { prefs.edit().clear().commit() }

    companion object {
        private const val KEY_ACCESS = "access"
        private const val KEY_REFRESH = "refresh"
        private const val KEY_USER_ID = "user_id"
        fun create(context: Context): TokenStore = runCatching {
            val app = context.applicationContext
            val key = MasterKey.Builder(app).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
            EncryptedTokenStore(
                EncryptedSharedPreferences.create(
                    app, "institutional_session", key,
                    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
                )
            )
        }.getOrElse { InMemoryTokenStore() }
    }
}

class InMemoryTokenStore : TokenStore {
    private var accessValue: String? = null
    private var refreshValue: String? = null
    private var userIdValue: Int? = null
    override val access: String? get() = accessValue
    override val refresh: String? get() = refreshValue
    override val userId: Int? get() = userIdValue
    override fun save(access: String, refresh: String) { accessValue = access; refreshValue = refresh }
    override fun saveUserId(userId: Int) { userIdValue = userId }
    override fun clear() { accessValue = null; refreshValue = null; userIdValue = null }
}

/**
 * One institutional read. [me] is required — if identity cannot be read there is no session to
 * show. Supervisor reads are handled separately; ADMIN, SUPPORT_STAFF and unknown roles receive
 * an explicit restricted-mobile state rather than being allowed into the resident workspace.
 */
data class InstitutionalSnapshot(
    val me: JsonObject,
    val onboarding: JsonObject? = null,
    val documents: List<JsonObject> = emptyList(),
    val training: List<JsonObject> = emptyList(),
    val assignments: List<JsonObject> = emptyList(),
    val rotations: List<JsonObject> = emptyList(),
    val leaves: List<JsonObject> = emptyList(),
    val logbook: List<JsonObject> = emptyList(),
    val logbookCategories: List<JsonObject> = emptyList(),
    val academicOptions: JsonObject? = null,
    val assessments: List<JsonObject> = emptyList(),
    val evaluationTemplates: List<JsonObject> = emptyList(),
    val research: JsonObject? = null,
    val workshops: List<JsonObject> = emptyList(),
    val residentSummary: JsonObject? = null,
    val academicProgress: JsonObject? = null,
    val progressMonitoring: JsonObject? = null,
    /** Populated only for a SUPERVISOR-role account; see [snapshot]. */
    val supervisorSummary: JsonObject? = null,
    val supervisorDashboard: JsonObject? = null,
    /** Human-readable names of sections this account may not read. Shown, not treated as failure. */
    val unavailable: List<String> = emptyList(),
)

class InstitutionalRepository internal constructor(
    private val baseUrl: String,
    private val tokens: TokenStore,
) {
    constructor(context: Context) : this(
        BuildConfig.INSTITUTIONAL_API_BASE_URL,
        EncryptedTokenStore.create(context),
    )

    private val json = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    // Built lazily: constructing OkHttp/Retrofit is not free and must not sit on the startup path
    // of an app whose approved baseline is fully offline.
    private val authorizedApi: InstitutionalApi by lazy {
        val client = baseClient().addInterceptor { chain ->
            val request = chain.request().newBuilder()
                .apply { tokens.access?.let { header("Authorization", "Bearer $it") } }
                .build()
            chain.proceed(request)
        }.build()
        retrofit(client)
    }

    /** Refresh and login must never carry a stale Authorization header. */
    private val anonymousApi: InstitutionalApi by lazy { retrofit(baseClient().build()) }

    private fun baseClient() = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
    // No logging interceptor, in any build type: request bodies here contain credentials.

    private fun retrofit(client: OkHttpClient): InstitutionalApi = Retrofit.Builder()
        .baseUrl(baseUrl)
        .client(client)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()
        .create(InstitutionalApi::class.java)

    fun isConnected(): Boolean = !tokens.access.isNullOrBlank() && !tokens.refresh.isNullOrBlank()
    fun currentUserId(): Int? = tokens.userId

    suspend fun login(username: String, password: String): Result<JsonObject> =
        withContext(Dispatchers.IO) {
            runCatching {
                val response = call { anonymousApi.login(LoginPayload(username.trim(), password)) }
                if (!response.isSuccessful) throw InstitutionalException(loginErrorFor(response.code()))
                val body = response.body()
                    ?: throw InstitutionalException("PGR SIMS returned an empty sign-in response.")
                val access = body.string("access")
                    ?: throw InstitutionalException("PGR SIMS did not return a session token.")
                val refresh = body.string("refresh")
                    ?: throw InstitutionalException("PGR SIMS did not return a refresh token.")
                tokens.save(access, refresh)
                val user = body["user"]?.jsonObject ?: JsonObject(emptyMap())
                user.string("id")?.toIntOrNull()?.let(tokens::saveUserId)
                user
            }
        }

    suspend fun snapshot(): Result<InstitutionalSnapshot> = withContext(Dispatchers.IO) {
        runCatching {
            val me = required(authorized { authorizedApi.me() }, "your institutional profile")
            me.string("id")?.toIntOrNull()?.let(tokens::saveUserId)
            val unavailable = mutableListOf<String>()
            if (me.string("role") == "SUPERVISOR") {
                val supervisorSummary = optional(authorized { authorizedApi.supervisorSummary() }, "Supervisor summary", unavailable)
                val supervisorDashboard = optional(authorized { authorizedApi.supervisorDashboard() }, "Supervisor dashboard", unavailable)
                return@runCatching InstitutionalSnapshot(
                    me = me, unavailable = unavailable,
                    supervisorSummary = supervisorSummary, supervisorDashboard = supervisorDashboard,
                )
            }
            if (me.string("role") != "RESIDENT") {
                return@runCatching InstitutionalSnapshot(me = me, unavailable = listOf("Mobile workspace"))
            }
            val onboarding = optional(authorized { authorizedApi.onboarding() }, "Onboarding", unavailable)
            val documents = optionalArray(authorized { authorizedApi.documents() }, "Documents", unavailable)
            val training = optional(authorized { authorizedApi.training() }, "Training", unavailable).paged()
            val assignments = optional(authorized { authorizedApi.assignments() }, "Supervisor", unavailable).paged()
            val rotations = optional(authorized { authorizedApi.rotations() }, "Rotations", unavailable).paged()
            val leaves = optional(authorized { authorizedApi.leaves() }, "Leave requests", unavailable).paged()
            val logbook = optional(authorized { authorizedApi.logbook() }, "Logbook", unavailable).paged()
            val logbookCategories = optional(authorized { authorizedApi.logbookCategories() }, "Logbook categories", unavailable).paged()
            val academicOptions = optional(authorized { authorizedApi.academicOptions() }, "Academic options", unavailable)
            val assessments = optional(authorized { authorizedApi.assessments() }, "Assessments", unavailable).paged()
            val evaluationTemplates = optional(authorized { authorizedApi.evaluationTemplates() }, "Evaluation templates", unavailable).paged()
            val research = optional(authorized { authorizedApi.research() }, "Research", unavailable)
            val workshops = optional(authorized { authorizedApi.workshops() }, "Workshops", unavailable).paged()
            val residentSummary = optional(authorized { authorizedApi.residentSummary() }, "Resident summary", unavailable)
            val academicProgress = optional(authorized { authorizedApi.academicProgress() }, "Academic progress", unavailable)
            val progressMonitoring = optional(authorized { authorizedApi.progressMonitoring() }, "Progress monitoring", unavailable)
            InstitutionalSnapshot(
                me = me, onboarding = onboarding, documents = documents, training = training,
                assignments = assignments, rotations = rotations, leaves = leaves, logbook = logbook,
                logbookCategories = logbookCategories, academicOptions = academicOptions, assessments = assessments,
                evaluationTemplates = evaluationTemplates, research = research, workshops = workshops,
                residentSummary = residentSummary, academicProgress = academicProgress,
                progressMonitoring = progressMonitoring, unavailable = unavailable,
            )
        }
    }

    /** Notification centre reads are on demand: failure never breaks the institutional workspace. */
    suspend fun notifications(): Result<List<JsonObject>> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.notifications() }, "your notifications").paged() }
    }

    suspend fun me(): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching {
            required(authorized { authorizedApi.me() }, "your institutional profile").also { me ->
                me.string("id")?.toIntOrNull()?.let(tokens::saveUserId)
            }
        }
    }

    suspend fun ownProfile(): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.ownProfile() }, "your profile") }
    }

    suspend fun updateOwnProfile(fields: Map<String, String>): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.updateOwnProfile(fields) }, "your profile") }
    }

    suspend fun changePassword(oldPassword: String, newPassword: String, confirmation: String): Result<JsonObject> =
        withContext(Dispatchers.IO) {
            runCatching {
                required(
                    authorized { authorizedApi.changePassword(ChangePasswordPayload(oldPassword, newPassword, confirmation)) },
                    "your password",
                )
            }
        }

    suspend fun requestPasswordReset(email: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(call { anonymousApi.requestPasswordReset(PasswordResetPayload(email.trim())) }, "the password reset request") }
    }

    suspend fun confirmPasswordReset(
        uid: String,
        token: String,
        newPassword: String,
        confirmation: String,
    ): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching {
            required(
                call { anonymousApi.confirmPasswordReset(PasswordResetConfirmPayload(uid, token, newPassword, confirmation)) },
                "the password reset",
            )
        }
    }

    suspend fun completeProfileForm(): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.completeProfileForm() }, "your profile requirements") }
    }

    suspend fun identityOptions(): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.identityOptions() }, "profile options") }
    }

    suspend fun users(page: Int = 1, role: String? = null, search: String? = null, active: Boolean? = null): Result<PagedJsonResponse> =
        withContext(Dispatchers.IO) {
            runCatching {
                val body = required(authorized { authorizedApi.users(page, role, search?.takeIf { it.isNotBlank() }, active) }, "the user directory")
                PagedJsonResponse(
                    count = body.string("count")?.toIntOrNull() ?: body.paged().size,
                    next = body.string("next"),
                    previous = body.string("previous"),
                    results = body.paged(),
                )
            }
        }

    suspend fun createUser(payload: UniversalUserPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.createUser(payload) }, "the new identity") }
    }

    suspend fun userDetail(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.userDetail(id) }, "this user") }
    }

    suspend fun completeProfile(fields: Map<String, String>): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.completeProfile(fields) }, "your profile") }
    }

    suspend fun acceptDeclaration(): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.acceptDeclaration(DeclarationPayload()) }, "your declaration") }
    }

    suspend fun notificationTarget(kind: String, id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching {
            val response = when (kind.lowercase()) {
                "leave" -> authorized { authorizedApi.leaveDetail(id) }
                "logbook" -> authorized { authorizedApi.logbookDetail(id) }
                "evaluation" -> authorized { authorizedApi.evaluationDetail(id) }
                "rotation" -> authorized { authorizedApi.rotationDetail(id) }
                else -> throw InstitutionalException("This notification target is not supported by this app version.")
            }
            required(response, "this notification target")
        }
    }

    suspend fun unreadNotificationCount(): Result<Int> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.notificationUnreadCount() }, "your notification count").string("unread")?.toIntOrNull() ?: 0 }
    }

    suspend fun markNotifications(ids: List<Int>, read: Boolean): Result<Unit> = withContext(Dispatchers.IO) {
        runCatching {
            if (ids.isNotEmpty()) {
                val request = NotificationIdsPayload(ids.distinct())
                val response = if (read) authorized { authorizedApi.markNotificationsRead(request) }
                else authorized { authorizedApi.markNotificationsUnread(request) }
                required(response, "your notifications")
                Unit
            }
        }
    }

    suspend fun registerPushToken(token: String): Result<Unit> = withContext(Dispatchers.IO) {
        runCatching {
            val request = DeviceRegistrationPayload(token = token, platform = "android")
            required(authorized { authorizedApi.registerDevice(request) }, "your push registration")
            Unit
        }
    }

    /** On-demand detail for one resident, fetched only when a supervisor opens that resident. */
    suspend fun supervisorResidentProgress(residentId: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.supervisorResidentProgress(residentId) }, "this resident's progress") }
    }

    // --- Supervisor workflow queues (on-demand, fetched only when a workflow tab is opened) ----

    suspend fun supervisorLogbookQueue(): Result<List<JsonObject>> = withContext(Dispatchers.IO) {
        runCatching {
            required(authorized { authorizedApi.logbook() }, "the logbook queue")
                .paged()
                .filter { it.string("status") == "SUBMITTED" }
        }
    }

    suspend fun supervisorLeaveQueue(): Result<List<JsonObject>> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.supervisorLeaveQueue() }, "the leave queue").paged() }
    }

    suspend fun supervisorRotationQueue(): Result<List<JsonObject>> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.supervisorRotationQueue() }, "the rotation queue").paged() }
    }

    suspend fun supervisorResearchQueue(): Result<List<JsonObject>> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.supervisorResearchQueue() }, "the research queue").paged() }
    }

    suspend fun supervisorEvaluationQueue(): Result<List<JsonObject>> = withContext(Dispatchers.IO) {
        runCatching {
            required(authorized { authorizedApi.assessments() }, "the evaluation queue")
                .paged().filter { it.string("status") in setOf("SUBMITTED", "UNDER_REVIEW") }
        }
    }

    // --- Supervisor workflow actions -----------------------------------------------------------

    suspend fun verifyLogbook(id: Int, comment: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.verifyLogbook(id, SupervisorCommentPayload(comment)) }, "this logbook entry") }
    }

    suspend fun returnLogbook(id: Int, comment: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.returnLogbook(id, SupervisorCommentPayload(comment)) }, "this logbook entry") }
    }

    suspend fun rejectLogbook(id: Int, comment: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.rejectLogbook(id, SupervisorCommentPayload(comment)) }, "this logbook entry") }
    }

    suspend fun approveLeave(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.approveLeave(id) }, "this leave request") }
    }

    suspend fun rejectLeave(id: Int, reason: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.rejectLeave(id, ReasonPayload(reason)) }, "this leave request") }
    }

    suspend fun approveRotation(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.reviewRotation(id, RotationReviewPayload("approve")) }, "this rotation") }
    }

    suspend fun rejectRotation(id: Int, reason: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.reviewRotation(id, RotationReviewPayload("reject", reason)) }, "this rotation") }
    }

    suspend fun returnRotation(id: Int, reason: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.reviewRotation(id, RotationReviewPayload("defer", reason)) }, "this rotation") }
    }

    suspend fun approveResearch(projectId: Int, feedback: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.approveResearch(ResearchActionPayload(projectId, feedback)) }, "this research submission") }
    }

    suspend fun returnResearch(projectId: Int, feedback: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.returnResearch(ResearchActionPayload(projectId, feedback)) }, "this research submission") }
    }

    suspend fun createLeave(payload: LeaveRequestPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.createLeave(payload) }, "your leave request") }
    }
    suspend fun updateLeave(id: Int, payload: LeaveRequestPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.updateLeave(id, payload) }, "your leave request") }
    }
    suspend fun submitLeave(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.submitLeave(id) }, "your leave request") }
    }
    suspend fun createEvaluation(payload: EvaluationSubmissionPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.createEvaluation(payload) }, "your evaluation") }
    }
    suspend fun updateEvaluation(id: Int, payload: EvaluationSubmissionPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.updateEvaluation(id, payload) }, "your evaluation") }
    }
    suspend fun submitEvaluation(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.submitEvaluation(id) }, "your evaluation") }
    }
    suspend fun cancelEvaluation(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.cancelEvaluation(id) }, "your evaluation") }
    }
    suspend fun startEvaluationReview(id: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.startEvaluationReview(id) }, "this evaluation") }
    }
    suspend fun approveEvaluation(id: Int, comments: String, score: Double? = null, maxScore: Double? = null): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.approveEvaluation(id, EvaluationReviewPayload(comments, score, maxScore)) }, "this evaluation") }
    }
    suspend fun returnEvaluation(id: Int, comments: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.returnEvaluation(id, SupervisorCommentPayload(comments)) }, "this evaluation") }
    }
    suspend fun rejectEvaluation(id: Int, comments: String): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.rejectEvaluation(id, SupervisorCommentPayload(comments)) }, "this evaluation") }
    }

    suspend fun createLogbook(payload: AcademicLogbookPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.createLogbook(payload) }, "your logbook entry") }
    }

    suspend fun submitLogbook(entryId: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.submitLogbook(entryId) }, "your logbook entry") }
    }
    suspend fun cancelLogbook(entryId: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.cancelLogbook(entryId) }, "your logbook entry") }
    }

    suspend fun updateLogbook(entryId: Int, payload: AcademicLogbookPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.updateLogbook(entryId, payload) }, "your logbook entry") }
    }

    suspend fun update(fields: Map<String, String?>): Result<JsonObject> =
        withContext(Dispatchers.IO) {
            runCatching {
                required(
                    authorized { authorizedApi.updateOnboarding(FieldPatch(fields)) },
                    "your institutional profile",
                )
            }
        }

    suspend fun upload(documentId: Int, file: File, displayName: String): Result<JsonObject> =
        withContext(Dispatchers.IO) {
            runCatching {
                validateUpload(displayName, file.length())?.let { throw InstitutionalException(it) }
                val part = MultipartBody.Part.createFormData(
                    "file", displayName, file.asRequestBody(mimeTypeFor(displayName).toMediaType()),
                )
                required(authorized { authorizedApi.upload(documentId, part) }, "the uploaded document")
            }
        }

    suspend fun deferDocument(documentId: Int): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.deferDocument(documentId) }, "this document requirement") }
    }

    suspend fun notificationPreferences(): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.notificationPreferences() }, "notification preferences") }
    }

    suspend fun updateNotificationPreferences(payload: NotificationPreferencesPayload): Result<JsonObject> = withContext(Dispatchers.IO) {
        runCatching { required(authorized { authorizedApi.updateNotificationPreferences(payload) }, "notification preferences") }
    }

    /** Clears the institutional session only. Personal Workspace data is untouched. */
    suspend fun logout() = withContext(Dispatchers.IO) {
        tokens.refresh?.let { token ->
            // Best-effort blacklist; a failure here must still sign the user out locally.
            // PGR SIMS intentionally protects the blacklist endpoint with the current
            // bearer token. Use the authorized path so server-side revocation succeeds;
            // local clearing below remains guaranteed if the network/session has expired.
            runCatching { authorized { authorizedApi.logout(LogoutPayload(token)) } }
        }
        tokens.clear()
    }

    // --- request plumbing -------------------------------------------------------------------

    private suspend fun <T> authorized(request: suspend () -> Response<T>): Response<T> {
        val first = call(request)
        if (first.code() != 401) return first
        return if (refreshToken()) call(request) else first
    }

    private suspend fun <T> call(request: suspend () -> Response<T>): Response<T> = try {
        request()
    } catch (io: IOException) {
        throw InstitutionalException(
            "Cannot reach PGR SIMS. Check your connection and try again."
        )
    }

    private suspend fun refreshToken(): Boolean {
        val token = tokens.refresh ?: return false
        val response = runCatching { anonymousApi.refresh(RefreshPayload(token)) }.getOrNull() ?: return false
        if (!response.isSuccessful) {
            // The refresh token is spent or revoked: drop the session rather than loop on 401.
            tokens.clear()
            return false
        }
        val body = response.body() ?: return false
        val access = body.string("access") ?: return false
        // The backend rotates refresh tokens; keep the old one only if none was returned.
        tokens.save(access, body.string("refresh") ?: token)
        return true
    }

    private fun required(response: Response<JsonObject>, what: String): JsonObject =
        if (response.isSuccessful) {
            response.body() ?: throw InstitutionalException("PGR SIMS returned no $what.")
        } else {
            val validation = if (response.code() == 400 || response.code() == 409) response.validationMessage() else null
            throw InstitutionalException(validation ?: errorFor(response.code(), what))
        }

    private fun Response<*>.validationMessage(): String? = runCatching {
        val body = errorBody()?.string()?.takeIf { it.isNotBlank() } ?: return@runCatching null
        val parsed = json.parseToJsonElement(body).jsonObject
        val value = parsed["detail"] ?: parsed["error"] ?: return@runCatching null
        when (value) {
            is kotlinx.serialization.json.JsonArray -> value.joinToString(" ") { it.jsonPrimitive.content }
            else -> value.jsonPrimitive.content
        }.trim().takeIf { it.isNotBlank() }?.let { if (it.endsWith(".")) it else "$it." }
    }.getOrNull()

    private fun optional(
        response: Response<JsonObject>,
        section: String,
        unavailable: MutableList<String>,
    ): JsonObject? = when {
        response.isSuccessful -> response.body()
        response.code() == 403 || response.code() == 404 -> { unavailable += section; null }
        else -> throw InstitutionalException(errorFor(response.code(), section.lowercase()))
    }

    private fun optionalArray(
        response: Response<JsonArray>,
        section: String,
        unavailable: MutableList<String>,
    ): List<JsonObject> = when {
        response.isSuccessful -> response.body()?.map { it.jsonObject }.orEmpty()
        response.code() == 403 || response.code() == 404 -> { unavailable += section; emptyList() }
        else -> throw InstitutionalException(errorFor(response.code(), section.lowercase()))
    }

    companion object {
        /** Mirrors the backend's own limits so the trainee gets the error before the upload runs. */
        val ALLOWED_UPLOAD_EXTENSIONS = setOf("pdf", "jpg", "jpeg", "png", "doc", "docx")
        const val MAX_UPLOAD_BYTES = 10L * 1024 * 1024

        /** @return null when acceptable, otherwise a message to show the trainee. */
        fun validateUpload(displayName: String, sizeBytes: Long): String? {
            val extension = displayName.substringAfterLast('.', "").lowercase()
            if (extension.isBlank() || extension !in ALLOWED_UPLOAD_EXTENSIONS) {
                return "PGR SIMS accepts ${ALLOWED_UPLOAD_EXTENSIONS.sorted().joinToString(", ")} files only."
            }
            if (sizeBytes <= 0L) return "The selected file is empty."
            if (sizeBytes > MAX_UPLOAD_BYTES) return "The selected file is larger than 10 MB."
            return null
        }

        fun mimeTypeFor(displayName: String): String =
            when (displayName.substringAfterLast('.', "").lowercase()) {
                "pdf" -> "application/pdf"
                "jpg", "jpeg" -> "image/jpeg"
                "png" -> "image/png"
                "doc" -> "application/msword"
                "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                else -> "application/octet-stream"
            }

        fun loginErrorFor(code: Int): String = when (code) {
            400, 401 -> "Incorrect username or password."
            403 -> "This account is not permitted to sign in from the mobile app."
            429 -> "Too many sign-in attempts. Please wait a few minutes and try again."
            in 500..599 -> "PGR SIMS is unavailable right now. Please try again later."
            else -> "Sign in failed (HTTP $code)."
        }

        fun errorFor(code: Int, what: String): String = when (code) {
            401 -> "Your session has expired. Please sign in again."
            403 -> "This account is not permitted to view $what."
            404 -> "$what is not available in PGR SIMS."
            429 -> "Too many requests. Please wait a few minutes and try again."
            in 500..599 -> "PGR SIMS is unavailable right now. Please try again later."
            else -> "Could not load $what (HTTP $code)."
        }
    }
}

/** DRF page ({count,next,previous,results}) or a plain {data:[...]} envelope. */
internal fun JsonObject?.paged(): List<JsonObject> {
    val body = this ?: return emptyList()
    val results = body["results"] ?: body["data"] ?: return emptyList()
    return runCatching { results.jsonArray.map { it.jsonObject } }.getOrDefault(emptyList())
}

internal fun JsonObject.string(key: String): String? =
    runCatching { this[key]?.jsonPrimitive?.contentOrNull }.getOrNull()
