package pk.vexel.pgrportal

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.booleanOrNull
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

private fun JsonObject.value(key: String): String = string(key).orEmpty()
private fun JsonObject.idValue(): Int? = runCatching { this["id"]?.jsonPrimitive?.intOrNull }.getOrNull()
private fun JsonObject.objectValue(key: String): JsonObject? = runCatching { this[key]?.jsonObject }.getOrNull()
private fun JsonObject.boolValue(key: String): Boolean =
    runCatching { this[key]?.jsonPrimitive?.booleanOrNull }.getOrNull() ?: false

internal fun residentStatus(value: String): String = when (value.uppercase()) {
    "DRAFT" -> "Draft"
    "SUBMITTED" -> "Submitted"
    "RETURNED", "CORRECTION_REQUIRED", "REUPLOAD_REQUIRED" -> "Correction required"
    "APPROVED", "VERIFIED" -> "Approved"
    "ACTIVE" -> "Active"
    "COMPLETED" -> "Completed"
    "PENDING_REVIEW", "UNDER_REVIEW" -> "Under review"
    "REJECTED" -> "Rejected"
    "CANCELLED" -> "Cancelled"
    "NOT_STARTED" -> "Not started"
    "IN_PROGRESS" -> "In progress"
    else -> value.replace('_', ' ').lowercase().replaceFirstChar { it.titlecase() }
}

@Composable
internal fun CurrentTrainingCard(data: InstitutionalSnapshot, onOpenTraining: () -> Unit) {
    val rotation = data.residentSummary?.objectValue("current_rotation")
    Card(Modifier.fillMaxWidth().clickable(onClick = onOpenTraining)) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text("Current training", fontWeight = FontWeight.SemiBold)
            data.training.firstOrNull()?.let {
                Text(it.value("program_name").ifBlank { it.value("program_code") })
            }
            if (rotation == null) {
                Text("No active rotation is currently assigned to your training record.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                Text(rotation.value("department").ifBlank { "Current rotation" }, style = MaterialTheme.typography.titleMedium)
                val period = listOf(rotation.value("start_date"), rotation.value("end_date")).filter { it.isNotBlank() }.joinToString(" – ")
                if (period.isNotBlank()) Text(period, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(residentStatus(rotation.value("status")), color = MaterialTheme.colorScheme.primary)
            }
            Text("View training", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
internal fun TrainingDashboard(data: InstitutionalSnapshot) {
    var detail by remember { mutableStateOf<JsonObject?>(null) }
    Text("Training", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    data.training.firstOrNull()?.let { record ->
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("Programme", fontWeight = FontWeight.SemiBold)
                Text(record.value("program_name").ifBlank { record.value("program_code").ifBlank { "Training record" } }, style = MaterialTheme.typography.titleMedium)
                detailLines(
                    "Current stage" to record.value("current_level"),
                    "Training start" to record.value("start_date"),
                    "Expected completion" to record.value("expected_end_date"),
                )
            }
        }
    } ?: ResidentEmpty("No training record is currently available for your account.")

    Text("Current rotation", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    val current = data.residentSummary?.objectValue("current_rotation")
    if (current == null) ResidentEmpty("No active rotation is currently assigned to your training record.")
    else RotationCard(current, true) { detail = current }

    Text("Rotation history", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    if (data.rotations.isEmpty()) ResidentEmpty("No rotation history is available yet.")
    else data.rotations.forEach { rotation -> RotationCard(rotation, false) { detail = rotation } }

    Text("Supervisor", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    if (data.assignments.isEmpty()) ResidentEmpty("No current supervisor is assigned.")
    else data.assignments.forEach { assignment ->
        val supervisor = assignment.objectValue("supervisor")
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text(supervisor?.value("name").orEmpty().ifBlank { "Supervisor" }, fontWeight = FontWeight.SemiBold)
                detailLines(
                    "Department" to supervisor?.value("department").orEmpty(),
                    "Assignment" to residentStatus(assignment.value("status")),
                    "Period" to listOf(assignment.value("start_date"), assignment.value("end_date")).filter { it.isNotBlank() }.joinToString(" – "),
                )
            }
        }
    }
    detail?.let { RotationDetail(it) { detail = null } }
}

@Composable
private fun RotationCard(rotation: JsonObject, current: Boolean, onOpen: () -> Unit) {
    Card(Modifier.fillMaxWidth().clickable(onClick = onOpen)) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(rotation.value("department").ifBlank { rotation.value("template_name").ifBlank { "Rotation" } }, fontWeight = FontWeight.SemiBold)
            detailLines(
                "Training site" to rotation.value("hospital"),
                "Period" to listOf(rotation.value("start_date"), rotation.value("end_date")).filter { it.isNotBlank() }.joinToString(" – "),
            )
            Text(if (current) "Current · ${residentStatus(rotation.value("status"))}" else residentStatus(rotation.value("status")), color = MaterialTheme.colorScheme.primary)
            Text("View details", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
private fun RotationDetail(rotation: JsonObject, onDismiss: () -> Unit) {
    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = { TextButton(onClick = onDismiss) { Text("Close") } },
        title = { Text("Rotation details") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                detailLines(
                    "Department" to rotation.value("department"), "Training site" to rotation.value("hospital"),
                    "Posting" to rotation.value("template_name"), "Start" to rotation.value("start_date"),
                    "End" to rotation.value("end_date"), "Status" to residentStatus(rotation.value("status")),
                    "Notes" to rotation.value("notes"), "Feedback" to rotation.value("return_reason").ifBlank { rotation.value("reject_reason") },
                )
            }
        },
    )
}

@Composable
internal fun LogbookScreen(
    data: InstitutionalSnapshot,
    busy: Boolean,
    onCreate: (AcademicLogbookPayload) -> Unit,
    onSubmit: (Int) -> Unit,
    onUpdate: (Int, AcademicLogbookPayload) -> Unit,
) {
    var adding by remember { mutableStateOf(false) }
    var selected by remember { mutableStateOf<JsonObject?>(null) }
    Text("Logbook", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    val counts = data.logbook.groupingBy { it.value("status") }.eachCount()
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text("Activity summary", fontWeight = FontWeight.SemiBold)
            Text("Draft ${counts["DRAFT"] ?: 0} · Submitted ${counts["SUBMITTED"] ?: 0} · Correction required ${counts["RETURNED"] ?: 0} · Approved ${counts["APPROVED"] ?: 0}")
        }
    }
    Button(onClick = { adding = true }, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Add logbook entry") }
    if (data.logbook.isEmpty()) ResidentEmpty("No logbook entries are recorded yet.")
    else data.logbook.forEach { entry ->
        Card(Modifier.fillMaxWidth().clickable { selected = entry }) {
            Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text(entry.value("title").ifBlank { entry.value("category_name").ifBlank { "Logbook entry" } }, fontWeight = FontWeight.SemiBold)
                Text(listOf(entry.value("entry_date"), residentStatus(entry.value("status"))).filter { it.isNotBlank() }.joinToString(" · "))
                entry.value("supervisor_comments").takeIf { it.isNotBlank() }?.let { Text("Feedback: $it", color = MaterialTheme.colorScheme.error) }
            }
        }
    }
    if (adding) LogbookEntryDialog(data.logbookCategories, busy, { adding = false }, onCreate)
    selected?.let { LogbookDetailDialog(it, busy, { selected = null }, onSubmit, onUpdate) }
}

@Composable
private fun LogbookEntryDialog(categories: List<JsonObject>, busy: Boolean, onDismiss: () -> Unit, onCreate: (AcademicLogbookPayload) -> Unit) {
    var category by remember { mutableStateOf(categories.firstOrNull()?.idValue()?.toString().orEmpty()) }
    var date by remember { mutableStateOf("") }
    var title by remember { mutableStateOf("") }
    var reflection by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New logbook entry") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                if (categories.isEmpty()) Text("No logbook categories are currently available.", color = MaterialTheme.colorScheme.error)
                else Text("Category: ${categories.firstOrNull { it.idValue()?.toString() == category }?.value("name").orEmpty()}")
                OutlinedTextField(category, { category = it }, label = { Text("Category ID") }, enabled = !busy, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(date, { date = it }, label = { Text("Entry date (YYYY-MM-DD)") }, enabled = !busy, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(title, { title = it }, label = { Text("Activity title") }, enabled = !busy, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(reflection, { reflection = it }, label = { Text("Reflection (optional)") }, enabled = !busy, modifier = Modifier.fillMaxWidth())
                Text("Do not include patient-identifying information.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        },
        confirmButton = {
            TextButton(enabled = !busy && category.toIntOrNull() != null && date.isNotBlank() && title.isNotBlank(), onClick = {
                onCreate(AcademicLogbookPayload(category.toInt(), date, title, resident_reflection = reflection)); onDismiss()
            }) { Text("Save draft") }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") } },
    )
}

@Composable
private fun LogbookDetailDialog(
    entry: JsonObject,
    busy: Boolean,
    onDismiss: () -> Unit,
    onSubmit: (Int) -> Unit,
    onUpdate: (Int, AcademicLogbookPayload) -> Unit,
) {
    var editing by remember { mutableStateOf(false) }
    var title by remember { mutableStateOf(entry.value("title")) }
    var reflection by remember { mutableStateOf(entry.value("resident_reflection")) }
    val canEdit = entry.value("status") in setOf("DRAFT", "RETURNED")
    AlertDialog(
        onDismissRequest = onDismiss, title = { Text("Logbook entry") },
        text = { Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            detailLines("Date" to entry.value("entry_date"), "Status" to residentStatus(entry.value("status")), "Description" to entry.value("description"), "Feedback" to entry.value("supervisor_comments"))
            if (editing) {
                OutlinedTextField(title, { title = it }, label = { Text("Activity title") }, modifier = Modifier.fillMaxWidth(), enabled = !busy)
                OutlinedTextField(reflection, { reflection = it }, label = { Text("Reflection") }, modifier = Modifier.fillMaxWidth(), enabled = !busy)
            } else detailLines("Activity" to entry.value("title"), "Reflection" to entry.value("resident_reflection"))
        } },
        confirmButton = { entry.idValue()?.let { id ->
            if (editing) TextButton(onClick = {
                val category = entry.value("category").toIntOrNull()
                if (category != null) onUpdate(id, AcademicLogbookPayload(category, entry.value("entry_date"), title, entry.value("description"), entry.value("case_identifier"), entry.value("patient_age"), entry.value("patient_gender"), reflection))
                onDismiss()
            }, enabled = !busy && title.isNotBlank()) { Text("Save changes") }
            else if (canEdit) TextButton(onClick = { onSubmit(id); onDismiss() }, enabled = !busy) { Text("Submit") }
        } },
        dismissButton = { if (canEdit && !editing) TextButton(onClick = { editing = true }, enabled = !busy) { Text("Edit") } else TextButton(onClick = onDismiss) { Text("Close") } },
    )
}

@Composable
internal fun RequirementsScreen(data: InstitutionalSnapshot, documents: @Composable () -> Unit) {
    Text("Requirements", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Card(Modifier.fillMaxWidth()) { Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text("Assessments", fontWeight = FontWeight.SemiBold)
        Text(if (data.assessments.isEmpty()) "No assessments are currently available." else "${data.assessments.size} assessment${if (data.assessments.size == 1) "" else "s"} recorded")
    } }
    Card(Modifier.fillMaxWidth()) { Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text("Research / synopsis", fontWeight = FontWeight.SemiBold)
        Text(data.research?.value("status")?.takeIf { it.isNotBlank() }?.let(::residentStatus) ?: "No research project is currently recorded.")
    } }
    Card(Modifier.fillMaxWidth()) { Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text("Workshops", fontWeight = FontWeight.SemiBold)
        Text(if (data.workshops.isEmpty()) "No workshop completions are currently recorded." else "${data.workshops.size} completion${if (data.workshops.size == 1) "" else "s"} recorded")
    } }
    Text("Documents", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    documents()
}

@Composable
private fun detailLines(vararg lines: Pair<String, String>) {
    lines.filter { it.second.isNotBlank() }.forEach { (label, value) -> Text("$label: $value", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
}

@Composable
private fun ResidentEmpty(text: String) = Text(text, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(vertical = 4.dp))
