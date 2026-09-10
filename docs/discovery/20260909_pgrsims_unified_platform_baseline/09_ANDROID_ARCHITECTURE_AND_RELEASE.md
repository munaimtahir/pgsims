# 09 — Android Baseline Facts, Architecture, Auth/Security, Release State

Scope: PGR Companion Android app only. Verified directly against source on 2026-09-09; not derived
from docs alone. Vexel MedSIMS (`pk.vexel.medsims`) is an explicitly out-of-scope, unrelated
product — a repo-wide grep (`grep -rli medsims android/ docs/ *.md`) found **zero references**
anywhere in the current tree. No contamination risk found.

## 1. Baseline facts (from source)

Source: `android/app-companion/build.gradle.kts` (read directly, 2026-09-10).

| Field | Value | Evidence |
|---|---|---|
| `applicationId` | `pk.vexel.pgrcompanion` | `build.gradle.kts:19` |
| `namespace` | `pk.vexel.pgrcompanion` | `build.gradle.kts:12` |
| `versionCode` | `4` | `build.gradle.kts:22` |
| `versionName` | `1.1.4` | `build.gradle.kts:23` |
| `compileSdk` / `targetSdk` / `minSdk` | 36 / 36 / 26 | `build.gradle.kts:13,20-21` |
| Production API base | `https://android.pgsims.alshifalab.pk/` | `buildConfigField "INSTITUTIONAL_API_BASE_URL"`, `build.gradle.kts:25` |
| Staging API base | `https://staging.pgsims.alshifalab.pk/` (default; overridable via `-PpgrCompanionStagingBaseUrl`) | `build.gradle.kts` |
| Build types | `debug` (`.debug` suffix, debuggable), `staging` (`.staging` suffix, debug-derived, own base URL), `release` (minified, shrunk, signed) | `build.gradle.kts:64-83` |
| Signing | `signingConfigs.release` reads `storeFile/storePassword/keyAlias/keyPassword` from an externally supplied `-PpgrCompanionSigningPropertiesFile`; task **errors out** (does not silently fall back to debug signing) if release signing is requested and any key is missing or the keystore file doesn't exist (`build.gradle.kts:29-61`). No keystore or credential is committed to the repo (confirmed: no `.jks`/`.keystore` file under `android/`, no plaintext password in `build.gradle.kts` or `gradle.properties`). Key identity (SHA-256 `a858f42c...b61f010`) is documented, not embedded. |

The repository has since been consolidated to one module: `android/app-companion`, version
`1.1.7`/code `7`, package `pk.vexel.pgrcompanion`.

## 2. Module classification

| Module | Package | Classification | Evidence |
|---|---|---|---|
| `android/app-companion` | `pk.vexel.pgrcompanion` | **CANONICAL AND ONLY MODULE** | Included in `settings.gradle.kts`, built by CI and release scripts, version `1.1.7`/code `7`; login-gated institutional client. |
| `core:common` | N/A (library) | Active shared library | Shared Compose theme (`PgrTheme`) only, used by both app modules; not a feature/business-logic layer. |

**Package-ID rule**: the single module ships the immutable Google Play package
`applicationId pk.vexel.pgrcompanion`.

## 3. Architecture audit

Source: `android/app-companion/src/main/java/pk/vexel/pgrcompanion/` — Kotlin sources for the single app
(`InstitutionalRepository.kt`, `InstitutionalScreen.kt`, `Onboarding.kt`, `CompanionActivity.kt`,
`CompanionApplication.kt`, and workflow screens).

- **Navigation**: no Compose Navigation library (`androidx.navigation`) is used or declared as a
  dependency. Navigation is a single Activity (`CompanionActivity`) rendering one root Composable
  (`InstitutionalWorkspace`) that manages a `ResidentDestination` enum (`HOME, TRAINING, LOGBOOK,
  REQUIREMENTS, PROFILE` — `InstitutionalScreen.kt:62-67`) via a `NavigationBar`/`NavigationBarItem`
  (Material3 bottom bar, `InstitutionalScreen.kt:311-313`) driven by plain `remember { mutableStateOf(...) }`
  tab-selection state. This is intentionally minimal for 5 flat tabs; it would need real
  Navigation-Compose (or at least a nav-state abstraction) before adding deep-linkable sub-screens
  (e.g., a logbook entry detail screen reachable independently of its tab).
- **State holders**: **no `ViewModel` classes exist anywhere in the module** (confirmed by grep — 0
  matches for `ViewModel` under `android/app-companion/src`). All state (`snapshot`, `error`, `notice`,
  `busy`, `reloadKey`, form field values) is held as `remember`/`mutableStateOf` inside the root
  `InstitutionalWorkspace` Composable and passed down, with `rememberCoroutineScope()` used to
  launch repository calls directly from UI callbacks. This works for the current single-screen-tree
  app but does not survive configuration changes as robustly as a ViewModel would (Compose
  `remember` state is lost on process death, only `rememberSaveable` survives it, and this code uses
  plain `remember`, not `rememberSaveable`, for `snapshot`/`state`) — a real gap versus platform
  best practice, filed in the bug register.
- **Repository/API layer**: one repository class, `InstitutionalRepository`
  (`InstitutionalRepository.kt:176-`), wraps a Retrofit interface `InstitutionalApi`
  (`InstitutionalRepository.kt:81-101`) built on OkHttp + kotlinx.serialization
  (`Retrofit.Builder()...addConverterFactory` via kotlinx-serialization converter,
  `InstitutionalRepository.kt:208-213`). All 15 backend endpoints the client calls are declared
  here (auth, onboarding, documents, training, rotations, supervision assignments, logbook CRUD +
  submit, assessments, research, workshops, resident summary) — see full endpoint list already
  documented and independently verified in `PGR_SIMS_ANDROID_API_INTEGRATION.md`.
- **DTOs**: minimal and mostly *not* used — the client parses raw `kotlinx.serialization.json.JsonObject`/`JsonArray`
  responses with small extension helpers (`.value(key)`, `.child(key)`, `.flag(key)`,
  `.optionalArray(...)`, `InstitutionalRepository.kt:331-403`) rather than typed response DTOs for
  most reads. Only request bodies are typed `@Serializable data class`es (`LoginPayload`,
  `RefreshPayload`, `LogoutPayload`, `FieldPatch`, `AcademicLogbookPayload`,
  `InstitutionalRepository.kt:54-79`). This is a deliberate low-ceremony choice that trades
  compile-time schema safety for speed against a backend whose response shapes are still settling
  (confirmed by SPRINT_STATE.md's note about correcting the rotation shape post-hoc) — reasonable
  for the current stage, but a scaling risk if the JSON surface grows much further without any
  typed models.
- **Session/token storage**: `EncryptedTokenStore` (`InstitutionalRepository.kt:120-144`) wraps
  Android `EncryptedSharedPreferences` (Tink/AndroidX Security Crypto), created via
  `EncryptedTokenStore.create(context)` with a fallback to `InMemoryTokenStore`
  (`InstitutionalRepository.kt:131-151`) if encrypted storage construction fails (e.g. corrupted
  keystore) — degrades gracefully rather than crashing, at the cost of losing persistence in that
  edge case. Tokens are excluded from Android backup/D2D transfer explicitly
(`android/app-companion/src/main/res/xml/data_extraction_rules.xml`, `backup_rules.xml` — excludes
  `institutional_session.xml` and the Tink-encrypted-prefs file from both cloud-backup and
  device-transfer paths), and `android:allowBackup="false"` at the manifest level as a second layer.
- **Error handling**: centralized HTTP-status → message mapping (`loginErrorFor`, `errorFor`,
  `InstitutionalRepository.kt:384-403`): 401 "session expired", 403 "not permitted", 429 "too many
  attempts", 5xx "server unavailable", `IOException` → "unreachable" — no raw exception text or
  stack trace is surfaced to the UI.
- **Loading states**: a single `busy: Boolean` flag gates the whole workspace (not per-tab/per-call
  granular loading), acceptable for the current scope but coarse — a slow logbook submit blocks the
  whole UI's loading indicator, not just that action.
- **File picker/upload**: Storage Access Framework via `ActivityResultContracts` (implied by
  `displayNameOf(context, uri)` in `CompanionActivity.kt:21-27`, resolving `OpenableColumns.DISPLAY_NAME`)
  feeding `InstitutionalRepository.upload()` (`InstitutionalRepository.kt:277-`), which does
  client-side size/extension validation (`validateUpload`, `InstitutionalRepository.kt:364-`)
  mirroring the server's 10 MB / `.pdf .jpg .jpeg .png .doc .docx` rule before sending — matches
  `PGR_SIMS_ANDROID_API_INTEGRATION.md`'s documented behavior exactly.

**Can the current architecture support Assessments/Research/Workshops without a major rewrite?**
Yes for continuing the current read-only-summary pattern (it already does, trivially, via the same
repository/JsonObject approach). **Marginal but workable** for adding real submission/edit flows
(assessment responses, research milestones, workshop registration) in the same style as Logbook —
the repository/Retrofit/error-handling scaffold generalizes fine. The one real constraint is the
**lack of ViewModels and Navigation-Compose**: as more screens/sub-flows are added, the single
root-Composable-with-`remember`-state pattern will become harder to reason about and more prone to
state-loss-on-recreation bugs. Recommend introducing ViewModels and Navigation-Compose before (not
necessarily blocking) a third or fourth full CRUD domain is added — not a rewrite, an incremental
adoption.

## 4. Auth/security baseline

- **Login flow**: username/password form → `POST /api/auth/login/` → stores `access`/`refresh` via
  `EncryptedTokenStore.save()` (`InstitutionalRepository.kt:217-232`).
- **Token storage**: `EncryptedSharedPreferences` (AndroidX Security Crypto / Tink), file name
  `institutional_session.xml`, excluded from backup/device-transfer as above. No plaintext token
  storage path found.
- **Refresh**: `refreshToken()` (`InstitutionalRepository.kt:316-`) called on a `401`; a **separate**
  unauthenticated Retrofit client issues `POST /api/auth/refresh/` (bearer interceptor is only
  attached to the authorized client, not the refresh/logout client — `InstitutionalRepository.kt`
  around `authorized()`/`call()`, matching `PGR_SIMS_ANDROID_API_INTEGRATION.md`'s documented
  behavior). Refresh rotates the refresh token per the backend contract.
- **401 retry**: `authorized()` wrapper (`InstitutionalRepository.kt:302-`) refreshes once and
  replays the original request; a failed refresh clears the session (forces re-login) rather than
  looping.
- **Logout**: `logout()` (`InstitutionalRepository.kt:289-301`) calls `POST /api/auth/logout/`
  (server-side blacklist) then clears local tokens regardless of server response.
- **Session restoration**: `isConnected()` checks for non-blank access+refresh tokens at Activity
  start and jumps straight to `CONNECTED` state without a redundant login round-trip — confirmed
  working post-force-stop in `ANDROID_RELEASE_VERIFICATION.md` item 19 (survives R8 + Tink keep
  rules in the actual signed release build).
- **Secret redaction in logs**: `LoginPayload`, `RefreshPayload`, `LogoutPayload` all override
  `toString()` to mask their sensitive field (`***`) so Kotlin's default data-class `toString()`
  can't leak credentials/tokens into any log line that stringifies the object
  (`InstitutionalRepository.kt:54-63`), and there is a dedicated `CredentialRedactionTest.kt` unit
  test (1 test, passing) guarding this. No `Log.*`/`println`/`Timber` calls exist anywhere in
  `android/app-companion/src/main` (confirmed by grep — zero matches), so there is no first-party log
  surface to leak through in the first place. `ANDROID_RELEASE_VERIFICATION.md` item 22 independently
  confirms a 3,475-line logcat scan of the signed release build found zero password/JWT/Bearer
  matches.
- **HTTPS enforcement**: `android:usesCleartextTraffic="false"` in the manifest
  (`AndroidManifest.xml`), production/staging both use `https://` base URLs
  (`build.gradle.kts:25,74`); no cleartext debug-network-security-config override file exists under
  `android/app-companion/src/debug/` (the directory contains no files at all — contrary to what might
  be inferred from the module having a `debug/res/xml` path reference; verified empty by direct
  listing on 2026-09-09). Only the `staging` build type has its own network-security-adjacent
  concern, and that's solely the configurable base URL via Gradle property, not a cleartext
  allowance.

No security gaps found in this pass beyond the architectural note above (ViewModel/state-survival)
and the un-executed live-upload-success path noted in the feature matrix.

## 5. Release state summary

| | |
|---|---|
| Version | `1.1.4`, versionCode `4` |
| Package | `pk.vexel.pgrcompanion` |
| Branch / tag | `main`; tag `v1.1.4` exists (confirmed: `git tag` lists `v1.1.4`) |
| Source freeze commit | `4f8e27624c0c01c6dadd82322220ad06b99cdc51` (per `ANDROID_RELEASE_1.1.4.md`) |
| Signing identity | Same upload key as prior releases, certificate SHA-256 `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`, supplied externally via `-PpgrCompanionSigningPropertiesFile`; keystore location is host-external (`~/.config/pgr-companion/signing/`, per `ANDROID_RELEASE_VERIFICATION.md`), not present in this repo — contents not inspected or exfiltrated, only the documented fingerprint checked. |
| Artifacts | APK/AAB build outputs and their SHA-256 hashes recorded in `ANDROID_RELEASE_1.1.4.md`; not re-verified byte-for-byte in this pass (no `assembleRelease`/`bundleRelease` run — signing secrets are not available in this environment, per task instruction). |
| In-repo verification claims | Clean Gradle test/lint PASS, signed APK/AAB PASS, API-36 emulator smoke PASS, production API + correction/resubmission E2E PASS, crash buffer clean — all per `ANDROID_RELEASE_1.1.4.md` (this pass independently re-ran `testDebugUnitTest`/`lintDebug` only; see `10_TEST_AND_CI_BASELINE.md`). |
| Play Console status | **Not verifiable from this repo.** `ANDROID_RELEASE_1.1.4.md` states "Version code 4 is confirmed available by the owner. The AAB is ready for Google Play upload. Play Console upload and Data Safety/App Access configuration remain external console actions and were not performed by this release freeze." `docs/ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md` (last updated for the *prior* `1.1.3` release) shows Play Console-side steps (store listing, Data Safety, reviewer access, screenshots) marked done by the user as of 2026-09-08 for `1.1.3`; there is no equivalent checklist entry yet confirming the same steps were repeated for `1.1.4`. This report makes no claim about actual Play Store review/publication status beyond what is written in these two files — that must be confirmed externally in Play Console. |

**Doc gap flagged**: `docs/ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md` was not updated for `1.1.4`
(still references `versionCode 3`/`1.1.3` as "the release candidate" throughout) even though
`ANDROID_RELEASE_1.1.4.md` documents a newer, already-signed `1.1.4` build. This is a real
process gap, not just wording drift: whoever uploads `1.1.4` to Play Console has no `1.1.4`-specific
checklist to follow. Filed as P1 in `12_BUG_TECH_DEBT_REGISTER.md`.
