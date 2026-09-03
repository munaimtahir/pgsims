package fmu.pg.sims.feature.documents

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
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
import fmu.pg.sims.ui.components.DocumentRow
import fmu.pg.sims.ui.components.ErrorRetryView
import fmu.pg.sims.ui.components.FullScreenLoading
import fmu.pg.sims.ui.components.InlineErrorBanner

@Composable
fun DocumentsScreen(
    viewModelFactory: ViewModelFactory,
    viewModel: DocumentsViewModel = viewModel(factory = viewModelFactory),
) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.loading -> FullScreenLoading()
        uiState.error != null -> ErrorRetryView(message = uiState.error!!, onRetry = viewModel::refresh)
        else -> Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(text = "Documents", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            if (uiState.documents.isEmpty()) {
                Text("No documents on file.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            uiState.documents.forEach { document ->
                DocumentRow(
                    document = document,
                    busy = document.id in uiState.busyIds,
                    onUpload = { file, mime -> viewModel.upload(document.id, file, mime) },
                    onDefer = { viewModel.defer(document.id) },
                )
            }
            if (uiState.actionError != null) {
                InlineErrorBanner(message = uiState.actionError!!)
            }
        }
    }
}
