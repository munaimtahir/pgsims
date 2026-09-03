package fmu.pg.sims.core.documents

import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.ResidentDocumentDto
import fmu.pg.sims.core.model.ResidentDocumentRequirementDto
import fmu.pg.sims.core.model.map
import fmu.pg.sims.core.network.ApiService
import fmu.pg.sims.core.network.safeCall
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

class DocumentsRepository(private val apiService: ApiService) {

    suspend fun getRequirements(): NetworkResult<List<ResidentDocumentRequirementDto>> =
        safeCall { apiService.getDocumentRequirements() }.map { it.results }

    suspend fun getDocuments(): NetworkResult<List<ResidentDocumentDto>> =
        safeCall { apiService.getResidentDocuments() }

    suspend fun defer(documentId: Int): NetworkResult<ResidentDocumentDto> =
        safeCall { apiService.deferDocument(documentId) }

    suspend fun upload(documentId: Int, file: File, mimeType: String): NetworkResult<ResidentDocumentDto> {
        val requestBody = file.asRequestBody(mimeType.toMediaTypeOrNull())
        val part = MultipartBody.Part.createFormData("file", file.name, requestBody)
        return safeCall { apiService.uploadDocument(documentId, part) }
    }
}
