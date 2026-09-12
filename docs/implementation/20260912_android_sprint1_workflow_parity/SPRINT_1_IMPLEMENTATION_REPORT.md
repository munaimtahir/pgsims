# PGSIMS Android — Sprint 1 Workflow Parity Report

Date: 2026-09-12
Verdict: CONDITIONAL GO

## 1. Baseline

- Starting branch: `remediation/pgsims-final-production-readiness`
- Starting SHA: `67e604087715251559de4abf170a705241ef0681`
- Final implementation SHA: `500f95ef6a4d07170d9dafca7923fa909950d43b`
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
| `python3 manage.py check` on VPS | PASS |
| `python3 manage.py makemigrations --check --dry-run` on VPS | PASS |
| `python3 manage.py test --noinput` on VPS | PASS — 921 tests |
| `bash scripts/check_update_0_identity_cleanup.sh` on VPS | PASS |
| `adb` install/launch on `emulator-5554` | PASS — sign-in screen rendered, no crash |
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

- Full authenticated UI walkthrough through the installed Android app was not automated; the
  emulator smoke verified cold launch/sign-in rendering, while the complete mutation chain was
  verified against the live backend contract with curl.
- Release `assembleRelease`/AAB signing was not run because owner-controlled signing properties
  were not supplied. Release Kotlin compilation and lint passed.
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

Implementation is complete for the scoped code paths. Sprint 1 remains **CONDITIONAL GO** until an
authenticated emulator walkthrough and owner-approved signed release build are completed. Sprint 2
and later remain pending.
