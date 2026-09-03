package fmu.pg.sims.core.onboarding

import fmu.pg.sims.core.model.IdentityOptionsResponse
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.OnboardingFieldUpdateRequest
import fmu.pg.sims.core.model.OnboardingStateResponse
import fmu.pg.sims.core.model.SubmitOnboardingRequest
import fmu.pg.sims.core.network.ApiService
import fmu.pg.sims.core.network.safeCall

class OnboardingRepository(private val apiService: ApiService) {

    suspend fun getState(): NetworkResult<OnboardingStateResponse> =
        safeCall { apiService.getOnboardingState() }

    suspend fun getIdentityOptions(): NetworkResult<IdentityOptionsResponse> =
        safeCall { apiService.getIdentityOptions() }

    suspend fun saveField(field: String, value: String?): NetworkResult<OnboardingStateResponse> =
        safeCall { apiService.updateOnboardingFields(OnboardingFieldUpdateRequest(field = field, value = value)) }

    suspend fun saveFields(fields: Map<String, String?>): NetworkResult<OnboardingStateResponse> =
        safeCall { apiService.updateOnboardingFields(OnboardingFieldUpdateRequest(fields = fields)) }

    suspend fun submit(): NetworkResult<OnboardingStateResponse> =
        safeCall { apiService.submitOnboarding(SubmitOnboardingRequest(accepted = true)) }
}
