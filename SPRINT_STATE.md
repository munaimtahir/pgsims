# SPRINT_STATE.md — Android Sprints 1–5 release closure

## Scope

Close the Android Sprints 1–5 release only with reproducible local and VPS evidence. FCM remains
disabled; PGSIMS remains the notification authority.

## Completed implementation

- Confirmed laptop `origin/main` baseline `a08bb16eb321f6154774d1c9edf6be28bffc4a2f` and created the remediation branch.
- Updated Django constraint to `>=5.2,<5.3`; Django 5.2.17 full suite passed (921 tests), checks and migration drift passed.
- Fixed disaster archive destination creation; backup orchestration passed (22 tests), including missing nested path coverage.
- Ran `repair_identity_profiles`: 37 scanned, 0 invalid users, 0 duplicate profiles; Update 0 gate passed.
- Frontend `npm ci`, lint, typecheck, Jest (39 suites / 240 tests), and Next 16.3.4 / React 19.2.0 production build passed locally and on VPS Node 20.20.2.
- Applied non-forced frontend dependency remediation; production audit is zero, with one indirect dev/build-only `glob` advisory documented.
- Updated React 19 tests, Next 16 async route params, ESLint 9 flat config, and generated-report ignores.
- Disposable PostgreSQL 15 tmpfs container migrated from zero and was removed; compose config parsed with unset-secret warnings.
- Preserved `AUDIT/PGSIMS/FINAL/` unchanged and created the remediation evidence package.
- Remediation commit: `228dc0c`; PR #16 remains open against `main` and unmerged.
- Disposable canonical stack smoke gate passed 25/25; stack and project-scoped volumes were removed.
- Canonical workflow gate passed 4/4; VPS production was checked read-only (healthz, frontend HTTP 200, migrations applied) with no mutation or restart.
- RBAC/negative passed 31/31; broader workflows passed 23 with 1 explicit conditional skip; Android `:app-companion` unit tests, lint, and debug assembly passed.
- Android signed release artifacts were produced successfully with external owner signing properties:
  - `android/app-companion/build/outputs/apk/release/app-companion-release.apk`
  - `android/app-companion/build/outputs/bundle/release/app-companion-release.aab`
- Added encrypted app-private staging for documents, persisted retry metadata, constrained
  WorkManager recovery, and logout purge for all offline institutional material.
- Added recipient-scoped inbox preferences UI and an Android `FCM_ENABLED=false` build-time gate.
- Android debug gate passed: unit tests, lint, debug assembly, installation, and unauthenticated
  launch on emulator `pgsims`; see `docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md`.
- Reviewed change set committed and pushed as `3b4a6f0` on
  `remediation/pgsims-final-production-readiness`; VPS remains deliberately unchanged pending
  disposable backend and authenticated regression gates.
- Production PGSIMS rollout completed at `46eccbd`: PostgreSQL backup
  `/home/munaim/srv/backups/pgsims/pre_android_release_20260914_192142.sql.gz` created and
  checksummed; backend/worker/beat rebuilt and recreated only. Backend health, Celery, frontend
  HTTP 200, Django checks, notification/training migrations, and identity repair all passed.
- Production FCM verification: `FCM_ENABLED=False`.

## Pending work

1. On emulator `pgsims`, use supplied disposable/demo accounts to record ADMIN/SUPPORT_STAFF routing, restored session, forced token refresh, resident/supervisor workflow regression, offline leave/logbook restart recovery, and encrypted document upload retry/discard behavior.
2. Resolve or isolate the existing full-suite backup/restore test lock. The production-disposable run found 922 tests and progressed normally, but a `pg_restore` relation lock in `test_sims_db` did not complete; the disposable test container and database were stopped/removed to protect production resources. Rerun the full suite in a truly isolated database host before a GO verdict.
3. Record the authenticated mobile matrix and the rerun full-suite result in `docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md`, then update the final release verdict. Do not enable FCM or change Caddy.

## Known conditions

- Ruff reports 2,663 existing findings; broad legacy cleanup is deferred and documented.
- VPS host Node is 18.19.1; Next 16 verification used disposable Node 20.20.2 tooling, matching the frontend image requirement.
- Playwright smoke executed 25 tests: 25 passed; workflow-gate 4/4 passed; RBAC/negative 31/31 passed; broader workflows 23 passed with 1 explicit conditional skip.
- Final certification: CONDITIONAL GO for Android Sprint 1; authenticated walkthrough completed and signed release verification complete.
