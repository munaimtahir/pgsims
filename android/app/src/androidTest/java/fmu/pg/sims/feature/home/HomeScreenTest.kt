package fmu.pg.sims.feature.home

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import fmu.pg.sims.core.AppContainer
import fmu.pg.sims.core.ViewModelFactory
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.onboarding.OnboardingRepository
import fmu.pg.sims.core.training.TrainingRepository
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.testutil.TestFixtures
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import retrofit2.Response

/** Covers the persistent outstanding-document reminder: it must be re-derived from server state
 * every time Home loads, never a one-time locally-dismissed flag. */
@RunWith(AndroidJUnit4::class)
class HomeScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    // HomeScreen's `viewModel` parameter has a default that resolves through this factory, but
    // every test below overrides `viewModel` directly with one built on FakeApiService — this
    // factory is only supplied because the parameter itself is required, not because it's used.
    private fun unusedRealFactory(): ViewModelFactory =
        ViewModelFactory(AppContainer(InstrumentationRegistry.getInstrumentation().targetContext))

    private fun buildHomeViewModel(apiService: FakeApiService): HomeViewModel {
        val authRepository = AuthRepository(apiService, FakeTokenStorage(accessToken = "fake-access", refreshToken = "fake-refresh"))
        return HomeViewModel(authRepository, OnboardingRepository(apiService), TrainingRepository(apiService))
    }

    @Test
    fun outstandingDocuments_showTheActionRequiredBanner_andRouteToDocumentsTab() {
        val apiService = FakeApiService(authMeResult = { Response.success(TestFixtures.authMe(pendingUploadCount = 2)) })
        var navigatedToDocuments = false

        composeTestRule.setContent {
            HomeScreen(
                viewModelFactory = unusedRealFactory(),
                onGoToDocuments = { navigatedToDocuments = true },
                viewModel = buildHomeViewModel(apiService),
            )
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) {
            composeTestRule.onAllNodesWithTagCompat(TestTags.HOME_OUTSTANDING_BANNER).isNotEmpty()
        }
        composeTestRule.onNodeWithTag(TestTags.HOME_OUTSTANDING_BANNER).assertIsDisplayed()
        composeTestRule.onNodeWithTag(TestTags.HOME_UPLOAD_DOCUMENTS_BUTTON).performClick()
        assertTrue(navigatedToDocuments)
    }

    @Test
    fun noOutstandingDocuments_showsAllCompleteBanner_notTheReminder() {
        val apiService = FakeApiService(authMeResult = { Response.success(TestFixtures.authMe(pendingUploadCount = 0)) })

        composeTestRule.setContent {
            HomeScreen(viewModelFactory = unusedRealFactory(), onGoToDocuments = {}, viewModel = buildHomeViewModel(apiService))
        }

        composeTestRule.waitUntil(timeoutMillis = 5_000) {
            composeTestRule.onAllNodesWithTagCompat(TestTags.HOME_ALL_COMPLETE_BANNER).isNotEmpty()
        }
        composeTestRule.onNodeWithTag(TestTags.HOME_ALL_COMPLETE_BANNER).assertIsDisplayed()
        assertTrue(composeTestRule.onAllNodesWithTag(TestTags.HOME_OUTSTANDING_BANNER).fetchSemanticsNodes().isEmpty())
    }
}

private fun androidx.compose.ui.test.junit4.ComposeContentTestRule.onAllNodesWithTagCompat(tag: String) =
    this.onAllNodesWithTag(tag).fetchSemanticsNodes()
