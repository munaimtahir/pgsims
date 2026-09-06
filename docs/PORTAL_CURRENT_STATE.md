# Portal current state

`PGR Portal Dev` is an FMU-first institutional client (`pk.vexel.pgrportal.dev`, version
`0.1.1-dev` / code `2`), not a Companion
feature flag. It provides PGR SIMS sign-in, encrypted JWT restore/refresh/logout, resident
onboarding/profile updates, programme/training, supervisor assignment, documents, upload, and
resubmission. Server records, validation, RBAC, and completion state remain canonical.

`release` uses production; `staging` is configured as `https://staging.pgsims.alshifalab.pk/`.
An isolated VM staging stack is now live on loopback port 18014 with dedicated Postgres/Redis/media
volumes and `android.demo.*` staging-only accounts. The API 36 Portal staging variant completed
live login and rendered canonical onboarding data through an SSH tunnel. The public hostname still
has no DNS record, so public HTTPS staging and full upload/resubmission workflow verification remain
open. See `docs/ANDROID_STAGING_E2E_VERIFICATION.md` and `docs/STAGING_ENVIRONMENT.md`.

The rebuilt development artifacts are `builds/portal/PGR-Portal-0.1.1-dev.aab` (SHA-256
`f5d06bc2d9dba4a6d7bc63c6fac4b27788ec4294fca61f930858d6bfd0b69cfc`) and
`builds/portal/PGR-Portal-0.1.1-dev.apk` (SHA-256
`cce6574780c9d9ea28433400af3747a3bd7fda1b8886456dee1b068131505d45`).
