package pk.vexel.pgrcompanion

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.booleanOrNull
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

private fun JsonObject.noticeText(key: String): String = string(key).orEmpty()
private fun JsonObject.noticeNumber(key: String): Int? = runCatching { this[key]?.jsonPrimitive?.intOrNull }.getOrNull()
private fun JsonObject.noticeFlag(key: String): Boolean = runCatching { this[key]?.jsonPrimitive?.booleanOrNull }.getOrNull() ?: false
private fun JsonObject.noticeChild(key: String): JsonObject? = runCatching { this[key]?.jsonObject }.getOrNull()

/**
 * Backend-owned inbox.  Only the serializer's validated `target` object is interpreted; legacy
 * metadata remains display-only, which prevents a notification body from becoming navigation.
 */
@Composable
internal fun NotificationCenterScreen(
    repository: InstitutionalRepository,
    onBack: () -> Unit,
    onTarget: (kind: String, id: Int?) -> Unit,
) {
    val scope = rememberCoroutineScope()
    var rows by remember { mutableStateOf<List<JsonObject>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var message by remember { mutableStateOf<String?>(null) }
    var preferencesOpen by remember { mutableStateOf(false) }
    fun load() = scope.launch {
        loading = true
        repository.notifications().fold(
            { rows = it; message = null },
            { message = it.message ?: "Could not load notifications." },
        )
        loading = false
    }
    LaunchedEffect(Unit) { load() }

    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Action required", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Row {
                TextButton(onClick = { preferencesOpen = true }) { Text("Preferences") }
                TextButton(onClick = onBack) { Text("Back") }
            }
        }
        Text("Notifications are private to your PGR SIMS account.", style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
        if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
        message?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        if (!loading && rows.isEmpty()) Text("You have no notifications.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        rows.forEach { notification ->
            val id = notification.noticeNumber("id") ?: return@forEach
            val read = notification.noticeFlag("is_read")
            val target = notification.noticeChild("target")
            val kind = target?.noticeText("kind")
            val targetId = target?.noticeNumber("id")
            Card(
                Modifier.fillMaxWidth().clickable {
                    scope.launch { repository.markNotifications(listOf(id), true) }
                    if (!kind.isNullOrBlank()) onTarget(kind, targetId)
                },
                colors = if (read) CardDefaults.cardColors() else CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.secondaryContainer,
                ),
            ) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(notification.noticeText("title").ifBlank { "PGR SIMS update" }, fontWeight = FontWeight.SemiBold)
                    Text(notification.noticeText("body"), style = MaterialTheme.typography.bodyMedium)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(if (read) "Read" else "Unread", style = MaterialTheme.typography.bodySmall)
                        if (!kind.isNullOrBlank()) Text("Open ${InstitutionalLabels.humanize(kind)}", style = MaterialTheme.typography.bodySmall)
                        TextButton(onClick = {
                            scope.launch {
                                repository.markNotifications(listOf(id), !read)
                                rows = rows.map { if (it.noticeNumber("id") == id) it else it }
                                load()
                            }
                        }) { Text(if (read) "Mark unread" else "Mark read") }
                    }
                }
            }
        }
    }
    if (preferencesOpen) NotificationPreferencesDialog(repository) { preferencesOpen = false }
}

@Composable
private fun NotificationPreferencesDialog(repository: InstitutionalRepository, onDismiss: () -> Unit) {
    val scope = rememberCoroutineScope()
    var loading by remember { mutableStateOf(true) }
    var saving by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var email by remember { mutableStateOf(true) }
    var inApp by remember { mutableStateOf(true) }
    var push by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) {
        repository.notificationPreferences().fold(
            { value ->
                email = value.noticeFlag("email_enabled")
                inApp = value.noticeFlag("in_app_enabled")
                push = value.noticeFlag("push_enabled")
            },
            { error = it.message ?: "Could not load preferences." },
        )
        loading = false
    }
    AlertDialog(
        onDismissRequest = { if (!saving) onDismiss() },
        title = { Text("Notification preferences") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                if (loading) LinearProgressIndicator(Modifier.fillMaxWidth()) else {
                    PreferenceToggle("Email", email) { email = it }
                    PreferenceToggle("In-app inbox", inApp) { inApp = it }
                    PreferenceToggle("Push notifications", push, enabled = BuildConfig.FCM_ENABLED) { push = it }
                    if (!BuildConfig.FCM_ENABLED) Text("Push delivery is not enabled for this release.", style = MaterialTheme.typography.bodySmall)
                }
                error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            }
        },
        confirmButton = {
            TextButton(enabled = !loading && !saving, onClick = {
                saving = true
                scope.launch {
                    repository.updateNotificationPreferences(NotificationPreferencesPayload(email, inApp, push)).fold(
                        { onDismiss() }, { error = it.message ?: "Could not save preferences."; saving = false },
                    )
                }
            }) { Text(if (saving) "Saving…" else "Save") }
        },
        dismissButton = { TextButton(enabled = !saving, onClick = onDismiss) { Text("Cancel") } },
    )
}

@Composable
private fun PreferenceToggle(label: String, checked: Boolean, enabled: Boolean = true, onCheckedChange: (Boolean) -> Unit) {
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label)
        Switch(checked = checked, enabled = enabled, onCheckedChange = onCheckedChange)
    }
}
