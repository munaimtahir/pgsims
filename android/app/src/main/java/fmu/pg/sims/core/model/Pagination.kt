package fmu.pg.sims.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * DRF's default PageNumberPagination envelope. Some list endpoints return this
 * (resident-document-requirements, resident-training, supervision/assignments); others return a
 * bare array via a custom `list()` override (resident-documents, supervision/options) — this is
 * a genuine inconsistency in the backend, not an Android assumption, confirmed against the real
 * running dev server.
 */
@Serializable
data class PaginatedResponse<T>(
    @SerialName("count") val count: Int = 0,
    @SerialName("next") val next: String? = null,
    @SerialName("previous") val previous: String? = null,
    @SerialName("results") val results: List<T> = emptyList(),
)
