package pk.vexel.pgrcompanion

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.net.Uri
import android.os.*
import androidx.activity.ComponentActivity
import androidx.activity.compose.*
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import java.text.SimpleDateFormat
import java.util.*

private val Teal = Color(0xFF087F78)
private val Navy = Color(0xFF123047)

class MainActivity : ComponentActivity() {
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        if (Build.VERSION.SDK_INT >= 26) {
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(NotificationChannel("reminders", "Residency reminders", NotificationManager.IMPORTANCE_DEFAULT))
        }
        setContent { CompanionTheme { CompanionApp((application as CompanionApplication).store) } }
    }
}

@Composable private fun CompanionTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = lightColorScheme(primary = Teal, secondary = Color(0xFF4B6584), background = Color(0xFFF7FAF9), surface = Color.White, onSurface = Navy, onBackground = Navy), content = content)
}

private enum class Page { HOME, TRAINING, DOCUMENTS, PROFILE }

@Composable private fun CompanionApp(store: LocalStore) {
    var data by remember { mutableStateOf(store.read()) }
    var page by remember { mutableStateOf(Page.HOME) }
    fun save(next: AppData) { store.save(next); data = next }
    if (data.profile == null) Welcome { save(AppData(profile = it)) } else Scaffold(bottomBar = {
        NavigationBar { listOf(Page.HOME to "Home", Page.TRAINING to "Training", Page.DOCUMENTS to "Documents", Page.PROFILE to "Profile").forEach { (item, label) ->
            NavigationBarItem(page == item, { page = item }, { Icon(if (item == Page.HOME) Icons.Default.Home else if (item == Page.TRAINING) Icons.Default.Timeline else if (item == Page.DOCUMENTS) Icons.Default.Folder else Icons.Default.Person, label) }, label = { Text(label) })
        } }
    }) { padding -> Box(Modifier.padding(padding)) { when (page) { Page.HOME -> Home(data, { page = it }, ::save); Page.TRAINING -> Training(data, ::save); Page.DOCUMENTS -> Documents(data, ::save); Page.PROFILE -> Profile(data, store) { next -> save(next); page = if (next.profile == null) Page.HOME else Page.PROFILE } } } }
}

@Composable private fun Welcome(onSave: (ResidentProfile) -> Unit) {
    var form by remember { mutableStateOf(false) }
    if (!form) Column(Modifier.fillMaxSize().padding(28.dp).verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.Center) {
        Text("PGR Companion", style = MaterialTheme.typography.displaySmall, color = Teal, fontWeight = FontWeight.Bold)
        Text("Residency Portfolio", style = MaterialTheme.typography.headlineSmall, color = Navy)
        Spacer(Modifier.height(20.dp)); Text("Organize your postgraduate training, milestones, activities, documents and reminders in one private place.")
        Spacer(Modifier.height(12.dp)); Text("Works offline. Your information stays on this device. No account, institution or cloud connection is required.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        Spacer(Modifier.height(28.dp)); Button({ form = true }, Modifier.fillMaxWidth()) { Text("Create residency profile") }
        Spacer(Modifier.height(18.dp)); Disclaimer()
    } else ProfileForm(onSave)
}

@Composable private fun Disclaimer() { Text("PGR Companion is an independent productivity tool for postgraduate medical trainees. It is not affiliated with, endorsed by, or an official application of any university, regulatory authority, examination body, or government institution.", style = MaterialTheme.typography.bodySmall) }

@Composable private fun ProfileForm(onSave: (ResidentProfile) -> Unit) {
    var name by remember { mutableStateOf("") }; var institution by remember { mutableStateOf("") }; var programme by remember { mutableStateOf("") }; var specialty by remember { mutableStateOf("") }; var year by remember { mutableStateOf("") }; var supervisor by remember { mutableStateOf("") }
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Your residency profile", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold); Text("Only your name is needed to begin. You can add the rest later.")
        Field("Full name *", name) { name = it }; Field("Institution", institution) { institution = it }; Field("Programme (FCPS, MD, MS, or other)", programme) { programme = it }; Field("Specialty", specialty) { specialty = it }; Field("Current training year", year) { year = it }; Field("Supervisor", supervisor) { supervisor = it }
        Button(onClick = { onSave(ResidentProfile(name.trim(), institution, programme, specialty, trainingYear = year, supervisor = supervisor)) }, enabled = name.isNotBlank(), modifier = Modifier.fillMaxWidth()) { Text("Continue to Home") }
    }
}

@Composable private fun Home(data: AppData, onPage: (Page) -> Unit, save: (AppData) -> Unit) {
    val p = data.profile!!; var reminder by remember { mutableStateOf(false) }
    if (reminder) AddReminder({ save(data.copy(reminders = data.reminders + it)); reminder = false }) { reminder = false }
    LazyColumn(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item { Text("Good to see you, ${p.fullName.substringBefore(' ')}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold); Text("Your residency, organized privately.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
        item { Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color(0xFFE2F3F0))) { Column(Modifier.padding(18.dp)) { Text("Residency snapshot", fontWeight = FontWeight.Bold); Text(listOf(p.programme, p.specialty, p.institution).filter(String::isNotBlank).joinToString(" · ").ifBlank { "Add programme and institution in Profile" }); if (p.trainingYear.isNotBlank()) Text("Training year ${p.trainingYear}") } } }
        item { Text("Progress", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }
        item { Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) { Stat("Milestones", data.milestones.count { it.status == "Completed" }, data.milestones.size); Stat("Documents", data.documents.size); Stat("Activities", data.activities.size) } }
        item { Text("Quick actions", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }
        item { Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) { Action("Training", Icons.Default.AddTask) { onPage(Page.TRAINING) }; Action("Documents", Icons.Default.UploadFile) { onPage(Page.DOCUMENTS) }; Action("Reminder", Icons.Default.Notifications) { reminder = true } } }
        item { Text("Upcoming", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }
        item { val upcoming = data.reminders.filterNot { it.completed }.take(3) + data.milestones.filter { it.status != "Completed" }.take(3); if (upcoming.isEmpty()) Empty("Nothing scheduled yet. Add a milestone or reminder to keep your next step visible.") else upcoming.forEach { Text("• ${if (it is ReminderRecord) it.title else (it as Milestone).title}") } }
    }
}

@Composable private fun RowScope.Stat(label: String, value: Int, total: Int? = null) { Card(Modifier.weight(1f)) { Column(Modifier.padding(10.dp)) { Text("$value${if (total != null) "/$total" else ""}", style = MaterialTheme.typography.titleLarge, color = Teal, fontWeight = FontWeight.Bold); Text(label, style = MaterialTheme.typography.labelSmall) } } }
@Composable private fun RowScope.Action(label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, action: () -> Unit) { OutlinedButton(action, Modifier.weight(1f), contentPadding = PaddingValues(4.dp)) { Icon(icon, null, Modifier.size(18.dp)); Spacer(Modifier.width(2.dp)); Text(label, maxLines = 1) } }

@Composable private fun Training(data: AppData, save: (AppData) -> Unit) {
    var kind by remember { mutableStateOf<String?>(null) }; if (kind != null) AddTraining(kind!!, { r, a, m -> save(data.copy(rotations = data.rotations + listOfNotNull(r), activities = data.activities + listOfNotNull(a), milestones = data.milestones + listOfNotNull(m))); kind = null }) { kind = null }
    LazyColumn(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item { Text("Training", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold); Text("Build a timeline of the work that matters to you.") }
        item { Row(horizontalArrangement = Arrangement.spacedBy(5.dp)) { Button({ kind = "Rotation" }) { Text("Rotation") }; Button({ kind = "Activity" }) { Text("Activity") }; Button({ kind = "Milestone" }) { Text("Milestone") } } }
        item { Text("Rotations", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }; if (data.rotations.isEmpty()) item { Empty("No rotations recorded yet.") } else items(data.rotations) { r -> Record(r.title + " · " + r.status, listOf(r.unit, r.startDate, r.endDate).filter(String::isNotBlank).joinToString(" · ")) { save(data.copy(rotations = data.rotations - r)) } }
        item { Text("Activities", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }; if (data.activities.isEmpty()) item { Empty("No training activities recorded yet.") } else items(data.activities) { a -> Record(a.title, "${a.type}${if (a.date.isNotBlank()) " · ${a.date}" else ""}") { save(data.copy(activities = data.activities - a)) } }
        item { Text("Milestones", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }; if (data.milestones.isEmpty()) item { Empty("Track important steps in your postgraduate training.") } else items(data.milestones) { m -> Record(m.title, "${m.status}${if (m.dueDate.isNotBlank()) " · due ${m.dueDate}" else ""}", if (m.status != "Completed") "Complete" else null, { save(data.copy(milestones = data.milestones.map { if (it.id == m.id) it.copy(status = "Completed", completionDate = today()) else it })) }) { save(data.copy(milestones = data.milestones - m)) } }
    }
}

@Composable private fun Record(title: String, subtitle: String, action: String? = null, onAction: () -> Unit = {}, onDelete: () -> Unit) { Card(Modifier.fillMaxWidth()) { Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) { Column(Modifier.weight(1f)) { Text(title, fontWeight = FontWeight.SemiBold); if (subtitle.isNotBlank()) Text(subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }; if (action != null) TextButton(onAction) { Text(action) }; IconButton(onDelete) { Icon(Icons.Default.DeleteOutline, "Delete") } } } }
@Composable private fun Empty(text: String) { Text(text, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(vertical = 8.dp)) }

@Composable private fun Documents(data: AppData, save: (AppData) -> Unit) {
    val context = LocalContext.current; var query by remember { mutableStateOf("") }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri: Uri? -> if (uri != null) runCatching { val dir = context.filesDir.resolve("documents").apply { mkdirs() }; val file = dir.resolve("doc_${System.currentTimeMillis()}"); context.contentResolver.openInputStream(uri)!!.use { input -> file.outputStream().use(input::copyTo) }; save(data.copy(documents = data.documents + StoredDocument(title = "Residency document", category = "Other", filename = file.name, path = file.absolutePath, addedDate = today()))) } }
    Column(Modifier.fillMaxSize().padding(16.dp)) { Row(verticalAlignment = Alignment.CenterVertically) { Text("Document vault", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f)); FilledTonalButton({ picker.launch(arrayOf("application/pdf", "image/*")) }) { Icon(Icons.Default.Add, null); Text(" Add") } }; Text("Keep certificates, training letters and other residency documents organized here.", color = MaterialTheme.colorScheme.onSurfaceVariant); OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth().padding(vertical = 10.dp), label = { Text("Search documents") }, singleLine = true); val docs = data.documents.filter { it.title.contains(query, true) || it.category.contains(query, true) }; if (docs.isEmpty()) Empty("No documents stored yet.") else LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) { items(docs) { d -> Record(d.title, "${d.category} · ${d.addedDate}") { java.io.File(d.path).delete(); save(data.copy(documents = data.documents - d)) } } } }
}

@Composable private fun Profile(data: AppData, store: LocalStore, save: (AppData) -> Unit) { val context = LocalContext.current; var confirm by remember { mutableStateOf(false) }; if (confirm) AlertDialog(onDismissRequest = { confirm = false }, title = { Text("Delete all app data?") }, text = { Text("This permanently removes your profile, records, documents and reminders from this device.") }, confirmButton = { TextButton(onClick = { store.clear(context); save(AppData()); confirm = false }) { Text("Delete everything") } }, dismissButton = { TextButton(onClick = { confirm = false }) { Text("Cancel") } }); Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) { Text("Profile", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold); Text(data.profile!!.fullName, style = MaterialTheme.typography.titleLarge); Text(listOf(data.profile.institution, data.profile.programme, data.profile.specialty).filter(String::isNotBlank).joinToString(" · ")); Text("Your information is stored locally on this device. PGR Companion has no account, advertising, analytics, cloud sync, or institutional connection.", color = MaterialTheme.colorScheme.onSurfaceVariant); Disclaimer(); OutlinedButton(onClick = { confirm = true }, modifier = Modifier.fillMaxWidth()) { Icon(Icons.Default.DeleteForever, null); Spacer(Modifier.width(8.dp)); Text("Delete All App Data") }; Text("PGR Companion 1.0.0 · Vexel Consultants", style = MaterialTheme.typography.bodySmall) } }

@Composable private fun Field(label: String, value: String, change: (String) -> Unit) { OutlinedTextField(value, change, Modifier.fillMaxWidth(), label = { Text(label) }, singleLine = true) }
@Composable private fun AddTraining(kind: String, save: (Rotation?, ActivityRecord?, Milestone?) -> Unit, cancel: () -> Unit) { var title by remember { mutableStateOf("") }; var detail by remember { mutableStateOf("") }; var date by remember { mutableStateOf("") }; AlertDialog(onDismissRequest = cancel, title = { Text("Add $kind") }, text = { Column(verticalArrangement = Arrangement.spacedBy(8.dp)) { Field("Title", title) { title = it }; Field(if (kind == "Rotation") "Department / unit" else if (kind == "Activity") "Activity type" else "Category", detail) { detail = it }; Field("Date or due date", date) { date = it } } }, confirmButton = { TextButton(onClick = { if (title.isNotBlank()) when (kind) { "Rotation" -> save(Rotation(title = title, unit = detail, startDate = date), null, null); "Activity" -> save(null, ActivityRecord(type = detail.ifBlank { "Academic" }, title = title, date = date), null); else -> save(null, null, Milestone(title = title, category = detail.ifBlank { "General" }, dueDate = date)) } }) { Text("Save") } }, dismissButton = { TextButton(onClick = cancel) { Text("Cancel") } }) }
@Composable private fun AddReminder(save: (ReminderRecord) -> Unit, cancel: () -> Unit) { var title by remember { mutableStateOf("") }; var date by remember { mutableStateOf("") }; AlertDialog(onDismissRequest = cancel, title = { Text("Add reminder") }, text = { Column(verticalArrangement = Arrangement.spacedBy(8.dp)) { Field("Reminder", title) { title = it }; Field("Due date / time", date) { date = it } } }, confirmButton = { TextButton(onClick = { if (title.isNotBlank()) save(ReminderRecord(title = title, dueDate = date)) }) { Text("Save") } }, dismissButton = { TextButton(onClick = cancel) { Text("Cancel") } }) }
private fun today() = SimpleDateFormat("dd MMM yyyy", Locale.getDefault()).format(Date())
