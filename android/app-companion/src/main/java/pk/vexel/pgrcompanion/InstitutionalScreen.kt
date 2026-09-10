package pk.vexel.pgrcompanion

import android.content.Context
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.filled.Checklist
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.School
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
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
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import java.io.File

/**
 * The four states named in INSTITUTIONAL_WORKSPACE_ARCHITECTURE.md. An institutional failure is
 * confined to this screen: it can never stop the Personal Workspace from rendering.
 */
enum class InstitutionalState { DISCONNECTED, SIGNING_IN, CONNECTED, ERROR }

/** Mirrors [InstitutionalRepository.ALLOWED_UPLOAD_EXTENSIONS] so the picker cannot offer a reject. */
private val UPLOAD_MIME_TYPES = arrayOf(
    "application/pdf",
    "image/jpeg",
    "image/png",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)

private fun JsonObject.text(key: String): String = string(key).orEmpty()
private fun JsonObject.number(key: String): Int? =
    runCatching { this[key]?.jsonPrimitive?.intOrNull }.getOrNull()
private fun JsonObject.flag(key: String): Boolean =
    runCatching { this[key]?.jsonPrimitive?.booleanOrNull }.getOrNull() ?: false
private fun JsonObject.child(key: String): JsonObject? =
    runCatching { this[key]?.jsonObject }.getOrNull()

private fun humanize(value: String): String = InstitutionalLabels.humanize(value)

private enum class ResidentDestination(val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
    HOME("Home", Icons.Default.Home),
    TRAINING("Training", Icons.Default.School),
    LOGBOOK("Logbook", Icons.AutoMirrored.Filled.MenuBook),
    REQUIREMENTS("Requirements", Icons.Default.Checklist),
    PROFILE("Profile", Icons.Default.Person),
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
    var reloadKey by remember { mutableIntStateOf(0) }

    suspend fun reload() {
        busy = true
        repository.snapshot().fold(
            { snapshot = it; error = null; state = InstitutionalState.CONNECTED },
            { error = it.message ?: "Could not load your PGR SIMS information."; state = InstitutionalState.ERROR },
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

        InstitutionalState.CONNECTED -> if (snapshot?.me?.string("role") == "SUPERVISOR") SupervisorPane(
            repository = repository,
            snapshot = snapshot,
            busy = busy,
            onSignOut = { signOut() },
            onRefresh = { reloadKey++ },
        ) else ConnectedPane(
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
                        { notice = "Uploaded \"$name\". PGR SIMS will review it."; reloadKey++ },
                        { notice = it.message ?: "Upload failed." },
                    )
                }
            },
            onSaveField = { field, value ->
                scope.launch {
                    busy = true; notice = null
                    repository.update(mapOf(field to value)).fold(
                        { notice = "Saved to PGR SIMS."; reloadKey++ },
                        { notice = it.message ?: "Could not save that change."; busy = false },
                    )
                }
            },
            onCreateLogbook = { payload ->
                scope.launch {
                    busy = true; notice = null
                    repository.createLogbook(payload).fold(
                        { notice = "Logbook draft saved to PGR SIMS."; reloadKey++ },
                        { notice = it.message ?: "Could not save the logbook entry."; busy = false },
                    )
                }
            },
            onSubmitLogbook = { entryId ->
                scope.launch {
                    busy = true; notice = null
                    repository.submitLogbook(entryId).fold(
                        { notice = "Logbook entry submitted to PGR SIMS."; reloadKey++ },
                        { notice = it.message ?: "Could not submit the logbook entry."; busy = false },
                    )
                }
            },
            onUpdateLogbook = { entryId, payload ->
                scope.launch {
                    busy = true; notice = null
                    repository.updateLogbook(entryId, payload).fold(
                        { notice = "Logbook entry updated in PGR SIMS."; reloadKey++ },
                        { notice = it.message ?: "Could not update the logbook entry."; busy = false },
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
        Text("PGR Companion", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text(
            "Sign in with the PGR SIMS credentials provided for your residency account. Your records, " +
                "permissions, and completion status come from the server.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Your postgraduate residency workspace", color = MaterialTheme.colorScheme.onSurfaceVariant)
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
            "Your username and password are sent only to PGR SIMS over an encrypted " +
                "connection. They are never stored on this device; only an encrypted session is retained.",
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
        Text("PGR Companion", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color(0xFFFDECEA))) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("Server unavailable", fontWeight = FontWeight.Bold)
                Text(message.ifBlank { "Could not load your PGR SIMS information." })
            }
        }
        Text(
            "Check your connection and try again, or sign out and sign back in.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onRetry, enabled = !busy) { Text("Retry") }
            OutlinedButton(onClick = onSignOut, enabled = !busy) { Text("Sign out") }
        }
    }
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
private fun ConnectedPane(
    snapshot: InstitutionalSnapshot?,
    busy: Boolean,
    notice: String?,
    onSignOut: () -> Unit,
    onRefresh: () -> Unit,
    onNotice: (String) -> Unit,
    onUpload: (Int, Uri) -> Unit,
    onSaveField: (String, String) -> Unit,
    onCreateLogbook: (AcademicLogbookPayload) -> Unit,
    onSubmitLogbook: (Int) -> Unit,
    onUpdateLogbook: (Int, AcademicLogbookPayload) -> Unit,
) {
    val context = LocalContext.current
    var destination by rememberSaveable { mutableStateOf(ResidentDestination.HOME) }
    var targetDocument by remember { mutableStateOf<Int?>(null) }
    var confirmReplace by remember { mutableStateOf<Pair<Int, String>?>(null) }
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

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("PGR Companion") },
                actions = { TextButton(onClick = onSignOut, enabled = !busy) { Text("Sign out") } },
            )
        },
        bottomBar = {
            NavigationBar {
                ResidentDestination.entries.forEach { item ->
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
            Modifier.fillMaxSize().verticalScroll(rememberScrollState())
                .padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
        if (busy) LinearProgressIndicator(Modifier.fillMaxWidth())
        notice?.let {
            Card(Modifier.fillMaxWidth()) { Text(it, Modifier.padding(12.dp), style = MaterialTheme.typography.bodyMedium) }
        }

        val data = snapshot
        if (data == null) {
            Text("Loading your PGR SIMS record…", color = MaterialTheme.colorScheme.onSurfaceVariant)
            return@Column
        }

        val me = data.me
        val summary = remember(data) { OnboardingSummary.from(data.onboarding, data.documents) }
        if (destination == ResidentDestination.HOME) {
        Text("Welcome, ${me.text("username").ifBlank { "Resident" }}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text("Your residency at a glance", color = MaterialTheme.colorScheme.onSurfaceVariant)
        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color(0xFFE2F3F0))) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(me.text("username"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("Role: ${humanize(me.text("role").ifBlank { "unknown" })}")
                if (me.flag("must_change_password")) {
                    Text(
                        "A password change is required. Please use PGR SIMS on the web to set a new password.",
                        color = MaterialTheme.colorScheme.error,
                    )
                }
            }
        }

        // Spec 11.8: derived from the institution's own onboarding payload, never from local records.
        if (data.onboarding != null) {
            Text("Onboarding status", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    val review = summary.reviewStatus.ifBlank { me.text("onboarding_review_status") }
                    Text("Review: ${InstitutionalLabels.reviewStatus(review)}", fontWeight = FontWeight.SemiBold)
                    summary.reviewNote.takeIf { it.isNotBlank() }?.let {
                        Text("Reviewer note: $it", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                    }
                    Text("Profile: ${if (summary.profileComplete) "Complete" else "Incomplete"}")
                    Text("Declaration: ${if (summary.declarationAccepted) "Accepted" else "Not accepted"}")
                    Text("Supervisor: ${InstitutionalLabels.supervisorStatus(summary.supervisorStatus)}")
                    if (summary.onboardingComplete && !summary.hasOutstanding) {
                        Text("Your onboarding requirements are complete.")
                    } else {
                        Text("Outstanding requirements", fontWeight = FontWeight.SemiBold)
                        if (summary.outstanding.isEmpty()) {
                            Text("Nothing outstanding.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        } else {
                            summary.outstanding.forEach { Text("• $it", style = MaterialTheme.typography.bodySmall) }
                        }
                    }
                }
            }
        }

        DashboardSummary(data, summary, onOpenTraining = { destination = ResidentDestination.TRAINING })
        }

        if (destination == ResidentDestination.PROFILE) data.onboarding?.let { onboarding ->
            val sections = onboarding.objectList("sections")
            if (sections.isNotEmpty()) {
                Text("Profile", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text(
                    "These fields are defined and validated by PGR SIMS. Only details available " +
                        "for resident editing can be changed here.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                sections.forEach { section -> OnboardingSection(section, busy, onSaveField) }
            }
        }

        if (destination == ResidentDestination.TRAINING) TrainingDashboard(data)

        if (destination == ResidentDestination.LOGBOOK) LogbookScreen(data, busy, onCreateLogbook, onSubmitLogbook, onUpdateLogbook)

        if (destination == ResidentDestination.REQUIREMENTS) RequirementsScreen(data) {
        Text("Documents", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Text("Upload requested documents and follow review feedback.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        if (data.documents.isEmpty()) {
            InstitutionalEmpty("No document requirements are currently assigned to your account.")
        } else {
            data.documents.forEach { document ->
                val id = document.number("id")
                val status = document.text("status")
                val needsAction = InstitutionalLabels.documentNeedsAction(status)
                Card(Modifier.fillMaxWidth()) {
                    Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(document.text("title").ifBlank { "Required document" }, fontWeight = FontWeight.SemiBold)
                            Text(
                                InstitutionalLabels.documentStatus(status),
                                style = MaterialTheme.typography.bodySmall,
                                color = if (needsAction) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            document.text("original_filename").takeIf { it.isNotBlank() }?.let {
                                Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            // Spec 11.7: the reviewer's own words, shown against the requirement
                            // they belong to, are what makes a correction actionable.
                            document.text("verification_remarks").takeIf { it.isNotBlank() }?.let {
                                Text("Reviewer: $it", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                            }
                        }
                        if (id != null) {
                            TextButton(
                                enabled = !busy,
                                onClick = {
                                    // Replacing something already submitted or approved is an
                                    // explicit resubmission, never a silent overwrite.
                                    if (InstitutionalLabels.replacementNeedsConfirmation(status)) {
                                        confirmReplace = id to document.text("title").ifBlank { "this document" }
                                    } else {
                                        targetDocument = id
                                        picker.launch(UPLOAD_MIME_TYPES)
                                    }
                                },
                            ) { Text(InstitutionalLabels.documentAction(status)) }
                        }
                    }
                }
            }
        }
        confirmReplace?.let { (id, title) ->
            AlertDialog(
                onDismissRequest = { confirmReplace = null },
                title = { Text("Replace $title?") },
                text = {
                    Text(
                        "A copy of this document is already on record. Uploading a new file " +
                            "replaces it and sends it back for review."
                    )
                },
                confirmButton = {
                    TextButton(onClick = {
                        confirmReplace = null
                        targetDocument = id
                        picker.launch(UPLOAD_MIME_TYPES)
                    }) { Text("Choose a replacement") }
                },
                dismissButton = { TextButton(onClick = { confirmReplace = null }) { Text("Cancel") } },
            )
        }

        }

        if (data.unavailable.isNotEmpty()) {
            Text(
                "Not available to this account: ${data.unavailable.joinToString(", ")}.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }

        OutlinedButton(onClick = onRefresh, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Refresh") }
        Text(
            "Your residency information is securely managed by PGR SIMS. Signing out removes only " +
                "this device's encrypted session.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
    }
}

@Composable
private fun DashboardSummary(data: InstitutionalSnapshot, summary: OnboardingSummary, onOpenTraining: () -> Unit) {
    val approved = data.documents.count { it.text("status").uppercase() == "VERIFIED" }
    val underReview = data.documents.count { it.text("status").uppercase() in setOf("UPLOADED", "PENDING_REVIEW") }
    val actionNeeded = data.documents.count { InstitutionalLabels.documentNeedsAction(it.text("status")) }
    Text("Your progress", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            val actions = summary.outstanding.size
            Text(if (actions == 0) "Onboarding complete" else "$actions action${if (actions == 1) "" else "s"} remaining", fontWeight = FontWeight.SemiBold)
            Text(if (summary.profileComplete) "Profile complete" else "Profile needs attention")
            data.training.firstOrNull()?.let { training ->
                Text("Training: ${training.text("program_name").ifBlank { training.text("program_code").ifBlank { "Recorded" } }}")
            } ?: Text("Training: no active record")
            Text("Supervisor: ${InstitutionalLabels.supervisorStatus(summary.supervisorStatus)}")
            Text("Documents: ${data.documents.size} required · $approved approved · $underReview under review · $actionNeeded action required")
        }
    }
    CurrentTrainingCard(data, onOpenTraining)
}

@Composable
private fun OnboardingSection(section: JsonObject, busy: Boolean, onSave: (String, String) -> Unit) {
    val fields = section.objectList("fields")
    if (fields.isEmpty()) return
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(section.text("title").ifBlank { humanize(section.text("key")) }, fontWeight = FontWeight.SemiBold)
            fields.forEach { field ->
                val key = field.text("field")
                val label = field.text("label").ifBlank { humanize(key) }
                val required = field.flag("required")
                val original = field.text("value")
                val readOnlyReason = OnboardingFieldPolicy.readOnlyReason(key)
                if (readOnlyReason != null) {
                    // Rendered, not editable: these resolve server-side to a row id or an ISO date,
                    // so a text box here would show a database id and invite a damaging typo.
                    Column {
                        Text(if (required) "$label *" else label, style = MaterialTheme.typography.labelMedium)
                        Text(
                            OnboardingFieldPolicy.displayValue(key, original),
                            style = MaterialTheme.typography.bodyMedium,
                            color = if (required && original.isBlank()) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
                        )
                        Text(readOnlyReason, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                } else {
                    var value by remember(key, original) { mutableStateOf(original) }
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
}

@Composable
private fun InstitutionalEmpty(text: String) {
    Text(text, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(vertical = 4.dp))
}
