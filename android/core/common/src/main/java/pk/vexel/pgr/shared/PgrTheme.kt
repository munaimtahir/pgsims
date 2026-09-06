package pk.vexel.pgr.shared

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val PgrTeal = Color(0xFF087F78)
val PgrNavy = Color(0xFF123047)

@Composable
fun PgrTheme(content: @Composable () -> Unit) = MaterialTheme(
    colorScheme = lightColorScheme(primary = PgrTeal, secondary = Color(0xFF4B6584), background = Color(0xFFF7FAF9), surface = Color.White, onSurface = PgrNavy, onBackground = PgrNavy),
    content = content,
)
