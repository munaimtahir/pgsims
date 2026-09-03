package fmu.pg.sims.testutil

import fmu.pg.sims.core.auth.TokenStorage
import fmu.pg.sims.core.model.Role

/** In-memory [TokenStorage] — avoids EncryptedSharedPreferences/Keystore in tests. */
class FakeTokenStorage(
    private var accessToken: String? = null,
    private var refreshToken: String? = null,
    private var role: Role? = null,
) : TokenStorage {
    override fun saveTokens(accessToken: String, refreshToken: String) {
        this.accessToken = accessToken
        this.refreshToken = refreshToken
    }

    override fun getAccessToken(): String? = accessToken
    override fun getRefreshToken(): String? = refreshToken
    override fun saveUserRole(role: Role) { this.role = role }
    override fun getUserRole(): Role? = role

    override fun clear() {
        accessToken = null
        refreshToken = null
        role = null
    }
}
