package fmu.pg.sims.feature.onboarding

import androidx.compose.ui.test.assert
import androidx.compose.ui.test.hasText
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
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import retrofit2.Response

@RunWith(AndroidJUnit4::class)
class OnboardingStatusScreensTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun pendingReview_refreshAndSignOut_invokeTheirCallbacks() {
        var refreshed = false
        var loggedOut = false

        composeTestRule.setContent {
            OnboardingPendingReviewScreen(onLogout = { loggedOut = true }, onRefresh = { refreshed = true })
        }

        composeTestRule.onNodeWithTag(TestTags.PENDING_REVIEW_REFRESH_BUTTON).performClick()
        composeTestRule.onNodeWithTag(TestTags.PENDING_REVIEW_SIGN_OUT_BUTTON).performClick()

        assertTrue(refreshed)
        assertTrue(loggedOut)
    }

    @Test
    fun correctionRequired_showsTheAdminReviewNote_verbatim() {
        composeTestRule.setContent {
            OnboardingCorrectionRequiredScreen(
                reviewNote = "Registration number does not match PM&DC records.",
                onFixNow = {},
                onLogout = {},
            )
        }

        composeTestRule
            .onNodeWithTag(TestTags.CORRECTION_REQUIRED_REVIEW_NOTE)
            .assert(hasText("Registration number does not match PM&DC records."))
    }

    @Test
    fun correctionRequired_fixNowAndSignOut_invokeTheirCallbacks() {
        var fixNowTapped = false
        var loggedOut = false

        composeTestRule.setContent {
            OnboardingCorrectionRequiredScreen(
                reviewNote = "",
                onFixNow = { fixNowTapped = true },
                onLogout = { loggedOut = true },
            )
        }

        composeTestRule.onNodeWithTag(TestTags.CORRECTION_REQUIRED_FIX_NOW_BUTTON).performClick()
        composeTestRule.onNodeWithTag(TestTags.CORRECTION_REQUIRED_SIGN_OUT_BUTTON).performClick()

        assertTrue(fixNowTapped)
        assertTrue(loggedOut)
    }

    /** Resubmission reuses the exact same POST /api/resident-onboarding/state/ transition as the
     * first submit — this proves a resident coming from CORRECTION_REQUIRED can fix a field and
     * resubmit back to PENDING_REVIEW through the real review screen. */
    @Test
    fun residentInCorrectionRequired_canFixAndResubmit_backToPendingReview() {
        val apiService = FakeApiService(
            onboardingStateResult = {
                Response.success(
                    TestFixtures.onboardingState(
                        reviewStatus = ReviewStatus.CORRECTION_REQUIRED,
                        reviewNote = "CNIC field is invalid.",
                        profileComplete = true,
                    ),
                )
            },
        )
        val authRepository = AuthRepository(apiService, FakeTokenStorage())
        val viewModel = OnboardingViewModel(
            OnboardingRepository(apiService),
            SupervisionRepository(apiService),
            DocumentsRepository(apiService),
            authRepository,
        )
        var resubmitted = false

        composeTestRule.setContent {
            OnboardingReviewScreen(viewModel = viewModel, onBack = {}, onSubmitted = { resubmitted = true })
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        assertEquals(ReviewStatus.CORRECTION_REQUIRED, viewModel.uiState.value.state?.reviewStatus)

        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_REVIEW_SUBMIT_BUTTON).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) { resubmitted }
        assertEquals(ReviewStatus.PENDING_REVIEW, viewModel.uiState.value.state?.reviewStatus)
    }
}
