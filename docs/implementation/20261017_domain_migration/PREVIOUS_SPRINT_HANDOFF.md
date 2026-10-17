# Preserved pre-migration sprint context

Both sides of the pre-existing ledger conflict are preserved below. These
backlogs are not acceptance requirements for the domain migration.

# Android mega sprint — complete mobile workflow and release closure

## Scope

Close every Android item in `pendingwork.md` and `android.md`, including the
canonical backend work it requires, VPS deployment verification, physical-device
acceptance, and the requested Play release `1.1.9` / code `9`.

Excluded by owner decision: FCM activation, Google Drive, Android backup/restore,
academic seed/demo actions, and web-only audit work. The Update 0 identity gate is
already `GO` (`docs/implementation/20260626_update_0_universal_identity_dynamic_onboarding/FINAL_VERDICT.md`).

The separate three-account demonstration dataset is complete; see
`DEMO_WALKTHROUGH.md` for live IDs and pending examples. Preserve those records.

## Completed Work

- Reconciled the mega-sprint scope with the canonical Android backlog and confirmed
  the Update 0 gate passes on `main` (`9ea8420`).
- Prior Android pagination, non-credentialed emulator, inbox UI, and synthetic
  recovery verification remain valid baseline evidence.
- Added the Android admin authoring workspace for canonical document requirements,
  supervision assignments, training records, periods, rotation/evaluation templates,
  logbook categories, and review-queue records. Repository mutations are restricted
  to a fixed canonical API allow-list and have MockWebServer coverage.
- Added pending-supervisor list/resolution, authoritative user-detail loading, and the
  missing resident-progress report/CSV contract; corrected the existing CSV label
  mismatch affecting logbook, evaluation, and workload exports.
- Added standard CSV/Excel import selection with an explicit dry-run-before-apply gate
  for canonical master, identity, supervision, and academic datasets.
- Added the backend-backed flexible-import workflow: schema-driven source-column mapping,
  header detection, mapping validation, named mapping presets, and a dry-run-before-apply
  safeguard. The fixed-contract and flexible flows both remain restricted to canonical datasets.
- Added MockWebServer coverage for flexible header detection, mapping validation, and mapped
  import uploads; the Android unit suite passes after the new contract coverage.
- Added allow-listed master-data template and current-data CSV export actions in the same
  import workspace, routed through the Android share sheet without persisting institutional data.
- Pushed `d2f2646` and fast-forwarded the VPS checkout at
  `/home/munaim/srv/apps/pgsims` to that commit. Production HTTPS health returned
  `{"status":"ok","database":"ok"}`; no backend migration or service restart was required
  because this slice changes Android source only.
- Factory-reset only the dedicated `pgsims` AVD, which restarted as `emulator-5556` on Android 16.
  The fresh-device connected suite reports `OK (29 tests)`; the seven authenticated recovery tests
  remain intentionally credential-gated and skipped.
- Added canonical admin edit controls plus guarded lifecycle actions to end supervision assignments,
  close training records, and atomically change a resident's primary supervisor. The Android client
  exposes no arbitrary mutation path and has MockWebServer coverage for the new contract.
- Added a distinct debuggable `staging` Android build type (`.staging` application-id suffix) with
  an owner-overridable isolated staging base URL; it falls back to the documented HTTPS staging host.
  The staging-only Android fixture command now also provisions the final `SUPPORT_STAFF` role.
- Android gate after the changes: `:app-companion:testDebugUnitTest`, `lintDebug`, and
  `assembleDebug` pass.
- `pgsims` emulator connected suite passes 51 tests with the existing 22 credential-gated
  authenticated/lifecycle tests intentionally skipped.
- Fixed resident web onboarding: declaration acceptance is saved independently before final
  submission, and the final documents step now exposes upload/replace controls backed by the
  resident document upload API.
# Three-account demonstration dataset and coverage closure

## Scope
Seed web/Android examples only for existing `admin`, `supervisor`, `resident`
profiles on the VPS, then raise automated coverage across all maintained backend,
frontend and Android application areas. Preserve identities, credentials, training
and primary links. The owner authorized the demonstration data; coverage work remains
manual and must not mutate production services.
This sprint enforces the `sprint_risk_reduction` profile: backend 85% lines / 90.01%
branches overall with 80% / 80% in each source-bearing area; frontend 60% / 50% /
58% / 55% overall with exact per-area floors in
`docs/implementation/20260921_coverage_95/COVERAGE_TARGETS.md`. The 95% per-area
release floor and 99% preferred target remain phased follow-up work. Android is
deferred to a dedicated Laptop connected-coverage sprint; it is not counted here.
Focused behavior-preserving refactors and regression-tested fixes are authorized.
No production mutations, deployments, integration activation or release publication.

## Completed Work
- Confirmed three active demo logins and resident-to-supervisor primary link.
- Locked four examples each for logbook, evaluations, leave, rotations, documents.
- Implemented guarded seeder and import samples; 15 isolated tests pass, including replay, file/database rollback, access checks and real workflow actions.
- Drafted `DEMO_WALKTHROUGH.md`; prior Android scope is preserved in its handoff.
- Reviewed coverage baseline: web 29.16% lines/25.50% branches; saved backend 81.61%/64.42%; Android unmeasured.
- Preserved unfinished Android sprint in docs/implementation/20260921_coverage_95/ANDROID_BACKLOG_SNAPSHOT.md.
- Added a 319-file area manifest, strict manual coverage reporter, accounting tests and manual CI workflow.
- Corrected backend test-file exclusions; added web middleware to measured source; Android unit/combined JaCoCo reports now build.
- Added web identity creation, middleware routing, directory and academic API contract tests; fixed displayed credentials/role and missing error fallback.
- Added backend draft/document boundary tests and validation fixes for malformed dates/references; corrected one test expectation for code-based foreign keys.
- Added and verified Android onboarding policy/summary edge-case tests; debug unit suite passes.
- Fresh frontend evidence: 421 tests in 48 suites pass with 48.23% line and 36.80% branch coverage; backup administration rose from 0% to 52.20% line coverage.
- Added academic authoring and supervision dashboard/API contract coverage; the focused backend onboarding boundary suite passes all 10 tests. Training area rose from 0% to 73.33% lines and 59.70% branches.
- Android unit-only JaCoCo baseline is reproducible: 16.06% lines, 6.02% branches, and 13.24% methods. It is explicitly not a connected-test gate.
- Added named, fail-closed coverage target profiles and accounting tests; the manual CI gate now enforces the current sprint profile for backend/frontend.
- Completed an isolated backend diagnostic run: 1,236 passed, 9 skipped; 82.16% lines and 66.74% branches. Per-area baselines are in `docs/implementation/20260921_coverage_95/TEST_RESULTS.md`; its evidence predates the final target-profile source hash and cannot pass the gate.
- Verified the allowed Update 0 onboarding regression suite: 28 tests passed in 4.061 seconds using a disposable SQLite database; this covers resident draft/state/declaration/document negative and authorization paths.
- Enabled and verified the eight formerly skipped backup/Google Drive tests: two backup proof tests passed in 75.81 seconds and six fully mocked Google Drive tests passed in 92.99 seconds. Added the disposable PostgreSQL coverage-runner path and marked the leave idempotency test for that runner instead of skipping it.
- Removed the non-importable legacy demo-case command and replaced stale `sims.logbook` references with canonical training-logbook queries.
- Fresh merged coverage evidence: 1,252 tests passed with zero skipped/failed; 84.21% backend lines and 69.17% branches. The 90.01% overall / 80% per-area branch gate remains BLOCKED; details are in `docs/implementation/20260921_coverage_95/TEST_RESULTS.md`.
- Added focused form coverage and corrected the specialty-filtered supervisor assignment field lookup; the isolated form test suite passes. A fresh full run is required after these source changes.

## Pending Work
1. Commit/push source, fetch into VPS, preview/apply/verify the marked demonstration dataset.
2. Complete `DEMO_WALKTHROUGH.md` with actual IDs, counts and web/Android limitations; preserve pending production records during verification.
3. Add coverage for `sims/_devtools/truthmap_extract.py` and `sims/supervision/management/commands/seed_pilot_supervision.py`, then rerun the backend gate so every executable manifest source is represented.
4. Raise backend branches from 3,095/4,510 (68.63%) to at least 4,060/4,510 (90.01%), with every area at 80%+: prioritize `users/userbase_views.py`, `training/views.py`, user-management commands, bulk services/engine, and notifications.
5. Establish fresh frontend coverage with commit/environment provenance; retain Android's deferred Laptop handoff.
6. Expand Android repository, screen and offline recovery tests; execute authenticated isolated workflows.
7. Reach the exact current profile thresholds per backend/frontend area, then schedule phase 2 hardening and the separate Android Laptop sprint toward the 95% release floor and 99% preferred target.
8. Run full verification and manual gates; document results, commit/push, verify matching checkout on laptop.

1. Complete resident progress/report detail and cross-screen list/filter/error behavior.
2. Complete supervisor generic review queue/workload/status parity and workflow refresh behavior.
3. Add guarded staging-only synthetic fixture cleanup tooling and certify all four fixture roles.
4. Certify resident leave/evaluation edit-resubmit, notifications, onboarding/session, and
   offline lifecycle paths with authenticated four-role fixtures on `pgsims`.
5. Add Android unit/instrumentation coverage for the remaining new contract and failure paths.
6. Run physical-device accessibility/lifecycle/performance acceptance, rebuild/sign/version-verify
   `1.1.9` / code `9`, then upload and verify Play Console publication if code `9` is unused.

## Next Command

Add report detail/filter/error parity without enabling seed/demo actions; staging build and all four
fixture identities are available for the later authenticated gate.
## Current Workspace
/home/munaim/srv/apps/pgsims; starting commit eee60ba.
Concurrent repository work advanced HEAD to 822fab8; preserve unrelated changes.
Next: run the disposable backend coverage suite to completion, then cover the remaining supervision assignment/data-quality pages and reports/imports workflows before the next fresh web report.
VPS has SDK/JDK but no KVM or dedicated pgsims AVD; connected acceptance requires laptop.
