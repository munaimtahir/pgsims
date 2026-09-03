package fmu.pg.sims.feature.auth

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextInput
import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.auth.AuthRepository
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.ui.TestTags
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/** Covers the mandatory must_change_password gate a fresh resident hits on first login. */
@RunWith(AndroidJUnit4::class)
class ChangePasswordScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun successfulChange_invokesOnChangedCallback() {
        val viewModel = ChangePasswordViewModel(AuthRepository(FakeApiService(), FakeTokenStorage()))
        var changed = false

        composeTestRule.setContent {
            ChangePasswordScreen(viewModel = viewModel, onChanged = { changed = true })
        }

        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_OLD_FIELD).performTextInput("pgfmu123")
        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_NEW_FIELD).performTextInput("N3wSecurePass!")
        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_CONFIRM_FIELD).performTextInput("N3wSecurePass!")
        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_SUBMIT_BUTTON).performClick()

        composeTestRule.waitUntil(timeoutMillis = 5_000) { changed }
        assertTrue(changed)
    }

    @Test
    fun mismatchedConfirmation_showsLocalErrorWithoutCallingServer() {
        val apiService = FakeApiService()
        var changePasswordCalls = 0
        apiService.changePasswordResult = { changePasswordCalls++; throw AssertionError("should not call server") }
        val viewModel = ChangePasswordViewModel(AuthRepository(apiService, FakeTokenStorage()))

        composeTestRule.setContent {
            ChangePasswordScreen(viewModel = viewModel, onChanged = {})
        }

        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_OLD_FIELD).performTextInput("pgfmu123")
        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_NEW_FIELD).performTextInput("aaa")
        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_CONFIRM_FIELD).performTextInput("bbb")
        composeTestRule.onNodeWithTag(TestTags.CHANGE_PASSWORD_SUBMIT_BUTTON).performClick()

        composeTestRule.onNodeWithText("New passwords do not match.", substring = true).assertExists()
        assertTrue(changePasswordCalls == 0)
    }
}
