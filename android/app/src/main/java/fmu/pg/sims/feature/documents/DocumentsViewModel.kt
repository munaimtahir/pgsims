package fmu.pg.sims.feature.documents

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fmu.pg.sims.core.documents.DocumentsRepository
import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.ResidentDocumentDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.io.File

/** Standalone documents-tab state — always re-derives outstanding status from the server. */
data class DocumentsUiState(
    val loading: Boolean = true,
    val error: String? = null,
    val documents: List<ResidentDocumentDto> = emptyList(),
    val busyIds: Set<Int> = emptySet(),
    val actionError: String? = null,
)

class DocumentsViewModel(private val documentsRepository: DocumentsRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(DocumentsUiState())
    val uiState: StateFlow<DocumentsUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(loading = true, error = null) }
            when (val result = documentsRepository.getDocuments()) {
                is NetworkResult.Success -> _uiState.update { it.copy(loading = false, documents = result.data) }
                is NetworkResult.Error -> _uiState.update { it.copy(loading = false, error = result.message) }
                is NetworkResult.Loading -> Unit
            }
        }
    }

    fun defer(documentId: Int) = act(documentId) { documentsRepository.defer(documentId) }

    fun upload(documentId: Int, file: File, mimeType: String) =
        act(documentId) { documentsRepository.upload(documentId, file, mimeType) }

    private fun act(documentId: Int, action: suspend () -> NetworkResult<ResidentDocumentDto>) {
        _uiState.update { it.copy(busyIds = it.busyIds + documentId, actionError = null) }
        viewModelScope.launch {
            when (val result = action()) {
                is NetworkResult.Success -> _uiState.update {
                    it.copy(
                        busyIds = it.busyIds - documentId,
                        documents = it.documents.map { d -> if (d.id == documentId) result.data else d },
                    )
                }
                is NetworkResult.Error -> _uiState.update {
                    it.copy(busyIds = it.busyIds - documentId, actionError = result.message)
                }
                is NetworkResult.Loading -> Unit
            }
        }
    }
}
