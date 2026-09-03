package fmu.pg.sims.ui.components

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import fmu.pg.sims.core.copyUriToCacheFile
import fmu.pg.sims.core.designsystem.FmuStatusAmber
import fmu.pg.sims.core.designsystem.FmuStatusAmberBg
import fmu.pg.sims.core.designsystem.FmuStatusGreen
import fmu.pg.sims.core.designsystem.FmuStatusGreenBg
import fmu.pg.sims.core.designsystem.FmuStatusRed
import fmu.pg.sims.core.designsystem.FmuStatusRedBg
import fmu.pg.sims.core.designsystem.FmuSurfaceVariant
import fmu.pg.sims.core.designsystem.FmuTextSecondary
import fmu.pg.sims.core.mimeTypeFor
import fmu.pg.sims.core.model.DocumentStatus
import fmu.pg.sims.core.model.ResidentDocumentDto

@Composable
fun DocumentRow(
    document: ResidentDocumentDto,
    busy: Boolean,
    onUpload: (java.io.File, String) -> Unit,
    onDefer: () -> Unit,
) {
    val context = LocalContext.current
    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            val file = copyUriToCacheFile(context, uri)
            if (file != null) onUpload(file, mimeTypeFor(context, uri))
        }
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text(text = document.title, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(end = 8.dp))
                StatusChip(status = document.status)
            }
            if (document.verificationRemarks.isNotBlank() &&
                document.status in setOf(DocumentStatus.REJECTED, DocumentStatus.REUPLOAD_REQUIRED)
            ) {
                Text(
                    text = document.verificationRemarks,
                    style = MaterialTheme.typography.bodySmall,
                    color = FmuStatusRed,
                    modifier = Modifier.padding(top = 4.dp),
                )
            }
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.padding(top = 8.dp),
            ) {
                if (busy) {
                    CircularProgressIndicator(modifier = Modifier.padding(4.dp))
                } else {
                    if (document.status != DocumentStatus.VERIFIED) {
                        OutlinedButton(onClick = {
                            launcher.launch(arrayOf("image/*", "application/pdf"))
                        }) { Text("Upload") }
                    }
                    if (document.status == DocumentStatus.NOT_STARTED) {
                        TextButton(onClick = onDefer) { Text("Complete Later") }
                    }
                }
            }
        }
    }
}

@Composable
private fun StatusChip(status: String) {
    val (bg, fg, label) = when (status) {
        DocumentStatus.VERIFIED -> Triple(FmuStatusGreenBg, FmuStatusGreen, "Verified")
        DocumentStatus.UPLOADED, DocumentStatus.PENDING_REVIEW -> Triple(FmuStatusAmberBg, FmuStatusAmber, "Pending Review")
        DocumentStatus.REJECTED, DocumentStatus.REUPLOAD_REQUIRED -> Triple(FmuStatusRedBg, FmuStatusRed, "Needs Attention")
        DocumentStatus.DEFERRED -> Triple(FmuSurfaceVariant, FmuTextSecondary, "Deferred")
        else -> Triple(FmuSurfaceVariant, FmuTextSecondary, "Outstanding")
    }
    Surface(shape = RoundedCornerShape(6.dp), color = bg) {
        Text(text = label, color = fg, style = MaterialTheme.typography.labelSmall, modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
    }
}
