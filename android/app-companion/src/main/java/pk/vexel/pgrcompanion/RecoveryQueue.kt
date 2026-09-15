package pk.vexel.pgrcompanion

import android.content.Context
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.withLock

/** A failed request may finish after logout. Never retain it under the next session. */
internal suspend fun retainDraft(
    context: Context, repository: InstitutionalRepository, owner: Int?,
    save: (OfflineDraftStore, Int) -> Unit,
): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        RecoveryCoordinator.mutex.withLock {
            check(owner != null && repository.isConnected() && repository.currentUserId() == owner) {
                "Your session changed. Reconnect before saving a draft."
            }
            save(OfflineDraftStore(context), owner)
            (context.applicationContext as CompanionApplication).enqueueOfflineRecovery()
        }
    }
}

@Composable
internal fun OfflineDraftQueue(repository: InstitutionalRepository) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var drafts by remember { mutableStateOf<List<OfflineDraft>>(emptyList()) }
    var message by remember { mutableStateOf<String?>(null) }
    LaunchedEffect(Unit) { drafts = withContext(Dispatchers.IO) { OfflineDraftStore(context).all() } }
    if (drafts.isEmpty()) return
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text("Offline drafts")
            drafts.forEach { draft ->
                val owned = draft.ownerUserId != null && draft.ownerUserId == repository.currentUserId()
                Text(if (owned) "${InstitutionalLabels.humanize(draft.kind)} draft · ${draft.state}" else "Draft from another or unknown account; discard required")
                Row {
                    TextButton(enabled = owned, onClick = { (context.applicationContext as CompanionApplication).enqueueOfflineRecovery(replacePending = true); message = "Recovery queued." }) { Text("Retry") }
                    TextButton(onClick = { scope.launch {
                        runCatching { withContext(Dispatchers.IO) { RecoveryCoordinator.mutex.withLock {
                            val store = OfflineDraftStore(context)
                            store.remove(draft.id)
                            drafts = store.all()
                        } } }.onFailure { message = "Could not discard draft. Please retry." }
                    } }) { Text("Discard") }
                }
            }
            message?.let { Text(it) }
        }
    }
}
