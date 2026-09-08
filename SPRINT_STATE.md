# SPRINT_STATE.md — PGR Companion production resident expansion

## Scope

Expand `android/app-portal` from resident foundation commit
`ed1d137c76beec33ddc7cb2c6140fc01a94102de` into the production PGR SIMS resident client. The
owner has explicitly authorized production integration/deployment only after a safe synthetic
resident, production state, migrations, and rollback path are verified. Preserve `.claude/`.

## Completed work

- Started from `ed1d137c`; completed implementation commits `96a5c4c` and `f081a6d` are pushed
  to `origin/main`. Unrelated `.claude/` remains untracked and untouched.
- Audited active resident contracts: training rotations use `training.RotationAssignment`, while
  the active web logbook uses `academics.LogbookEntry`; Android now uses those authoritative APIs.
- Implemented Android Home training card, Training rotation history/detail, Logbook draft/edit/
  submit, and Requirements summaries; debug/staging Android unit tests pass and debug lint/build
  pass (no errors; existing unused-resource warnings only).
- Added a production-guarded synthetic-only E2E fixture command. Production is now at `f081a6d`,
  the backend image was rebuilt/restarted, health is 200, Django check/migration consistency/plan
  pass, and the command prepared only `android.demo.*` records with synthetic rotations and a
  primary supervisor. No schema migration or live API contract change was required.
- Verified all production reads for the synthetic resident. Verified API logbook create, edit and
  submit and then created a separate synthetic draft through the API-36 Android UI. Corrected the
  actual production response shape (`rotation.current`, `department_name`/`hospital_name`) in the
  Android Training presentation.

## Pending work

1. Finish API-36 production regression: Requirements/Documents/Profile, release-candidate login,
   training/detail and logbook create/submit, session restore, logout/re-login, uninstall
   isolation, and crash-buffer review. Use only `android.demo.resident1` and no patient data.
2. Commit the final production-contract/UI/test-placement corrections; pull/rebuild only if the
   backend test move changes deployed code, then run `PrepareAndroidProductionE2ECommandTests` in
   an ephemeral SQLite-backed container (never the production database).
3. Run signed release APK/AAB gates, certificate/hash verification and final security scan; finish
   evidence documents, update `android/README.md`, push, and verify remote and production SHAs.
