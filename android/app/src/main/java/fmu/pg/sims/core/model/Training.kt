package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Mirrors sims.training.serializers.ResidentTrainingRecordSerializer — the record behind
 * onboarding_state.training_record_id (sims.training.ResidentTrainingRecord, NOT the separate
 * sims.academics.ResidentTrainingRecord used elsewhere in the platform).
 */
@Serializable
data class ResidentTrainingRecordDto(
    @SerialName("id") val id: Int,
    @SerialName("resident_user") val residentUser: Int,
    @SerialName("resident_name") val residentName: String = "",
    @SerialName("program") val program: Int? = null,
    @SerialName("program_name") val programName: String = "",
    @SerialName("program_code") val programCode: String = "",
    @SerialName("start_date") val startDate: String? = null,
    @SerialName("expected_end_date") val expectedEndDate: String? = null,
    @SerialName("current_level") val currentLevel: String = "",
    @SerialName("active") val active: Boolean = true,
)
