package fmu.pg.sims.core.training

import fmu.pg.sims.core.model.NetworkResult
import fmu.pg.sims.core.model.ResidentTrainingRecordDto
import fmu.pg.sims.core.model.map
import fmu.pg.sims.core.network.ApiService
import fmu.pg.sims.core.network.safeCall

class TrainingRepository(private val apiService: ApiService) {

    /** Backend already scopes this list to the caller's own records for RESIDENT users. */
    suspend fun getMyTrainingRecords(): NetworkResult<List<ResidentTrainingRecordDto>> =
        safeCall { apiService.getResidentTrainingRecords() }.map { it.results }
}
