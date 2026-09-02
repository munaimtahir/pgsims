package fmu.pg.sims

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import fmu.pg.sims.core.model.Role

class RoleContractTest {

    private val json = Json { ignoreUnknownKeys = true }

    @Test
    fun testOnlyFourCanonicalRolesExist() {
        val roles = Role.entries.map { it.name }
        assertEquals(4, roles.size)
        assertTrue(roles.contains("ADMIN"))
        assertTrue(roles.contains("RESIDENT"))
        assertTrue(roles.contains("SUPERVISOR"))
        assertTrue(roles.contains("SUPPORT_STAFF"))
    }

    @Test
    fun testRoleSerialization() {
        val adminJson = json.encodeToString(Role.ADMIN)
        assertEquals("\"ADMIN\"", adminJson)

        val residentJson = json.encodeToString(Role.RESIDENT)
        assertEquals("\"RESIDENT\"", residentJson)

        val supervisorJson = json.encodeToString(Role.SUPERVISOR)
        assertEquals("\"SUPERVISOR\"", supervisorJson)

        val staffJson = json.encodeToString(Role.SUPPORT_STAFF)
        assertEquals("\"SUPPORT_STAFF\"", staffJson)
    }

    @Test
    fun testRoleDeserialization() {
        val adminRole = json.decodeFromString<Role>("\"ADMIN\"")
        assertEquals(Role.ADMIN, adminRole)

        val residentRole = json.decodeFromString<Role>("\"RESIDENT\"")
        assertEquals(Role.RESIDENT, residentRole)

        val supervisorRole = json.decodeFromString<Role>("\"SUPERVISOR\"")
        assertEquals(Role.SUPERVISOR, supervisorRole)

        val staffRole = json.decodeFromString<Role>("\"SUPPORT_STAFF\"")
        assertEquals(Role.SUPPORT_STAFF, staffRole)
    }
}
