# SPRINT_STATE.md — Companion release finalization and Portal staging closure

## Scope

Freeze/audit Companion 1.1.0 and close Portal staging/onboarding verification without using
production resident data or credentials. Starting verified commit: `d311e5d`.

## Completed work

- Confirmed frozen Companion AAB hash and preserved the unrelated untracked `.claude/` directory.
- Validated Companion AAB, generated connected-device APKs with bundletool, installed them on the
  API 36 emulator, and verified cold launch, local profile persistence, and offline restart.
- Audited Companion package/version/permissions/dependencies/signature and recorded SHA-256.
- Confirmed production health (`200`) and login method contract (`GET` → `405 Allow: POST`).
- Provisioned an isolated `pgsims-staging` Compose stack on the VM: unique database/Redis/media
  volumes, mode-600 ignored secrets, current migrations, healthy database/cache/Celery, and safe
  `android.demo.*` accounts. Public staging DNS/TLS is now live through a validated Caddy route.
- Live-tested VM staging login (valid/invalid), bearer identity/onboarding/documents/training/
  assignment reads, refresh, and authenticated logout/revocation. API 36 Portal staging logged in
  through an SSH tunnel and rendered canonical incomplete onboarding data.
- Fixed Portal logout to send the required bearer token and fixed staging variant shared-core
  resolution; staging unit tests and APK assembly passed.
- Added canonical staging fixtures for active training, primary supervisor, and document review
  states; public staging passed profile PATCH, upload, correction review, and resubmission.
- Final Android debug unit/lint/release APK/AAB build set passed. Targeted backend authentication,
  onboarding and security suite passed 38 tests. Portal is now `0.1.2-dev` / code `3`.
- Installed Companion and Portal together on API 36; both packages coexist and Portal launch is sound.
- Corrected stale Companion wording in the separate Portal login UI; final Portal release artifacts
  are `0.1.2-dev` / code `3`.

## Pending work

1. Manual/API-36 closure: install final `0.1.2-dev`, verify session restoration, Android document
   picker upload, logout, and Portal-uninstall isolation against public staging.
2. External: compare Companion upload certificate in Play Console.
