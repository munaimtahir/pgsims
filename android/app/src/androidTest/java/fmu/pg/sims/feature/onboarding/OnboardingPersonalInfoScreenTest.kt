package fmu.pg.sims.feature.onboarding

import androidx.compose.ui.test.assert
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextClearance
import androidx.compose.ui.test.performTextInput
import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.supervision.SupervisionRepository
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/** Covers onboarding save/resume: existing backend values prefill the form, edits round-trip
 * through a real save call, and the saved value is what the next load would resume with. */
@RunWith(AndroidJUnit4::class)
class OnboardingPersonalInfoScreenTest {

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
    fun existingBackendValues_arePrefilled_onLoad() {
        val viewModel = buildViewModel(FakeApiService())

        composeTestRule.setContent {
            OnboardingPersonalInfoScreen(viewModel = viewModel, onBack = {}, onNext = {})
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_PERSONAL_FULL_NAME_FIELD).assert(hasText("Test Resident"))
    }

    @Test
    fun editingAndSaving_persistsTheNewValue_andAdvances() {
        val apiService = FakeApiService()
        var savedPhone: String? = null
        val originalUpdate = apiService.updateOnboardingFieldsResult
        apiService.updateOnboardingFieldsResult = { req ->
            savedPhone = (req.fields ?: emptyMap())["phone"]
            originalUpdate(req)
        }
        val viewModel = buildViewModel(apiService)
        var advanced = false

        composeTestRule.setContent {
            OnboardingPersonalInfoScreen(viewModel = viewModel, onBack = {}, onNext = { advanced = true })
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) { !viewModel.uiState.value.loading }
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_PERSONAL_PHONE_FIELD).performTextClearance()
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_PERSONAL_PHONE_FIELD).performTextInput("03009999999")
        composeTestRule.onNodeWithTag(TestTags.ONBOARDING_PERSONAL_PRIMARY_BUTTON).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) { advanced }
        assertTrue(advanced)
        assertTrue("expected the edited phone value to reach the backend call", savedPhone == "03009999999")
    }
}
