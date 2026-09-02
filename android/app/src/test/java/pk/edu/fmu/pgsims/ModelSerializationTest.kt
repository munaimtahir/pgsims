package pk.edu.fmu.pgsims

import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import pk.edu.fmu.pgsims.core.model.AuthMeResponse
import pk.edu.fmu.pgsims.core.model.AuthTokens
import pk.edu.fmu.pgsims.core.model.HealthStatus
import pk.edu.fmu.pgsims.core.model.Role
import pk.edu.fmu.pgsims.core.model.User

class ModelSerializationTest {

    private val json = Json {
        ignoreUnknownKeys = true
        coerceInputValues = true
    }

    @Test
    fun testUserDeserialization() {
        val rawJson = """
            {
                "id": 42,
                "username": "pgr001",
                "email": "pgr001@example.com",
                "first_name": "Fatima",
                "last_name": "Ali",
                "full_name": "Fatima Ali",
                "display_name": "Dr. Fatima Ali",
                "role": "RESIDENT",
                "specialty": "MEDICINE",
                "year": 2,
                "is_active": true,
                "must_change_password": false,
                "is_profile_complete": true
            }
        """.trimIndent()

        val user = json.decodeFromString<User>(rawJson)
        assertEquals(42, user.id)
        assertEquals("pgr001", user.username)
        assertEquals(Role.RESIDENT, user.role)
        assertEquals("Fatima Ali", user.fullName)
        assertTrue(user.isActive)
        assertFalse(user.mustChangePassword)
        assertTrue(user.isProfileComplete)
    }

    @Test
    fun testAuthMeResponseDeserialization() {
        val rawJson = """
            {
                "id": 10,
                "username": "sup001",
                "role": "SUPERVISOR",
                "must_change_password": false,
                "is_profile_complete": false,
                "profile_type": "SUPERVISOR",
                "profile_id": 5,
                "profile_status": "INCOMPLETE",
                "profile_schema_version": 1,
                "completed_schema_version": 0,
                "missing_required_fields": ["pmdc_no", "department_ref"],
                "allowed_next_route": "/complete-profile"
            }
        """.trimIndent()

        val authMe = json.decodeFromString<AuthMeResponse>(rawJson)
        assertEquals(10, authMe.id)
        assertEquals("sup001", authMe.username)
        assertEquals(Role.SUPERVISOR, authMe.role)
        assertFalse(authMe.isProfileComplete)
        assertEquals(2, authMe.missingRequiredFields.size)
        assertEquals("/complete-profile", authMe.allowedNextRoute)
    }

    @Test
    fun testHealthStatusDeserialization() {
        val rawJson = """
            {
                "status": "ok",
                "database": "ok",
                "app": "pgms",
                "version": "v0.12"
            }
        """.trimIndent()

        val health = json.decodeFromString<HealthStatus>(rawJson)
        assertEquals("ok", health.status)
        assertEquals("ok", health.database)
        assertEquals("pgms", health.app)
        assertEquals("v0.12", health.version)
    }

    @Test
    fun testAuthTokensDeserialization() {
        val rawJson = """
            {
                "access": "jwt-access-token-123",
                "refresh": "jwt-refresh-token-456"
            }
        """.trimIndent()

        val tokens = json.decodeFromString<AuthTokens>(rawJson)
        assertEquals("jwt-access-token-123", tokens.access)
        assertEquals("jwt-refresh-token-456", tokens.refresh)
    }
}
