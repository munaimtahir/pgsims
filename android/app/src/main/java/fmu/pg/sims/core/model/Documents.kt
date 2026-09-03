package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/** Status values from sims.users.models.ResidentDocument.STATUS_CHOICES. */
object DocumentStatus {
    const val NOT_STARTED = "NOT_STARTED"
    const val DEFERRED = "DEFERRED"
    const val UPLOADED = "UPLOADED"
    const val PENDING_REVIEW = "PENDING_REVIEW"
    const val VERIFIED = "VERIFIED"
    const val REJECTED = "REJECTED"
    const val REUPLOAD_REQUIRED = "REUPLOAD_REQUIRED"
}

/** Mirrors ResidentDocumentViewSet._data() exactly — used for both list and action responses. */
@Serializable
data class ResidentDocumentDto(
    @SerialName("id") val id: Int,
    @SerialName("resident_id") val residentId: Int,
    @SerialName("requirement_id") val requirementId: Int? = null,
    @SerialName("document_type") val documentType: String = "",
    @SerialName("title") val title: String = "",
    @SerialName("stage") val stage: String = "OPTIONAL",
    @SerialName("status") val status: String = DocumentStatus.NOT_STARTED,
    @SerialName("original_filename") val originalFilename: String = "",
    @SerialName("verification_remarks") val verificationRemarks: String = "",
    @SerialName("file") val file: String? = null,
    @SerialName("file_url") val fileUrl: String? = null,
) {
    val isOutstanding: Boolean
        get() = status in setOf(
            DocumentStatus.NOT_STARTED,
            DocumentStatus.DEFERRED,
            DocumentStatus.REUPLOAD_REQUIRED,
        )
}

@Serializable
data class ResidentDocumentRequirementDto(
    @SerialName("id") val id: Int,
    @SerialName("display_name") val displayName: String = "",
    @SerialName("document_type") val documentType: String = "",
    @SerialName("stage") val stage: String = "OPTIONAL",
    @SerialName("is_required") val isRequired: Boolean = false,
    @SerialName("is_active") val isActive: Boolean = true,
    @SerialName("display_order") val displayOrder: Int = 0,
)
