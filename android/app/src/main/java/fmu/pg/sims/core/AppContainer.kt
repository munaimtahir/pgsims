package fmu.pg.sims.core

import android.content.Context
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.auth.SecureTokenStorage
import fmu.pg.sims.core.auth.TokenStorage
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.network.ApiClient
import fmu.pg.sims.core.network.ApiService
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.supervision.SupervisionRepository
import fmu.pg.sims.core.training.TrainingRepository

/**
 * App-wide singleton wiring. No DI framework is used anywhere in this codebase yet (Hilt/Koin
 * are not dependencies) — this continues the existing manual-singleton pattern already
 * established by [ApiClient] rather than introducing a new one.
 */
class AppContainer(context: Context) {
    val tokenStorage: TokenStorage = SecureTokenStorage(context.applicationContext)
    val apiService: ApiService = ApiClient.create(tokenStorage = tokenStorage)

    val authRepository = AuthRepository(apiService, tokenStorage)
    val onboardingRepository = OnboardingRepository(apiService)
    val supervisionRepository = SupervisionRepository(apiService)
    val documentsRepository = DocumentsRepository(apiService)
    val trainingRepository = TrainingRepository(apiService)
}
