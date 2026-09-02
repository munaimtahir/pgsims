package pk.edu.fmu.pgsims.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.CloudDone
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Security
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch
import pk.edu.fmu.pgsims.BuildConfig
import pk.edu.fmu.pgsims.core.auth.AuthRepository
import pk.edu.fmu.pgsims.core.designsystem.FmuPrimary
import pk.edu.fmu.pgsims.core.designsystem.FmuPrimaryDark
import pk.edu.fmu.pgsims.core.designsystem.FmuStatusAmber
import pk.edu.fmu.pgsims.core.designsystem.FmuStatusAmberBg
import pk.edu.fmu.pgsims.core.designsystem.FmuStatusGreen
import pk.edu.fmu.pgsims.core.designsystem.FmuStatusGreenBg
import pk.edu.fmu.pgsims.core.designsystem.FmuStatusRed
import pk.edu.fmu.pgsims.core.designsystem.FmuStatusRedBg
import pk.edu.fmu.pgsims.core.designsystem.FmuSurfaceVariant
import pk.edu.fmu.pgsims.core.designsystem.FmuTextMuted
import pk.edu.fmu.pgsims.core.designsystem.FmuTextPrimary
import pk.edu.fmu.pgsims.core.designsystem.FmuTextSecondary
import pk.edu.fmu.pgsims.core.model.HealthStatus
import pk.edu.fmu.pgsims.core.model.NetworkResult

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FoundationScreen(
    authRepository: AuthRepository,
    modifier: Modifier = Modifier
) {
    val coroutineScope = rememberCoroutineScope()
    var healthResult by remember { mutableStateOf<NetworkResult<HealthStatus>?>(null) }
    var isChecking by remember { mutableStateOf(false) }

    fun runHealthCheck() {
        isChecking = true
        coroutineScope.launch {
            healthResult = authRepository.checkHealth()
            isChecking = false
        }
    }

    LaunchedEffect(Unit) {
        runHealthCheck()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = "PGR SIMS",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                        Text(
                            text = "Faisalabad Medical University",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color.White.copy(alpha = 0.85f)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = FmuPrimaryDark
                )
            )
        },
        modifier = modifier
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(MaterialTheme.colorScheme.background)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {

            // Header Banner
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = FmuPrimary.copy(alpha = 0.08f),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(FmuPrimary),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Security,
                            contentDescription = "Foundation Shield",
                            tint = Color.White,
                            modifier = Modifier.size(28.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(
                            text = "Platform Foundation",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = FmuTextPrimary
                        )
                        Text(
                            text = "Internal Testing Build · v${BuildConfig.VERSION_NAME} (${BuildConfig.VERSION_CODE})",
                            style = MaterialTheme.typography.bodyMedium,
                            color = FmuTextSecondary
                        )
                    }
                }
            }

            // Backend Health Card
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Live Backend Connectivity",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold
                        )
                        Button(
                            onClick = { runHealthCheck() },
                            enabled = !isChecking,
                            colors = ButtonDefaults.buttonColors(containerColor = FmuPrimary),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            if (isChecking) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(16.dp),
                                    color = Color.White,
                                    strokeWidth = 2.dp
                                )
                            } else {
                                Icon(
                                    imageVector = Icons.Default.Refresh,
                                    contentDescription = "Refresh",
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(text = "Check", fontSize = 12.sp)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    when (val res = healthResult) {
                        null -> {
                            StatusRow(
                                icon = Icons.Default.Info,
                                iconTint = FmuTextMuted,
                                label = "Status",
                                value = "Initiating health check...",
                                bg = FmuSurfaceVariant
                            )
                        }
                        is NetworkResult.Success -> {
                            StatusRow(
                                icon = Icons.Default.CheckCircle,
                                iconTint = FmuStatusGreen,
                                label = "API Health",
                                value = "ONLINE (${res.data.status.uppercase()})",
                                bg = FmuStatusGreenBg
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            StatusRow(
                                icon = Icons.Default.CloudDone,
                                iconTint = FmuStatusGreen,
                                label = "Database Engine",
                                value = res.data.database.uppercase(),
                                bg = FmuStatusGreenBg
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            StatusRow(
                                icon = Icons.Default.Info,
                                iconTint = FmuPrimary,
                                label = "Backend App",
                                value = "${res.data.app} ${res.data.version}",
                                bg = FmuPrimary.copy(alpha = 0.08f)
                            )
                        }
                        is NetworkResult.Error -> {
                            StatusRow(
                                icon = Icons.Default.Error,
                                iconTint = FmuStatusRed,
                                label = "Connectivity",
                                value = res.message,
                                bg = FmuStatusRedBg
                            )
                        }
                        is NetworkResult.Loading -> {
                            StatusRow(
                                icon = Icons.Default.Info,
                                iconTint = FmuStatusAmber,
                                label = "Status",
                                value = "Connecting to backend...",
                                bg = FmuStatusAmberBg
                            )
                        }
                    }
                }
            }

            // Architecture Specs Card
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Foundation Architecture Spec",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(12.dp))

                    SpecItem(label = "Application ID", value = BuildConfig.APPLICATION_ID)
                    SpecDivider()
                    SpecItem(label = "Compile / Target SDK", value = "Android 15 (API 35)")
                    SpecDivider()
                    SpecItem(label = "Minimum SDK", value = "Android 8.0 Oreo (API 26)")
                    SpecDivider()
                    SpecItem(label = "UI Toolkit", value = "Jetpack Compose + Material 3")
                    SpecDivider()
                    SpecItem(label = "Network & Serializer", value = "Retrofit 2.11 + Kotlinx Serialization")
                    SpecDivider()
                    SpecItem(label = "Secure Storage", value = "AndroidX EncryptedSharedPreferences (AES-256)")
                    SpecDivider()
                    SpecItem(label = "Identity Model", value = "4 Roles: ADMIN, RESIDENT, SUPERVISOR, SUPPORT_STAFF")
                }
            }

            // Notice Box
            Surface(
                shape = RoundedCornerShape(8.dp),
                color = FmuSurfaceVariant,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "This build delivers the certified Android platform foundation. User-facing onboarding workflows unlock in subsequent milestone releases.",
                    style = MaterialTheme.typography.bodySmall,
                    color = FmuTextSecondary,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(12.dp)
                )
            }
        }
    }
}

@Composable
private fun StatusRow(
    icon: ImageVector,
    iconTint: Color,
    label: String,
    value: String,
    bg: Color
) {
    Surface(
        shape = RoundedCornerShape(8.dp),
        color = bg,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = iconTint,
                modifier = Modifier.size(20.dp)
            )
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = "$label: ",
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.SemiBold,
                color = FmuTextPrimary
            )
            Text(
                text = value,
                style = MaterialTheme.typography.bodyMedium,
                color = FmuTextPrimary
            )
        }
    }
}

@Composable
private fun SpecItem(label: String, value: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = FmuTextSecondary
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodySmall,
            fontWeight = FontWeight.Medium,
            color = FmuTextPrimary
        )
    }
}

@Composable
private fun SpecDivider() {
    androidx.compose.material3.HorizontalDivider(
        color = MaterialTheme.colorScheme.outline.copy(alpha = 0.2f),
        thickness = 0.5.dp,
        modifier = Modifier.padding(vertical = 2.dp)
    )
}
