package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * The 4 canonical roles of the PGSIMS clean-room identity architecture.
 * Legacy roles (HOD, TEACHER, STUDENT, etc.) are strictly forbidden.
 */
@Serializable
enum class Role {
    @SerialName("ADMIN")
    ADMIN,

    @SerialName("RESIDENT")
    RESIDENT,

    @SerialName("SUPERVISOR")
    SUPERVISOR,

    @SerialName("SUPPORT_STAFF")
    SUPPORT_STAFF;

    val displayName: String
        get() = when (this) {
            ADMIN -> "Administrator"
            RESIDENT -> "Postgraduate Resident"
            SUPERVISOR -> "Clinical Supervisor"
            SUPPORT_STAFF -> "Support Staff"
        }
}
