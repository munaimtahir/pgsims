package pk.vexel.pgrcompanion

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonPrimitive

/**
 * Supervisor action-capable workflow queues: approve, reject and return pending Logbook, Leave,
 * Rotation and Research items. Every backend endpoint used here already existed and was already
 * scoped to the caller's own supervised residents — see android/docs/SUPERVISOR_API_CAPABILITY_MATRIX.md.
 */

internal enum class SupervisorWorkflow(val title: String, val supportsReject: Boolean, val supportsReturn: Boolean) {
    LOGBOOK("Logbook", supportsReject = true, supportsReturn = true),
    LEAVE("Leave Requests", supportsReject = true, supportsReturn = false),
    ROTATION("Rotations", supportsReject = true, supportsReturn = true),
    RESEARCH("Research / Synopsis", supportsReject = false, supportsReturn = true),
}

private fun JsonObject.value(key: String): String = string(key).orEmpty()
private fun JsonObject.idValue(): Int? = runCatching { this["id"]?.jsonPrimitive?.intOrNull }.getOrNull()

/** Each workflow's list resource has different field names — see SUPERVISOR_API_CAPABILITY_MATRIX.md. */
private fun itemTitle(item: JsonObject, workflow: SupervisorWorkflow): String = when (workflow) {
    SupervisorWorkflow.LOGBOOK -> item.value("title")
    SupervisorWorkflow.LEAVE -> InstitutionalLabels.humanize(item.value("leave_type")).ifBlank { "Leave request" }
    SupervisorWorkflow.ROTATION -> item.value("department_name").ifBlank { item.value("template_name") }.ifBlank { "Rotation" }
    SupervisorWorkflow.RESEARCH -> item.value("title").ifBlank { "Research submission" }
}.ifBlank { "Item #${item.idValue() ?: ""}" }

private fun itemDetailLines(item: JsonObject, workflow: SupervisorWorkflow): List<Pair<String, String>> = when (workflow) {
    SupervisorWorkflow.LOGBOOK -> listOf(
        "Status" to InstitutionalLabels.humanize(item.value("status")),
        "Description" to item.value("description"),
    )
    SupervisorWorkflow.LEAVE -> listOf(
        "Dates" to "${item.value("start_date")} – ${item.value("end_date")}",
        "Reason" to item.value("reason"),
        "Status" to InstitutionalLabels.humanize(item.value("status")),
    )
    SupervisorWorkflow.ROTATION -> listOf(
        "Training site" to item.value("hospital_name"),
        "Dates" to "${item.value("start_date")} – ${item.value("end_date")}",
        "Notes" to item.value("notes"),
        "Status" to InstitutionalLabels.humanize(item.value("status")),
    )
    SupervisorWorkflow.RESEARCH -> listOf(
        "Topic area" to item.value("topic_area"),
        "Status" to InstitutionalLabels.humanize(item.value("status_display").ifBlank { item.value("status") }),
    )
}.filter { it.second.isNotBlank() }

@Composable
internal fun SupervisorWorkflowQueueScreen(
    repository: InstitutionalRepository,
    workflow: SupervisorWorkflow,
    onBack: () -> Unit,
    onActioned: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var items by remember(workflow) { mutableStateOf<List<JsonObject>>(emptyList()) }
    var loading by remember(workflow) { mutableStateOf(true) }
    var loadError by remember(workflow) { mutableStateOf<String?>(null) }
    var selected by remember(workflow) { mutableStateOf<JsonObject?>(null) }
    var actionBusy by remember(workflow) { mutableStateOf(false) }
    var actionError by remember(workflow) { mutableStateOf<String?>(null) }
    var reasonPromptFor by remember(workflow) { mutableStateOf<String?>(null) } // "reject" | "return"

    fun reload() {
        scope.launch {
            loading = true
            loadError = null
            val result = when (workflow) {
                SupervisorWorkflow.LOGBOOK -> repository.supervisorLogbookQueue()
                SupervisorWorkflow.LEAVE -> repository.supervisorLeaveQueue()
                SupervisorWorkflow.ROTATION -> repository.supervisorRotationQueue()
                SupervisorWorkflow.RESEARCH -> repository.supervisorResearchQueue()
            }
            result.fold({ items = it }, { loadError = it.message ?: "Could not load this queue." })
            loading = false
        }
    }

    LaunchedEffect(workflow) { reload() }

    fun runAction(block: suspend () -> Result<JsonObject>) {
        val itemId = selected?.idValue() ?: return
        scope.launch {
            actionBusy = true
            actionError = null
            block().fold(
                {
                    items = items.filterNot { it.idValue() == itemId }
                    selected = null
                    reasonPromptFor = null
                    onActioned()
                },
                { actionError = it.message ?: "Could not update this item." },
            )
            actionBusy = false
        }
    }

    TextButton(onClick = onBack) { Text("← Back") }
    Text(workflow.title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)

    if (loading) {
        LinearProgressIndicator(Modifier.fillMaxWidth())
        return
    }
    loadError?.let {
        Text(it, color = MaterialTheme.colorScheme.error)
        return
    }
    if (items.isEmpty()) {
        Text("No pending items in this queue.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        return
    }

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        items.forEach { item ->
            Card(Modifier.fillMaxWidth().clickable { selected = item }) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(itemTitle(item, workflow), fontWeight = FontWeight.SemiBold)
                    item.value("resident_name").takeIf { it.isNotBlank() }?.let {
                        Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }

    val current = selected
    if (current != null) {
        SupervisorWorkflowItemDialog(
            item = current,
            workflow = workflow,
            busy = actionBusy,
            error = actionError,
            onApprove = {
                runAction {
                    when (workflow) {
                        SupervisorWorkflow.LOGBOOK -> repository.verifyLogbook(current.idValue()!!, "")
                        SupervisorWorkflow.LEAVE -> repository.approveLeave(current.idValue()!!)
                        SupervisorWorkflow.ROTATION -> repository.approveRotation(current.idValue()!!)
                        SupervisorWorkflow.RESEARCH -> repository.approveResearch(current.idValue()!!, "")
                    }
                }
            },
            onReject = { reasonPromptFor = "reject" },
            onReturn = { reasonPromptFor = "return" },
            onDismiss = { selected = null; actionError = null },
        )
    }

    val prompt = reasonPromptFor
    if (current != null && prompt != null) {
        ReasonConfirmDialog(
            actionLabel = if (prompt == "reject") "Reject" else "Return for revision",
            requireReason = workflow == SupervisorWorkflow.LOGBOOK && prompt == "return",
            busy = actionBusy,
            onDismiss = { reasonPromptFor = null },
            onConfirm = { reason ->
                runAction {
                    when (workflow to prompt) {
                        SupervisorWorkflow.LOGBOOK to "reject" -> repository.rejectLogbook(current.idValue()!!, reason)
                        SupervisorWorkflow.LOGBOOK to "return" -> repository.returnLogbook(current.idValue()!!, reason)
                        SupervisorWorkflow.LEAVE to "reject" -> repository.rejectLeave(current.idValue()!!, reason)
                        SupervisorWorkflow.ROTATION to "reject" -> repository.rejectRotation(current.idValue()!!, reason)
                        SupervisorWorkflow.ROTATION to "return" -> repository.returnRotation(current.idValue()!!, reason)
                        SupervisorWorkflow.RESEARCH to "return" -> repository.returnResearch(current.idValue()!!, reason)
                        else -> error("Unsupported action")
                    }
                }
            },
        )
    }
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
private fun SupervisorWorkflowItemDialog(
    item: JsonObject,
    workflow: SupervisorWorkflow,
    busy: Boolean,
    error: String?,
    onApprove: () -> Unit,
    onReject: () -> Unit,
    onReturn: () -> Unit,
    onDismiss: () -> Unit,
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(itemTitle(item, workflow)) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                item.value("resident_name").takeIf { it.isNotBlank() }?.let { Text("Resident: $it") }
                itemDetailLines(item, workflow).forEach { (label, text) -> Text("$label: $text", style = MaterialTheme.typography.bodySmall) }
                error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            }
        },
        confirmButton = { TextButton(onClick = onApprove, enabled = !busy) { Text("Approve") } },
        dismissButton = {
            Column {
                if (workflow.supportsReturn) TextButton(onClick = onReturn, enabled = !busy) { Text("Return for revision") }
                if (workflow.supportsReject) TextButton(onClick = onReject, enabled = !busy) { Text("Reject") }
                TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") }
            }
        },
    )
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
private fun ReasonConfirmDialog(
    actionLabel: String,
    requireReason: Boolean,
    busy: Boolean,
    onConfirm: (String) -> Unit,
    onDismiss: () -> Unit,
) {
    var reason by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(actionLabel) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("This will notify the resident and cannot be undone from Android.")
                OutlinedTextField(
                    value = reason,
                    onValueChange = { reason = it },
                    label = { Text(if (requireReason) "Comments (required)" else "Comments (optional)") },
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        },
        confirmButton = {
            TextButton(
                onClick = { onConfirm(reason) },
                enabled = !busy && (!requireReason || reason.isNotBlank()),
            ) { Text(actionLabel) }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Cancel") } },
    )
}
