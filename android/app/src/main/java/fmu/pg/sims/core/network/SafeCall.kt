package fmu.pg.sims.core.network

import fmu.pg.sims.core.model.NetworkResult
import retrofit2.Response

/** Shared success/error mapping so every repository handles HTTP + network failure identically. */
suspend inline fun <T> safeCall(crossinline block: suspend () -> Response<T>): NetworkResult<T> {
    return try {
        val response = block()
        val body = response.body()
        if (response.isSuccessful && body != null) {
            NetworkResult.Success(body)
        } else {
            NetworkResult.Error(response.code(), extractErrorDetail(response.errorBody()?.string()))
        }
    } catch (e: Exception) {
        NetworkResult.Error(message = e.localizedMessage ?: "Network request failed", cause = e)
    }
}
