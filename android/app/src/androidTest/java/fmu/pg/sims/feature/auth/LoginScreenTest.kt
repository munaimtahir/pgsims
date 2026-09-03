package fmu.pg.sims.feature.auth

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextInput
import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.testutil.TestFixtures
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import retrofit2.Response

@RunWith(AndroidJUnit4::class)
class LoginScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun validCredentials_signInSucceeds_andReturnsTheAuthenticatedUser() {
        val viewModel = LoginViewModel(AuthRepository(FakeApiService(), FakeTokenStorage()))
        var loggedInUser: AuthMeResponse? = null

        composeTestRule.setContent {
            LoginScreen(viewModel = viewModel, onLoginSuccess = { loggedInUser = it })
        }

        composeTestRule.onNodeWithTag(TestTags.LOGIN_USERNAME_FIELD).performTextInput(TestFixtures.VALID_USERNAME)
        composeTestRule.onNodeWithTag(TestTags.LOGIN_PASSWORD_FIELD).performTextInput(TestFixtures.VALID_PASSWORD)
        composeTestRule.onNodeWithTag(TestTags.LOGIN_SUBMIT_BUTTON).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) { loggedInUser != null }
        assertEquals(TestFixtures.VALID_USERNAME, loggedInUser?.username)
    }

    @Test
    fun invalidCredentials_showsServerErrorMessage_andDoesNotSignIn() {
        val viewModel = LoginViewModel(AuthRepository(FakeApiService(), FakeTokenStorage()))
        var loggedInUser: AuthMeResponse? = null

        composeTestRule.setContent {
            LoginScreen(viewModel = viewModel, onLoginSuccess = { loggedInUser = it })
        }

        composeTestRule.onNodeWithTag(TestTags.LOGIN_USERNAME_FIELD).performTextInput("wrong-user")
        composeTestRule.onNodeWithTag(TestTags.LOGIN_PASSWORD_FIELD).performTextInput("wrong-password")
        composeTestRule.onNodeWithTag(TestTags.LOGIN_SUBMIT_BUTTON).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) {
            composeTestRule
                .onAllNodesWithText("Incorrect username or password.", substring = true)
                .fetchSemanticsNodes()
                .isNotEmpty()
        }
        assertEquals(null, loggedInUser)
    }

    @Test
    fun blankFields_showsLocalValidationError_withoutCallingTheServer() {
        val apiService = FakeApiService()
        var loginCalls = 0
        apiService.loginResult = { req -> loginCalls++; Response.success(TestFixtures.loginResponse()) }
        val viewModel = LoginViewModel(AuthRepository(apiService, FakeTokenStorage()))

        composeTestRule.setContent {
            LoginScreen(viewModel = viewModel, onLoginSuccess = {})
        }

        composeTestRule.onNodeWithTag(TestTags.LOGIN_SUBMIT_BUTTON).performClick()

        composeTestRule.onNodeWithText("Enter your username and password.", substring = true).assertExists()
        assertEquals(0, loginCalls)
    }
}
