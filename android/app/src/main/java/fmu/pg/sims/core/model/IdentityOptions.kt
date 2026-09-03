package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/** GET /api/identity/options/ — dropdown source for onboarding enrollment fields. */
@Serializable
data class IdentityOptionsResponse(
    @SerialName("institutions") val institutions: List<OptionItem> = emptyList(),
    @SerialName("training_sites") val trainingSites: List<OptionItem> = emptyList(),
    @SerialName("hospitals") val hospitals: List<OptionItem> = emptyList(),
    @SerialName("departments") val departments: List<OptionItem> = emptyList(),
    @SerialName("programs") val programs: List<OptionItem> = emptyList(),
    @SerialName("academic_sessions") val academicSessions: List<OptionItem> = emptyList(),
    @SerialName("designations") val designations: List<OptionItem> = emptyList(),
    @SerialName("specialties") val specialties: List<OptionItem> = emptyList(),
)

/**
 * A selectable dropdown option. [id] is what must be sent back as the onboarding field value:
 * for hospital/department_ref/program_ref this is the numeric primary key (as a string); for
 * academic_session_ref/specialty_ref it's the record's `code`, per
 * sims.users.onboarding_api._set_resident_onboarding_field.
 */
@Serializable
data class OptionItem(
    @SerialName("id") val id: String,
    @SerialName("name") val name: String,
    @SerialName("code") val code: String? = null,
)
