# PGSIMS Android — Remaining Release Work

Updated 2026-09-15. **CONDITIONAL GO** for the tested Sprint 1–5 baseline.
Canonical report: [TEST_RESULTS.md](docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md).
The parallel `feature/android-parity-stages-1-6` effort is separate; its runtime changes are not
certified by the verification below. `[x]` means evidenced, `[ ]` means failed or explicitly unverified.

## Closed verification gates

- [x] Reconcile four-role production API login and historical ADMIN restricted-device result.
- [x] SUPPORT_STAFF restricted-mobile screen and clean sign-out, including rebuilt APK.
- [x] RESIDENT/SUPERVISOR fresh login, dashboard, logout/relogin, restored session and forced refresh.
- [x] Resident training/posting/history/assignment, progress, profile/requirements and workflow lists;
  supervisor assigned list/progress and queue/action-control read-only smoke checks (limits below).
- [x] Offline leave/logbook draft creation in the real UI and retention across process restart.
- [x] Logbook reconnect/replay yields exactly one server record per key (record 31).
- [x] Encrypted synthetic document normal restart, explicit retry failure/discard, and logout purge
  of populated draft/upload queues plus orphan file. This covers the discard acceptance branch.
- [x] Baseline Android debug assembly, 30 unit tests across five suites, lint and test APK assembly.
- [x] Disposable network-isolated VPS SQLite suite: 922 tests, 0 failures/errors, 3 explicit skips,
  59.308 seconds; test container and SQLite files removed.
- [x] Production database/cache/Celery health, frontend/Android API HTTP 200, FCM disabled.
- [x] Reproducible sanitized evidence reconciled into the canonical report and Sprint 1–5 release report.

## Mandatory failed gates — not GO

- [ ] **Resident Inbox crash:** fix nested vertical scrolling in `InstitutionalScreen.kt` /
  `NotificationCenter.kt`; verify Inbox renders and supports read/unread/preferences/targets.
- [ ] **Supervisor Inbox absent:** add accessible Inbox navigation in `SupervisorScreens.kt` and
  verify it remains recipient-scoped; successful API reads alone are insufficient.
- [ ] **Leave idempotency broken:** persist `client_request_id` through `LeaveRequestSerializer` /
  `LeaveRequestViewSet`. Same key created drafts 17/18/19 with null keys. Use fresh labeled keys to
  prove one server record and retain rollback/duplicate-request API tests.
- [ ] **Logbook count mismatch:** normalize backend status values before counting; Approved 0
  disagrees with the visible approved entry and Progress's 1 verified.
- [ ] **Abrupt upload metadata loss:** reproduce immediate death after staging on the repaired
  frozen candidate, assert the upload count is retained, and verify orphan handling. Normal settled
  restart and logout cleanup already pass; they do not close abrupt-death durability.

## Explicitly unverified / deferred acceptance

- [ ] Complete resident/supervisor write-action transitions using dedicated fixtures. This pass did
  not approve/reject/submit unrelated leave, logbook, research, rotation or evaluation records.
- [ ] Notification UI behavior and deep-link targets remain blocked by Inbox failures.
- [ ] Real document picker/upload/replacement success remains unverified; synthetic encrypted-store
  retry/discard was the branch exercised. Canonical resident has no assigned document requirement.
- [ ] The three `DeploymentDomainConfigTests` skipped inside the image need repository files for
  execution; the isolated SQLite suite itself passed. PostgreSQL-specific behavior is not inferred.
- [ ] Signed release/Play package, accessibility/performance/physical-device QA and later parity
  changes require their own frozen-candidate evidence; historical signed artifacts are not newly certified.

## Boundaries and retained fixtures

FCM stays disabled. No Caddy/route/production-service changes, external messaging or unrelated record
changes. Labeled test server remnants are unsubmitted leave drafts 17/18/19 and logbook draft 31.
Device recovery material and tokens were purged; test payload cache removed; networking restored.
ADMIN and SUPPORT_STAFF administrative functions remain web-first for this tested baseline.
No next-stage GO is granted until the failed and unverified mandatory gates are resolved and the
final candidate's evidence is committed on main.
