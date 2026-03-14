# 1. Executive truth summary

PGSIMS is a **mid-development unstable** build: substantial active implementation exists, but system-level reliability is not yet trustworthy. The backend is runnable only under test settings in this environment; default startup fails from file permission misconfiguration. Frontend builds and serves successfully. Core userbase/canonical data features are implemented and tested, but important training workflow integrations are broken due frontend-backend payload/action drift. Test trust is mixed: active backend modules pass, while full backend suite, frontend unit tests, and E2E execution are currently broken/non-runnable. Main risks are contract drift, test gate unreliability, and environment/permission hygiene.

True status now: **feature-rich slices exist, but operational and contract consistency is not yet production-grade.**

# 2. Environment and execution evidence

## Commands run and outcomes

- `cd backend && SECRET_KEY='audit-secret' DEBUG='True' python3 manage.py check`
  - Failed: `PermissionError` for `backend/logs/sims_error.log`; logger handler init fails.

- `ls -ld backend/logs && ls -l backend/logs/sims_error.log`
  - `sims_error.log` owner is `ubuntu:ubuntu`; not writable by current user.

- `cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test python3 manage.py check`
  - Passed.

- `cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test python3 manage.py migrate --noinput`
  - Passed (`No migrations to apply`).

- `runserver 127.0.0.1:18014` + `curl /healthz/`
  - 200 OK; health JSON shows DB/cache ok, celery not available.

- `cd frontend && npm run build`
  - Passed.

- `cd frontend && npm run start -- -p 13000`
  - Serves 200 but warns `next start` is not correct for `output: standalone`.

- `cd frontend && PORT=13001 HOSTNAME=127.0.0.1 node .next/standalone/server.js`
  - Serves 200.

- `python3 -m pip install -r backend/requirements.txt --dry-run`
  - Failed: externally-managed environment (PEP 668).

- `python3 -m venv .audit-venv`
  - Failed: `ensurepip` unavailable (`python3.12-venv` missing).

## Seed status

- `manage.py help` shows `create_superadmin`, `import_trainees`; **no `sims_seed_demo` command found**.
- Seed workflow not executed.

## What could / could not be directly verified

- Verified directly: backend check/migrate/health under test settings, frontend build/serve, multiple test and lint commands.
- Could not verify end-to-end user workflows in browser due Playwright write-permission errors.

# 3. Module-by-module status table

See `audit/MODULE_TRUTHMAP.md` for full table. Summary:

| Module / Feature | Intended Purpose | Evidence Found | Status | Reason |
|---|---|---|---|---|
| Backend default startup | Run Django in normal dev mode | `manage.py check` fails on logger file permissions | Broken | Runtime blocked by file ownership |
| Backend test-settings startup | Runnable API instance | check+migrate+health pass | Done | Executable in audit context |
| Frontend build + standalone serve | Production frontend runtime | build pass + 200 response | Done | Works with standalone server |
| Auth API backend | Login/register/profile/password reset | API endpoints and views present | Done | Implemented server-side |
| Forgot password page | UI reset flow | TODO + “coming soon” placeholder | Broken | Not wired to API |
| Userbase org graph | Hospitals/departments/users/linking | Endpoints, pages, tests pass | Done | End-to-end implementation present |
| Canonical model | Single Department/Hospital | Model evidence + migration gate tests pass | Done | Contract intent enforced |
| Training research return action | Supervisor return feedback | FE calls unsupported backend action | Broken | Endpoint/state-machine mismatch |
| Training eligibility display | Resident eligibility UI | FE parser shape mismatch vs backend payload | Broken | Data not rendered correctly |
| Notifications canonical schema | In-app/email canonical fields | model/service/drift test evidence | Done | Correct schema in active code |
| Full backend test suite | Global safety gate | `pytest sims` collection errors in `_legacy` | Broken | Not CI-green |
| Frontend unit tests | Component/unit confidence | `npm test` reports no tests found | Broken | No effective unit test execution |
| Frontend E2E tests | Workflow confidence | Playwright EACCES on output dirs | Broken | Execution blocked by FS permissions |

# 4. Done

- **Canonical Department/Hospital model**
  - Implemented in `backend/sims/academics/models.py` and `backend/sims/rotations/models.py`.
  - Migration gate tests pass: `sims/rotations/test_canonical_migration_gate.py`.

- **Userbase/org graph API + pages**
  - Endpoints in `backend/sims/users/userbase_urls.py` + `userbase_views.py`.
  - Frontend pages under `/dashboard/utrmc/*` and `/dashboard/pg/departments/[id]/roster`.
  - Backend userbase tests pass in active-suite run.

- **Notifications canonical schema**
  - `Notification` model uses `recipient`, `verb`, `body`, `metadata`.
  - `NotificationService` writes canonical fields.
  - Drift guards pass.

- **Frontend production build and standalone serve**
  - `npm run build` and `node .next/standalone/server.js` both verified.

# 5. Partially done

- **Frontend standard startup path**
  - Works but emits standalone mismatch warning.
  - Needs startup convention correction in run/deploy docs/scripts.

- **Legacy isolation**
  - Legacy modules are not in active apps, but legacy tests still break full test runs.
  - Requires test discovery strategy (or legacy archive strategy) to restore a single green command.

- **Supervisor research approvals UX**
  - Data fetch wiring exists (`{count, results}` handled), approvals path works in code.
  - Page references `p.resident` field that serializer does not provide (`resident_name` exists).

# 6. Broken

- **Backend default run mode broken**
  - Failure: logger permission at `backend/logs/sims_error.log`.
  - Root cause: file ownership mismatch (`ubuntu:ubuntu`).
  - Type: local/ops.
  - Severity: **high**.

- **Research return action broken**
  - FE calls `/api/my/research/action/supervisor-return/`.
  - Backend `ResearchProjectActionView.VALID_ACTIONS` lacks `supervisor-return`.
  - Type: integration contract drift.
  - Severity: **high**.

- **Eligibility rendering broken**
  - Backend returns object with `eligibilities` and serializer field `reasons_json`.
  - FE expects array and `reasons`.
  - Result: UI likely renders empty/incorrect eligibility list.
  - Type: integration contract drift.
  - Severity: **high**.

- **Forgot password UI broken/incomplete**
  - Page explicitly TODO and shows “coming soon” timer message.
  - Backend reset endpoints exist but UI not connected.
  - Type: frontend workflow gap.
  - Severity: **medium**.

- **Backend full suite broken**
  - `pytest sims` fails with 9 collection errors from `_legacy` import paths.
  - Type: test infrastructure/repo hygiene.
  - Severity: **high**.

- **Frontend unit test baseline broken**
  - `npm test` exits with no tests found.
  - Type: quality gate gap.
  - Severity: **high**.

- **Frontend E2E broken in environment**
  - Playwright fails with `EACCES` on root-owned result/report dirs.
  - Type: environment/permissions.
  - Severity: **high**.

- **Static quality gates broken**
  - Frontend lint fails with many TS/ESLint errors.
  - Backend flake8 fails with 355 issues.
  - Type: code quality.
  - Severity: **medium** (high when enforcing CI quality gates).

# 7. Contract and integration mismatch review

- **Missing/unsupported action**
  - FE: `trainingApi.supervisorReturnResearch()` posts action `supervisor-return`.
  - BE: no such action in research state machine.

- **Eligibility payload mismatch**
  - BE `/api/my/eligibility/`: object wrapper with `eligibilities`.
  - FE `getMyEligibility()`: `toArray` expecting array or `{results}`.
  - Serializer field drift: `reasons_json` (BE) vs `reasons` (FE interface).

- **Route contract drift**
  - `docs/contracts/ROUTES.md` freezes `/dashboard/utrmc/linking/supervision` and `/linking/hod`.
  - Implemented app routes are `/dashboard/utrmc/supervision` and `/dashboard/utrmc/hod`.

- **Truth-test contract drift**
  - `docs/contracts/TRUTH_TESTS.md` references tests under `sims.logbook` and `sims.analytics` not present in active code layout.

- **UI/API disconnect**
  - Forgot-password page not using available auth API (`/api/auth/password-reset/`).

# 8. Test truth review

- **Suites that exist**
  - Backend app tests (active + legacy), drift tests, migration gate tests.
  - Frontend Playwright suites (many specs).
  - Jest config exists.

- **What they really validate now**
  - Active backend modules: meaningful validation (80 passing tests).
  - Drift/migration tests: targeted governance checks pass.
  - Full backend command: unusable due legacy import failures.
  - Jest: effectively no runnable unit tests in current tree/config.
  - Playwright: blocked by FS permissions before test truth can be established.

- **Critical untested/under-verified flows**
  - End-to-end training UI workflows against live backend in this environment.
  - Password-reset UX path.
  - Real-world supervisor return + resident eligibility display correctness from UI.

- **Do tests reflect reality?**
  - Partially. Active backend app tests do, but global and frontend gates do not currently provide trustworthy release confidence.

- **Test trustworthiness score:** **4/10**.

# 9. Real blockers

See `audit/BLOCKERS.md`.

Priority blockers:
1. FE↔BE training contract drift in active user workflows.
2. No single green test gate across backend/frontend/E2E.
3. Permission/run hygiene (backend logger path, Playwright output ownership).
4. Contracts/docs no longer match executable truth.

# 10. Next critical milestone

- **Milestone name:** Contract & Gate Stabilization Baseline

- **Why this is next:**
  - It removes false confidence first: currently visible features are broken by contract drift and quality gates are unreliable.

- **Exact scope:**
  - Fix active FE↔BE contract mismatches in training flows.
  - Restore one reliable backend full-suite command and one frontend test gate.
  - Fix environment ownership/startup issues blocking deterministic execution.
  - Update contract docs (`TRUTH_TESTS.md`, `ROUTES.md`, training payload contracts) to match executable reality.

- **What should be fixed/finished in this milestone:**
  - Research return action alignment.
  - Eligibility payload alignment (`eligibilities` wrapper + reason field naming).
  - Password reset UI wiring to existing backend endpoint.
  - Test discovery/legacy strategy so `pytest sims` is meaningful.
  - Playwright output directory ownership and rerun smoke.
  - Backend logging path ownership fix.

- **What should NOT be touched yet:**
  - New feature expansion.
  - Major UX/route renaming beyond explicit route-contract correction.
  - Broad refactors not tied to contract/gate stabilization.

- **Expected outcome after completion:**
  - Active user workflows stop failing due contract mismatch.
  - One reproducible green baseline for backend + frontend test execution.
  - Documentation becomes a truthful execution contract again.

# 11. Final classification snapshot

- Done: **6** items
- Partially done: **3** items
- Broken: **9** items

Top 5 immediate priorities:
1. Fix research return action contract mismatch.
2. Fix eligibility response/typing mismatch end-to-end.
3. Restore global backend test gate (`pytest sims`) by resolving legacy collection failures.
4. Make frontend tests executable (unit + Playwright FS permissions).
5. Resolve backend default startup logging permission issue.

Overall status verdict: **Mid-development unstable**.
