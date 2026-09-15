# PGSIMS Android — Sprint 1 Workflow Parity Report

Date: 2026-09-14
Verdict: CONDITIONAL GO

## 1. Baseline

- Starting branch: `remediation/pgsims-final-production-readiness`
- Starting SHA: `67e604087715251559de4abf170a705241ef0681`
- Final implementation SHA: `921969bbeed29fb897fe57dc32f8614de6ab446b`
- Android package: `pk.vexel.pgrcompanion`
- Android version: `1.1.7` / code `7`
- Backend: Django 5.2 / DRF; laptop and VPS were synchronized before work.

## 2. Scope

Sprint 1 delivered explicit mobile role safety, resident leave requests, resident evaluation/WBA
views and actions, supervisor evaluation review, shared workflow status presentation, tests, and
documentation updates. Admin and support-staff mobile functionality remains intentionally web-first.

## 3. Files changed

- `pendingwork.md`
- Android repository, screens, labels, supervisor workflow, and unit tests
- Android API/capability/runbook documentation
- `PGR_SIMS_ANDROID_API_INTEGRATION.md`
- `docs/implementation/20260912_android_sprint1_workflow_parity/`

## 4. APIs used

- `/api/auth/me/`
- `/api/my/leaves/`, `/api/leaves/`, `/api/leaves/{id}/submit/`
- `/api/academics/evaluation-templates/`
- `/api/academics/evaluation-submissions/` and submit/review actions
- Existing supervisor summary, dashboard, queue, and approval APIs

No backend endpoint or migration was added.

## 5. Android changes

- Added explicit `RESIDENT`, `SUPERVISOR`, `ADMIN`, `SUPPORT_STAFF`, and unknown-role routing.
- Added a restricted mobile-role screen for admin/support/unsupported accounts.
- Added resident Leave and Evaluations destinations with backend-backed list/detail/create/draft/
  submit behavior and leave filters.
- Added supervisor evaluation queue and approve/return/reject actions.
- Added shared `InstitutionalLabels.workflowStatus()` mapping.

## 6. Tests executed

| Command | Result |
|---|---|
| `./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleDebug` | PASS |
| `./gradlew :app-companion:compileReleaseKotlin :app-companion:lintRelease` | PASS |
| `./gradlew :app-companion:assembleRelease :app-companion:bundleRelease -PpgrCompanionSigningPropertiesFile=/home/munaim/.config/pgr-companion/signing/signing.properties` | PASS |
| `python3 manage.py check` on VPS | PASS |
| `python3 manage.py makemigrations --check --dry-run` on VPS | PASS |
| `python3 manage.py test --noinput` on VPS | PASS — 921 tests |
| `bash scripts/check_update_0_identity_cleanup.sh` on VPS | PASS |
| `adb` install/launch and version check on `emulator-5554` | PASS — app launched, `versionName=1.1.7`, `versionCode=7` |
| Manual supervisor walkthrough on device (`supervisor` / `supervisor123`) | PASS — evaluation queue open, detail actions (`Approve`, `Reject`, `Return for revision`, `Cancel`) available |
| Manual resident walkthrough on device (`pgrdrmuhammadadeelbas` / `pgfmu123`) | PASS — resident workspace rendered and navigation validated |
| Instrumentation/UI suite | NOT AVAILABLE — no Android instrumentation test sources exist |

## 7. Real backend evidence

Against the live Android API using seeded demo accounts and uniquely labelled Sprint 1 records:

- Resident leave request was created and submitted; supervisor saw and approved it; resident reread
  `APPROVED`.
- Resident evaluation was created and submitted; supervisor saw and approved it; resident reread
  `APPROVED`.
- Authenticated API reads for resident and supervisor leave/evaluation/template resources returned
  expected HTTP 200 responses; supervisor access to resident-only leaves returned 403 as expected.

The production records are intentionally retained as labelled verification evidence. No deployment
or unrelated production data was changed.

## 8. Known limitations / blockers

- Full authenticated UI walkthrough was completed on device; no end-to-end mutation was automated
  by instrumentation, so functional steps remain manual but observed and recorded.
- Owner-supplied signed release APK/AAB was produced and verified with `apksigner` v2 (APK) and `jarsigner` for AAB.
- Leave backend has no valid transition from `REJECTED` back to `SUBMITTED`; Android therefore does
  not claim unsupported rejected-request resubmission.
- No instrumentation test suite currently exists.

## 9. Documentation updated

- `pendingwork.md`
- `PGR_SIMS_ANDROID_API_INTEGRATION.md`
- Android resident feature matrix
- Supervisor capability matrix
- Supervisor demo runbook
- This implementation report

## 10. Final status

Implementation is complete for the scoped code paths. Sprint 1 remains **CONDITIONAL GO** pending
device-level restored-session/token-refresh checks and the full legacy-feature regression matrix. Sprint
2 and later remain pending.


## Sprint 1–5 final verification — 2026-09-15

Final baseline verdict remains **CONDITIONAL GO**. Support-staff restricted routing, resident/supervisor
session restoration and forced refresh now pass, as does the isolated full Django SQLite suite
(922 tests, zero failures/errors, three explicit repository-file skips). Later device checks found
resident Inbox crashing, supervisor Inbox absent, leave replay creating duplicates, inconsistent
logbook counts, and an abrupt-upload metadata risk. Normal upload restart/discard/logout purge and
logbook exactly-once replay pass within their documented boundaries. Full write-action regression
and later feature/signed-candidate certification remain unverified. See the authoritative
[combined report](../20260914_android_sprints_2_3_4/TEST_RESULTS.md) for artifact hashes, failures,
fixture IDs, reproducible commands and remaining gates. No GO or deployment is granted here.

The later `feature/android-parity-stages-1-6` candidate supersedes the source defects listed above:
all-role Inbox, synchronous owner-bound upload metadata, persisted/deduplicated leave request IDs and
normalized logbook counts are implemented with automated coverage. Historical baseline failures stay
recorded for provenance; authenticated candidate acceptance and deployment remain separate gates.
