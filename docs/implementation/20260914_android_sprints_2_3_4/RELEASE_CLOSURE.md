# Android 1.1.9 — focused Sprint 1–5 release closure

**GO — all five release blockers and mandatory session/recovery gates passed.**
All five original defects have passed their production acceptance checks.
Runtime source: `5f922657ea6dec17317a00eb4060168a816e1e1f`; merged through
[PR #17](https://github.com/munaimtahir/pgsims/pull/17) and
[PR #18](https://github.com/munaimtahir/pgsims/pull/18).
The broader parity branch remains preserved at `d8e2ce6` and is not included.

## Five-defect acceptance

| Defect | Repair and observed result |
|---|---|
| Resident Inbox crash | One scrolling owner. Compose regression and signed production Inbox PASS. Exact record #31, recipient isolation, missing and unsupported target messages verified. |
| Missing supervisor Inbox | Native Inbox destination; exact assigned record #31 and scoped navigation PASS. Missing/unsupported targets remain recoverable. |
| Duplicate leave drafts | UUID writable on creation, immutable thereafter; training target immutable. Permission checks precede lookup, cross-target collisions return a generic 409, races use a savepoint. Signed offline UI draft survives restart and creates leave #20 exactly once; two HTTPS replays return 200/same ID. |
| Inconsistent logbook counts | Both screens use a shared trimmed/case-normalized classifier; VERIFIED and APPROVED sum together. Returned aliases normalize; other states remain distinct. Both signed screens show 1 verified/approved for their loaded records. |
| Lost encrypted upload metadata | Ciphertext close/fsync and directory fsync precede checked synchronous metadata commit; shared reconciliation lock, owner binding, streamed retry and coordinated logout purge. Host-kill/fault/race tests PASS. Real picker/restart/retry uploads document #2 with exact source hash. Replacement discard and populated-queue logout purge PASS. |

Concurrent token refresh is serialized across repository instances. Notification refresh now completes
before displaying a target failure, so it cannot erase the recovery message. Explicit Retry replaces
pending WorkManager backoff; normal scheduling retains KEEP. These fixes came from acceptance findings.

## Tests and reproducible evidence

- Fresh deployed backend image: **928 tests, zero failures/errors, 87.707s**, one PostgreSQL-only
  skip. The separate PostgreSQL concurrent-create test passes in 0.794s (one 201 + one 200, same row).
  Three repository-dependent deployment tests ran with their fixtures. Migration drift check,
  migrate from zero and Django system check PASS.
- Earlier current-image/source gate also passed 928 tests in 102.644s and PostgreSQL race in 0.878s.
- SQLite containers used `--rm --network none`, temporary files inside the container, no production
  environment or mounts. PostgreSQL used temporary tmpfs and an internal disposable network with no
  published port. All verification containers/networks were removed; sanitized logs retained.
- Android: **33 unit tests across 8 suites, zero failures/errors**; lint, debug/test APK, signed APK
  and signed AAB builds PASS. Final frozen-debug Inbox/ownership/purge instrumentation passes 5 tests in 7.312s. Host-controlled
  death after acknowledgment, before acknowledgment and during upload, plus source/metadata failures
  and staging/reconciliation race PASS. See [process-death evidence](evidence/closure-process-death.txt).
- SUPPORT_STAFF restricted screen/sign-out; resident/supervisor fresh login, restoration,
  logout/relogin and forced invalid-access refresh PASS. Existing four-role API-login and ADMIN
  restricted-screen evidence is inherited; no separate four-role API-login matrix was repeated.
  An authenticated resident session was obtained specifically for actual HTTPS idempotency replay.
- Signed real UI workflow: offline leave/logbook drafts and a document selection, force-stop/restart,
  reconnect, retry, discard and populated-queue logout/relogin. See
  [production recovery](evidence/closure-production-recovery.txt) and
  [HTTPS replay](evidence/closure-https-replay.txt).
- Update0 identity gate PASS. Canonical production compose render PASS with only the existing
  obsolete-version warning. Root `compose.yml` is absent; `docker/docker-compose.prod.yml` was used.

Reproduce with `scripts/verify_android_backend_closure.sh IMAGE [postgres]`,
`scripts/verify_android_process_death.py` (signed-out debug app only),
`scripts/android_acceptance_ui.py`, and `scripts/verify_android_demo_replay.py --authorized-demo`.
The latter helpers read `PGR_ACCEPTANCE_CREDENTIALS` from an owner-only JSON file. Never log credentials.

## Signed artifacts

Package `pk.vexel.pgrcompanion`, version **1.1.9 / code 9**. APK signature and AAB signature verify;
both certificates match the earlier 1.1.3 release certificate:
`a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`.

| Artifact | SHA256 |
|---|---|
| `builds/companion/1.1.9/PGR-Companion-1.1.9.apk` | `38d90bb1c4b329582d706f7914678ae19e2f1a7e5ef8621e105c8edf054b3043` |
| `builds/companion/1.1.9/PGR-Companion-1.1.9.aab` | `b42837a4ca4d051bf2046066cab7723f86f8a0677dd2e1644cccea4a99770984` |

Absolute artifact root on the laptop:
`/media/munaim/shared1/Documents/github/pgsims/builds/companion/1.1.9/`.
[Artifact verification](evidence/closure-release-artifacts.txt) records sizes, source and certificates.
No Play publication was performed.

## Production deployment and rollback

VPS `/home/munaim/srv/apps/pgsims` fetched merged main and verified backend sources against the tested
image before replacement. Deployment used only
`docker compose --env-file .env -f docker/docker-compose.prod.yml up -d --no-deps --no-build backend worker beat`.

- Backend: `sha256:7fe0b71e2c2d5e87e7e36e1ded9deaeab9f74995b9ae965497c3547dba8401e3`.
- Worker: `sha256:5089231eafacb5360b1347ea3bf3168e603d3d43d3b2bcd7e2777cf647060741`.
- Beat: `sha256:4d14287536a833e78085dd14d14b2836b017d0cf1d64ad156a0c234898d6bf27`.
- Their filesystem layers match. Forward migrations rename a notification index and align the
  historical leave UUID index; no database reset or identity/profile schema change occurred.
- Verified PostgreSQL backup: `/home/munaim/srv/backups/pgsims/pre_android_closure_20260915_0300.sql.gz`,
  201883 bytes, gzip integrity PASS, SHA256
  `f70ff86ba76925161fcc45a30b913fd97350fe9447b9c6c5a1a86b60663d5cc0`.
- Prior images remain under `pgsims-rollback-android-closure-{backend,worker,beat}:20260915`.
  Rollback can restore those three images without restoring the database; the index migrations are
  compatible with the prior code. No forced APK downgrade or app-data wipe was used.
- Actual upload testing exposed a host-directory permission problem. Only
  `backend/media/resident_documents`, its `2026` directory and `2026/09` directory changed from
  owner/group 1003:1003 mode 775 to 1003:1000 mode 2775. Existing files/other media directories were
  untouched. Container UID/GID 1000 can write, and future children inherit the writable group.

Backend database/cache/Celery health and frontend/API HTTP 200 pass. FCM stays disabled; no Caddy,
PostgreSQL/Redis service, frontend deployment, unrelated application or persistent-volume changes.

## Retained synthetic fixtures and scope

- Leave #20, DRAFT, UUID `6767c572-ea7a-4bfb-a130-699e3145d0a2`: exactly 1 row.
- Logbook #32, DRAFT, UUID `27c2cbf2-43d5-448d-b769-7720e5bd1553`: exactly 1 row.
- Optional resident document #2, no global requirement created; PENDING_REVIEW, 607 bytes,
  SHA256 `d83de7f81d4aa1e6b3e306b2ea39343005e229a90655f97df0d81b6e523015c5`.
- Demo in-app notification IDs 1–3 (resident), 4–6 (supervisor). No email/push delivery was sent.
- Earlier baseline leave #17–19/logbook #31 remain untouched. Purge-marker drafts never reached the
  server; discarded/purged replacement did not change document #2 filename/hash/upload time.

Roles remain ADMIN, RESIDENT, SUPERVISOR, SUPPORT_STAFF; ADMIN/SUPPORT_STAFF stay restricted in this
focused mobile baseline. No legacy folders/modules were recreated or changed. GO is scoped to these
five release blockers and their required session/recovery gates. Broader parity, full workflow-action
certification, physical-device/accessibility/performance QA and Play publication remain outside scope.

Final health and cleanup: [evidence](evidence/closure-final-health.txt). All required evidence is committed with this verdict on `main`.
