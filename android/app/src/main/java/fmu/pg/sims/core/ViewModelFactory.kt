package fmu.pg.sims.core

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.CreationExtras
import fmu.pg.sims.core.auth.SessionViewModel
import fmu.pg.sims.feature.auth.ChangePasswordViewModel
import fmu.pg.sims.feature.auth.LoginViewModel
import fmu.pg.sims.feature.documents.DocumentsViewModel
import fmu.pg.sims.feature.home.HomeViewModel
import fmu.pg.sims.feature.onboarding.OnboardingViewModel
import fmu.pg.sims.feature.training.TrainingViewModel

/** No DI framework in this codebase — a small manual factory keyed off [AppContainer]. */
class ViewModelFactory(private val container: AppContainer) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>, extras: CreationExtras): T {
        @Suppress("UNCHECKED_CAST")
        return when (modelClass) {
            SessionViewModel::class.java -> SessionViewModel(container.authRepository) as T
            LoginViewModel::class.java -> LoginViewModel(container.authRepository) as T
            ChangePasswordViewModel::class.java -> ChangePasswordViewModel(container.authRepository) as T
            OnboardingViewModel::class.java -> OnboardingViewModel(
                container.onboardingRepository,
                container.supervisionRepository,
                container.documentsRepository,
                container.authRepository,
            ) as T
            HomeViewModel::class.java -> HomeViewModel(
                container.authRepository,
                container.onboardingRepository,
                container.trainingRepository,
            ) as T
            TrainingViewModel::class.java -> TrainingViewModel(container.trainingRepository) as T
            DocumentsViewModel::class.java -> DocumentsViewModel(container.documentsRepository) as T
            else -> throw IllegalArgumentException("Unknown ViewModel class: ${modelClass.name}")
        }
    }
}
