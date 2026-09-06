# SPRINT_STATE.md — Dual-track Android architecture

## Scope

Separate the Play-listed offline Companion from a separately-installable PGR SIMS Portal, verify
both builds, generate non-versioned release artifacts, and document the integration boundary.

## Completed work

- Identified baseline tag `play-closed-testing-baseline-1.0.0` and current `main` had the
  institutional client embedded in the Companion Play package.
- Created `:app-companion`, `:app-portal`, and `:core:common`; moved offline Companion and the
  PGR SIMS client into their respective product modules.
- Removed Companion's `INTERNET`, Retrofit, encrypted-token storage, and institutional UI.
- Portal is `pk.vexel.pgrportal.dev` with separate encrypted session storage and debug/staging/release builds.

## Completed work

- Both modules compile. `:app-companion:testDebugUnitTest`, `:app-portal:testDebugUnitTest`,
  both debug lint tasks, both signed release APK tasks, and both release bundle tasks passed.
- Portal release R8 was repaired by adding Tink's Error Prone annotation runtime dependency.
- Generated untracked APK/AAB plus metadata/reports under `builds/companion/` and `builds/portal/`.
- Added architecture, current-state, API-contract, parity, release, and Play-policy documentation.

## Pending work

1. Commit the dual-track implementation, leaving pre-existing untracked `.claude/` untouched.
2. Live device coexistence, staging authentication, and real staging upload require an emulator and
   provisioned staging resident/service. Confirm the Companion upload certificate in Play Console
   before any Play upload.
