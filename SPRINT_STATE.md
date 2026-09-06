# SPRINT_STATE.md — Android release and staging verification

## Scope

Freeze/audit Companion 1.1.0 and close Portal staging/onboarding verification without using
production resident data or credentials.

## Completed work

- Confirmed `main` at `05451a9` baseline and preserved the unrelated untracked `.claude/` directory.
- Validated Companion AAB, generated connected-device APKs with bundletool, installed them on the
  API 36 emulator, and verified cold launch, local profile persistence, and offline restart.
- Audited Companion package/version/permissions/dependencies/signature and recorded SHA-256.
- Confirmed production health (`200`) and login method contract (`GET` → `405 Allow: POST`).
- Classified `https://staging.pgsims.alshifalab.pk/` as configured-but-not-deployed: DNS resolution
  fails. No staging service, database, or dedicated account can safely be exercised.
- Installed Companion and Portal together on API 36; both packages coexist and Portal launch is sound.
- Corrected stale Companion wording in the separate Portal login UI; rebuilt Portal `0.1.1-dev`/
  code `2`, then reran both Android unit/lint/release APK/AAB task sets successfully.

## Pending work

1. Commit/push verification evidence without artifacts or credentials.
2. External: deploy DNS/TLS-backed staging with isolated database/secrets, seed a dedicated resident,
   then run live Portal login/onboarding/upload/resubmission and uninstall-isolation tests.
4. External: compare Companion SHA-256 signing certificate with the Play Console upload key.
