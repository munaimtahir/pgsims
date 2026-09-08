package pk.vexel.pgrportal

import android.content.Context
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.sp
import pk.vexel.pgr.shared.PgrTheme

class PortalActivity : ComponentActivity() {
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        setContent { PgrTheme { InstitutionalWorkspace((application as PortalApplication).institutional) } }
    }
}

internal fun displayNameOf(context: Context, uri: Uri): String {
    val resolved = runCatching {
        context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)
            ?.use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
    }.getOrNull()
    return resolved?.takeIf { it.isNotBlank() } ?: uri.lastPathSegment?.substringAfterLast('/').orEmpty().ifBlank { "document" }
}

@Composable
internal fun Disclaimer() = Text(
    "PGR Companion is a login-gated postgraduate residency application. Access is managed through PGR SIMS.",
    style = MaterialTheme.typography.bodySmall,
    fontSize = 12.sp,
)
