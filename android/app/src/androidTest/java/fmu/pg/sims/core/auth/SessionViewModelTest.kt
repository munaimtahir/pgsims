package fmu.pg.sims.core.auth

import androidx.test.ext.junit.runners.AndroidJUnit4
import fmu.pg.sims.core.model.Role
import fmu.pg.sims.testutil.FakeApiService
import fmu.pg.sims.testutil.FakeTokenStorage
import fmu.pg.sims.testutil.TestFixtures
import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import retrofit2.Response

/**
 * SessionViewModel is the single source of truth for top-level routing (see PgsimsNavHost) — it
 * must always derive the destination from backend state (mustChangePassword / role /
 * review_status), never from locally-cached booleans. No Compose needed; this is plain
 * ViewModel + coroutine logic, but lives under androidTest per this sandbox's constraint that
 * Espresso/instrumentation infra isn't runnable here — it's still meant to run via
 * connectedDebugAndroidTest on a real device/emulator alongside the rest of this suite.
 */
@RunWith(AndroidJUnit4::class)
class SessionViewModelTest {

    private lateinit var tokenStorage: FakeTokenStorage

    @Before
    fun setUp() {
        tokenStorage = FakeTokenStorage()
    }

    private fun waitFor(timeoutMillis: Long = 5_000, condition: () -> Boolean) {
        val deadline = System.currentTimeMillis() + timeoutMillis
        while (System.currentTimeMillis() < deadline) {
            if (condition()) return
            Thread.sleep(20)
        }
        assert(condition()) { "condition not met within ${timeoutMillis}ms" }
    }

    @Test
    fun noStoredToken_routesToLoggedOut() {
        val apiService = FakeApiService()
        val viewModel = SessionViewModel(AuthRepository(apiService, tokenStorage))

        waitFor { viewModel.destination.value != SessionDestination.Loading }
        assertEquals(SessionDestination.LoggedOut, viewModel.destination.value)
    }

    @Test
    fun mustChangePassword_takesPriorityOverEverythingElse() {
        tokenStorage.saveTokens("access", "refresh")
        val apiService = FakeApiService(
            authMeResult = { Response.success(TestFixtures.authMe(mustChangePassword = true, reviewStatus = "APPROVED")) },
        )
        val viewModel = SessionViewModel(AuthRepository(apiService, tokenStorage))

        waitFor { viewModel.destination.value != SessionDestination.Loading }
        assertEquals(SessionDestination.ChangePassword, viewModel.destination.value)
    }

    @Test
    fun reviewStatusCorrectionRequired_routesToCorrectionScreen() {
        tokenStorage.saveTokens("access", "refresh")
        val apiService = FakeApiService(
            authMeResult = { Response.success(TestFixtures.authMe(reviewStatus = "CORRECTION_REQUIRED", reviewNote = "Fix CNIC")) },
        )
        val viewModel = SessionViewModel(AuthRepository(apiService, tokenStorage))

        waitFor { viewModel.destination.value != SessionDestination.Loading }
        assertEquals(SessionDestination.CorrectionRequired, viewModel.destination.value)
    }

    @Test
    fun reviewStatusApproved_routesToHome() {
        tokenStorage.saveTokens("access", "refresh")
        val apiService = FakeApiService(authMeResult = { Response.success(TestFixtures.authMe(reviewStatus = "APPROVED")) })
        val viewModel = SessionViewModel(AuthRepository(apiService, tokenStorage))

        waitFor { viewModel.destination.value != SessionDestination.Loading }
        assertEquals(SessionDestination.Home, viewModel.destination.value)
    }

    @Test
    fun nonResidentRole_alwaysRoutesToHome_regardlessOfReviewStatus() {
        tokenStorage.saveTokens("access", "refresh")
        val apiService = FakeApiService(
            authMeResult = { Response.success(TestFixtures.authMe(role = Role.SUPERVISOR, reviewStatus = "NOT_SUBMITTED")) },
        )
        val viewModel = SessionViewModel(AuthRepository(apiService, tokenStorage))

        waitFor { viewModel.destination.value != SessionDestination.Loading }
        assertEquals(SessionDestination.Home, viewModel.destination.value)
    }

    @Test
    fun logout_thenLoginAgain_reEstablishesACorrectSession_fromServerStateOnly() {
        tokenStorage.saveTokens("access", "refresh")
        val apiService = FakeApiService(authMeResult = { Response.success(TestFixtures.authMe(reviewStatus = "APPROVED")) })
        val authRepository = AuthRepository(apiService, tokenStorage)
        val viewModel = SessionViewModel(authRepository)

        waitFor { viewModel.destination.value == SessionDestination.Home }

        viewModel.logout()
        waitFor { viewModel.destination.value == SessionDestination.LoggedOut }
        assertEquals(null, tokenStorage.getAccessToken())

        // Relaunching the app with a stale/no token must not resurrect the old Home destination.
        val freshViewModel = SessionViewModel(authRepository)
        waitFor { freshViewModel.destination.value != SessionDestination.Loading }
        assertEquals(SessionDestination.LoggedOut, freshViewModel.destination.value)

        // A fresh login re-derives the destination purely from the server response.
        viewModel.onLoginSuccess(TestFixtures.authMe(reviewStatus = "PENDING_REVIEW"))
        assertEquals(SessionDestination.PendingReview, viewModel.destination.value)
    }
}
