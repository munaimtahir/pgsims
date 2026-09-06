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
  `android.demo.*` accounts. The public staging DNS record still does not exist.
- Live-tested VM staging login (valid/invalid), bearer identity/onboarding/documents/training/
  assignment reads, refresh, and authenticated logout/revocation. API 36 Portal staging logged in
  through an SSH tunnel and rendered canonical incomplete onboarding data.
- Fixed Portal logout to send the required bearer token and fixed staging variant shared-core
  resolution; staging unit tests and APK assembly passed.
- Installed Companion and Portal together on API 36; both packages coexist and Portal launch is sound.
- Corrected stale Companion wording in the separate Portal login UI; rebuilt Portal `0.1.1-dev`/
  code `2`, then reran both Android unit/lint/release APK/AAB task sets successfully.

## Pending work

1. Extend staging fixtures using canonical services with programme, supervisor and reviewed-document
   states; run live profile PATCH, upload/resubmission, session restore and uninstall isolation.
2. Deploy DNS/TLS-backed public staging at `staging.pgsims.alshifalab.pk` using the documented
   Caddy fragment; this needs DNS control.
3. Run final Android release/lint tests, commit/push documentation, and compare Companion upload
   certificate in Play Console.
