package fmu.pg.sims.core.designsystem

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = FmuPrimary,
    onPrimary = Color.White,
    primaryContainer = FmuPrimaryContainer,
    onPrimaryContainer = FmuOnPrimaryContainer,
    secondary = FmuSecondary,
    onSecondary = Color.White,
    secondaryContainer = FmuSecondaryContainer,
    onSecondaryContainer = FmuOnSecondaryContainer,
    background = FmuBackground,
    onBackground = FmuTextPrimary,
    surface = FmuSurface,
    onSurface = FmuTextPrimary,
    surfaceVariant = FmuSurfaceVariant,
    onSurfaceVariant = FmuTextSecondary,
    outline = FmuOutline,
)

private val DarkColorScheme = darkColorScheme(
    primary = FmuPrimaryLight,
    onPrimary = Color(0xFF064E3B),
    primaryContainer = FmuPrimaryDark,
    onPrimaryContainer = FmuPrimaryContainer,
    secondary = Color(0xFF38BDF8),
    onSecondary = Color(0xFF0C4A6E),
    background = Color(0xFF0F172A),
    onBackground = Color(0xFFF8FAFC),
    surface = Color(0xFF1E293B),
    onSurface = Color(0xFFF8FAFC),
    surfaceVariant = Color(0xFF334155),
    onSurfaceVariant = Color(0xFFCBD5E1),
    outline = Color(0xFF475569),
)

@Composable
fun PgsimsTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
