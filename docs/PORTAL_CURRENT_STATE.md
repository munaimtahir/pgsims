# Portal current state

`PGR Portal Dev` is an FMU-first institutional client (`pk.vexel.pgrportal.dev`), not a Companion
feature flag. It provides PGR SIMS sign-in, encrypted JWT restore/refresh/logout, resident
onboarding/profile updates, programme/training, supervisor assignment, documents, upload, and
resubmission. Server records, validation, RBAC, and completion state remain canonical.

`release` uses production; `staging` uses `https://staging.pgsims.alshifalab.pk/`. Live staging
verification needs that service and a dedicated resident account.
