package fmu.pg.sims.feature.onboarding

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.supervision.SupervisionRepository
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Covers document deferral (a real state transition through the fake backend) and that the
 * upload affordance is offered/withheld correctly per document status. Actually driving the
 * system document picker to complete an upload requires a real device content resolver and is
 * left to the on-device pass (see PENDING_WORK_AND_EMULATOR_TEST_PLAN.md §4) — this test proves
 * the button is present, enabled, and wired to the real upload endpoint contract instead.
 */
@RunWith(AndroidJUnit4::class)
class OnboardingDocumentsScreenTest {

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
    fun outstandingDocument_offersUploadAndDefer_verifiedDocumentOffersNeither() {
        val viewModel = buildViewModel(FakeApiService())

        composeTestRule.setContent {
            OnboardingDocumentsScreen(viewModel = viewModel, onBack = {}, onNext = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.documentUploadButton(101)).assertIsDisplayed().assertIsEnabled()
        composeTestRule.onNodeWithTag(TestTags.documentDeferButton(101)).assertIsDisplayed().assertIsEnabled()
        // Document 102 is VERIFIED: neither upload nor defer should be offered.
        assertEquals(0, composeTestRule.onAllNodesWithTag(TestTags.documentUploadButton(102)).fetchSemanticsNodes().size)
        assertEquals(0, composeTestRule.onAllNodesWithTag(TestTags.documentDeferButton(102)).fetchSemanticsNodes().size)
    }

    @Test
    fun deferringAnEligibleDocument_updatesItsStatus_andKeepsItOutstanding() {
        val apiService = FakeApiService()
        val viewModel = buildViewModel(apiService)

        composeTestRule.setContent {
            OnboardingDocumentsScreen(viewModel = viewModel, onBack = {}, onNext = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.documentDeferButton(101)).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) {
            viewModel.uiState.value.documents.firstOrNull { it.id == 101 }?.status == "DEFERRED"
        }
        val deferred = viewModel.uiState.value.documents.first { it.id == 101 }
        assertEquals("DEFERRED", deferred.status)
        // Deferral must never read as done — it stays in the outstanding set.
        assertEquals(true, deferred.isOutstanding)
    }
}
