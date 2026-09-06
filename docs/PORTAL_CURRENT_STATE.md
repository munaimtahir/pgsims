# Portal current state

`PGR Portal Dev` is an FMU-first institutional client (`pk.vexel.pgrportal.dev`, version
`0.1.1-dev` / code `2`), not a Companion
feature flag. It provides PGR SIMS sign-in, encrypted JWT restore/refresh/logout, resident
onboarding/profile updates, programme/training, supervisor assignment, documents, upload, and
resubmission. Server records, validation, RBAC, and completion state remain canonical.

`release` uses production; `staging` is configured as `https://staging.pgsims.alshifalab.pk/`.
On 2026-09-06 the hostname had no DNS record, so staging is configured but not deployed/reachable.
Live staging verification needs a DNS/TLS-backed isolated service and dedicated resident account.

The rebuilt development artifacts are `builds/portal/PGR-Portal-0.1.1-dev.aab` (SHA-256
`f5d06bc2d9dba4a6d7bc63c6fac4b27788ec4294fca61f930858d6bfd0b69cfc`) and
`builds/portal/PGR-Portal-0.1.1-dev.apk` (SHA-256
`cce6574780c9d9ea28433400af3747a3bd7fda1b8886456dee1b068131505d45`).
