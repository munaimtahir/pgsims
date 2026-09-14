# Focused Android release closure — 2026-09-15

Status: **CONDITIONAL GO**, production candidate acceptance/deployment pending.
Runtime candidate: `e0c98b5`; backend source unchanged from tested `431e09d`.
Preserved concurrent parity branch: `feature/android-parity-stages-1-6` at `d8e2ce6`.
User confirmed a paused handoff and authorized the focused five-defect release,
including backend deployment and signed APK/AAB, excluding Play publication.

## Repairs and evidence

| Original defect | Candidate repair | Verification |
|---|---|---|
| Resident Inbox crashes | Role shell owns vertical scrolling | Real resident production-backed UI PASS; Compose scrolling/exact-record test PASS |
| Supervisor Inbox absent | Inbox destination shares role-scoped notification content | Compose supervisor navigation PASS; authenticated login, Inbox, restoration and refresh PASS |
| Leave UUID discarded/duplicates | Explicit UUID serializer; immutable key/training target; authorize before lookup; generic cross-target 409; savepoint-safe race replay | Full SQLite suite and separate PostgreSQL race PASS; production replay pending deployment |
| Logbook verified counts disagree | Shared trimmed, case-normalized classifier; APPROVED + VERIFIED summed; loaded-record labels | Mixed-state unit coverage PASS; production loaded-count comparison pending |
| Staging acknowledgment loses metadata | Ciphertext close/fsync + directory fsync before checked synchronous metadata commit; shared reconciliation lock; owner binding; stream decryption; coordinated logout purge | Host-controlled pre/post-ack kill, in-flight interruption, source failure, failed commit, staging/reconcile race PASS; ownership/purge tests PASS; real picker/retry pending |

The session/refresh acceptance additionally exposed concurrent rotating-refresh requests.
A shared refresh lock and stale-response check now ensure one rotation across repository
instances; the concurrent regression test passes and resident post-refresh restoration passes.

## Automated gates

- Fresh release image `sha256:7fe0b71e2c2d5e87e7e36e1ded9deaeab9f74995b9ae965497c3547dba8401e3`: **928 tests in 87.707s, zero failures/errors, one PostgreSQL-only skip**; separate PostgreSQL race PASS in 0.794s. Backend/worker/beat filesystem layers match.
- Existing production runtime image `sha256:b1984da08b5eaa50509dbec55519c33e2aab8cf51e9f8b500a323d42b9b4998a`
  with committed backend source: 928 tests in 102.644s, zero failures/errors,
  one PostgreSQL-only skip. Three deployment-domain tests ran with repository fixtures.
- Separate disposable PostgreSQL: concurrent identical leave creates return 201/200,
  same ID, one database row; one test in 0.878s PASS.
- Both environments were isolated from production: temporary SQLite inside a `--rm`
  network-disabled container; disposable PostgreSQL tmpfs on a temporary internal
  network, no published ports or persistent mounts. All removed after verification.
- `makemigrations --check --dry-run`, migrate from zero, Django check PASS.
- Android 33 unit tests PASS; debug/test APK assembly and lint PASS.
- `InboxUiTest` + `RecoveryOwnershipTest`: `OK (5 tests)`, 11.879s.
- `scripts/verify_android_process_death.py` kills from the host on an explicit
  instrumentation status acknowledgment, then verifies in a new process. It does
  not infer process-death durability from same-process reconstruction or a delay.
- Update 0 identity gate PASS. Canonical production compose render PASS (obsolete
  `version` warning only); root `compose.yml` does not exist in this checkout.

Reproduce backend gates on VPS with `scripts/verify_android_backend_closure.sh IMAGE [postgres]`.
Device storage tests require a signed-out debug app and explicit synthetic-only flag;
never run the kill harness against an authenticated institutional session.

## Scope and retained records

Four roles stay ADMIN, RESIDENT, SUPERVISOR, SUPPORT_STAFF. ADMIN/SUPPORT_STAFF remain
restricted in this focused baseline. No new identity/admin/reporting parity features,
FCM enablement, Caddy changes, physical-device/Play certification, or unrelated record
transitions. Prior labeled leave drafts 17–19 and logbook 31 remain historical fixtures.
No credentials, session tokens, or private signing values belong in evidence.

## Remaining release gates

1. Freeze and verify signed APK/AAB certificate, package, version and hashes.
2. Run full backend suite against freshly built release image before deployment.
3. Finish resident/supervisor candidate sessions, Inbox behavior, scoped workflow/count checks.
4. Verified PostgreSQL backup complete; reviewed merge to main, source verification on VPS,
   scoped backend/worker/beat deployment, rollback tags retained.
5. Production labeled leave/logbook exactly-once and real document picker/retry/discard/purge.
6. Final production health and committed evidence/main verdict.

## Backup / rollback readiness

Backup `/home/munaim/srv/backups/pgsims/pre_android_closure_20260915_0300.sql.gz`,
201883 bytes, `gzip -t` PASS; SHA256
`f70ff86ba76925161fcc45a30b913fd97350fe9447b9c6c5a1a86b60663d5cc0`.
Rollback tags: `pgsims-rollback-android-closure-{backend,worker,beat}:20260915`.
No production service has been replaced at this checkpoint.
