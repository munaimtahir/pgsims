# Portal current state

`PGR Portal Dev` is an FMU-first institutional client (`pk.vexel.pgrportal.dev`, version
`0.1.2-dev` / code `3`), not a Companion
feature flag. It provides PGR SIMS sign-in, encrypted JWT restore/refresh/logout, resident
onboarding/profile updates, programme/training, supervisor assignment, documents, upload, and
resubmission. Server records, validation, RBAC, and completion state remain canonical.

`release` uses production; `staging` is configured as `https://staging.pgsims.alshifalab.pk/`.
An isolated VM staging stack is publicly available at `https://staging.pgsims.alshifalab.pk/`,
with dedicated Postgres/Redis/media volumes and `android.demo.*` staging-only accounts. Live API
verification covers authentication, permitted profile update, training, supervisor assignment,
document states, upload, review feedback, and resubmission. See
`docs/ANDROID_STAGING_E2E_VERIFICATION.md` and `docs/STAGING_ENVIRONMENT.md`.

The rebuilt development artifacts are `builds/portal/PGR-Portal-0.1.2-dev.aab` (SHA-256
`5e26a98ed25ce69646562f0d9cca10d87355607b85784018d0a6efda6c4e6d88`) and
`builds/portal/PGR-Portal-0.1.2-dev.apk` (SHA-256
`00aceb7079be8149e3db50a7f6780b2a137fe7caf65408ba66c0a536c8741626`).
