package pk.vexel.pgrcompanion

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Groups
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

/**
 * Supervisor — LIMITED MVP (read-only): own info, assigned residents, per-workflow pending counts,
 * and a resident progress view. No approve/reject/revision actions here — see
 * docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md "Supervisor — LIMITED MVP" and
 * android/docs/SUPERVISOR_API_CAPABILITY_MATRIX.md for what is deferred and why.
 */

private fun JsonObject.text(key: String): String = string(key).orEmpty()
private fun JsonObject.number(key: String): Int? =
    runCatching { this[key]?.jsonPrimitive?.intOrNull }.getOrNull()
private fun JsonObject.child(key: String): JsonObject? =
    runCatching { this[key]?.jsonObject }.getOrNull()

private enum class SupervisorDestination(val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
    HOME("Home", Icons.Default.Home),
    RESIDENTS("Residents", Icons.Default.Groups),
    PROFILE("Profile", Icons.Default.Person),
}

private data class WorkflowPending(val title: String, val count: Int?, val workflow: SupervisorWorkflow?)

@Composable
private fun InstitutionalEmpty(text: String) {
    Text(text, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(vertical = 4.dp))
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
fun SupervisorPane(
    repository: InstitutionalRepository,
    snapshot: InstitutionalSnapshot?,
    busy: Boolean,
    onSignOut: () -> Unit,
    onRefresh: () -> Unit,
) {
    var destination by rememberSaveable { mutableStateOf(SupervisorDestination.HOME) }
    var selectedResidentId by rememberSaveable { mutableStateOf<Int?>(null) }
    var selectedWorkflow by rememberSaveable { mutableStateOf<SupervisorWorkflow?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("PGR Companion") },
                actions = { TextButton(onClick = onSignOut, enabled = !busy) { Text("Sign out") } },
            )
        },
        bottomBar = {
            NavigationBar {
                SupervisorDestination.entries.forEach { item ->
                    NavigationBarItem(
                        selected = destination == item && selectedResidentId == null && selectedWorkflow == null,
                        onClick = { destination = item; selectedResidentId = null; selectedWorkflow = null },
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
            if (busy) LinearProgressIndicator(Modifier.fillMaxWidth())

            val data = snapshot
            if (data == null) {
                Text("Loading your PGR SIMS record…", color = MaterialTheme.colorScheme.onSurfaceVariant)
                return@Column
            }

            val residentId = selectedResidentId
            val workflow = selectedWorkflow
            if (residentId != null) {
                SupervisorResidentDetailScreen(
                    repository = repository,
                    residentId = residentId,
                    onBack = { selectedResidentId = null },
                )
            } else if (workflow != null) {
                SupervisorWorkflowQueueScreen(
                    repository = repository,
                    workflow = workflow,
                    onBack = { selectedWorkflow = null },
                    onActioned = onRefresh,
                )
            } else when (destination) {
                SupervisorDestination.HOME -> SupervisorHomeContent(data) { selectedWorkflow = it }
                SupervisorDestination.RESIDENTS -> SupervisorResidentsContent(data) { selectedResidentId = it }
                SupervisorDestination.PROFILE -> SupervisorProfileContent(data, onSignOut, busy)
            }

            if (data.unavailable.isNotEmpty()) {
                Text(
                    "Not available to this account: ${data.unavailable.joinToString(", ")}.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            OutlinedButton(onClick = onRefresh, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Refresh") }
        }
    }
}

@Composable
private fun SupervisorHomeContent(data: InstitutionalSnapshot, onOpenWorkflow: (SupervisorWorkflow) -> Unit) {
    val me = data.me
    val summary = data.supervisorSummary
    val dashboard = data.supervisorDashboard
    val pending = summary?.child("pending")

    val residentsCount = dashboard?.number("assigned_residents_count")
        ?: summary?.objectList("residents")?.size ?: 0

    val workflows = listOf(
        WorkflowPending("Logbook", dashboard?.number("pending_logbook_reviews_count"), SupervisorWorkflow.LOGBOOK),
        WorkflowPending("Research / Synopsis", pending?.number("research_approvals"), SupervisorWorkflow.RESEARCH),
        WorkflowPending("Leave Requests", pending?.number("leave_approvals"), SupervisorWorkflow.LEAVE),
        WorkflowPending("Rotations", pending?.number("rotation_approvals"), SupervisorWorkflow.ROTATION),
        WorkflowPending("Evaluations", dashboard?.number("pending_evaluation_reviews_count"), null),
    )
    val totalPending = workflows.mapNotNull { it.count }.sum()

    Text("Welcome, ${me.text("username").ifBlank { "Supervisor" }}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
    Text("Your supervision queue at a glance", color = MaterialTheme.colorScheme.onSurfaceVariant)

    Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
        SupervisorStatCard("My Residents", residentsCount.toString(), Modifier.weight(1f))
        SupervisorStatCard("Pending Approvals", totalPending.toString(), Modifier.weight(1f))
    }

    Text("Workflows", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Card(Modifier.fillMaxWidth()) {
        Column {
            workflows.forEachIndexed { index, workflow ->
                if (index > 0) HorizontalDivider()
                Row(
                    Modifier.fillMaxWidth()
                        .then(if (workflow.workflow != null) Modifier.clickable { onOpenWorkflow(workflow.workflow) } else Modifier)
                        .padding(horizontal = 16.dp, vertical = 14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(workflow.title, fontWeight = FontWeight.SemiBold)
                    val count = workflow.count
                    Text(
                        if (count == null || count == 0) "No pending items" else "$count pending",
                        color = if (count != null && count > 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
    Text(
        "Tap a workflow to review and act on pending items.",
        style = MaterialTheme.typography.bodySmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
    )
}

@Composable
private fun SupervisorStatCard(label: String, value: String, modifier: Modifier = Modifier) {
    Card(modifier) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(value, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text(label, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun SupervisorResidentsContent(data: InstitutionalSnapshot, onOpenResident: (Int) -> Unit) {
    val residents = remember(data) { data.supervisorSummary?.objectList("residents").orEmpty() }
    var query by rememberSaveable { mutableStateOf("") }
    val filtered = remember(residents, query) {
        if (query.isBlank()) residents else residents.filter { it.text("name").contains(query, ignoreCase = true) }
    }

    Text("My Residents", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    OutlinedTextField(
        value = query,
        onValueChange = { query = it },
        modifier = Modifier.fillMaxWidth(),
        label = { Text("Search by name") },
        singleLine = true,
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
    )

    if (residents.isEmpty()) {
        InstitutionalEmpty("You have no assigned residents.")
        return
    }
    if (filtered.isEmpty()) {
        InstitutionalEmpty("No residents match \"$query\".")
        return
    }
    filtered.forEach { resident ->
        val id = resident.number("id")
        Card(
            Modifier.fillMaxWidth(),
        ) {
            Row(
                Modifier.fillMaxWidth()
                    .then(if (id != null) Modifier.clickable { onOpenResident(id) } else Modifier)
                    .padding(14.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(Modifier.weight(1f)) {
                    Text(resident.text("name").ifBlank { "Resident" }, fontWeight = FontWeight.SemiBold)
                    Text(resident.text("program").ifBlank { "Programme not recorded" }, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    resident.text("current_rotation").takeIf { it.isNotBlank() }?.let {
                        Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Column(horizontalAlignment = Alignment.End) {
                    resident.text("imm_status").takeIf { it.isNotBlank() }?.let { Text("IMM: ${humanizeStatus(it)}", style = MaterialTheme.typography.bodySmall) }
                    resident.text("final_status").takeIf { it.isNotBlank() }?.let { Text("Final: ${humanizeStatus(it)}", style = MaterialTheme.typography.bodySmall) }
                }
            }
        }
    }
}

@Composable
private fun SupervisorResidentDetailScreen(repository: InstitutionalRepository, residentId: Int, onBack: () -> Unit) {
    var progress by remember(residentId) { mutableStateOf<JsonObject?>(null) }
    var error by remember(residentId) { mutableStateOf<String?>(null) }
    var loading by remember(residentId) { mutableStateOf(true) }

    LaunchedEffect(residentId) {
        loading = true; error = null
        repository.supervisorResidentProgress(residentId).fold(
            { progress = it },
            { error = it.message ?: "Could not load this resident's progress." },
        )
        loading = false
    }

    TextButton(onClick = onBack) { Text("← Back to residents") }

    if (loading) {
        LinearProgressIndicator(Modifier.fillMaxWidth())
        return
    }
    error?.let {
        Text(it, color = MaterialTheme.colorScheme.error)
        return
    }
    val data = progress ?: return

    val resident = data.child("RESIDENT")
    Text(resident?.text("name").orEmpty().ifBlank { "Resident" }, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)

    val training = data.child("training_record")
    if (training != null) {
        Text("Training", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(training.text("program_name").ifBlank { training.text("program_code") }, fontWeight = FontWeight.SemiBold)
                Text("Degree: ${training.text("degree_type").ifBlank { "—" }}")
                Text("Induction: ${training.text("start_date").ifBlank { "—" }}")
                training.number("current_month_index")?.let { Text("Month $it of training") }
            }
        }
    }

    val rotation = data.child("current_rotation")
    Text("Current Posting", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            if (rotation == null) {
                Text("No active rotation on record.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                Text(rotation.text("department").ifBlank { "Department not recorded" }, fontWeight = FontWeight.SemiBold)
                Text(rotation.text("hospital").ifBlank { "Hospital not recorded" })
                Text("${rotation.text("start_date")} – ${rotation.text("end_date")}", style = MaterialTheme.typography.bodySmall)
            }
        }
    }

    Text("Progress", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            val research = data.child("research")
            Text("Research: ${humanizeStatus(research?.text("status").orEmpty()).ifBlank { "Not started" }}")
            research?.text("title")?.takeIf { it.isNotBlank() }?.let { Text(it, style = MaterialTheme.typography.bodySmall) }
            val thesis = data.child("thesis")
            Text("Thesis: ${humanizeStatus(thesis?.text("status").orEmpty()).ifBlank { "Not started" }}")
            val workshops = data.child("workshops")
            Text("Workshops completed: ${workshops?.number("total_completed") ?: 0}")
        }
    }

    val eligibility = data.child("eligibility")
    if (eligibility != null) {
        Text("Milestone Eligibility", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                eligibility.child("IMM")?.let { Text("IMM: ${humanizeStatus(it.text("status")).ifBlank { "—" }}") }
                eligibility.child("FINAL")?.let { Text("Final: ${humanizeStatus(it.text("status")).ifBlank { "—" }}") }
            }
        }
    }
}

@Composable
private fun SupervisorProfileContent(data: InstitutionalSnapshot, onSignOut: () -> Unit, busy: Boolean) {
    val me = data.me
    Text("Profile", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(me.text("username"), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("Role: Supervisor")
        }
    }
    Button(onClick = onSignOut, enabled = !busy) { Text("Sign out") }
    Disclaimer()
}

private fun humanizeStatus(value: String): String = InstitutionalLabels.humanize(value)
