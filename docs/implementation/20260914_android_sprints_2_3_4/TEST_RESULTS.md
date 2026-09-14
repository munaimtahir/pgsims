# Android Sprints 1–5 — Canonical Test Results

**GO — focused five-defect release, 2026-09-15 PKT.**

Current authoritative results: [RELEASE_CLOSURE.md](RELEASE_CLOSURE.md). Production backend is deployed;
1.1.9/code9 signed APK/AAB verify with the existing certificate. Fresh-image Django 928 tests and
separate PostgreSQL race PASS; Android 33 unit tests, final device/recovery and signed production
acceptance PASS. All five original failures are closed. No Play publication or broader parity certification.

## Historical baseline verification (superseded release verdict)

The following failures/results describe the earlier baseline and remain as traceable historical evidence.

## Tested baseline and evidence boundary

- Laptop physical checkout: `/media/munaim/shared1/Documents/github/pgsims` (also accessible through
  `/home/munaim/Documents/github/pgsims`). Laptop and VPS started at `13f1bb7`.
- VPS: `/home/munaim/srv/apps/pgsims`, current production image
  `sha256:b1984da08b5eaa50509dbec55519c33e2aab8cf51e9f8b500a323d42b9b4998a`.
- AVD `pgsims`, `emulator-5554`, API 36, package `pk.vexel.pgrcompanion.debug`.
- Initial pre-existing APK: 1.1.7 (7), SHA256
  `650ef76525648984cdc9376d3c0e6de6b3db1d70da7d70a67f0b78bc7b8d21e9`.
- Reassembled/installed baseline-source APK: 1.1.8 (8), SHA256
  `e7994e24b282b0656f2873389d94e027e618a20f5ae89252a68ebc29d524455e`.
  The version bump was a concurrent edit, not part of this verification change. Runtime source
  was the `13f1bb7` baseline when this APK was assembled; dependencies added here affect tests only.
- During verification another session switched the shared checkout to
  `feature/android-parity-stages-1-6` and began runtime changes. **Those later edits are not certified
  by this evidence.** No feature-branch merge or runtime deployment is part of this pass.

## Acceptance matrix

| Gate | Result | Evidence / exact boundary |
|---|---|---|
| Four-role production API login | PASS, inherited | Shared ledger recorded HTTP 200 with expected ADMIN, SUPPORT_STAFF, RESIDENT, SUPERVISOR roles. Standalone API login checks were not repeated. |
| ADMIN restricted-mobile screen | PASS, inherited | Accepted shared-ledger authenticated emulator result; raw historical device artifact was not retained. |
| SUPPORT_STAFF restricted screen and sign-out | PASS | Initial and rebuilt APK show Support staff restricted screen, then login after Sign out. [Current UI](evidence/current-support-staff-routing.txt), [initial token/queue cleanup](evidence/support-staff-logout.txt). |
| Resident fresh login/dashboard/logout/relogin | PASS | Canonical `resident` exercises the rebuilt app, including re-login after offline purge and AVD cold boot. No identity fields/passwords changed. |
| Supervisor fresh login/dashboard/logout/relogin | PASS | Rebuilt app shows 7 assigned residents and 1 pending approval. [Dashboard](evidence/current-supervisor-dashboard.txt), [final sign-out](evidence/final-signout.txt). |
| Resident restored session and forced refresh | PASS | Restart returns to resident Home; deliberately invalid access token plus retained refresh produces successful role-scoped snapshot and notification list/count/preferences reads. [Current refresh](evidence/canonical-resident-refresh.txt). |
| Supervisor restored session and forced refresh | PASS | [Current refresh](evidence/current-supervisor-refresh.txt), [restored dashboard](evidence/current-supervisor-restored.txt). |
| Resident Inbox | **FAIL** | Rebuilt app crashes at 01:36:55 PKT with nested vertical-scroll infinite-height constraints. [Current crash](evidence/current-resident-inbox-crash.txt). |
| Supervisor Inbox | **FAIL** | Rebuilt app exposes only Home, Residents, Profile; no Inbox destination. Successful notification API reads do not satisfy the UI gate. |
| Role-scoped existing workflow regression | **PARTIAL / FAIL** | Read-only surfaces render within resident/supervisor workspaces, but Inbox fails and counts disagree. See scope below. Full write-action regression was not rerun. |
| Offline logbook: restart/reconnect/idempotency | PASS | Real UI draft survives process restart; worker sync and two repeated creates yield only record 31 for the same key. [Restart](evidence/offline-restart.txt), [server counts](evidence/server-idempotency.txt). |
| Offline leave: restart/reconnect/idempotency | **FAIL** | Draft survives restart and syncs, but repeated identical key creates three records (17, 18, 19), all with a null stored key. [Failing instrumentation](evidence/offline-replay.txt), [server counts](evidence/server-idempotency.txt). |
| Encrypted upload normal restart/retry/explicit discard | PASS, discard branch | Synthetic target -1 cannot replace a real document. Settled metadata/file survive restart; encryption/decryption checked. Reconnect retries and shows an explicit error; Discard removes entry. [Restart](evidence/offline-restart.txt), [retry](evidence/upload-retry-ui.txt), [discard](evidence/upload-discard-ui.txt). Successful real upload and file-picker integration are not established by this store-level synthetic probe. |
| Immediate-exit upload durability | **FAIL / recheck on repaired candidate** | Initial APK stage returned success, but immediate instrumentation-process exit lost metadata while a 113-byte encrypted orphan survived. This is an abrupt-death probe, not normal Activity lifecycle evidence. [Counts](evidence/upload-immediate-restart-missing-metadata.txt). |
| Logout purge with material present | PASS | One leave, one logbook, one upload present before offline sign-out; afterwards tokens, queues and staged files (including orphan) absent. [Before](evidence/pre-logout-queues.txt), [after](evidence/resident-logout-purge.txt), [final cleanup](evidence/final-session-cleanup.txt). |
| Full Django suite in isolated SQLite container | PASS with 3 explicit skips | 922 tests, 0 failures/errors, 3 skips, 59.308s, exit 0. [Sanitized log](evidence/backend-full-suite.log). |
| Android baseline build/unit/lint | PASS | `assembleDebug`, `testDebugUnitTest`, `lintDebug`: 5 unit suites / 30 tests / 0 failures/errors/skips. Android test APK also assembled and installed. [Build summary](evidence/android-build-summary.txt). |
| Production post-test health / FCM | PASS | Backend database/cache/Celery healthy, frontend and Android API health HTTP 200; FCM false. [Health](evidence/production-health.txt). |
| Signed release / later feature candidate | NOT RE-CERTIFIED | Historical signing evidence remains historical; this pass tests debug artifacts. Later feature edits require their own frozen build and acceptance evidence. |

## Exact failures and regression scope

1. Resident Inbox: `InstitutionalScreen.kt` provides a vertically scrolling parent;
   `NotificationCenter.kt` adds another vertical scroll. Tapping either Inbox entry crashes.
2. Supervisor Inbox: `SupervisorDestination` in `SupervisorScreens.kt` has no Inbox member.
3. Leave idempotency: `LeaveRequest.client_request_id` is `editable=False`; the ModelSerializer
   treats it as read-only and `perform_create` does not explicitly persist it. The lookup cannot
   match subsequent requests. Instrumentation's repeated responses **18 != 19** fail
   `ReleaseAcceptanceTest.replaySyntheticDrafts`. No further leave replay was attempted.
4. Logbook counts: rebuilt UI displays Draft 1 / Approved 0 while showing an Approved entry;
   Progress correctly shows 1 verified. [Current count evidence](evidence/current-logbook-counts.txt).
5. Abrupt upload exit: asynchronous queue metadata can be lost while an encrypted file remains.
   Initial probe must be repeated with a test asserting the expected upload count after repair.
   Normal restart and logout orphan cleanup passed; neither erases the abrupt-exit finding.

Resident read-only checks: Home/onboarding requirements, dynamic Profile, Training/programme,
current posting and rotation-history empty states, supervisor assignment, Progress, logbook list,
leave list/new draft, evaluation list, Requirements/research/workshop summaries. The canonical
resident still has academic-session/declaration requirements; these were displayed, not modified.
Supervisor read-only checks: Home, 7 assigned residents, one assigned resident's progress, empty
logbook/leave/research/rotation queues, evaluation queue and its Approve/Reject/Return/Cancel controls.
No approval/rejection was executed on unrelated workflow records. Empty queue screens alone do not
prove permission-denied and empty-result states are distinguished. Full action-transition regression,
notification read/unread UI, and notification target navigation remain **NOT VERIFIED** because the
Inbox gates fail and no new action-transition fixture set was exercised in this pass.

The historical resident account from the earlier report was used in the first pass. Canonical
`resident` and `staff` credentials were then supplied by the owner. The supplied supervisor password
variant was rejected; its previously documented, already verified credential succeeded. No credential
values, tokens, password changes or new account seeding are included in this evidence.

## Recovery records and procedure

1. Sign in as canonical resident on `pgsims`. Disable emulator Wi-Fi and mobile data with
   `adb -s emulator-5554 shell svc wifi disable` and `... svc data disable`.
2. In Leave, create an annual one-day draft for 2026-09-20 with marker
   `ANDROID-ACCEPTANCE-20260915-OFFLINE-LEAV` (the typed final E was absent in the saved value).
   In Logbook, create a 2026-09-15 draft titled
   `ANDROID-ACCEPTANCE-20260915-OFFLINE-LOGBOOK`, synthetic reflection, no patient data.
   Both real UI flows report encrypted local retention.
3. `retainSyntheticDraftsForReplay` asserts two labeled drafts and saves only these synthetic
   payloads to a temporary test fixture. [Keys](evidence/offline-draft-keys.txt):
   leave `d17eb5f9-d032-4fc2-8bd9-ad2e12d199ba`, logbook `1f93d8ad-9808-4826-8eed-a2bb99e009b0`.
4. `stageSyntheticUpload` calls the real encrypted store with a labeled test PDF payload and target
   `-1`. The normal-restart probe allows 1 second for asynchronous persistence. Force-stop, then
   `inspectEncryptedRecovery`: leave=1/logbook=1/upload=1, decrypt length correct, ciphertext differs.
5. Re-enable Wi-Fi/data, install/start the rebuilt baseline app. Real WorkManager drains the drafts
   and retains the failed nonexistent-target upload. Requirements → Discard removes that queue item.
6. `replaySyntheticDrafts` replays each exact payload twice. Logbook returns 31 both times; leave
   returns 18 then 19. Read-only production ORM queries verify counts and keys.
7. While offline again, stage one upload and restore the two synthetic local payloads for the logout
   probe. Sign out from the offline error screen. `assertLogoutPurge` verifies absent tokens and
   empty stores/directory. Re-enable networking only after purge. Test fixture is removed afterwards.

Server remnants are intentional, clearly labeled **DRAFT** test records: leave IDs 17/18/19 and
logbook ID 31. None were submitted or approved. No unrelated workflow records were changed.
The emulator later exited; the same AVD was cold-booted without wiping data to finish smoke checks.

## Reproduce device instrumentation

The test class is manual and opt-in. Run **one named method at a time**, only with the authorized
signed-in demo account and the phase/preconditions above. Do not opt in to the whole class as a batch.
The harness does not perform API login and never logs credentials or tokens.

```bash
cd android
./gradlew :app-companion:assembleDebug :app-companion:assembleDebugAndroidTest
adb -s emulator-5554 install -r app-companion/build/outputs/apk/debug/app-companion-debug.apk
adb -s emulator-5554 install -r app-companion/build/outputs/apk/androidTest/debug/app-companion-debug-androidTest.apk
adb -s emulator-5554 shell am instrument -w -e releaseAcceptance authorized-demo -e expectedRole RESIDENT -e class pk.vexel.pgrcompanion.ReleaseAcceptanceTest#forceRefresh pk.vexel.pgrcompanion.debug.test/androidx.test.runner.AndroidJUnitRunner
```

Use `expectedRole SUPERVISOR` for that role. Replace the method with `inspectEncryptedRecovery`,
`retainSyntheticDraftsForReplay`, `replaySyntheticDrafts`, `stageSyntheticUpload`,
`stageSyntheticDraftsForLogout`, or `assertLogoutPurge` only at its documented phase.
UI evidence uses `uiautomator dump` and XML text/bounds inspection. Refresh probes invalidate only
local access tokens, preserve refresh tokens, and verify the real 401 → refresh → retried read path.

## Isolated backend full-suite command and result

Executed on VPS with the **current production image**, no mounts, no ports, no production env file,
network disabled, 1 CPU / 1500 MB / 256 PIDs, disposable secret, memory Celery transports, and FCM off.
The generated settings explicitly force a temporary SQLite test file, not PostgreSQL or in-memory DB.
Reproduction (on VPS; Docker output may be verbose, retain it privately and sanitize before sharing):

```bash
image_id=$(docker inspect --format '{{.Image}}' pgsims_backend_prod)
docker run --rm -i --network none --cpus 1 --memory 1500m --pids-limit 256 --no-healthcheck   --entrypoint sh -e SECRET_KEY=disposable-verification-only   -e DATABASE_URL=sqlite:////tmp/android-verification.sqlite3   -e DJANGO_SETTINGS_MODULE=verification_settings -e PYTHONPATH=/tmp:/app   -e FCM_ENABLED=False "$image_id" -s <<'CONTAINER'
cat > /tmp/verification_settings.py <<'SETTINGS'
from sims_project.settings_test import *
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/tmp/android-verification.sqlite3', 'TEST': {'NAME': '/tmp/android-verification-test.sqlite3'}}}
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'
FCM_ENABLED = False
SETTINGS
python manage.py test --noinput --verbosity 2
CONTAINER
```

Actual named container `android-final-20260915` exited 0 and was removed automatically. Start/end:
2026-09-14 20:14:08–20:16:37 UTC (2026-09-15 01:14:08–01:16:37 PKT), including migrations.
**Ran 922 tests in 59.308s; OK (skipped=3)**. Skips are these repository-dependent tests:

- `DeploymentDomainConfigTests.test_canonical_caddyfile_routes_both_domains` — Caddyfile absent.
- `DeploymentDomainConfigTests.test_primary_frontend_api_url_defaults_to_new_domain_in_production_variants` — Compose files absent.
- `DeploymentDomainConfigTests.test_production_settings_and_compose_defaults_include_new_domain` — repository files absent.

This is a SQLite suite pass, not proof of PostgreSQL-specific behavior or those three skipped checks.
No production DB, volume, route, Caddy configuration or running service was changed. Raw and sanitized
VPS logs are retained under `/home/munaim/srv/apps/pgsims-verification/`; committed output contains
only test names/status lines, totals and timing. Earlier full-suite lock is closed by this isolated run.

## Remaining release gates

- Repair and reverify both Inbox failures, including read/unread/preferences/target UI.
- Persist the leave idempotency key and prove one record per key with fresh labeled drafts.
- Fix logbook status-count normalization and recheck list/detail/Progress agreement.
- Reproduce/repair abrupt upload metadata loss on a frozen candidate; verify expected counts after death.
- Complete missing write-action regression with dedicated fixtures and real document picker/upload
  integration if successful-upload certification is required (this pass covers explicit discard).
- Freeze any later feature candidate, rebuild and re-run affected acceptance; do not transfer these
  results to untested feature edits or a newly signed release. Repository-file skips remain explicit.

**Final verdict: CONDITIONAL GO.** Evidence consolidation closes the verification pass; it does not
make the failed application gates pass. FCM stays disabled. No next-stage GO is granted by this report.
