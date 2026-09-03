package fmu.pg.sims.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import fmu.pg.sims.core.ViewModelFactory
import fmu.pg.sims.core.auth.SessionDestination
import fmu.pg.sims.core.auth.SessionViewModel
import fmu.pg.sims.feature.auth.ChangePasswordScreen
import fmu.pg.sims.feature.auth.ChangePasswordViewModel
import fmu.pg.sims.feature.auth.LoginScreen
import fmu.pg.sims.feature.auth.LoginViewModel
import fmu.pg.sims.feature.home.HomeShellScreen
import fmu.pg.sims.feature.onboarding.OnboardingCorrectionRequiredScreen
import fmu.pg.sims.feature.onboarding.OnboardingDocumentsScreen
import fmu.pg.sims.feature.onboarding.OnboardingPendingReviewScreen
import fmu.pg.sims.feature.onboarding.OnboardingPersonalInfoScreen
import fmu.pg.sims.feature.onboarding.OnboardingReviewScreen
import fmu.pg.sims.feature.onboarding.OnboardingSupervisorScreen
import fmu.pg.sims.feature.onboarding.OnboardingTrainingScreen
import fmu.pg.sims.feature.onboarding.OnboardingViewModel
import fmu.pg.sims.feature.onboarding.OnboardingWelcomeScreen
import fmu.pg.sims.ui.components.FullScreenLoading

private object Routes {
    const val LOGIN = "login"
    const val CHANGE_PASSWORD = "change_password"
    const val ONBOARDING_WELCOME = "onboarding/welcome"
    const val ONBOARDING_PERSONAL = "onboarding/personal"
    const val ONBOARDING_TRAINING = "onboarding/training"
    const val ONBOARDING_SUPERVISOR = "onboarding/supervisor"
    const val ONBOARDING_DOCUMENTS = "onboarding/documents"
    const val ONBOARDING_REVIEW = "onboarding/review"
    const val ONBOARDING_PENDING = "onboarding/pending"
    const val ONBOARDING_CORRECTION = "onboarding/correction"
    const val HOME = "home"
}

private fun routeFor(destination: SessionDestination): String = when (destination) {
    SessionDestination.LoggedOut -> Routes.LOGIN
    SessionDestination.ChangePassword -> Routes.CHANGE_PASSWORD
    SessionDestination.Onboarding -> Routes.ONBOARDING_WELCOME
    SessionDestination.PendingReview -> Routes.ONBOARDING_PENDING
    SessionDestination.CorrectionRequired -> Routes.ONBOARDING_CORRECTION
    SessionDestination.Home -> Routes.HOME
    SessionDestination.Loading -> Routes.LOGIN
}

@Composable
fun PgsimsNavHost(viewModelFactory: ViewModelFactory) {
    val sessionViewModel: SessionViewModel = viewModel(factory = viewModelFactory)
    val destination by sessionViewModel.destination.collectAsState()

    if (destination == SessionDestination.Loading) {
        FullScreenLoading()
        return
    }

    val navController = rememberNavController()
    val onboardingViewModel: OnboardingViewModel = viewModel(factory = viewModelFactory)
    val me by sessionViewModel.me.collectAsState()

    LaunchedEffect(destination) {
        val route = routeFor(destination)
        if (navController.currentDestination?.route != route) {
            navController.navigate(route) {
                popUpTo(0) { inclusive = true }
                launchSingleTop = true
            }
        }
    }

    NavHost(navController = navController, startDestination = routeFor(destination)) {
        composable(Routes.LOGIN) {
            val loginViewModel: LoginViewModel = viewModel(factory = viewModelFactory)
            LoginScreen(viewModel = loginViewModel, onLoginSuccess = { user -> sessionViewModel.onLoginSuccess(user) })
        }
        composable(Routes.CHANGE_PASSWORD) {
            val changePasswordViewModel: ChangePasswordViewModel = viewModel(factory = viewModelFactory)
            ChangePasswordScreen(viewModel = changePasswordViewModel, onChanged = { sessionViewModel.refresh() })
        }
        composable(Routes.ONBOARDING_WELCOME) {
            OnboardingWelcomeScreen(viewModel = onboardingViewModel, onStart = { navController.navigate(Routes.ONBOARDING_PERSONAL) })
        }
        composable(Routes.ONBOARDING_PERSONAL) {
            OnboardingPersonalInfoScreen(
                viewModel = onboardingViewModel,
                onBack = { navController.popBackStack() },
                onNext = { navController.navigate(Routes.ONBOARDING_TRAINING) },
            )
        }
        composable(Routes.ONBOARDING_TRAINING) {
            OnboardingTrainingScreen(
                viewModel = onboardingViewModel,
                onBack = { navController.popBackStack() },
                onNext = { navController.navigate(Routes.ONBOARDING_SUPERVISOR) },
            )
        }
        composable(Routes.ONBOARDING_SUPERVISOR) {
            OnboardingSupervisorScreen(
                viewModel = onboardingViewModel,
                residentProfileId = me?.profileId,
                onBack = { navController.popBackStack() },
                onNext = { navController.navigate(Routes.ONBOARDING_DOCUMENTS) },
            )
        }
        composable(Routes.ONBOARDING_DOCUMENTS) {
            OnboardingDocumentsScreen(
                viewModel = onboardingViewModel,
                onBack = { navController.popBackStack() },
                onNext = { navController.navigate(Routes.ONBOARDING_REVIEW) },
            )
        }
        composable(Routes.ONBOARDING_REVIEW) {
            OnboardingReviewScreen(
                viewModel = onboardingViewModel,
                onBack = { navController.popBackStack() },
                onSubmitted = { sessionViewModel.refresh() },
            )
        }
        composable(Routes.ONBOARDING_PENDING) {
            OnboardingPendingReviewScreen(
                onLogout = { sessionViewModel.logout() },
                onRefresh = { sessionViewModel.refresh() },
            )
        }
        composable(Routes.ONBOARDING_CORRECTION) {
            OnboardingCorrectionRequiredScreen(
                reviewNote = me?.onboardingReviewNote.orEmpty(),
                onFixNow = {
                    onboardingViewModel.load()
                    navController.navigate(Routes.ONBOARDING_WELCOME)
                },
                onLogout = { sessionViewModel.logout() },
            )
        }
        composable(Routes.HOME) {
            HomeShellScreen(viewModelFactory = viewModelFactory, onLogout = { sessionViewModel.logout() })
        }
    }
}
