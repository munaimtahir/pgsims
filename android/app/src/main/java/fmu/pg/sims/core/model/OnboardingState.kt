package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class OnboardingState(
    @SerialName("onboarding_complete") val onboardingComplete: Boolean = false,
    @SerialName("stage") val stage: String = "INITIAL",
    @SerialName("missing_fields") val missingFields: List<String> = emptyList(),
    @SerialName("pending_documents_count") val pendingDocumentsCount: Int = 0,
)
