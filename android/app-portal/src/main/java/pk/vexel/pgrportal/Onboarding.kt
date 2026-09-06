package pk.vexel.pgrportal

import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.booleanOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

/**
 * Pure translation of the institution's onboarding vocabulary. Every value here originates in
 * `sims.users.onboarding_api` / `ResidentDocument.STATUS_*`; nothing is a client-invented state.
 * Unknown values are humanised rather than dropped, so a backend that grows a status still renders.
 */
object InstitutionalLabels {

    fun humanize(value: String): String =
        value.replace('_', ' ').lowercase().replaceFirstChar { it.uppercase() }

    /** `ResidentDocument.STATUS_*`. */
    fun documentStatus(raw: String): String = when (raw.uppercase()) {
        "NOT_STARTED" -> "Not uploaded"
        "DEFERRED" -> "Deferred"
        "UPLOADED" -> "Uploaded"
        "PENDING_REVIEW" -> "Under review"
        "VERIFIED" -> "Approved"
        "REJECTED" -> "Rejected"
        "REUPLOAD_REQUIRED" -> "Correction required"
        else -> humanize(raw).ifBlank { "Unknown" }
    }

    /** The backend's upload action *is* the resubmission route, so name the button for the state. */
    fun documentAction(raw: String): String = when (raw.uppercase()) {
        "NOT_STARTED", "DEFERRED" -> "Upload"
        "REUPLOAD_REQUIRED", "REJECTED" -> "Replace"
        else -> "Replace"
    }

    /** Replacing something the institution already accepted must be deliberate, never incidental. */
    fun replacementNeedsConfirmation(raw: String): Boolean =
        raw.uppercase() in setOf("VERIFIED", "PENDING_REVIEW", "UPLOADED")

    fun documentNeedsAction(raw: String): Boolean =
        raw.uppercase() in setOf("NOT_STARTED", "DEFERRED", "REUPLOAD_REQUIRED", "REJECTED")

    /** `ResidentProfile.REVIEW_*`. */
    fun reviewStatus(raw: String): String = when (raw.uppercase()) {
        "NOT_SUBMITTED" -> "Not submitted"
        "PENDING_REVIEW" -> "Under review"
        "APPROVED" -> "Approved"
        "CORRECTION_REQUIRED" -> "Correction required"
        "" -> "Not available"
        else -> humanize(raw)
    }

    fun supervisorStatus(raw: String): String = when (raw.uppercase()) {
        "ASSIGNED" -> "Assigned"
        "PENDING" -> "Awaiting the institution's confirmation"
        "NOT_STARTED", "NOT_ASSIGNED", "" -> "Not assigned yet"
        else -> humanize(raw)
    }
}

/**
 * Which onboarding fields a resident may actually edit from the phone.
 *
 * The backend accepts free text only for the fields below. The reference fields resolve to a
 * Hospital / Department / TrainingProgram / AcademicSession / Specialty row by primary key or code,
 * and the date fields demand ISO-8601 — presenting either as a text box would show the resident a
 * raw database id and let a typo repoint their institutional record. Those stay read-only here and
 * are changed through the institution, which is where the backend treats them as administrative.
 */
object OnboardingFieldPolicy {

    val RESIDENT_EDITABLE = setOf("full_name", "phone", "email", "registration_no", "cnic", "notes")
    val REFERENCE = setOf("hospital", "department_ref", "program_ref", "academic_session_ref", "specialty_ref")
    val ADMINISTRATIVE_DATE = setOf("training_start_date", "expected_end_date", "current_level")

    fun isEditable(field: String): Boolean = field in RESIDENT_EDITABLE

    /** @return null when the field is editable, otherwise why it is not. */
    fun readOnlyReason(field: String): String? = when (field) {
        in RESIDENT_EDITABLE -> null
        in REFERENCE -> "Set by your institution."
        in ADMINISTRATIVE_DATE -> "Part of your training record, maintained by your institution."
        else -> "Maintained by your institution."
    }

    /**
     * Reference fields arrive as a bare row id, which means nothing to a resident. Show what the
     * institution actually named, or say it is unset — never the id.
     */
    fun displayValue(field: String, rawValue: String, resolved: String? = null): String = when {
        !resolved.isNullOrBlank() -> resolved
        field in REFERENCE -> if (rawValue.isBlank()) "Not set" else "Recorded"
        rawValue.isBlank() -> "Not set"
        else -> rawValue
    }
}

/**
 * The institution's own view of where this resident stands. Every element is read from the
 * backend's onboarding payload; nothing is recomputed locally from personal data.
 */
data class OnboardingSummary(
    val reviewStatus: String = "",
    val reviewNote: String = "",
    val supervisorStatus: String = "",
    val profileComplete: Boolean = false,
    val declarationAccepted: Boolean = false,
    val onboardingComplete: Boolean = false,
    val outstanding: List<String> = emptyList(),
) {
    val hasOutstanding: Boolean get() = outstanding.isNotEmpty()

    companion object {
        fun from(onboarding: JsonObject?, documents: List<JsonObject> = emptyList()): OnboardingSummary {
            val body = onboarding ?: return OnboardingSummary()
            val labels = fieldLabels(body)
            val outstanding = mutableListOf<String>()

            body.strings("required_onboarding_fields").forEach { field ->
                outstanding += "Complete ${labels[field] ?: InstitutionalLabels.humanize(field)}"
            }

            val documentSource = body.objectList("documents").ifEmpty { documents }
            documentSource.forEach { document ->
                val status = document.string("status").orEmpty()
                if (InstitutionalLabels.documentNeedsAction(status)) {
                    val title = document.string("title").orEmpty().ifBlank { "a required document" }
                    outstanding += "${InstitutionalLabels.documentAction(status)} $title (${InstitutionalLabels.documentStatus(status)})"
                }
            }

            val supervisor = body.string("supervisor_status").orEmpty()
            if (supervisor.uppercase() != "ASSIGNED") outstanding += "Supervisor assignment: ${InstitutionalLabels.supervisorStatus(supervisor)}"

            val declaration = body.boolean("declaration_accepted")
            if (!declaration) outstanding += "Accept your institution's declaration to submit for review"

            return OnboardingSummary(
                reviewStatus = body.string("review_status").orEmpty(),
                reviewNote = body.string("review_note").orEmpty(),
                supervisorStatus = supervisor,
                profileComplete = body.boolean("profile_complete"),
                declarationAccepted = declaration,
                onboardingComplete = body.boolean("onboarding_complete"),
                outstanding = outstanding,
            )
        }

        /** field key -> the institution's own label for it, taken from the declared sections. */
        fun fieldLabels(onboarding: JsonObject): Map<String, String> =
            onboarding.objectList("sections")
                .flatMap { it.objectList("fields") }
                .mapNotNull { field ->
                    val key = field.string("field").orEmpty()
                    val label = field.string("label").orEmpty()
                    if (key.isBlank()) null else key to label.ifBlank { InstitutionalLabels.humanize(key) }
                }
                .toMap()
    }
}

internal fun JsonObject.objectList(key: String): List<JsonObject> =
    runCatching { this[key]?.jsonArray?.map { it.jsonObject } }.getOrNull().orEmpty()

internal fun JsonObject.strings(key: String): List<String> =
    runCatching { this[key]?.jsonArray?.mapNotNull { it.jsonPrimitive.contentOrNullSafe() } }.getOrNull().orEmpty()

internal fun JsonObject.boolean(key: String): Boolean =
    runCatching { this[key]?.jsonPrimitive?.booleanOrNull }.getOrNull() ?: false

private fun kotlinx.serialization.json.JsonPrimitive.contentOrNullSafe(): String? =
    runCatching { if (this is kotlinx.serialization.json.JsonNull) null else content }.getOrNull()
