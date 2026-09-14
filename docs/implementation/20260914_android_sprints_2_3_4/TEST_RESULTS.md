# Combined Android Sprints 2–4 — Test Results

## 2026-09-15 local update

Passed in the current checkout after encrypted document-queue and FCM kill-switch changes:

```text
./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleDebug
```

All five unit-test XML suites report zero failures and zero errors. The generated debug APK was
installed and launched on emulator `pgsims` (`emulator-5554`); the unauthenticated PGR Companion
sign-in screen rendered without a crash.

This is build/smoke evidence only. Authenticated role/session and offline recovery evidence,
backend migration/test evidence, signed release verification, and VPS rollout verification remain
required before a GO verdict.

## 2026-09-15 production verification

- VPS branch fast-forwarded to `46eccbd` after a checksummed PostgreSQL backup.
- Rebuilt and recreated only `pgsims_backend_prod`, `pgsims_worker`, and `pgsims_beat`.
- Backend health returned database/cache/Celery `ok`; frontend returned HTTP 200; `manage.py check`
  passed; `notifications.0003_mobile_push` and `training.0011_leaverequest_client_request_id` are
  applied; identity repair passed with 59 users and zero invalid or duplicate profiles.
- `FCM_ENABLED=False` was confirmed in the deployed backend.
- Focused `sims.notifications` and `sims.training` tests passed in disposable Compose containers.
- The 922-test full suite was stopped without a result after its backup/restore test reached a
  `pg_restore` relation lock in disposable `test_sims_db`. The test container and test database
  were removed; this remains a release gate rather than a pass.

## Completed locally

- `python3 -m py_compile` passed for changed Django modules and the new migration.
- `./gradlew :app-companion:compileDebugKotlin :app-companion:testDebugUnitTest` passed.
- `git diff --check` passed.

## Required VPS follow-up

The local checkout has no installed Django environment, so Django execution tests were not run
here. After commit/push and synchronization to `/home/munaim/srv/apps/pgsims`, run:

```bash
cd backend
python3 manage.py makemigrations --check --dry-run
python3 manage.py migrate
python3 manage.py test sims.notifications sims.training sims.academics
python3 manage.py check
```

Then use emulator `pgsims` to verify an offline leave and logbook draft survives restart, syncs
once after reconnecting, and an inbox target opens its matching screen.
