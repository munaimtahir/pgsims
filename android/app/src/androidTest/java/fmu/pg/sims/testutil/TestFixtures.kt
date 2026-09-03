package fmu.pg.sims.testutil

import fmu.pg.sims.core.model.AuthMeResponse
import fmu.pg.sims.core.model.LoginResponse
import fmu.pg.sims.core.model.OnboardingField
import fmu.pg.sims.core.model.OnboardingSection
import fmu.pg.sims.core.model.OnboardingStateResponse
import fmu.pg.sims.core.model.ResidentDocumentDto
import fmu.pg.sims.core.model.ResidentTrainingRecordDto
import fmu.pg.sims.core.model.Role
import fmu.pg.sims.core.model.SupervisionOptionsResponse
import fmu.pg.sims.core.model.SupervisorOption
import fmu.pg.sims.core.model.User

/**
 * Deterministic fixtures mirroring real backend payload shapes (same fields
 * SerializationContractTest deserializes from JSON captured against the live dev server).
 */
object TestFixtures {
    const val VALID_USERNAME = "pgr002"
    const val VALID_PASSWORD = "correct-horse-battery-staple"

    fun user(role: Role = Role.RESIDENT) = User(
        id = 4,
        username = VALID_USERNAME,
        email = "pgr002@fmu.edu.pk",
        fullName = "Test Resident",
        role = role,
        mustChangePassword = false,
        isProfileComplete = true,
    )

    fun loginResponse() = LoginResponse(
        access = "fake-access-token",
        refresh = "fake-refresh-token",
        user = user(),
        mustChangePassword = false,
    )

    fun authMe(
        mustChangePassword: Boolean = false,
        reviewStatus: String = "NOT_SUBMITTED",
        reviewNote: String? = null,
        pendingUploadCount: Int = 0,
        role: Role = Role.RESIDENT,
    ) = AuthMeResponse(
        id = 4,
        username = VALID_USERNAME,
        role = role,
        mustChangePassword = mustChangePassword,
        isProfileComplete = true,
        profileId = 4,
        onboardingReviewStatus = reviewStatus,
        onboardingReviewNote = reviewNote,
        onboardingComplete = true,
        pendingUploadCount = pendingUploadCount,
    )

    private val personalFields = listOf(
        "full_name" to "Test Resident",
        "phone" to "03001234567",
        "email" to "pgr002@fmu.edu.pk",
        "registration_no" to "",
        "cnic" to "",
    )
    private val enrollmentFields = listOf(
        "hospital" to "1",
        "department_ref" to "1",
        "program_ref" to "1",
        "academic_session_ref" to "2026",
        "specialty_ref" to "MED",
        "training_start_date" to "2026-01-01",
        "expected_end_date" to "",
        "current_level" to "Year 1",
        "notes" to "",
    )

    /** Builds an OnboardingStateResponse with the two field sections the wizard screens read,
     * applying [fieldOverrides] on top of the defaults (used to simulate a save round-trip). */
    fun onboardingState(
        reviewStatus: String = "NOT_SUBMITTED",
        reviewNote: String = "",
        profileComplete: Boolean = true,
        supervisorStatus: String = "NOT_STARTED",
        fieldOverrides: Map<String, String?> = emptyMap(),
    ): OnboardingStateResponse {
        fun section(key: String, title: String, defaults: List<Pair<String, String>>) = OnboardingSection(
            key = key,
            title = title,
            fields = defaults.map { (field, default) ->
                OnboardingField(field = field, label = field, value = fieldOverrides[field] ?: default, required = true)
            },
        )
        return OnboardingStateResponse(
            profileComplete = profileComplete,
            onboardingComplete = profileComplete,
            requiredOnboardingFields = if (profileComplete) emptyList() else listOf("full_name"),
            supervisorStatus = supervisorStatus,
            reviewStatus = reviewStatus,
            reviewNote = reviewNote,
            sections = listOf(
                section("identity", "Personal Information", personalFields),
                section("enrollment", "Training & Enrollment", enrollmentFields),
            ),
            documents = emptyList(),
        )
    }

    fun documents(): List<ResidentDocumentDto> = listOf(
        ResidentDocumentDto(id = 101, residentId = 4, title = "CNIC Copy", status = "NOT_STARTED"),
        ResidentDocumentDto(id = 102, residentId = 4, title = "PM&DC Certificate", status = "VERIFIED"),
    )

    fun supervisionOptions() = SupervisionOptionsResponse(
        supervisors = listOf(
            SupervisorOption(id = 201, name = "Dr. Ayesha Khan", department = "Medicine", trainingSite = "Allied Hospital"),
            SupervisorOption(id = 202, name = "Dr. Bilal Ahmed", department = "Surgery", trainingSite = "DHQ Hospital"),
        ),
    )

    fun trainingRecord() = ResidentTrainingRecordDto(
        id = 301,
        residentUser = 4,
        residentName = "Test Resident",
        programName = "MS Surgery",
        currentLevel = "Year 1",
        active = true,
    )
}
