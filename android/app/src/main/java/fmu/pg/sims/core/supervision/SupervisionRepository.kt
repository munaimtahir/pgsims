package fmu.pg.sims.core.supervision

import fmu.pg.sims.core.model.CreatePendingSupervisorLinkRequest
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.PendingSupervisorLinkDto
import fmu.pg.sims.core.model.ResidentSupervisorAssignmentDto
import fmu.pg.sims.core.model.SupervisionOptionsResponse
import fmu.pg.sims.core.model.map
import fmu.pg.sims.core.network.ApiService
import fmu.pg.sims.core.network.safeCall

class SupervisionRepository(private val apiService: ApiService) {

    suspend fun searchSupervisors(
        trainingSiteId: Int? = null,
        departmentId: Int? = null,
    ): NetworkResult<SupervisionOptionsResponse> =
        safeCall { apiService.getSupervisionOptions(trainingSiteId, departmentId) }

    suspend fun getMyAssignments(residentProfileId: Int): NetworkResult<List<ResidentSupervisorAssignmentDto>> =
        safeCall { apiService.getSupervisorAssignments(residentProfileId) }.map { it.results }

    /**
     * Requests linkage to a supervisor. Residents cannot create a ResidentSupervisorAssignment
     * directly (backend restricts that write to ADMIN, see IsSupervisionAdminOrReadOnly) — both
     * "pick an existing supervisor" and "supervisor not listed" therefore go through the same
     * PendingSupervisorAssignment request-for-admin-resolution mechanism. When [existingName] and
     * [existingDepartment] come from a real search result, this simply records a confirmable
     * request against a known identity rather than free text; no fake SupervisorProfile is ever
     * created client-side either way.
     */
    suspend fun requestSupervisorLink(
        residentProfileId: Int,
        supervisorName: String,
        department: String = "",
        institution: String = "",
        pmdcNumber: String = "",
        email: String = "",
        phone: String = "",
        notes: String = "",
    ): NetworkResult<PendingSupervisorLinkDto> =
        safeCall {
            apiService.createPendingSupervisorLink(
                CreatePendingSupervisorLinkRequest(
                    resident = residentProfileId,
                    supervisorNameText = supervisorName,
                    departmentText = department,
                    institutionText = institution,
                    pmdcNumberText = pmdcNumber,
                    emailText = email,
                    phoneText = phone,
                    notes = notes,
                )
            )
        }
}
