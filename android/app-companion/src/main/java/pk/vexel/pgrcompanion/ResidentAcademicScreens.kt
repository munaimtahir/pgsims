package pk.vexel.pgrcompanion

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonPrimitive

private fun JsonObject.ra(key: String): String = string(key).orEmpty()
private fun JsonObject.raId(key: String = "id"): Int? = runCatching { this[key]?.jsonPrimitive?.intOrNull }.getOrNull()

private fun leaveLabel(raw: String): String = InstitutionalLabels.humanize(raw).ifBlank { "Leave" }

@Composable
internal fun LeaveRequestsScreen(
    repository: InstitutionalRepository,
    data: InstitutionalSnapshot,
    busy: Boolean,
    onNotice: (String) -> Unit,
    onRefresh: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    var selected by remember { mutableStateOf<JsonObject?>(null) }
    var adding by remember { mutableStateOf(false) }
    var filter by remember { mutableStateOf("ALL") }
    Text("Leave requests", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("Create and track leave requests using the institution's canonical workflow.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    Button(onClick = { adding = true }, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("New leave request") }
    Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
        listOf("ALL", "SUBMITTED", "APPROVED", "REJECTED").forEach { option ->
            TextButton(onClick = { filter = option }) { Text(if (option == "ALL") "All" else InstitutionalLabels.workflowStatus(option)) }
        }
    }
    val visibleLeaves = data.leaves.filter { filter == "ALL" || it.ra("status") == filter }
    if (visibleLeaves.isEmpty()) Text("No leave requests match this filter.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    visibleLeaves.forEach { leave ->
        Card(Modifier.fillMaxWidth().clickable { selected = leave }) {
            Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(leaveLabel(leave.ra("leave_type")), fontWeight = FontWeight.SemiBold)
                Text("${leave.ra("start_date")} – ${leave.ra("end_date")}")
                Text(InstitutionalLabels.workflowStatus(leave.ra("status")), color = MaterialTheme.colorScheme.primary)
                leave.ra("reject_reason").takeIf { it.isNotBlank() }?.let { Text("Decision: $it", color = MaterialTheme.colorScheme.error) }
            }
        }
    }
    if (adding) LeaveRequestDialog(data, busy, { adding = false }) { payload ->
        adding = false
        scope.launch {
            val owner = repository.currentUserId()
            val retrySafePayload = payload.withOfflineId()
            repository.createLeave(retrySafePayload).fold(
                { onNotice("Leave request saved as a draft."); onRefresh() },
                {
                    retainDraft(context, repository, owner) { store, id -> store.saveLeave(retrySafePayload, id) }.fold(
                        { onNotice("PGR SIMS is unavailable. Your encrypted leave draft is retained on this device.") },
                        { onNotice("Could not retain the draft. Reconnect and try again.") },
                    )
                },
            )
        }
    }
    selected?.let { leave ->
        LeaveDetailDialog(repository, leave, busy, { selected = null }, onNotice, onRefresh)
    }
}

@Composable
private fun LeaveRequestDialog(
    data: InstitutionalSnapshot,
    busy: Boolean,
    onDismiss: () -> Unit,
    onCreate: (LeaveRequestPayload) -> Unit,
) {
    var type by remember { mutableStateOf("annual") }
    var menu by remember { mutableStateOf(false) }
    var start by remember { mutableStateOf("") }
    var end by remember { mutableStateOf("") }
    var reason by remember { mutableStateOf("") }
    val trainingId = data.training.firstOrNull()?.raId()
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New leave request") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                TextButton(onClick = { menu = true }, enabled = !busy) { Text("Type: ${leaveLabel(type)}") }
                DropdownMenu(expanded = menu, onDismissRequest = { menu = false }) {
                    listOf("annual", "sick", "casual", "study", "maternity", "other").forEach { value ->
                        DropdownMenuItem(text = { Text(leaveLabel(value)) }, onClick = { type = value; menu = false })
                    }
                }
                OutlinedTextField(start, { start = it }, label = { Text("Start date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth(), enabled = !busy)
                OutlinedTextField(end, { end = it }, label = { Text("End date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth(), enabled = !busy)
                OutlinedTextField(reason, { reason = it }, label = { Text("Reason") }, modifier = Modifier.fillMaxWidth(), enabled = !busy)
                if (trainingId == null) Text("No active training record is available for this account.", color = MaterialTheme.colorScheme.error)
            }
        },
        confirmButton = { TextButton(
            onClick = { onCreate(LeaveRequestPayload(trainingId!!, type, start, end, reason)) },
            enabled = !busy && trainingId != null && start.isNotBlank() && end.isNotBlank(),
        ) { Text("Save draft") } },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") } },
    )
}

@Composable
private fun LeaveDetailDialog(
    repository: InstitutionalRepository,
    leave: JsonObject,
    busy: Boolean,
    onDismiss: () -> Unit,
    onNotice: (String) -> Unit,
    onRefresh: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    val id = leave.raId()
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(leaveLabel(leave.ra("leave_type"))) },
        text = { Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text("Dates: ${leave.ra("start_date")} – ${leave.ra("end_date")}")
            Text("Reason: ${leave.ra("reason").ifBlank { "Not provided" }}")
            Text("Status: ${InstitutionalLabels.workflowStatus(leave.ra("status"))}")
            leave.ra("reject_reason").takeIf { it.isNotBlank() }?.let { Text("Decision: $it", color = MaterialTheme.colorScheme.error) }
        } },
        confirmButton = { if (id != null && leave.ra("status") == "DRAFT") TextButton(onClick = {
            scope.launch { repository.submitLeave(id).fold({ onNotice("Leave request submitted."); onRefresh(); onDismiss() }, { onNotice(it.message ?: "Could not submit the leave request.") }) }
        }, enabled = !busy) { Text("Submit") } },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Close") } },
    )
}

@Composable
internal fun EvaluationsScreen(
    repository: InstitutionalRepository,
    data: InstitutionalSnapshot,
    busy: Boolean,
    onNotice: (String) -> Unit,
    onRefresh: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var adding by remember { mutableStateOf(false) }
    var selected by remember { mutableStateOf<JsonObject?>(null) }
    Text("Evaluations / WBA", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("Assessment records and supervisor feedback from PGR SIMS.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    if (data.evaluationTemplates.isNotEmpty()) Button(onClick = { adding = true }, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Start evaluation") }
    else Text("No evaluation templates are currently available.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    if (data.assessments.isEmpty()) Text("No evaluations are recorded.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    data.assessments.forEach { evaluation ->
        Card(Modifier.fillMaxWidth().clickable { selected = evaluation }) {
            Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(evaluation.ra("template_name").ifBlank { "Evaluation" }, fontWeight = FontWeight.SemiBold)
                Text(InstitutionalLabels.workflowStatus(evaluation.ra("status")), color = MaterialTheme.colorScheme.primary)
                evaluation.ra("supervisor_comments").takeIf { it.isNotBlank() }?.let { Text("Feedback: $it") }
            }
        }
    }
    if (adding) EvaluationCreateDialog(data, busy, { adding = false }) { payload ->
        adding = false
        scope.launch {
            repository.createEvaluation(payload).fold({ onNotice("Evaluation saved as a draft."); onRefresh() }, { onNotice(it.message ?: "Could not save the evaluation.") })
        }
    }
    selected?.let { evaluation -> EvaluationDetailDialog(repository, evaluation, busy, { selected = null }, onNotice, onRefresh) }
}

@Composable
private fun EvaluationCreateDialog(data: InstitutionalSnapshot, busy: Boolean, onDismiss: () -> Unit, onCreate: (EvaluationSubmissionPayload) -> Unit) {
    var selectedTemplate by remember { mutableStateOf(data.evaluationTemplates.firstOrNull()?.raId()) }
    var comments by remember { mutableStateOf("") }
    AlertDialog(onDismissRequest = onDismiss, title = { Text("New evaluation") }, text = {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("Template: ${data.evaluationTemplates.firstOrNull { it.raId() == selectedTemplate }?.ra("name") ?: "Unavailable"}")
            OutlinedTextField(comments, { comments = it }, label = { Text("Resident comments") }, modifier = Modifier.fillMaxWidth(), enabled = !busy)
        }
    }, confirmButton = { TextButton(onClick = { onCreate(EvaluationSubmissionPayload(selectedTemplate!!, resident_comments = comments)) }, enabled = !busy && selectedTemplate != null) { Text("Save draft") } }, dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel") } })
}

@Composable
private fun EvaluationDetailDialog(repository: InstitutionalRepository, evaluation: JsonObject, busy: Boolean, onDismiss: () -> Unit, onNotice: (String) -> Unit, onRefresh: () -> Unit) {
    val scope = rememberCoroutineScope(); val id = evaluation.raId(); val status = evaluation.ra("status")
    AlertDialog(onDismissRequest = onDismiss, title = { Text(evaluation.ra("template_name").ifBlank { "Evaluation" }) }, text = {
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text("Status: ${InstitutionalLabels.workflowStatus(status)}")
            Text("Supervisor: ${evaluation.ra("supervisor_name").ifBlank { "Not assigned" }}")
            evaluation.ra("score").takeIf { it.isNotBlank() }?.let { Text("Score: $it / ${evaluation.ra("max_score")}") }
            evaluation.ra("resident_comments").takeIf { it.isNotBlank() }?.let { Text("Your comments: $it") }
            evaluation.ra("supervisor_comments").takeIf { it.isNotBlank() }?.let { Text("Supervisor feedback: $it") }
            evaluation.ra("responses").takeIf { it.isNotBlank() }?.let { Text(it) }
        }
    }, confirmButton = { if (id != null && status == "DRAFT") TextButton(onClick = { scope.launch { repository.submitEvaluation(id).fold({ onNotice("Evaluation submitted."); onRefresh(); onDismiss() }, { onNotice(it.message ?: "Could not submit the evaluation.") }) } }, enabled = !busy) { Text("Submit") } }, dismissButton = { TextButton(onClick = onDismiss) { Text("Close") } })
}
