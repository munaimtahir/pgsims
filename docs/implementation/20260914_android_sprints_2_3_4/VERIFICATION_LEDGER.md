# Shared Verification Ledger — Android Sprints 1–5

Last reconciled: 2026-09-15 PKT. **CONDITIONAL GO.**
Canonical, reproducible artifact-specific evidence: [TEST_RESULTS.md](TEST_RESULTS.md).
Implemented code, API tests and authenticated device acceptance are distinct claims.

## Closed baseline gates

| Area | Evidence / boundary |
|---|---|
| Four-role API login | Inherited 2026-09-15 HTTP 200 / expected role evidence for ADMIN, SUPPORT_STAFF, RESIDENT, SUPERVISOR; no standalone login API rerun. |
| ADMIN restricted screen | Inherited authenticated emulator result; raw historical device artifact unavailable. |
| SUPPORT_STAFF restricted screen / logout | Pass on both initial 1.1.7 (7) and rebuilt baseline-source 1.1.8 (8) APKs. |
| Resident/supervisor session and refresh | Canonical role logins, dashboard, restore, forced invalid-access refresh and sign-out pass. |
| Full Django suite | Network-isolated current VPS image, temporary SQLite file, no mounts; 922 tests / 0 failures/errors / 3 repository-file skips / 59.308s / exit 0. Container removed. |
| Android baseline build | Debug assembly, five unit suites / 30 tests, lint and test APK assembly pass. Manual instrumentation has an explicit leave replay failure. |
| Logbook offline recovery | UI creation and process restart pass; worker/replay yield only record 31 for key 1f93d8ad-9808-4826-8eed-a2bb99e009b0. |
| Upload normal restart / discard / purge | Synthetic encrypted-store probe, target -1, settles metadata before restart; retry retains error, explicit discard works. Populated-queue logout removes tokens, draft/upload data and orphan file. Real successful upload is not established. |
| Production health and FCM | Current backend database/cache/Celery healthy; frontend/Android API HTTP 200; FCM false. No rollout or Caddy changes in this pass. |
| Historical production schema | Prior rollout applied notification/training migrations and identity repair; this pass did not repeat migrations against production. |

## Failed or unverified gates

| Area | Exact result / next evidence |
|---|---|
| Resident Inbox | FAIL on rebuilt baseline APK: infinite-height nested vertical-scroll crash. Repair and test UI/read-unread/targets. |
| Supervisor Inbox | FAIL on rebuilt baseline APK: navigation has Home/Residents/Profile only. |
| Leave offline idempotency | FAIL: key d17eb5f9-d032-4fc2-8bd9-ad2e12d199ba is discarded; labeled DRAFT records 17/18/19 have null keys. Fix serializer persistence; verify a fresh key. Do not repeat this same failing payload. |
| Logbook consistency | FAIL: Approved 0 in logbook summary vs visible approved entry and Progress 1 verified. |
| Abrupt upload exit | Initial APK probe lost metadata with an encrypted orphan retained. Reproduce/repair with expected upload-count assertion on a frozen candidate; settled restart/purge pass separately. |
| Full action-transition regression | NOT VERIFIED this pass; read-only resident/supervisor screens and review controls checked. Use dedicated fixtures for further mutations. |
| Document picker / successful upload | NOT VERIFIED; canonical resident has no required document target. Explicit-discard branch was exercised instead. |
| Repository-file checks | Three DeploymentDomainConfigTests explicitly skipped inside the image. SQLite pass does not establish these or PostgreSQL-specific behavior. |
| Later parity / signed release | NOT VERIFIED. Historical signed artifacts are not recertified by a debug run. |

## Artifact and branch boundary

The tested hashes are in TEST_RESULTS.md. During verification a separate session started
`feature/android-parity-stages-1-6` and changed runtime files. Those later edits are outside this
verification. Evidence/test-support changes are committed to main without merging or checking out
that feature branch; the active feature worktree and its SPRINT_STATE.md remain owned by that session.

## Agent rules

- Read the canonical report and inspect branch/SHA/worktree before claiming a gate closed.
- Do not infer API/UI acceptance from builds or a single login.
- Do not expose passwords, tokens, signing/Firebase properties or VPS environment values.
- Preserve explicit failures, skipped checks, artifact boundaries and labeled test-record ownership.
- FCM remains disabled; Caddy and unrelated workflow records are out of scope.

## 2026-09-15 feature-candidate ledger

| Area | Candidate result / boundary |
|---|---|
| Identity | Source/API/unit PASS for authoritative route precedence, password change/reset, app link, dynamic completion, declaration and own profile. Live mail and authenticated four-role device QA deferred. |
| Inbox | Nested scroll removed; all four role shells expose Inbox; exact typed record fetch and stale/forbidden recovery wired. Authenticated recipient/read/preferences/target device QA deferred. |
| Resident/Supervisor | Full create/review payload increment builds and has MockWebServer coverage. Returned evaluation edit, leave edit, generic review queue/workload and authenticated transition loops remain open. |
| ADMIN/staff | Universal four-role create and paged universal directory/details built for ADMIN. Staff remains own-account/Inbox only. Broader document/supervision/report administration remains open. |
| Offline | Immediate synchronous owner-bound metadata and encrypted orphan cleanup pass instrumentation. Live lost-response exactly-once and foreground draft reconciliation remain open. |
| Android candidate | 1.1.8/code 8; 37 unit tests, lint, both APK assemblies and `OK (10 tests)` instrumentation pass. Debug APK SHA-256 `e603de08dc892c37506996f03adbd1c04c67329f0d3f56e227dcda14c64c691c`. |
| Backend/project | 21 focused and 922 full tests pass; 3 deployment-domain tests, Django check, Update 0 gate, disposable identity repair (0 scanned, final PASS) and canonical compose render pass. Migration drift check remains failing on two unrelated pre-existing state differences. |
| Release boundary | CONDITIONAL GO. No signing material found; no merge, VPS mutation, production deployment, Caddy or FCM change. |
