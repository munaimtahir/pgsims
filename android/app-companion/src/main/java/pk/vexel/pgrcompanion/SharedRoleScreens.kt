package pk.vexel.pgrcompanion

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.serialization.json.JsonObject

private enum class SharedDestination(val label: String, val icon: ImageVector) {
    HOME("Home", Icons.Default.Home),
    INBOX("Inbox", Icons.Default.Notifications),
    PROFILE("Profile", Icons.Default.Person),
}

/** A deliberately bounded shell for ADMIN and SUPPORT_STAFF. Backend permissions remain final. */
@Composable
@OptIn(ExperimentalMaterial3Api::class)
internal fun SharedRolePane(
    repository: InstitutionalRepository,
    me: JsonObject,
    onSignOut: () -> Unit,
    onRefresh: () -> Unit,
    onChangePassword: () -> Unit,
) {
    var destination by rememberSaveable { mutableStateOf(SharedDestination.HOME) }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("PGR Companion") },
                actions = { TextButton(onClick = onSignOut) { Text("Sign out") } },
            )
        },
        bottomBar = {
            NavigationBar {
                SharedDestination.entries.forEach { item ->
                    NavigationBarItem(
                        selected = destination == item,
                        onClick = { destination = item },
                        icon = { Icon(item.icon, contentDescription = item.label) },
                        label = { Text(item.label) },
                    )
                }
            }
        },
    ) { padding ->
        Column(
            Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            when (destination) {
                SharedDestination.HOME -> {
                    Text("Welcome, ${me.string("username").orEmpty()}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                    Text("Signed in as ${InstitutionalLabels.humanize(me.string("role").orEmpty())}.")
                    if (me.string("role") == "SUPPORT_STAFF") {
                        Text("Mobile access is limited to your own account and backend-authorized read-only information.")
                    } else {
                        Text("Identity administration and operational reports are being added in bounded mobile stages. The web portal remains available for configuration-heavy work.")
                    }
                    OutlinedButton(onClick = onRefresh, modifier = Modifier.fillMaxWidth()) { Text("Refresh") }
                }
                SharedDestination.INBOX -> NotificationCenterScreen(repository, { destination = SharedDestination.HOME }) { _, _ -> }
                SharedDestination.PROFILE -> {
                    OwnProfileEditor(repository, onRefresh)
                    Button(onClick = onChangePassword, modifier = Modifier.fillMaxWidth()) { Text("Change password") }
                    OutlinedButton(onClick = onSignOut, modifier = Modifier.fillMaxWidth()) { Text("Sign out") }
                }
            }
        }
    }
}
