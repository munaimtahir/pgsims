package fmu.pg.sims.core.network

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

/**
 * DRF error bodies are typically `{"detail": "..."}`, `{"error": "..."}`, or
 * `{"field_name": ["msg", ...]}` for validation errors. Best-effort human-readable extraction;
 * falls back to the raw body so a failure is never silently swallowed.
 */
fun extractErrorDetail(rawBody: String?): String {
    if (rawBody.isNullOrBlank()) return "Something went wrong. Please try again."
    return try {
        val json = Json.parseToJsonElement(rawBody)
        if (json !is JsonObject) return rawBody
        (json["detail"] as? JsonPrimitive)?.contentOrNullString()
            ?: (json["error"] as? JsonPrimitive)?.contentOrNullString()
            ?: json.entries.firstOrNull()?.let { (key, value) ->
                val message = when (value) {
                    is JsonArray -> value.jsonArray.joinToString(" ") { it.jsonPrimitive.content }
                    is JsonPrimitive -> value.content
                    else -> value.toString()
                }
                if (key == "detail" || key == "error") message else "$key: $message"
            }
            ?: rawBody
    } catch (e: Exception) {
        rawBody
    }
}

private fun JsonPrimitive.contentOrNullString(): String? = if (this.isString || content.isNotBlank()) content else null
