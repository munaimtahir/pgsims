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

/** Read-only mobile reporting assembled only from the resident-scoped snapshot endpoints. */
@Composable
internal fun ResidentProgressReport(data: InstitutionalSnapshot) {
    Text("My progress", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    Text("This is a read-only summary of your PGR SIMS record.", color = MaterialTheme.colorScheme.onSurfaceVariant)
    val logbook = logbookCounts(data.logbook)
    val evaluations = data.assessments.groupingBy { it.progressValue("status") }.eachCount()
    val rotation = data.residentSummary?.progressObject("rotation")?.progressObject("current")
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        ProgressCard("Current posting", rotation?.progressValue("template_name").orEmpty().ifBlank { "No current posting" })
        ProgressCard("Rotations", "${data.rotations.size} recorded")
        ProgressCard("Logbook (loaded records)", "${logbook["APPROVED"] ?: 0} verified · ${logbook["SUBMITTED"] ?: 0} awaiting review")
        ProgressCard("Evaluations / WBA", "${evaluations["APPROVED"] ?: evaluations["COMPLETED"] ?: 0} complete · ${evaluations["SUBMITTED"] ?: 0} awaiting review")
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
