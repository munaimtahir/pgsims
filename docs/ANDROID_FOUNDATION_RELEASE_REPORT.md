# PGR SIMS ANDROID — FOUNDATION TO INTERNAL-TESTING RELEASE REPORT
**Phase M1 + M2 Foundation Closure**
*Date: September 2, 2026*
*Platform: PGR SIMS / Faisalabad Medical University (FMU)*
*Application ID: `pk.edu.fmu.pgsims`*
*Target Android Version: Android 15 (API level 35) | Minimum: Android 8.0 Oreo (API level 26)*
*Status: GO (Production Platform Foundation Complete)*

---

## 1. Executive Summary

This mega-sprint successfully closes **Phase M1 (Security Remediation & API Contract Baseline)** and **Phase M2 (Android Production Platform Foundation & Play-Ready AAB)**.

The project has advanced from discovery state (Phase M0) to a **real, buildable, installable, production-architected Android application** with a signed, optimized release Android App Bundle (`app-release.aab`) ready for distribution via Google Play Internal Testing.

In strict adherence to the project governance and product policy, **no substantive resident onboarding UI was built in this sprint**. The deliverable is the hardened platform, security layer, network and authentication core, and branded launchable testing shell.

---

## 2. Security Remediation (Wave A - Four M0 P0 Blockers)

All four critical security blockers identified in Phase M0 were resolved and backed with comprehensive automated regression tests.

### P0-1: Self-Profile Privilege Escalation Protection
- **Vulnerability**: `PATCH /api/auth/profile/update/` previously accepted arbitrary fields via `UserSerializer`, permitting self-elevation to `ADMIN` or disabling accounts.
- **Remediation**:
  - Implemented [`SelfProfileUpdateSerializer`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/serializers.py#L48-L92) with an explicit allow-list of self-editable attributes (`first_name`, `last_name`, `phone_number`, `email`).
  - Read-only protection enforced for administrative fields (`role`, `is_active`, `username`, `is_staff`, `is_superuser`, `is_profile_complete`, `must_change_password`, `is_archived`, `date_joined`, `specialty`, `year`, `registration_number`).
  - Validation explicitly detects and rejects any payload attempting to mutate protected fields with HTTP `400 Bad Request`.
- **Validation**: Verified in `test_self_profile_update_cannot_elevate_role_to_admin`, `test_self_profile_update_cannot_mutate_is_active`, `test_self_profile_update_cannot_mutate_username`, and `test_self_profile_update_allows_safe_fields`.

### P0-2: Role-Profile API Scoping & Authorization Hardening
- **Vulnerability**: `AdminProfileViewSet`, `ResidentProfileViewSet`, `SupervisorProfileViewSet`, and `SupportStaffProfileViewSet` exposed unauthenticated or over-permissive list/detail/mutation operations.
- **Remediation**:
  - Applied `get_queryset()` filtering across all four viewsets in [`userbase_views.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py#L416-L498).
  - Non-administrators cannot list admin profiles (returns empty queryset).
  - Residents can only retrieve and view their own profile.
  - Supervisors can only view profiles of residents actively assigned to them via `ResidentSupervisorAssignment`.
  - Profile mutation (`create`, `update`, `partial_update`, `destroy`) restricted strictly to administrators or authenticated self-updates on safe fields.
- **Validation**: Verified in `test_resident_cannot_list_admin_profiles`, `test_resident_cannot_retrieve_other_resident_profile`, `test_resident_cannot_mutate_other_resident_profile`, `test_unassigned_supervisor_cannot_view_resident_profile`, `test_assigned_supervisor_can_view_resident_profile`, and `test_admin_can_view_any_resident_profile`.

### P0-3: Protected Resident Document Storage & Delivery
- **Vulnerability**: Caddy was configured to serve `/media/*` directly from disk with public cache headers; document downloads lacked authorization checks.
- **Remediation**:
  - Updated [`deploy/Caddyfile.pgsims`](file:///home/munaim/srv/apps/pgsims/deploy/Caddyfile.pgsims#L28-L32) to route media requests through Django rather than serving raw files publicly.
  - Implemented `@action(detail=True, methods=["get"], url_path="file")` on [`ResidentDocumentViewSet`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/onboarding_api.py#L294-L390).
  - Document access enforces: Admin OR Resident Owner OR Assigned Supervisor (via `ResidentSupervisorAssignment`).
  - File streaming uses Django `FileResponse` with secure headers: `Cache-Control: private, no-cache, no-store, must-revalidate`, `X-Content-Type-Options: nosniff`.
  - File upload sanitizes filenames (preventing path traversal) and enforces a strict extension allow-list (`.pdf`, `.jpg`, `.jpeg`, `.png`, `.doc`, `.docx`) and 10MB size limit.
- **Validation**: Verified in `test_unauthenticated_cannot_access_resident_document`, `test_unrelated_resident_cannot_access_document`, `test_unassigned_supervisor_cannot_access_document`, `test_document_owner_can_access_document`, `test_assigned_supervisor_can_access_document`, and `test_admin_can_access_document`.

### P0-4: Canonical Supervisor Assignment Enforcement on Progress Endpoint
- **Vulnerability**: `SupervisorResidentProgressView` (`/api/supervisors/residents/{resident_id}/progress/`) returned resident progress to any supervisor regardless of whether an active assignment existed (IDOR).
- **Remediation**:
  - Updated [`SupervisorResidentProgressView`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/views.py#L1826-L1855) to verify active `ResidentSupervisorAssignment` between the requesting supervisor and the requested resident. Non-assigned supervisors receive HTTP `403 Forbidden`.
- **Validation**: Verified in `test_unassigned_supervisor_cannot_access_resident_progress`, `test_assigned_supervisor_can_access_resident_progress`, and `test_admin_can_access_resident_progress`.

---

## 3. Session & Authentication Hardening (Waves B & C)

### JWT Token Blacklist on Logout
- Added `rest_framework_simplejwt.token_blacklist` to `INSTALLED_APPS` and applied database migrations (`token_blacklist.0001` through `0013`).
- Enabled `ROTATE_REFRESH_TOKENS = True` and `BLACKLIST_AFTER_ROTATION = True` in `SIMPLE_JWT` settings.
- Hardened `POST /api/auth/logout/` to blacklist the refresh token, invalidating further token refresh attempts.
- Verified in `test_jwt_logout_blacklists_refresh_token`.

### Password Strength Validation
- Added Django `validate_password` checks to `change_password_view` (`POST /api/auth/change-password/`) and `password_reset_confirm_view` (`POST /api/auth/password-reset/confirm/`).
- Weak, short, or common passwords are now rejected with clear validation messages.
- Verified in `test_change_password_validates_password_strength`.

---

## 4. Android Production Foundation (Phase M2)

### Build Toolchain & System Architecture
| Property | Value |
|---|---|
| **Application ID** | `pk.edu.fmu.pgsims` |
| **Compile SDK** | Android 15 (API 35) |
| **Target SDK** | Android 15 (API 35) |
| **Minimum SDK** | Android 8.0 Oreo (API 26) |
| **Version Code** | `1` |
| **Version Name** | `0.1.0` |
| **Gradle / AGP** | Gradle 8.7 / Android Gradle Plugin 8.5.2 |
| **Kotlin** | Kotlin 2.0.0 with Compose Compiler plugin |
| **UI Framework** | Jetpack Compose + Material 3 |
| **Networking** | Retrofit 2.11 + OkHttp 4.12 + Kotlinx Serialization 1.6.3 |
| **Secure Storage** | AndroidX Security Crypto 1.1.0-alpha06 (AES-256 GCM) |

### Core Architecture Implementation
1. **`core/model`**:
   - [`Role.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/model/Role.kt): The 4 canonical roles (`ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`).
   - [`User.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/model/User.kt): User and `AuthMeResponse` schemas matching the backend contract.
   - [`AuthTokens.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/model/AuthTokens.kt), [`HealthStatus.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/model/HealthStatus.kt), [`OnboardingState.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/model/OnboardingState.kt).
2. **`core/designsystem`**:
   - FMU Emerald Brand Palette (`#059669`, `#047857`, `#10B981`) and Material 3 Color Schemes.
   - Custom Typography and Shape scales.
   - [`PgsimsTheme.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/designsystem/Theme.kt).
3. **`core/network`**:
   - [`ApiService.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/network/ApiService.kt): Health check, JWT login, refresh, logout, profile endpoints.
   - [`AuthInterceptor.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/network/AuthInterceptor.kt): Bearer token injection and content-negotiation headers.
   - [`ApiClient.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/network/ApiClient.kt): Retrofit builder with Kotlinx JSON converter.
4. **`core/auth`**:
   - [`TokenStorage.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/auth/TokenStorage.kt): EncryptedSharedPreferences implementation.
   - [`AuthRepository.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/core/auth/AuthRepository.kt): StateFlow-based authentication session management.
5. **`ui`**:
   - [`FoundationScreen.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/ui/FoundationScreen.kt): Minimal branded platform foundation testing shell with live backend connectivity verification.
   - [`MainActivity.kt`](file:///home/munaim/srv/apps/pgsims/android/app/src/main/java/pk/edu/fmu/pgsims/ui/MainActivity.kt): ComponentActivity rendering `PgsimsTheme`.

---

## 5. Artifact Verification & Build Outputs

| Artifact | Type | Size | Path |
|---|---|---|---|
| **`app-debug.apk`** | Debug APK | 17 MB | `android/app/build/outputs/apk/debug/app-debug.apk` |
| **`app-release.aab`** | Play Release Bundle | 2.7 MB | `android/app/build/outputs/bundle/release/app-release.aab` |

*Release Signing: Signed with `release.keystore` using SHA256withRSA 2048-bit key (`pgsims-key`).*

---

## 6. Verification Results

| Suite | Status | Details |
|---|---|---|
| **Backend Security Tests** (`test_security_remediation_m1.py`) | **PASS** | 21/21 tests passed (100%) |
| **Backend Userbase Tests** (`test_userbase_api.py`) | **PASS** | 21/21 tests passed (100%) |
| **Identity Repair Command** (`repair_identity_profiles`) | **PASS** | 0 orphan records, final status PASS |
| **Update 0 Gate Script** (`check_update_0_identity_cleanup.sh`) | **PASS** | Gate PASS |
| **Frontend Typecheck** (`npm run typecheck`) | **PASS** | 0 errors |
| **Frontend Lint** (`npm run lint`) | **PASS** | 0 warnings, 0 errors |
| **Frontend Build** (`npm run build`) | **PASS** | 79/79 static routes generated |
| **Android Unit Tests** (`./gradlew test`) | **PASS** | 49 tasks executed, 100% passed |
| **Android Release Bundle** (`./gradlew bundleRelease`) | **PASS** | `BUILD SUCCESSFUL` |

---

## 7. Final Verdict

**VERDICT: GO**

The Phase M1 + M2 foundation closure is complete, fully verified, secure, and ready for deployment to Google Play Internal Testing.
