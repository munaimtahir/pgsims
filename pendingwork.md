# PGSIMS Android — Remaining Release Work

Updated 2026-09-15. **CONDITIONAL GO** for the tested Sprint 1–5 baseline.
Canonical report: [TEST_RESULTS.md](docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md).
The `feature/android-parity-stages-1-6` candidate now contains the repairs below. `[x]` means source
and automated verification complete; `[ ]` means authenticated/runtime acceptance or later scope.

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

## Repaired candidate gates

- [x] Resident nested-scroll crash removed and all four role shells expose Inbox.
- [x] Exact typed notification target lookup and stale/forbidden recovery wired and contract-tested.
- [x] Leave `client_request_id` is writable-on-create, persisted and deduplicated; focused API test
  proves a retry returns the same record and leaves one database row.
- [x] Logbook `VERIFIED` and `RETURNED_FOR_REVISION` values normalize into the displayed summary.
- [x] Draft/upload metadata uses synchronous persistence, is owner-bound, and removes encrypted
  orphan files; immediate durability/orphan instrumentation passes.
- [x] Migration drift reconciled by reviewed notification index and historical leave migrations;
  migrate-from-zero and `makemigrations --check --dry-run` pass.

## Explicitly unverified / deferred acceptance

- [ ] Complete resident/supervisor write-action transitions using dedicated fixtures. This pass did
  not approve/reject/submit unrelated leave, logbook, research, rotation or evaluation records.
- [ ] Authenticated notification read/unread/preferences, role isolation and exact-target UI behavior.
- [ ] Real document picker/upload/replacement success remains unverified; synthetic encrypted-store
  retry/discard was the branch exercised. Canonical resident has no assigned document requirement.
- [x] The three `DeploymentDomainConfigTests` pass in a repository-aware isolated run.
- [ ] Signed release/Play package, accessibility/performance/physical-device QA and later parity
  changes require their own frozen-candidate evidence; historical signed artifacts are not newly certified.

## Boundaries and retained fixtures

FCM stays disabled. No Caddy/route/production-service changes, external messaging or unrelated record
changes. Labeled test server remnants are unsubmitted leave drafts 17/18/19 and logbook draft 31.
Device recovery material and tokens were purged; test payload cache removed; networking restored.
ADMIN now has bounded universal-user management; SUPPORT_STAFF remains own-account/Inbox only.
No release GO is granted until authenticated candidate acceptance and remaining roadmap scope are
resolved. Merge/deployment remain separate decisions.
