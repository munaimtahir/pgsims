package pk.edu.fmu.pgsims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class HealthStatus(
    @SerialName("status") val status: String,
    @SerialName("database") val database: String = "ok",
    @SerialName("app") val app: String = "pgms",
    @SerialName("version") val version: String = "v0.12",
)
