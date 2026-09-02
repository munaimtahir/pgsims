package fmu.pg.sims.core.network

import okhttp3.Interceptor
import okhttp3.Response
import fmu.pg.sims.core.auth.TokenStorage

class AuthInterceptor(private val tokenStorage: TokenStorage) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()
        val builder = original.newBuilder()
            .header("Accept", "application/json")

        val token = tokenStorage.getAccessToken()
        if (!token.isNullOrBlank() && original.header("Authorization") == null) {
            builder.header("Authorization", "Bearer $token")
        }

        return chain.proceed(builder.build())
    }
}
