package pk.vexel.pgrcompanion

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.booleanOrNull
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import java.io.File

/**
 * The four states named in INSTITUTIONAL_WORKSPACE_ARCHITECTURE.md. An institutional failure is
 * confined to this screen: it can never stop the Personal Workspace from rendering.
 */
enum class InstitutionalState { DISCONNECTED, SIGNING_IN, CONNECTED, ERROR }

private fun JsonObject.text(key: String): String = string(key).orEmpty()
private fun JsonObject.number(key: String): Int? =
    runCatching { this[key]?.jsonPrimitive?.intOrNull }.getOrNull()
private fun JsonObject.flag(key: String): Boolean =
    runCatching { this[key]?.jsonPrimitive?.booleanOrNull }.getOrNull() ?: false
private fun JsonObject.objects(key: String): List<JsonObject> =
    runCatching { this[key]?.jsonArray?.map { it.jsonObject } }.getOrNull().orEmpty()
private fun JsonObject.child(key: String): JsonObject? =
    runCatching { this[key]?.jsonObject }.getOrNull()

private fun humanize(value: String): String =
    value.replace('_', ' ').lowercase().replaceFirstChar { it.uppercase() }

/** The picker hands back a content Uri; the backend validates on the *filename*, so resolve it. */
internal fun displayNameOf(context: Context, uri: Uri): String {
    val resolved = runCatching {
        context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)
            ?.use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
    }.getOrNull()
    return resolved?.takeIf { it.isNotBlank() }
        ?: uri.lastPathSegment?.substringAfterLast('/').orEmpty().ifBlank { "document" }
}

@Composable
fun InstitutionalWorkspace(repository: InstitutionalRepository) {
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    var state by remember {
        mutableStateOf(
            if (repository.isConnected()) InstitutionalState.CONNECTED else InstitutionalState.DISCONNECTED
        )
    }
    var snapshot by remember { mutableStateOf<InstitutionalSnapshot?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    var notice by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var reloadKey by remember { mutableStateOf(0) }

    suspend fun reload() {
        busy = true
        repository.snapshot().fold(
            { snapshot = it; error = null; state = InstitutionalState.CONNECTED },
            { error = it.message ?: "Could not load institutional information."; state = InstitutionalState.ERROR },
        )
        busy = false
    }

    LaunchedEffect(reloadKey) {
        if (state == InstitutionalState.CONNECTED || state == InstitutionalState.ERROR) {
            if (repository.isConnected()) reload() else state = InstitutionalState.DISCONNECTED
        }
    }

    fun signOut() = scope.launch {
        busy = true
        repository.logout()
        snapshot = null; error = null; notice = null
        state = InstitutionalState.DISCONNECTED
        busy = false
    }

    when (state) {
        InstitutionalState.DISCONNECTED, InstitutionalState.SIGNING_IN -> SignInPane(
            signingIn = state == InstitutionalState.SIGNING_IN,
            error = error,
            onSignIn = { username, password ->
                scope.launch {
                    state = InstitutionalState.SIGNING_IN; error = null
                    repository.login(username, password).fold(
                        { state = InstitutionalState.CONNECTED; reloadKey++ },
                        { error = it.message ?: "Sign in failed."; state = InstitutionalState.DISCONNECTED },
                    )
                }
            },
        )

        InstitutionalState.ERROR -> ErrorPane(
            message = error.orEmpty(),
            busy = busy,
            onRetry = { reloadKey++ },
            onSignOut = { signOut() },
        )

        InstitutionalState.CONNECTED -> ConnectedPane(
            snapshot = snapshot,
            busy = busy,
            notice = notice,
            onSignOut = { signOut() },
            onRefresh = { reloadKey++ },
            onNotice = { notice = it },
            onUpload = { documentId, uri ->
                scope.launch {
                    busy = true; notice = null
                    val name = displayNameOf(context, uri)
                    val result = runCatching {
                        val staged = File(context.cacheDir, "institutional_upload_$name")
                        try {
                            context.contentResolver.openInputStream(uri)?.use { input ->
                                staged.outputStream().use(input::copyTo)
                            } ?: throw InstitutionalException("The selected file could not be opened.")
                            repository.upload(documentId, staged, name).getOrThrow()
                        } finally {
                            // Never leave institutional documents lying in the cache directory.
                            staged.delete()
                        }
                    }
                    busy = false
                    result.fold(
                        { notice = "Uploaded \"$name\". The institution will review it."; reloadKey++ },
                        { notice = it.message ?: "Upload failed." },
                    )
                }
            },
            onSaveField = { field, value ->
                scope.launch {
                    busy = true; notice = null
                    repository.update(mapOf(field to value)).fold(
                        { notice = "Saved to the institution."; reloadKey++ },
                        { notice = it.message ?: "Could not save that change."; busy = false },
                    )
                }
            },
        )
    }
}

@Composable
private fun SignInPane(signingIn: Boolean, error: String?, onSignIn: (String, String) -> Unit) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        Text("Institutional Workspace", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text(
            "Optional. Connect to your institution only if it issues you a PGR SIMS account. " +
                "Everything else in PGR Companion keeps working offline whether or not you sign in here.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Faisalabad Medical University", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                Text("PGR SIMS resident services", color = MaterialTheme.colorScheme.onSurfaceVariant)
                OutlinedTextField(
                    username, { username = it }, Modifier.fillMaxWidth(),
                    label = { Text("Username") }, singleLine = true, enabled = !signingIn,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text, imeAction = ImeAction.Next),
                )
                OutlinedTextField(
                    password, { password = it }, Modifier.fillMaxWidth(),
                    label = { Text("Password") }, singleLine = true, enabled = !signingIn,
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password, imeAction = ImeAction.Done),
                )
                Button(
                    onClick = { onSignIn(username, password) },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !signingIn && username.isNotBlank() && password.isNotBlank(),
                ) { Text(if (signingIn) "Signing in…" else "Sign in") }
                if (signingIn) LinearProgressIndicator(Modifier.fillMaxWidth())
            }
        }
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        Text(
            "Your username and password are sent only to your institution over an encrypted " +
                "connection. They are never stored on this device and never written into your " +
                "personal records.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Disclaimer()
    }
}

@Composable
private fun ErrorPane(message: String, busy: Boolean, onRetry: () -> Unit, onSignOut: () -> Unit) {
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        Text("Institutional Workspace", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color(0xFFFDECEA))) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("Institution unavailable", fontWeight = FontWeight.Bold)
                Text(message.ifBlank { "Could not load institutional information." })
            }
        }
        Text(
            "This affects the Institutional Workspace only. Your Home, Training, Documents and " +
                "Profile tabs are stored on this device and are unaffected.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onRetry, enabled = !busy) { Text("Retry") }
            OutlinedButton(onClick = onSignOut, enabled = !busy) { Text("Sign out") }
        }
    }
}

@Composable
private fun ConnectedPane(
    snapshot: InstitutionalSnapshot?,
    busy: Boolean,
    notice: String?,
    onSignOut: () -> Unit,
    onRefresh: () -> Unit,
    onNotice: (String) -> Unit,
    onUpload: (Int, Uri) -> Unit,
    onSaveField: (String, String) -> Unit,
) {
    val context = LocalContext.current
    var targetDocument by remember { mutableStateOf<Int?>(null) }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri: Uri? ->
        val id = targetDocument
        targetDocument = null
        if (uri == null || id == null) return@rememberLauncherForActivityResult
        val name = displayNameOf(context, uri)
        val size = runCatching {
            context.contentResolver.openAssetFileDescriptor(uri, "r")?.use { it.length }
        }.getOrNull() ?: -1L
        val problem = InstitutionalRepository.validateUpload(name, if (size >= 0) size else 1L)
        if (problem != null) onNotice(problem) else onUpload(id, uri)
    }

    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text("Institutional Workspace", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text("Faisalabad Medical University · PGR SIMS", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            TextButton(onClick = onSignOut, enabled = !busy) { Text("Sign out") }
        }
        if (busy) LinearProgressIndicator(Modifier.fillMaxWidth())
        notice?.let {
            Card(Modifier.fillMaxWidth()) { Text(it, Modifier.padding(12.dp), style = MaterialTheme.typography.bodyMedium) }
        }

        val data = snapshot
        if (data == null) {
            Text("Loading your institutional record…", color = MaterialTheme.colorScheme.onSurfaceVariant)
            return@Column
        }

        val me = data.me
        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color(0xFFE2F3F0))) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(me.text("username"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("Role: ${humanize(me.text("role").ifBlank { "unknown" })}")
                val review = me.text("onboarding_review_status").ifBlank { data.onboarding?.text("review_status").orEmpty() }
                if (review.isNotBlank()) Text("Institutional review: ${humanize(review)}")
                val pending = me.number("pending_upload_count") ?: 0
                if (pending > 0) Text("$pending document(s) awaiting your upload")
                if (me.flag("must_change_password")) {
                    Text(
                        "Your institution requires a password change. Please sign in on the PGR SIMS web portal to set a new password.",
                        color = MaterialTheme.colorScheme.error,
                    )
                }
            }
        }

        data.onboarding?.let { onboarding ->
            val sections = onboarding.objects("sections")
            if (sections.isNotEmpty()) {
                Text("Institutional profile", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text(
                    "These fields are defined and validated by your institution.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                sections.forEach { section -> OnboardingSection(section, busy, onSaveField) }
            }
        }

        Text("Programme and training", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        if (data.training.isEmpty()) {
            InstitutionalEmpty("No training record is recorded for you at this institution.")
        } else {
            data.training.forEach { record ->
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(14.dp)) {
                        Text(
                            record.text("program_name").ifBlank { record.text("program_code").ifBlank { "Training record" } },
                            fontWeight = FontWeight.SemiBold,
                        )
                        val detail = listOf(
                            record.text("current_level"),
                            record.text("start_date"),
                            record.text("expected_end_date").let { if (it.isBlank()) "" else "to $it" },
                        ).filter { it.isNotBlank() }.joinToString(" · ")
                        if (detail.isNotBlank()) {
                            Text(detail, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }

        Text("Supervisor", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        if (data.assignments.isEmpty()) {
            InstitutionalEmpty("No supervisor assignment is currently recorded at this institution.")
        } else {
            data.assignments.forEach { assignment ->
                val supervisor = assignment.child("supervisor")
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(14.dp)) {
                        Text(supervisor?.text("name").orEmpty().ifBlank { "Supervisor" }, fontWeight = FontWeight.SemiBold)
                        val detail = listOfNotNull(
                            supervisor?.text("designation"),
                            supervisor?.text("department"),
                            humanize(assignment.text("assignment_type")),
                        ).filter { it.isNotBlank() }.joinToString(" · ")
                        if (detail.isNotBlank()) {
                            Text(detail, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }

        Text("Required documents", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        if (data.documents.isEmpty()) {
            InstitutionalEmpty("Your institution has not requested any documents.")
        } else {
            data.documents.forEach { document ->
                val id = document.number("id")
                Card(Modifier.fillMaxWidth()) {
                    Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(document.text("title").ifBlank { "Required document" }, fontWeight = FontWeight.SemiBold)
                            Text(
                                humanize(document.text("status")),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            document.text("verification_remarks").takeIf { it.isNotBlank() }?.let {
                                Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                            }
                        }
                        if (id != null) {
                            TextButton(
                                enabled = !busy,
                                onClick = {
                                    targetDocument = id
                                    picker.launch(
                                        arrayOf(
                                            "application/pdf",
                                            "image/jpeg",
                                            "image/png",
                                            "application/msword",
                                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        )
                                    )
                                },
                            ) { Text("Upload") }
                        }
                    }
                }
            }
        }

        if (data.unavailable.isNotEmpty()) {
            Text(
                "Not available to this account: ${data.unavailable.joinToString(", ")}.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }

        OutlinedButton(onClick = onRefresh, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Refresh from institution") }
        Text(
            "Everything on this tab comes from your institution and is stored on their server, " +
                "not on this device. Your personal records in the other tabs are separate and are " +
                "never sent to your institution.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun OnboardingSection(section: JsonObject, busy: Boolean, onSave: (String, String) -> Unit) {
    val fields = section.objects("fields")
    if (fields.isEmpty()) return
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(section.text("title").ifBlank { humanize(section.text("key")) }, fontWeight = FontWeight.SemiBold)
            fields.forEach { field ->
                val key = field.text("field")
                val label = field.text("label").ifBlank { humanize(key) }
                val required = field.flag("required")
                var value by remember(key, field.text("value")) { mutableStateOf(field.text("value")) }
                val original = field.text("value")
                OutlinedTextField(
                    value = value,
                    onValueChange = { value = it },
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text(if (required) "$label *" else label) },
                    singleLine = true,
                    enabled = !busy,
                    isError = required && value.isBlank(),
                    trailingIcon = {
                        if (value != original) {
                            TextButton(onClick = { onSave(key, value) }, enabled = !busy) { Text("Save") }
                        }
                    },
                )
            }
        }
    }
}

@Composable
private fun InstitutionalEmpty(text: String) {
    Text(text, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(vertical = 4.dp))
}
