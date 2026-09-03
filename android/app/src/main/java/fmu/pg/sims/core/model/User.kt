package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class User(
    @SerialName("id") val id: Int,
    @SerialName("username") val username: String,
    @SerialName("email") val email: String = "",
    @SerialName("first_name") val firstName: String = "",
    @SerialName("last_name") val lastName: String = "",
    @SerialName("full_name") val fullName: String = "",
    @SerialName("display_name") val displayName: String = "",
    @SerialName("role") val role: Role,
    @SerialName("specialty") val specialty: String? = null,
    @SerialName("year") val year: Int? = null,
    @SerialName("registration_number") val registrationNumber: String? = null,
    @SerialName("phone_number") val phoneNumber: String? = null,
    @SerialName("date_joined") val dateJoined: String? = null,
    @SerialName("is_active") val isActive: Boolean = true,
    @SerialName("must_change_password") val mustChangePassword: Boolean = false,
    @SerialName("is_profile_complete") val isProfileComplete: Boolean = false,
)

@Serializable
data class AuthMeResponse(
    @SerialName("id") val id: Int,
    @SerialName("username") val username: String,
    @SerialName("role") val role: Role,
    @SerialName("must_change_password") val mustChangePassword: Boolean = false,
    @SerialName("is_profile_complete") val isProfileComplete: Boolean = false,
    @SerialName("profile_type") val profileType: String? = null,
    @SerialName("profile_id") val profileId: Int? = null,
    @SerialName("profile_status") val profileStatus: String? = null,
    @SerialName("profile_schema_version") val profileSchemaVersion: Int = 1,
    @SerialName("completed_schema_version") val completedSchemaVersion: Int = 0,
    @SerialName("missing_required_fields") val missingRequiredFields: List<String> = emptyList(),
    @SerialName("allowed_next_route") val allowedNextRoute: String = "/users/dashboard/",
    @SerialName("required_onboarding_fields") val requiredOnboardingFields: List<String> = emptyList(),
    @SerialName("pending_upload_count") val pendingUploadCount: Int = 0,
    @SerialName("pending_uploads") val pendingUploads: List<OnboardingPendingUpload> = emptyList(),
    @SerialName("pending_supervisor_link") val pendingSupervisorLink: OnboardingPendingSupervisorLink? = null,
    @SerialName("onboarding_complete") val onboardingComplete: Boolean = false,
    @SerialName("onboarding_review_status") val onboardingReviewStatus: String? = null,
    @SerialName("onboarding_review_note") val onboardingReviewNote: String? = null,
    @SerialName("onboarding_submitted_at") val onboardingSubmittedAt: String? = null,
    @SerialName("onboarding_reviewed_at") val onboardingReviewedAt: String? = null,
) {
    /** Effective review state for routing; residents with no profile yet read as NOT_SUBMITTED. */
    val effectiveReviewStatus: String
        get() = onboardingReviewStatus ?: ReviewStatus.NOT_SUBMITTED
}
