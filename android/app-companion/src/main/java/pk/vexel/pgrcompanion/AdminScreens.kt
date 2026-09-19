package pk.vexel.pgrcompanion

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.People
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Assessment
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import java.io.File

private val ADMIN_ROLES = listOf("ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF")

private enum class AdminDestination(val label: String, val icon: ImageVector) {
    HOME("Home", Icons.Default.Home), USERS("Users", Icons.Default.People),
    REPORTS("Reports", Icons.Default.Assessment), SETUP("Setup", Icons.Default.Settings), IMPORTS("Import", Icons.Default.Settings), INBOX("Inbox", Icons.Default.Notifications), PROFILE("Profile", Icons.Default.Person),
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
internal fun AdminPane(
    repository: InstitutionalRepository,
    me: JsonObject,
    onSignOut: () -> Unit,
    onRefresh: () -> Unit,
    onChangePassword: () -> Unit,
) {
    var destination by rememberSaveable { mutableStateOf(AdminDestination.HOME) }
    Scaffold(
        topBar = { TopAppBar(title = { Text("PGR Companion Admin") }, actions = { TextButton(onClick = onSignOut) { Text("Sign out") } }) },
        bottomBar = {
            NavigationBar { AdminDestination.entries.forEach { item -> NavigationBarItem(destination == item, { destination = item }, { Icon(item.icon, item.label) }, label = { Text(item.label) }) } }
        },
    ) { padding ->
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(padding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            when (destination) {
                AdminDestination.HOME -> AdminDashboard(repository, onRefresh)
                AdminDestination.USERS -> AdminUserDirectory(repository)
                AdminDestination.REPORTS -> AdminReports(repository)
                AdminDestination.SETUP -> AdminSetup(repository)
                AdminDestination.IMPORTS -> AdminImportScreen(repository)
                AdminDestination.INBOX -> NotificationCenterScreen(repository, { destination = AdminDestination.HOME }) { _, _ -> }
                AdminDestination.PROFILE -> {
                    OwnProfileEditor(repository, onRefresh)
                    Button(onClick = onChangePassword, modifier = Modifier.fillMaxWidth()) { Text("Change password") }
                }
            }
        }
    }
}

private val BULK_IMPORT_LABELS = linkedMapOf(
    "residents" to "Residents", "supervisors" to "Supervisors", "supervision-links" to "Supervision links",
    "hospitals" to "Hospitals", "departments" to "Departments", "matrix" to "Hospital/department matrix",
    "training-programs" to "Training programs", "academic-sessions" to "Academic sessions",
    "rotation-templates" to "Rotation templates", "resident-training-records" to "Training records",
)

@Composable
private fun AdminImportScreen(repository: InstitutionalRepository) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var entity by rememberSaveable { mutableStateOf("residents") }
    var entityMenu by remember { mutableStateOf(false) }
    var selectedUri by remember { mutableStateOf<Uri?>(null) }
    var selectedName by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var dryRunPassed by remember { mutableStateOf(false) }
    var resultText by remember { mutableStateOf<String?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        selectedUri = uri
        selectedName = uri?.lastPathSegment?.substringAfterLast('/') ?: uri?.lastPathSegment
        dryRunPassed = false; resultText = null; error = null
    }
    fun runImport(action: String) {
        val uri = selectedUri ?: return
        scope.launch {
            busy = true; error = null
            val file = withContext(Dispatchers.IO) { copyImportToCache(context.cacheDir, context.contentResolver, uri, selectedName ?: "import.csv") }
            val result = file.fold(
                { repository.bulkImport(entity, action, it) },
                { Result.failure(it) },
            )
            file.getOrNull()?.delete()
            result.fold(
                { body -> resultText = importSummary(body); if (action == "dry-run") dryRunPassed = true },
                { error = it.message ?: "Could not ${if (action == "dry-run") "validate" else "apply"} this import." },
            )
            busy = false
        }
    }
    Text("Bulk import", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("Validate a CSV or Excel file before applying it. Imports are administrative writes and are never retried automatically.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    TextButton(onClick = { entityMenu = true }, enabled = !busy) { Text("Dataset: ${BULK_IMPORT_LABELS[entity]}") }
    DropdownMenu(expanded = entityMenu, onDismissRequest = { entityMenu = false }) {
        BULK_IMPORT_LABELS.forEach { (key, label) -> DropdownMenuItem(text = { Text(label) }, onClick = { entity = key; entityMenu = false; dryRunPassed = false; resultText = null }) }
    }
    OutlinedButton(onClick = { picker.launch(arrayOf("text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")) }, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text(selectedName?.let { "Selected: $it" } ?: "Choose CSV or Excel file") }
    Button(onClick = { runImport("dry-run") }, enabled = !busy && selectedUri != null, modifier = Modifier.fillMaxWidth()) { Text(if (busy) "Working…" else "Validate import") }
    OutlinedButton(onClick = { runImport("apply") }, enabled = !busy && selectedUri != null && dryRunPassed, modifier = Modifier.fillMaxWidth()) { Text("Apply validated import") }
    resultText?.let { Card(Modifier.fillMaxWidth()) { Text(it, Modifier.padding(12.dp)) } }
    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
}

private fun copyImportToCache(cacheDir: File, resolver: android.content.ContentResolver, uri: Uri, displayName: String): Result<File> = runCatching {
    val safeName = displayName.replace(Regex("[^A-Za-z0-9._-]"), "_").ifBlank { "import.csv" }
    File.createTempFile("pgr-import-", "-$safeName", cacheDir).also { target ->
        resolver.openInputStream(uri)?.use { input -> target.outputStream().use { input.copyTo(it) } }
            ?: throw InstitutionalException("The selected import file could not be opened.")
    }
}

private fun importSummary(body: JsonObject): String = body.entries.take(8).joinToString("\n") { (key, value) -> "${InstitutionalLabels.humanize(key)}: ${value.toString().trim('"')}" }

private enum class AdminFieldKind { TEXT, INTEGER, BOOLEAN, JSON, OPTION }

private data class AdminField(
    val key: String,
    val label: String,
    val kind: AdminFieldKind = AdminFieldKind.TEXT,
    val required: Boolean = false,
    val optionsKey: String? = null,
    val default: String = "",
)

private data class AdminCollection(
    val label: String,
    val path: String,
    val fields: List<AdminField>,
)

private val ADMIN_COLLECTIONS = listOf(
    AdminCollection("Document requirements", "resident-document-requirements", listOf(
        AdminField("display_name", "Display name", required = true),
        AdminField("document_type", "Document type", required = true),
        AdminField("stage", "Stage", default = "ONBOARDING"),
        AdminField("is_required", "Required", AdminFieldKind.BOOLEAN, default = "true"),
        AdminField("program", "Program", AdminFieldKind.OPTION, optionsKey = "programs"),
        AdminField("department", "Department", AdminFieldKind.OPTION, optionsKey = "departments"),
    )),
    AdminCollection("Supervision assignments", "supervision/assignments", listOf(
        AdminField("resident", "Resident", AdminFieldKind.OPTION, true, "residents"),
        AdminField("supervisor", "Supervisor", AdminFieldKind.OPTION, true, "supervisors"),
        AdminField("assignment_type", "Assignment type", required = true, default = "PRIMARY"),
        AdminField("start_date", "Start date (YYYY-MM-DD)", required = true),
        AdminField("notes", "Notes"),
    )),
    AdminCollection("Training records", "academics/training-records", listOf(
        AdminField("resident", "Resident", AdminFieldKind.OPTION, true, "residents"),
        AdminField("program", "Program", AdminFieldKind.OPTION, true, "programs"),
        AdminField("academic_session", "Academic session", AdminFieldKind.OPTION, true, "academic_sessions"),
        AdminField("training_site", "Training site", AdminFieldKind.OPTION, true, "training_sites"),
        AdminField("department", "Department", AdminFieldKind.OPTION, true, "departments"),
        AdminField("start_date", "Start date (YYYY-MM-DD)", required = true),
        AdminField("expected_end_date", "Expected end date (YYYY-MM-DD)"),
        AdminField("training_year", "Training year", AdminFieldKind.INTEGER, true),
        AdminField("notes", "Notes"),
    )),
    AdminCollection("Academic periods", "academics/periods", listOf(
        AdminField("name", "Name", required = true), AdminField("code", "Code", required = true),
        AdminField("academic_session", "Academic session", AdminFieldKind.OPTION, true, "academic_sessions"),
        AdminField("start_date", "Start date (YYYY-MM-DD)", required = true),
        AdminField("end_date", "End date (YYYY-MM-DD)", required = true),
        AdminField("period_type", "Period type", required = true, default = "ROTATION"),
        AdminField("sort_order", "Sort order", AdminFieldKind.INTEGER, default = "0"),
    )),
    AdminCollection("Rotation templates", "academics/rotation-templates", listOf(
        AdminField("name", "Name", required = true), AdminField("code", "Code", required = true),
        AdminField("program", "Program", AdminFieldKind.OPTION, true, "programs"),
        AdminField("department", "Department", AdminFieldKind.OPTION, true, "departments"),
        AdminField("training_year", "Training year", AdminFieldKind.INTEGER, true),
        AdminField("duration_weeks", "Duration (weeks)", AdminFieldKind.INTEGER, true),
        AdminField("is_required", "Required", AdminFieldKind.BOOLEAN, default = "true"),
    )),
    AdminCollection("Evaluation templates", "academics/evaluation-templates", listOf(
        AdminField("name", "Name", required = true), AdminField("code", "Code", required = true),
        AdminField("program", "Program", AdminFieldKind.OPTION, true, "programs"),
        AdminField("department", "Department", AdminFieldKind.OPTION, true, "departments"),
        AdminField("form_type", "Form type", required = true, default = "MINI_CEX"),
        AdminField("schema", "Field schema (JSON)", AdminFieldKind.JSON, true, default = "{\"fields\":[]}"),
    )),
    AdminCollection("Logbook categories", "academics/logbook-categories", listOf(
        AdminField("name", "Name", required = true), AdminField("code", "Code", required = true),
        AdminField("program", "Program", AdminFieldKind.OPTION, true, "programs"),
        AdminField("department", "Department", AdminFieldKind.OPTION, true, "departments"),
        AdminField("category_type", "Category type", required = true, default = "CLINICAL"),
        AdminField("minimum_required", "Minimum required", AdminFieldKind.INTEGER, default = "0"),
    )),
    AdminCollection("Review queue", "academics/review-queue", listOf(
        AdminField("resident", "Resident", AdminFieldKind.OPTION, true, "residents"),
        AdminField("supervisor", "Supervisor", AdminFieldKind.OPTION, true, "supervisors"),
        AdminField("queue_type", "Queue type", required = true, default = "EVALUATION_REVIEW"),
        AdminField("due_date", "Due date (YYYY-MM-DD)"), AdminField("notes", "Notes"),
    )),
)

@Composable
private fun AdminSetup(repository: InstitutionalRepository) {
    var loading by remember { mutableStateOf(true) }
    var sections by remember { mutableStateOf<List<Pair<String, Result<List<JsonObject>>>>>(emptyList()) }
    var options by remember { mutableStateOf<JsonObject?>(null) }
    var pendingSupervisorLinks by remember { mutableStateOf<List<JsonObject>>(emptyList()) }
    var createFor by remember { mutableStateOf<AdminCollection?>(null) }
    var resolvingPending by remember { mutableStateOf<JsonObject?>(null) }
    var reloadKey by remember { mutableIntStateOf(0) }
    LaunchedEffect(reloadKey) {
        sections = repository.adminSetup()
        repository.academicOptions().getOrNull()?.let { options = it }
        repository.pendingSupervisorLinks().getOrNull()?.let { pendingSupervisorLinks = it }
        loading = false
    }
    Text("Academic and supervision setup", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("Canonical administrative records. Changes remain governed by backend permissions and audits.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
    if (pendingSupervisorLinks.isNotEmpty()) {
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("Pending supervisor links", fontWeight = FontWeight.SemiBold)
                pendingSupervisorLinks.forEach { link ->
                    Text("${link.string("resident") ?: "Resident"} → ${link.string("supervisor_name") ?: "Requested supervisor"}")
                    OutlinedButton(onClick = { resolvingPending = link }, modifier = Modifier.fillMaxWidth()) { Text("Resolve link") }
                }
            }
        }
    }
    sections.forEach { (label, result) ->
        val collection = ADMIN_COLLECTIONS.firstOrNull { it.label == label }
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(label, fontWeight = FontWeight.SemiBold)
                result.fold(
                    { rows ->
                        Text("${rows.size} records loaded")
                        rows.take(3).forEach { row ->
                            val title = row.string("name") ?: row.string("title") ?: row.string("code") ?: row.string("id") ?: "Record"
                            Text("• $title", style = MaterialTheme.typography.bodySmall)
                        }
                    },
                    { error -> Text(error.message ?: "Unavailable.", color = MaterialTheme.colorScheme.error) },
                )
                collection?.let { supported ->
                    OutlinedButton(onClick = { createFor = supported }, modifier = Modifier.fillMaxWidth()) { Text("Add ${supported.label.removeSuffix("s")}") }
                }
            }
        }
    }
    createFor?.let { collection ->
        AdminCreateDialog(
            collection = collection,
            options = options,
            repository = repository,
            onDismiss = { createFor = null },
            onCreated = { createFor = null; loading = true; reloadKey++ },
        )
    }
    resolvingPending?.let { pending ->
        ResolvePendingSupervisorDialog(
            pending = pending,
            options = options,
            repository = repository,
            onDismiss = { resolvingPending = null },
            onResolved = { resolvingPending = null; loading = true; reloadKey++ },
        )
    }
}

@Composable
private fun ResolvePendingSupervisorDialog(
    pending: JsonObject,
    options: JsonObject?,
    repository: InstitutionalRepository,
    onDismiss: () -> Unit,
    onResolved: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    val supervisors = options?.objectList("supervisors").orEmpty()
    var selectedSupervisorId by remember { mutableStateOf<String?>(null) }
    var expanded by remember { mutableStateOf(false) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    val pendingId = pending.string("id")?.toIntOrNull()
    val selected = supervisors.firstOrNull { it.string("id") == selectedSupervisorId }
    AlertDialog(
        onDismissRequest = { if (!busy) onDismiss() },
        title = { Text("Resolve supervisor link") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Resident: ${pending.string("resident") ?: "—"}")
                Text("Requested: ${pending.string("supervisor_name") ?: "—"}")
                TextButton(onClick = { expanded = true }, enabled = !busy && supervisors.isNotEmpty()) { Text("Supervisor: ${selected?.string("name") ?: "Select"}") }
                DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                    supervisors.forEach { supervisor -> DropdownMenuItem(text = { Text(supervisor.string("name") ?: supervisor.string("username") ?: "Supervisor") }, onClick = { selectedSupervisorId = supervisor.string("id"); expanded = false }) }
                }
                if (supervisors.isEmpty()) Text("No active supervisors are available.", color = MaterialTheme.colorScheme.error)
                error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            }
        },
        confirmButton = { TextButton(onClick = {
            busy = true; error = null
            scope.launch {
                repository.resolvePendingSupervisor(pendingId!!, selectedSupervisorId!!.toInt()).fold(
                    { onResolved() }, { error = it.message ?: "Could not resolve this link."; busy = false },
                )
            }
        }, enabled = !busy && pendingId != null && selectedSupervisorId != null) { Text(if (busy) "Resolving…" else "Resolve") } },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") } },
    )
}

@Composable
private fun AdminCreateDialog(
    collection: AdminCollection,
    options: JsonObject?,
    repository: InstitutionalRepository,
    onDismiss: () -> Unit,
    onCreated: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    val values = remember(collection.path) { mutableStateMapOf<String, String>().apply { collection.fields.forEach { put(it.key, it.default) } } }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    AlertDialog(
        onDismissRequest = { if (!busy) onDismiss() },
        title = { Text("Add ${collection.label}") },
        text = {
            Column(Modifier.verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Values are sent only to the canonical PGR SIMS ${collection.label.lowercase()} API.", style = MaterialTheme.typography.bodySmall)
                collection.fields.forEach { field ->
                    when (field.kind) {
                        AdminFieldKind.BOOLEAN -> TextButton(onClick = { values[field.key] = (!(values[field.key]?.toBooleanStrictOrNull() ?: false)).toString() }) { Text("${field.label}: ${if (values[field.key]?.toBooleanStrictOrNull() == true) "Yes" else "No"}") }
                        AdminFieldKind.OPTION -> AdminOptionField(field, values, options, busy)
                        else -> OutlinedTextField(
                            value = values[field.key].orEmpty(), onValueChange = { values[field.key] = it }, modifier = Modifier.fillMaxWidth(),
                            label = { Text(field.label + if (field.required) " *" else "") }, enabled = !busy,
                            keyboardOptions = KeyboardOptions(keyboardType = if (field.kind == AdminFieldKind.INTEGER) KeyboardType.Number else KeyboardType.Text),
                        )
                    }
                }
                error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            }
        },
        confirmButton = {
            TextButton(onClick = {
                val payload = runCatching { adminPayload(collection.fields, values) }
                if (payload.isFailure) { error = payload.exceptionOrNull()?.message; return@TextButton }
                busy = true; error = null
                scope.launch {
                    repository.adminCreate(collection.path, payload.getOrThrow(), collection.label).fold(
                        { onCreated() }, { error = it.message ?: "Could not create this record."; busy = false },
                    )
                }
            }, enabled = !busy) { Text(if (busy) "Saving…" else "Save") }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") } },
    )
}

@Composable
private fun AdminOptionField(field: AdminField, values: MutableMap<String, String>, options: JsonObject?, busy: Boolean) {
    var expanded by remember(field.key) { mutableStateOf(false) }
    val rows = options?.objectList(field.optionsKey.orEmpty()).orEmpty()
    val selected = rows.firstOrNull { it.string("id") == values[field.key] }
    TextButton(onClick = { expanded = true }, enabled = !busy && rows.isNotEmpty()) { Text("${field.label}${if (field.required) " *" else ""}: ${selected?.string("name") ?: "Select"}") }
    DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
        rows.forEach { row -> DropdownMenuItem(text = { Text(row.string("name") ?: row.string("username") ?: "Record ${row.string("id")}") }, onClick = { values[field.key] = row.string("id").orEmpty(); expanded = false }) }
    }
    if (rows.isEmpty()) Text("No ${field.label.lowercase()} options are available.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
}

private fun adminPayload(fields: List<AdminField>, values: Map<String, String>): JsonObject = buildJsonObject {
    fields.forEach { field ->
        val value = values[field.key].orEmpty().trim()
        if (field.required && value.isBlank()) error("${field.label} is required.")
        if (value.isBlank()) return@forEach
        when (field.kind) {
            AdminFieldKind.INTEGER, AdminFieldKind.OPTION -> put(field.key, value.toIntOrNull() ?: error("${field.label} must be a valid number."))
            AdminFieldKind.BOOLEAN -> put(field.key, value.toBooleanStrictOrNull() ?: error("${field.label} must be Yes or No."))
            AdminFieldKind.JSON -> put(field.key, Json.parseToJsonElement(value))
            AdminFieldKind.TEXT -> put(field.key, JsonPrimitive(value))
        }
    }
}

@Composable
private fun AdminReports(repository: InstitutionalRepository) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var loading by remember { mutableStateOf(true) }
    var reports by remember { mutableStateOf<List<Pair<String, Result<JsonObject>>>>(emptyList()) }
    LaunchedEffect(Unit) {
        reports = repository.adminReports()
        loading = false
    }
    Text("Reports", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("Canonical administrative summaries from PGR SIMS.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
    reports.forEach { (label, result) ->
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(label, fontWeight = FontWeight.SemiBold)
                result.fold(
                    { body -> Text(reportSummary(body)) },
                    { error -> Text(error.message ?: "Report unavailable.", color = MaterialTheme.colorScheme.error) },
                )
                var exporting by remember(label) { mutableStateOf(false) }
                var exportError by remember(label) { mutableStateOf<String?>(null) }
                OutlinedButton(
                    onClick = {
                        exporting = true
                        exportError = null
                        scope.launch {
                            repository.adminReportCsv(label).fold(
                                { csv ->
                                    context.startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                                        type = "text/csv"
                                        putExtra(Intent.EXTRA_SUBJECT, "$label report")
                                        putExtra(Intent.EXTRA_TEXT, csv)
                                    }, "Share $label CSV"))
                                    exporting = false
                                },
                                { exportError = it.message ?: "Export unavailable."; exporting = false },
                            )
                        }
                    },
                    enabled = !exporting,
                ) { Text(if (exporting) "Preparing…" else "Export CSV") }
                exportError?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            }
        }
    }
}

private fun reportSummary(body: JsonObject): String {
    val summary = body["summary"]?.jsonObject ?: body["workload"]?.jsonObject ?: body
    return summary.entries.filter { it.value is kotlinx.serialization.json.JsonPrimitive }
        .take(6).joinToString(" · ") { (key, value) -> "${InstitutionalLabels.humanize(key)}: ${value.toString().trim('"')}" }
        .ifBlank { "Report loaded successfully." }
}

@Composable
private fun AdminDashboard(repository: InstitutionalRepository, onRefresh: () -> Unit) {
    var total by remember { mutableIntStateOf(0) }
    var active by remember { mutableIntStateOf(0) }
    var loading by remember { mutableStateOf(true) }
    var error by remember { mutableStateOf<String?>(null) }
    var overview by remember { mutableStateOf<JsonObject?>(null) }
    LaunchedEffect(Unit) {
        repository.users(page = 1).fold({ total = it.count }, { error = it.message })
        repository.users(page = 1, active = true).fold({ active = it.count }, { error = it.message })
        repository.adminWorkflowOverview().fold({ overview = it }, { error = it.message })
        loading = false
    }
    Text("Administration", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
    Text("Canonical identity totals from PGR SIMS.")
    if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
    Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
        AdminStat("All users", total, Modifier.weight(1f)); AdminStat("Active", active, Modifier.weight(1f))
    }
    val cards = overview?.get("cards")?.jsonObject
    if (cards != null) {
        Text("Academic and supervision overview", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            AdminOverviewRow("Active training records", cards.string("active_training_records"))
            AdminOverviewRow("Residents without training record", cards.string("residents_without_training_record"))
            AdminOverviewRow("Residents without primary supervisor", cards.string("residents_without_primary_supervisor"))
            AdminOverviewRow("Pending review items", cards.string("pending_review_items"))
        }
    }
    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    OutlinedButton(onClick = onRefresh, modifier = Modifier.fillMaxWidth()) { Text("Refresh account") }
}

@Composable
private fun AdminOverviewRow(label: String, value: String?) {
    Card(Modifier.fillMaxWidth()) {
        Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.SpaceBetween) {
            Text(label)
            Text(value ?: "—", fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
private fun AdminStat(label: String, count: Int, modifier: Modifier) = Card(modifier) {
    Column(Modifier.padding(16.dp)) { Text(count.toString(), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold); Text(label) }
}

@Composable
private fun AdminUserDirectory(repository: InstitutionalRepository) {
    val scope = rememberCoroutineScope()
    var page by remember { mutableIntStateOf(1) }
    var rows by remember { mutableStateOf<List<JsonObject>>(emptyList()) }
    var total by remember { mutableIntStateOf(0) }
    var next by remember { mutableStateOf<String?>(null) }
    var query by rememberSaveable { mutableStateOf("") }
    var role by rememberSaveable { mutableStateOf<String?>(null) }
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var creating by remember { mutableStateOf(false) }
    var selected by remember { mutableStateOf<JsonObject?>(null) }
    var detail by remember { mutableStateOf<JsonObject?>(null) }
    var detailError by remember { mutableStateOf<String?>(null) }

    fun load(reset: Boolean) = scope.launch {
        loading = true; error = null
        val requestedPage = if (reset) 1 else page
        repository.users(requestedPage, role, query).fold(
            { result -> rows = if (reset) result.results else rows + result.results; total = result.count; next = result.next; page = requestedPage + 1 },
            { error = it.message ?: "Could not load users." },
        )
        loading = false
    }
    LaunchedEffect(role) { load(true) }
    Text("User and role directories", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("$total matching identities")
    OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth(), label = { Text("Search name, username or email") }, singleLine = true)
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Button(onClick = { load(true) }, enabled = !loading) { Text("Search") }
        Button(onClick = { creating = true }, enabled = !loading) { Text("Create user") }
    }
    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        listOf<String?>(null, *ADMIN_ROLES.toTypedArray()).forEach { value -> TextButton(onClick = { role = value }) { Text(value?.let(InstitutionalLabels::humanize) ?: "All") } }
    }
    if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    rows.forEach { user -> Card(Modifier.fillMaxWidth().clickable { selected = user; detail = null; detailError = null }) { Column(Modifier.padding(12.dp)) {
        Text(user.string("full_name").orEmpty().ifBlank { user.string("username").orEmpty() }, fontWeight = FontWeight.SemiBold)
        Text("${InstitutionalLabels.humanize(user.string("role").orEmpty())} · ${if (user.boolean("is_active")) "Active" else "Inactive"}")
    } } }
    if (next != null) OutlinedButton(onClick = { load(false) }, enabled = !loading, modifier = Modifier.fillMaxWidth()) { Text("Load more") }
    if (creating) CreateIdentityDialog(repository, { creating = false }) { load(true) }
    selected?.let { user ->
        val id = user.string("id")?.toIntOrNull()
        LaunchedEffect(id) {
            if (id != null) repository.userDetail(id).fold({ detail = it }, { detailError = it.message ?: "Could not load user details." })
        }
        val shown = detail ?: user
        AlertDialog(onDismissRequest = { selected = null }, title = { Text(shown.string("full_name").orEmpty().ifBlank { "User details" }) }, text = { Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
            if (detail == null && detailError == null) LinearProgressIndicator(Modifier.fillMaxWidth())
            Text("Username: ${shown.string("username").orEmpty()}")
            Text("Role: ${InstitutionalLabels.humanize(shown.string("role").orEmpty())}")
            Text("Email: ${shown.string("email").orEmpty().ifBlank { "—" }}")
            Text("Phone: ${shown.string("phone").orEmpty().ifBlank { "—" }}")
            Text("Status: ${if (shown.boolean("is_active")) "Active" else "Inactive"}")
            shown.string("profile_type")?.let { Text("Profile: ${InstitutionalLabels.humanize(it)}") }
            detailError?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        } }, confirmButton = { TextButton(onClick = { selected = null }) { Text("Close") } })
    }
}

@Composable
private fun CreateIdentityDialog(repository: InstitutionalRepository, onDismiss: () -> Unit, onCreated: () -> Unit) {
    val scope = rememberCoroutineScope()
    var fullName by remember { mutableStateOf("") }; var email by remember { mutableStateOf("") }; var phone by remember { mutableStateOf("") }
    var role by remember { mutableStateOf("RESIDENT") }; var roleMenu by remember { mutableStateOf(false) }; var busy by remember { mutableStateOf(false) }; var error by remember { mutableStateOf<String?>(null) }
    AlertDialog(onDismissRequest = { if (!busy) onDismiss() }, title = { Text("Create PGR SIMS identity") }, text = { Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        TextButton(onClick = { roleMenu = true }, enabled = !busy) { Text("Role: ${InstitutionalLabels.humanize(role)}") }
        DropdownMenu(expanded = roleMenu, onDismissRequest = { roleMenu = false }) { ADMIN_ROLES.forEach { option -> DropdownMenuItem(text = { Text(InstitutionalLabels.humanize(option)) }, onClick = { role = option; roleMenu = false }) } }
        OutlinedTextField(fullName, { fullName = it }, Modifier.fillMaxWidth(), label = { Text("Full name *") }, enabled = !busy)
        OutlinedTextField(email, { email = it }, Modifier.fillMaxWidth(), label = { Text("Email") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email), enabled = !busy)
        OutlinedTextField(phone, { phone = it }, Modifier.fillMaxWidth(), label = { Text("Phone") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone), enabled = !busy)
        Text("PGR SIMS will generate the role-prefixed username and apply the temporary-password/onboarding policy.", style = MaterialTheme.typography.bodySmall)
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    } }, confirmButton = { TextButton(onClick = { busy = true; scope.launch { repository.createUser(UniversalUserPayload(role, fullName, email, phone)).fold({ onCreated(); onDismiss() }, { error = it.message; busy = false }) } }, enabled = !busy && fullName.isNotBlank()) { Text(if (busy) "Creating…" else "Create") } }, dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") } })
}
