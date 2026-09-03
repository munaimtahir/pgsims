package fmu.pg.sims.feature.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.HourglassTop
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import fmu.pg.sims.core.designsystem.FmuStatusAmber
import fmu.pg.sims.core.designsystem.FmuStatusRed
import fmu.pg.sims.core.designsystem.FmuStatusRedBg

@Composable
fun OnboardingPendingReviewScreen(onLogout: () -> Unit, onRefresh: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(Icons.Default.HourglassTop, contentDescription = null, tint = FmuStatusAmber, modifier = Modifier.size(56.dp))
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = "Pending Review", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Your onboarding profile has been submitted and is awaiting administrative review. " +
                "You'll be notified once it's approved.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(onClick = onRefresh, modifier = Modifier.fillMaxWidth()) { Text("Check Status") }
        Spacer(modifier = Modifier.height(8.dp))
        Button(onClick = onLogout, modifier = Modifier.fillMaxWidth()) { Text("Sign Out") }
    }
}

@Composable
fun OnboardingCorrectionRequiredScreen(
    reviewNote: String,
    onFixNow: () -> Unit,
    onLogout: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(Icons.Default.Edit, contentDescription = null, tint = FmuStatusRed, modifier = Modifier.size(56.dp))
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = "Correction Required", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "An administrator has requested changes to your onboarding profile before it can be approved.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(modifier = Modifier.height(16.dp))
        Surface(color = FmuStatusRedBg, modifier = Modifier.fillMaxWidth()) {
            Text(
                text = reviewNote.ifBlank { "No reason was provided." },
                color = FmuStatusRed,
                modifier = Modifier.padding(16.dp),
            )
        }
        Spacer(modifier = Modifier.height(32.dp))
        Button(onClick = onFixNow, modifier = Modifier.fillMaxWidth()) { Text("Review & Fix") }
        Spacer(modifier = Modifier.height(8.dp))
        Button(onClick = onLogout, modifier = Modifier.fillMaxWidth()) { Text("Sign Out") }
    }
}
