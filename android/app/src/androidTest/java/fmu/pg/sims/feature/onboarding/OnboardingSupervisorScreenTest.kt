package fmu.pg.sims.feature.onboarding

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.test.performTextInput
import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.supervision.SupervisionRepository
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/** Covers both supervisor paths: selecting an existing supervisor and the "not listed" request —
 * both must converge on PendingSupervisorAssignment, never a fake SupervisorProfile. */
@RunWith(AndroidJUnit4::class)
class OnboardingSupervisorScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private fun buildViewModel(apiService: FakeApiService): OnboardingViewModel {
        val authRepository = AuthRepository(apiService, FakeTokenStorage())
        return OnboardingViewModel(
            OnboardingRepository(apiService),
            SupervisionRepository(apiService),
            DocumentsRepository(apiService),
            authRepository,
        ).also { it.load() }
    }

    @Test
    fun searchingAndSelectingAnExistingSupervisor_createsAPendingLink_notAFakeSupervisor() {
        val apiService = FakeApiService()
        var pendingLinkRequestedName: String? = null
        val original = apiService.createPendingSupervisorLinkResult
        apiService.createPendingSupervisorLinkResult = { req -> pendingLinkRequestedName = req.supervisorNameText; original(req) }
        val viewModel = buildViewModel(apiService)

        composeTestRule.setContent {
            OnboardingSupervisorScreen(viewModel = viewModel, residentProfileId = 4, onBack = {}, onNext = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_SUPERVISOR_SEARCH_FIELD).performTextInput("Ayesha")
        composeTestRule.onNodeWithTag(TestTags.supervisorSelectButton(201)).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) { viewModel.uiState.value.supervisorRequestSuccess }
        assertEquals("Dr. Ayesha Khan", pendingLinkRequestedName)
    }

    @Test
    fun supervisorNotListed_submitsManualRequest_withoutFabricatingASupervisor() {
        val apiService = FakeApiService()
        var pendingLinkRequestedName: String? = null
        val original = apiService.createPendingSupervisorLinkResult
        apiService.createPendingSupervisorLinkResult = { req -> pendingLinkRequestedName = req.supervisorNameText; original(req) }
        val viewModel = buildViewModel(apiService)

        composeTestRule.setContent {
            OnboardingSupervisorScreen(viewModel = viewModel, residentProfileId = 4, onBack = {}, onNext = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_SUPERVISOR_NOT_LISTED_TOGGLE).performScrollTo().performClick()
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_SUPERVISOR_MANUAL_NAME_FIELD).performScrollTo().performTextInput("Dr. Off-Roster Person")
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_SUPERVISOR_SUBMIT_REQUEST_BUTTON).performScrollTo().performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) { viewModel.uiState.value.supervisorRequestSuccess }
        assertEquals("Dr. Off-Roster Person", pendingLinkRequestedName)
    }

    @Test
    fun supervisorNotListed_blankName_isRejectedLocally_withoutCallingTheServer() {
        val apiService = FakeApiService()
        var serverCalled = false
        apiService.createPendingSupervisorLinkResult = { serverCalled = true; throw AssertionError("should not reach server") }
        val viewModel = buildViewModel(apiService)

        composeTestRule.setContent {
            OnboardingSupervisorScreen(viewModel = viewModel, residentProfileId = 4, onBack = {}, onNext = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_SUPERVISOR_NOT_LISTED_TOGGLE).performScrollTo().performClick()
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_SUPERVISOR_SUBMIT_REQUEST_BUTTON).performScrollTo().performClick()

        composeTestRule.onNodeWithText("Supervisor name is required.", substring = true).assertExists()
        assertTrue(!serverCalled)
        assertNull(viewModel.uiState.value.state?.pendingSupervisorLink)
    }
}
