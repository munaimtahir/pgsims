package pk.vexel.pgrcompanion

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonObject

private fun JsonObject.progressValue(key: String): String = string(key).orEmpty()
private fun JsonObject.progressObject(key: String): JsonObject? = runCatching { this[key]?.jsonObject }.getOrNull()

/** Read-only mobile reporting from the canonical academic progress and monitoring endpoints. */
@Composable
internal fun ResidentProgressReport(data: InstitutionalSnapshot) {
    Text("My progress", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("This is a read-only summary of your PGR SIMS record.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    val progress = data.academicProgress
    val monitoring = data.progressMonitoring
    val rotation = data.residentSummary?.progressObject("rotation")?.progressObject("current")
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        ProgressCard("Current posting", rotation?.progressValue("template_name").orEmpty().ifBlank { "No current posting" })
        ProgressCard("Training status", progress?.progressValue("training_record_status").orEmpty().ifBlank { "Not available" })
        ProgressCard("Training year", progress?.progressValue("training_year").orEmpty().ifBlank { "Not available" })
        ProgressCard("Logbook", "${progress?.progressValue("logbooks_verified").orEmpty().ifBlank { "0" }} verified · ${progress?.progressValue("logbooks_total").orEmpty().ifBlank { "0" }} total")
        ProgressCard("Evaluations / WBA", "${progress?.progressValue("evaluations_approved").orEmpty().ifBlank { "0" }} approved · ${progress?.progressValue("evaluations_total").orEmpty().ifBlank { "0" }} total")
        ProgressCard("Monitoring", monitoring?.progressValue("overall_status").orEmpty().ifBlank { monitoring?.progressValue("status").orEmpty().ifBlank { "Current" } })
        ProgressCard("Research", data.research?.progressValue("status").orEmpty().ifBlank { "No research status recorded" })
        ProgressCard("Workshops", "${data.workshops.size} recorded")
    }
}

@Composable private fun ProgressCard(label: String, detail: String) = Card(Modifier.fillMaxWidth()) {
    Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(label, fontWeight = FontWeight.SemiBold)
        Text(detail, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
