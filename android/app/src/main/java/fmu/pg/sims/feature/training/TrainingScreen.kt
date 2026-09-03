package fmu.pg.sims.feature.training

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import fmu.pg.sims.core.ViewModelFactory
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading

@Composable
fun TrainingScreen(
    viewModelFactory: ViewModelFactory,
    viewModel: TrainingViewModel = viewModel(factory = viewModelFactory),
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.error != null -> ErrorRetryView(message = uiState.error!!, onRetry = viewModel::refresh)
        uiState.records.isEmpty() -> Column(
            modifier = Modifier.fillMaxSize().padding(24.dp),
        ) { Text("No training record found yet.") }
        else -> Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(text = "Training", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            uiState.records.forEach { record ->
                Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(text = record.programName.ifBlank { "Training Program" }, fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleMedium)
                        TrainingDetailRow(label = "Current level", value = record.currentLevel.ifBlank { "—" })
                        TrainingDetailRow(label = "Start date", value = record.startDate ?: "—")
                        TrainingDetailRow(label = "Expected end date", value = record.expectedEndDate ?: "—")
                        TrainingDetailRow(label = "Status", value = if (record.active) "Active" else "Inactive")
                    }
                }
            }
        }
    }
}

@Composable
private fun TrainingDetailRow(label: String, value: String) {
    Text(
        text = "$label: $value",
        style = MaterialTheme.typography.bodyMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
    )
}
