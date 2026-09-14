package pk.vexel.pgrcompanion

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.Modifier
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import okhttp3.mockwebserver.Dispatcher
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import okhttp3.mockwebserver.RecordedRequest
import org.junit.After
import org.junit.Rule
import org.junit.Test

class InboxUiTest {
    @get:Rule val compose = createComposeRule()
    private val server = MockWebServer().apply {
        dispatcher = object : Dispatcher() {
            override fun dispatch(request: RecordedRequest) = MockResponse().setHeader("Content-Type", "application/json").setBody(
                if (request.path == "/api/notifications/") """{"results":[{"id":1,"title":"Synthetic notice","body":"fixture","is_read":false,"target":{"kind":"leave","id":42}}]}"""
                else if (request.path == "/api/leaves/42/") """{"id":42,"status":"DRAFT","reason":"Exact target fixture"}"""
                else "{}"
            )
        }
        start()
    }
    private val repo = InstitutionalRepository(server.url("/").toString(), InMemoryTokenStore().apply { save("synthetic", "synthetic") })
    @After fun close() = server.shutdown()

    @Test fun residentInboxInsideScrollingShellOpensExactRecord() {
        compose.setContent { MaterialTheme {
            Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
                NotificationCenterScreen(repo, {}, { _, _ -> })
            }
        } }
        compose.waitUntil(10000) { compose.onAllNodesWithText("Synthetic notice").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithText("Synthetic notice").performScrollTo().performClick()
        compose.waitUntil(10000) { compose.onAllNodesWithText("Record #42").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithText("Exact target fixture", substring = true).assertExists()
        compose.onNodeWithText("Close").performClick()
        compose.onNodeWithText("Action required").assertExists()
    }

    @Test fun supervisorHasReachableInbox() {
        val snapshot = InstitutionalSnapshot(Json.parseToJsonElement("""{"id":9001,"role":"SUPERVISOR"}""").jsonObject)
        compose.setContent { MaterialTheme { SupervisorPane(repo, snapshot, false, {}, {}) } }
        compose.onNodeWithText("Inbox").performClick()
        compose.waitUntil(10000) { compose.onAllNodesWithText("Synthetic notice").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithText("Synthetic notice").performScrollTo().assertIsDisplayed()
    }
}
