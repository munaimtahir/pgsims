# PGR SIMS Android

The Gradle project has two application modules and one shared theme module:

| Module | Role | Application ID | Status |
| --- | --- | --- | --- |
| `:app-portal` | Login-gated PGR SIMS client and current `PGR Companion` Play candidate | `pk.vexel.pgrcompanion` (`1.1.3`, code `3`) | Canonical |
| `:app-companion` | Offline residency portfolio | `pk.vexel.pgrcompanion` (`1.0.2`, code `2`) | Frozen historical track |
| `:core:common` | Shared Compose theme | N/A | Active shared library |

`app-portal` intentionally supersedes the historical Companion listing under the same package ID.
Do not install or release both tracks as competing production artifacts. The Companion module remains
only to preserve the prior offline release source and artifact provenance.

## Technology

Kotlin, Jetpack Compose, Material 3, Retrofit/OkHttp, Kotlin serialization, and encrypted
SharedPreferences for Portal session tokens. The project uses Gradle 8.7, AGP 8.5.2, Kotlin 2.0.0,
Java 17 bytecode, `minSdk 26`, and `compileSdk`/`targetSdk 36`.

## Build the canonical application

```bash
cd android
./gradlew :app-portal:testDebugUnitTest :app-portal:lintDebug :app-portal:assembleDebug
./gradlew :app-portal:assembleRelease :app-portal:bundleRelease \
  -PpgrCompanionSigningPropertiesFile=/owner/controlled/path/signing.properties
```

Release signing properties are external and must provide `storeFile`, `storePassword`, `keyAlias`,
and `keyPassword`. The release task fails rather than silently using a debug key when they are not
provided.

## Runtime boundary

Portal is login-gated and consumes the PGR SIMS backend over HTTPS. It supports sign-in, session
refresh/logout, resident onboarding/profile display and permitted edits, programme/training and
supervisor summaries, and requested-document upload. The backend remains authoritative for roles,
permissions, validation, and workflow status.

See `../PGR_SIMS_ANDROID_API_INTEGRATION.md` for endpoint contracts,
`../ANDROID_RELEASE_VERIFICATION.md` for release evidence, and `../SPRINT_STATE.md` for the live
release/rollout state.
