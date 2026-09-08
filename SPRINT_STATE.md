# SPRINT_STATE.md — PGR Companion production resident expansion

## Scope

Expand `android/app-portal` from resident foundation commit
`ed1d137c76beec33ddc7cb2c6140fc01a94102de` into the production PGR SIMS resident client. The
owner has explicitly authorized production integration/deployment only after a safe synthetic
resident, production state, migrations, and rollback path are verified. Preserve `.claude/`.

## Completed work

- Confirmed local `main`, `origin/main`, and the sprint baseline all equal `ed1d137c` with only
  unrelated `.claude/` untracked.
- Audited active resident contracts: training rotations use `training.RotationAssignment`, while
  the active web logbook uses `academics.LogbookEntry`; Android now uses those authoritative APIs.
- Implemented Android Home training card, Training rotation history/detail, Logbook draft/edit/
  submit, and Requirements summaries; debug/staging Android unit tests pass and debug lint/build
  pass (no errors; existing unused-resource warnings only).
- Added a production-guarded synthetic-only E2E fixture command; no schema migration or live API
  contract change is required.

## Pending work

1. Commit/push the Android client and synthetic-only management command, then on `ssh test` pull
   main, rebuild the existing `docker/docker-compose.yml` backend/worker/beat image, run Django
   checks/migration plan, health check, and the guarded fixture command with an external password.
2. Verify production API responses and write paths for `android.demo.resident1`; then install the
   production-configured APK on API 36 and run the resident regression/E2E workflow.
3. Run signed release gates/certificate/hash checks, finish evidence/docs, inspect for secrets,
   amend/commit/push final state, and fetch-verify the final SHA from the production VM.
