# PGR Companion — Android

`pk.vexel.pgrcompanion`, store name **PGR Companion: Residency**. Single Gradle module (`:app`),
Kotlin + Compose + Material 3, `minSdk 26` / `target & compileSdk 36`.

## What this app is

Two things, in this order, and the order is load-bearing:

1. A **standalone offline residency portfolio** for postgraduate trainees. No account, no network,
   no institution. This is what Google Play reviewed and approved, and it is currently in closed
   testing. It must keep working on its own and must never be put behind a login.
2. An **optional Institutional Workspace** that connects to the canonical PGR SIMS backend
   (`backend/`) when — and only when — a trainee's institution has issued them an account.

For workspace 2 the backend is the single source of truth for data, business rules, permissions and
validation; the app consumes its API rather than recreating logic locally, and never presents local
personal records as an institutional submission. Workspace 1 has no server and answers to nothing.

See the repository-root `INSTITUTIONAL_WORKSPACE_ARCHITECTURE.md` for the boundary,
`PGR_SIMS_ANDROID_API_INTEGRATION.md` for the verified API contracts, and
`ANDROID_RELEASE_VERIFICATION.md` for build and device verification.

## Layout

```
android/
├── app/src/main/java/pk/vexel/pgrcompanion/
│   ├── CompanionApplication.kt      LocalStore eagerly; institutional repository lazily
│   ├── LocalStore.kt                Personal Workspace persistence (offline, no network)
│   ├── MainActivity.kt              Theme, five-tab shell, personal screens
│   ├── InstitutionalRepository.kt   Optional PGR SIMS client: API, tokens, error mapping
│   └── InstitutionalScreen.kt       Optional Institution tab and its four states
├── app/src/debug/AndroidManifest.xml  Cleartext to emulator loopback, debug only
└── app/src/test/                    JVM unit tests, incl. MockWebServer coverage
```

`core/` and `feature/` are empty `.gitkeep` directories left over from an abandoned multi-module
architecture built under a different application id. They contain no code and are not in
`settings.gradle.kts`. Do not treat them as a spec.

## Build

```bash
cd android
./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
./gradlew :app:assembleRelease :app:bundleRelease \
  -PpgrCompanionSigningPropertiesFile=/owner/controlled/path/signing.properties
```

Release signing comes from an owner-readable properties file
(`storeFile`, `storePassword`, `keyAlias`, `keyPassword`) passed by Gradle property. No keystore and
no password is committed; a release build fails loudly if the property is missing rather than
quietly producing an unsigned artifact.

## House rules for this module

- The Personal Workspace must render before, and independently of, any institutional session.
  A network or institution failure belongs inside the Institution tab and nowhere else.
- Never log request bodies, tokens or passwords — in any build type.
- Institutional payload shapes are verified against the live backend before use, not inferred.
  When you change one, update `PGR_SIMS_ANDROID_API_INTEGRATION.md` in the same change.
- In-app privacy copy, the store listing and the Play Data Safety form have to keep agreeing with
  each other. If you add a data flow, all three move together.
