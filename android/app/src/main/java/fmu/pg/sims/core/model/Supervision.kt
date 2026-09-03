package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/** GET /api/supervision/options/ */
@Serializable
data class SupervisionOptionsResponse(
    @SerialName("supervisors") val supervisors: List<SupervisorOption> = emptyList(),
)

@Serializable
data class SupervisorOption(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String = "",
    @SerialName("training_site") val trainingSite: String = "",
    @SerialName("department") val department: String = "",
    @SerialName("designation") val designation: String = "",
    @SerialName("active_primary_count") val activePrimaryCount: Int = 0,
    @SerialName("active_total_count") val activeTotalCount: Int = 0,
)

@Serializable
data class ResidentSummaryDto(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String = "",
    @SerialName("username") val username: String = "",
    @SerialName("department") val department: String = "",
    @SerialName("training_site") val trainingSite: String = "",
)

@Serializable
data class SupervisorSummaryDto(
    @SerialName("id") val id: Int,
    @SerialName("name") val name: String = "",
    @SerialName("department") val department: String = "",
    @SerialName("training_site") val trainingSite: String = "",
    @SerialName("designation") val designation: String = "",
)

/** GET/POST /api/supervision/assignments/ */
@Serializable
data class ResidentSupervisorAssignmentDto(
    @SerialName("id") val id: Int = 0,
    @SerialName("resident") val resident: ResidentSummaryDto? = null,
    @SerialName("supervisor") val supervisor: SupervisorSummaryDto? = null,
    @SerialName("assignment_type") val assignmentType: String = "PRIMARY",
    @SerialName("status") val status: String = "ACTIVE",
    @SerialName("is_active") val isActive: Boolean = true,
    @SerialName("start_date") val startDate: String? = null,
    @SerialName("end_date") val endDate: String? = null,
    @SerialName("notes") val notes: String = "",
)

/** POST body for /api/supervision/assignments/ (create). */
@Serializable
data class CreateSupervisorAssignmentRequest(
    @SerialName("resident_id") val residentId: Int,
    @SerialName("supervisor_id") val supervisorId: Int,
    @SerialName("assignment_type") val assignmentType: String = "PRIMARY",
    @SerialName("start_date") val startDate: String,
    @SerialName("notes") val notes: String = "",
)

/** POST /api/pending-supervisor-links/ — "supervisor not listed" request. Never fabricates a
 * SupervisorProfile; resolved later by an administrator. */
@Serializable
data class CreatePendingSupervisorLinkRequest(
    @SerialName("resident") val resident: Int,
    @SerialName("supervisor_name_text") val supervisorNameText: String,
    @SerialName("department_text") val departmentText: String = "",
    @SerialName("institution_text") val institutionText: String = "",
    @SerialName("pmdc_number_text") val pmdcNumberText: String = "",
    @SerialName("email_text") val emailText: String = "",
    @SerialName("phone_text") val phoneText: String = "",
    @SerialName("notes") val notes: String = "",
)

@Serializable
data class PendingSupervisorLinkDto(
    @SerialName("id") val id: Int,
    @SerialName("resident") val resident: Int,
    @SerialName("supervisor_name_text") val supervisorNameText: String = "",
    @SerialName("status") val status: String = "PENDING",
)
