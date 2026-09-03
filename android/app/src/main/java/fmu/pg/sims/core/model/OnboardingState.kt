package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/** Mirrors sims.users.onboarding_api.get_resident_onboarding_state() exactly. */
@Serializable
data class OnboardingStateResponse(
    @SerialName("password_change_required") val passwordChangeRequired: Boolean = false,
    @SerialName("profile_complete") val profileComplete: Boolean = false,
    @SerialName("onboarding_complete") val onboardingComplete: Boolean = false,
    @SerialName("required_onboarding_fields") val requiredOnboardingFields: List<String> = emptyList(),
    @SerialName("training_record_id") val trainingRecordId: Int? = null,
    @SerialName("supervisor_status") val supervisorStatus: String = "NOT_STARTED",
    @SerialName("declaration_accepted") val declarationAccepted: Boolean = false,
    @SerialName("review_status") val reviewStatus: String = ReviewStatus.NOT_SUBMITTED,
    @SerialName("review_note") val reviewNote: String = "",
    @SerialName("submitted_at") val submittedAt: String? = null,
    @SerialName("reviewed_at") val reviewedAt: String? = null,
    @SerialName("documents") val documents: List<OnboardingDocumentSummary> = emptyList(),
    @SerialName("baseline") val baseline: OnboardingBaseline? = null,
    @SerialName("workshops") val workshops: List<OnboardingWorkshop> = emptyList(),
    @SerialName("sections") val sections: List<OnboardingSection> = emptyList(),
    @SerialName("pending_upload_count") val pendingUploadCount: Int = 0,
    @SerialName("pending_uploads") val pendingUploads: List<OnboardingPendingUpload> = emptyList(),
    @SerialName("pending_supervisor_link") val pendingSupervisorLink: OnboardingPendingSupervisorLink? = null,
)

/** review_status values from ResidentProfile.REVIEW_STATUS_CHOICES. */
object ReviewStatus {
    const val NOT_SUBMITTED = "NOT_SUBMITTED"
    const val PENDING_REVIEW = "PENDING_REVIEW"
    const val APPROVED = "APPROVED"
    const val CORRECTION_REQUIRED = "CORRECTION_REQUIRED"
}

@Serializable
data class OnboardingDocumentSummary(
    @SerialName("id") val id: Int,
    @SerialName("requirement_id") val requirementId: Int? = null,
    @SerialName("title") val title: String = "",
    @SerialName("status") val status: String = "NOT_STARTED",
    @SerialName("stage") val stage: String = "OPTIONAL",
)

@Serializable
data class OnboardingPendingUpload(
    @SerialName("requirement_id") val requirementId: Int? = null,
    @SerialName("document_id") val documentId: Int,
    @SerialName("document_type") val documentType: String = "",
    @SerialName("display_name") val displayName: String = "",
    @SerialName("stage") val stage: String = "OPTIONAL",
    @SerialName("status") val status: String = "NOT_STARTED",
    @SerialName("verification_remarks") val verificationRemarks: String = "",
)

@Serializable
data class OnboardingPendingSupervisorLink(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String = "",
    @SerialName("status") val status: String = "PENDING",
)

@Serializable
data class OnboardingBaseline(
    @SerialName("research") val research: OnboardingResearch? = null,
    @SerialName("thesis") val thesis: OnboardingThesis? = null,
)

@Serializable
data class OnboardingResearch(
    @SerialName("title") val title: String = "",
    @SerialName("topic_area") val topicArea: String = "",
    @SerialName("status") val status: String = "DRAFT",
)

@Serializable
data class OnboardingThesis(
    @SerialName("status") val status: String = "NOT_STARTED",
    @SerialName("notes") val notes: String = "",
)

@Serializable
data class OnboardingWorkshop(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String = "",
    @SerialName("code") val code: String = "",
    @SerialName("completed_at") val completedAt: String? = null,
    @SerialName("completion_id") val completionId: Int? = null,
)

@Serializable
data class OnboardingSection(
    @SerialName("key") val key: String,
    @SerialName("title") val title: String,
    @SerialName("fields") val fields: List<OnboardingField> = emptyList(),
)

@Serializable
data class OnboardingField(
    @SerialName("field") val field: String,
    @SerialName("label") val label: String,
    @SerialName("value") val value: String? = null,
    @SerialName("required") val required: Boolean = false,
)

/** PATCH /api/auth/onboarding/ body: either a single field/value pair or a bulk "fields" map. */
@Serializable
data class OnboardingFieldUpdateRequest(
    @SerialName("field") val field: String? = null,
    @SerialName("value") val value: String? = null,
    @SerialName("fields") val fields: Map<String, String?>? = null,
)

/** POST /api/resident-onboarding/state/ body. */
@Serializable
data class SubmitOnboardingRequest(
    @SerialName("accepted") val accepted: Boolean = true,
)
