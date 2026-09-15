package pk.vexel.pgrcompanion

import android.content.Intent
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
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonObject

private val ADMIN_ROLES = listOf("ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF")

private enum class AdminDestination(val label: String, val icon: ImageVector) {
    HOME("Home", Icons.Default.Home), USERS("Users", Icons.Default.People),
    REPORTS("Reports", Icons.Default.Assessment), INBOX("Inbox", Icons.Default.Notifications), PROFILE("Profile", Icons.Default.Person),
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
                AdminDestination.INBOX -> NotificationCenterScreen(repository, { destination = AdminDestination.HOME }) { _, _ -> }
                AdminDestination.PROFILE -> {
                    OwnProfileEditor(repository, onRefresh)
                    Button(onClick = onChangePassword, modifier = Modifier.fillMaxWidth()) { Text("Change password") }
                }
            }
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
    rows.forEach { user -> Card(Modifier.fillMaxWidth().clickable { selected = user }) { Column(Modifier.padding(12.dp)) {
        Text(user.string("full_name").orEmpty().ifBlank { user.string("username").orEmpty() }, fontWeight = FontWeight.SemiBold)
        Text("${InstitutionalLabels.humanize(user.string("role").orEmpty())} · ${if (user.boolean("is_active")) "Active" else "Inactive"}")
    } } }
    if (next != null) OutlinedButton(onClick = { load(false) }, enabled = !loading, modifier = Modifier.fillMaxWidth()) { Text("Load more") }
    if (creating) CreateIdentityDialog(repository, { creating = false }) { load(true) }
    selected?.let { user -> AlertDialog(onDismissRequest = { selected = null }, title = { Text(user.string("full_name").orEmpty().ifBlank { "User details" }) }, text = { Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
        Text("Username: ${user.string("username").orEmpty()}"); Text("Role: ${InstitutionalLabels.humanize(user.string("role").orEmpty())}"); Text("Email: ${user.string("email").orEmpty().ifBlank { "—" }}")
    } }, confirmButton = { TextButton(onClick = { selected = null }) { Text("Close") } }) }
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
