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
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit

/**
 * Institutional Workspace networking boundary.
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

@Serializable data class FieldPatch(val fields: Map<String, String?>)

interface InstitutionalApi {
    @POST("api/auth/login/") suspend fun login(@Body body: LoginPayload): Response<JsonObject>
    @POST("api/auth/refresh/") suspend fun refresh(@Body body: RefreshPayload): Response<JsonObject>
    @POST("api/auth/logout/") suspend fun logout(@Body body: LogoutPayload): Response<JsonObject>
    @GET("api/auth/me/") suspend fun me(): Response<JsonObject>
    @GET("api/auth/onboarding/") suspend fun onboarding(): Response<JsonObject>
    @PATCH("api/auth/onboarding/") suspend fun updateOnboarding(@Body body: FieldPatch): Response<JsonObject>
    @GET("api/resident-documents/") suspend fun documents(): Response<JsonArray>
    @GET("api/resident-training/") suspend fun training(): Response<JsonObject>
    @GET("api/supervision/assignments/") suspend fun assignments(): Response<JsonObject>
    @Multipart @POST("api/resident-documents/{id}/upload/")
    suspend fun upload(@Path("id") id: Int, @Part file: MultipartBody.Part): Response<JsonObject>
}

/** A message that is safe to show a trainee. Never carries a token, password or raw stack trace. */
class InstitutionalException(message: String) : Exception(message)

/** Where the institutional session lives. Deliberately separate from the personal store. */
interface TokenStore {
    val access: String?
    val refresh: String?
    fun save(access: String, refresh: String)
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
    override fun save(access: String, refresh: String) {
        prefs.edit().putString(KEY_ACCESS, access).putString(KEY_REFRESH, refresh).apply()
    }
    override fun clear() { prefs.edit().clear().apply() }

    companion object {
        private const val KEY_ACCESS = "access"
        private const val KEY_REFRESH = "refresh"
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
    override val access: String? get() = accessValue
    override val refresh: String? get() = refreshValue
    override fun save(access: String, refresh: String) { accessValue = access; refreshValue = refresh }
    override fun clear() { accessValue = null; refreshValue = null }
}

/**
 * One institutional read. [me] is required — if identity cannot be read there is no session to
 * show. Every other section is optional so that a non-resident account (SUPERVISOR / ADMIN), for
 * which resident-only endpoints legitimately return 403, still gets a working screen.
 */
data class InstitutionalSnapshot(
    val me: JsonObject,
    val onboarding: JsonObject? = null,
    val documents: List<JsonObject> = emptyList(),
    val training: List<JsonObject> = emptyList(),
    val assignments: List<JsonObject> = emptyList(),
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

    suspend fun login(username: String, password: String): Result<JsonObject> =
        withContext(Dispatchers.IO) {
            runCatching {
                val response = call { anonymousApi.login(LoginPayload(username.trim(), password)) }
                if (!response.isSuccessful) throw InstitutionalException(loginErrorFor(response.code()))
                val body = response.body()
                    ?: throw InstitutionalException("The institution's server returned an empty sign-in response.")
                val access = body.string("access")
                    ?: throw InstitutionalException("The institution's server did not return a session token.")
                val refresh = body.string("refresh")
                    ?: throw InstitutionalException("The institution's server did not return a refresh token.")
                tokens.save(access, refresh)
                body["user"]?.jsonObject ?: JsonObject(emptyMap())
            }
        }

    suspend fun snapshot(): Result<InstitutionalSnapshot> = withContext(Dispatchers.IO) {
        runCatching {
            val me = required(authorized { authorizedApi.me() }, "your institutional profile")
            val unavailable = mutableListOf<String>()
            val onboarding = optional(authorized { authorizedApi.onboarding() }, "Onboarding", unavailable)
            val documents = optionalArray(authorized { authorizedApi.documents() }, "Documents", unavailable)
            val training = optional(authorized { authorizedApi.training() }, "Training", unavailable).paged()
            val assignments = optional(authorized { authorizedApi.assignments() }, "Supervisor", unavailable).paged()
            InstitutionalSnapshot(me, onboarding, documents, training, assignments, unavailable)
        }
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

    /** Clears the institutional session only. Personal Workspace data is untouched. */
    suspend fun logout() = withContext(Dispatchers.IO) {
        tokens.refresh?.let { token ->
            // Best-effort blacklist; a failure here must still sign the user out locally.
            runCatching { anonymousApi.logout(LogoutPayload(token)) }
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
            "Cannot reach the institution's server. Check your connection and try again."
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
            response.body() ?: throw InstitutionalException("The institution's server returned no $what.")
        } else {
            throw InstitutionalException(errorFor(response.code(), what))
        }

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
                return "This institution accepts ${ALLOWED_UPLOAD_EXTENSIONS.sorted().joinToString(", ")} files only."
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
            in 500..599 -> "The institution's server is unavailable right now. Please try again later."
            else -> "Sign in failed (HTTP $code)."
        }

        fun errorFor(code: Int, what: String): String = when (code) {
            401 -> "Your institutional session has expired. Please sign in again."
            403 -> "This account is not permitted to view $what."
            404 -> "$what is not available on this institution's server."
            429 -> "Too many requests. Please wait a few minutes and try again."
            in 500..599 -> "The institution's server is unavailable right now. Please try again later."
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
