package fmu.pg.sims.feature.onboarding

import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.assertIsNotEnabled
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.model.ReviewStatus
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.supervision.SupervisionRepository
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.testutil.TestFixtures
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import retrofit2.Response

@RunWith(AndroidJUnit4::class)
class OnboardingReviewScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private fun buildViewModel(apiService: FakeApiService): OnboardingViewModel {
        val authRepository = AuthRepository(apiService, FakeTokenStorage())
        return OnboardingViewModel(
            OnboardingRepository(apiService),
            SupervisionRepository(apiService),
            DocumentsRepository(apiService),
            authRepository,
        )
    }

    @Test
    fun incompleteProfile_disablesSubmit() {
        val apiService = FakeApiService(
            onboardingStateResult = { Response.success(TestFixtures.onboardingState(profileComplete = false)) },
        )
        val viewModel = buildViewModel(apiService)

        composeTestRule.setContent {
            OnboardingReviewScreen(viewModel = viewModel, onBack = {}, onSubmitted = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_REVIEW_SUBMIT_BUTTON).assertIsNotEnabled()
    }

    @Test
    fun completeProfile_submitCallsTheRealTransition_andReachesPendingReview() {
        val apiService = FakeApiService()
        var submitCalled = false
        val originalSubmit = apiService.submitOnboardingResult
        apiService.submitOnboardingResult = { req -> submitCalled = true; originalSubmit(req) }
        val viewModel = buildViewModel(apiService)
        var submitted = false

        composeTestRule.setContent {
            OnboardingReviewScreen(viewModel = viewModel, onBack = {}, onSubmitted = { submitted = true })
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_REVIEW_SUBMIT_BUTTON).assertIsEnabled().performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) {
            viewModel.uiState.value.state?.reviewStatus == ReviewStatus.PENDING_REVIEW
        }
        assertTrue(submitCalled)
        // onSubmitted() fires from the screen's LaunchedEffect watching reviewStatus, not a local boolean save.
        composeTestRule.waitUntil(timeoutMillis = 5_000) { submitted }
        assertTrue(submitted)
    }
}
