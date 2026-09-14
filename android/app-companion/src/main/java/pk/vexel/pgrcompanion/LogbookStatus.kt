package pk.vexel.pgrcompanion

import java.util.Locale
import kotlinx.serialization.json.JsonObject

internal fun canonicalLogbookBucket(status: String): String = when (val value = status.trim().uppercase(Locale.ROOT)) {
    "VERIFIED", "APPROVED" -> "APPROVED"
    "RETURNED_FOR_REVISION", "RETURNED" -> "RETURNED"
    else -> value
}

internal fun logbookCounts(rows: List<JsonObject>): Map<String, Int> =
    rows.groupingBy { canonicalLogbookBucket(it.string("status").orEmpty()) }.eachCount()
