# PGSIMS Module Truthmap

| Module / Feature | Intended Purpose | Evidence Found | Status | Reason |
|---|---|---|---|---|
| Backend core startup (default settings) | Run Django app in normal dev mode | `manage.py check` fails with file logger permission (`backend/logs/sims_error.log`) | Broken | Cannot start with default settings in this environment |
| Backend startup (test settings) | Run app and APIs for validation | `manage.py check`, `migrate`, `/healthz/` all succeed | Done | Runnable with `DJANGO_SETTINGS_MODULE=sims_project.settings_test` |
| Frontend build + standalone serve | Production bundle and HTTP serving | `npm run build` success; `node .next/standalone/server.js` returns 200 | Done | Build artifact is runnable |
| Frontend standard start command | Serve app via package start script | `npm run start` works but warns incompatible with `output: standalone` | Partially done | Works but operational contract mismatch in startup method |
| Auth API backend | JWT auth/profile/password reset endpoints | `backend/sims/users/api_urls.py`, `api_views.py` contain login/register/reset/confirm/change-password | Done | Backend auth surface is implemented |
| Forgot-password UI flow | User password reset request from frontend | `frontend/app/forgot-password/page.tsx` has TODO + `setTimeout("coming soon")` | Broken | UI route exists but not connected to backend reset API |
| Userbase org graph (hospital/department/matrix/users) | Canonical org CRUD + roster + assignments | `userbase_urls.py`, `userbase_views.py`; userbase API tests pass | Done | Endpoints + frontend pages + passing tests exist |
| Canonical Department/Hospital model | Single Department + Hospital + matrix relation | `academics.Department`, `rotations.Hospital`, `HospitalDepartment`; migration gate test passes | Done | Canonical model present and validated |
| Training: research action return | Supervisor returns synopsis with feedback | FE calls `/api/my/research/action/supervisor-return/`; BE `VALID_ACTIONS` lacks `supervisor-return` | Broken | Endpoint contract mismatch; action rejected as unknown |
| Training: resident eligibility flow | Resident sees milestone eligibility on progress page | BE `/api/my/eligibility/` returns object with `eligibilities` + `reasons_json`; FE expects array of `{ reasons }` | Broken | Shape mismatch causes FE parser to return empty list |
| Supervisor research approvals list | Supervisor review queue | BE returns `{count, results}`; FE `toArray` supports `results`; page wired | Partially done | Loads, but UI references `p.resident` field not in serializer |
| Notifications schema | Canonical notification model/service | `notifications/models.py` uses `recipient/verb/body/metadata`; `NotificationService` in use; drift test passes | Done | Canonical schema actively implemented |
| Audit history integrity | Track model change history | `HistoricalRecords` used across active models (`users`, `training`, `audit`) | Done | Audit trail mechanism present |
| Backend full test suite | Repo-wide confidence signal | `pytest sims` fails on `_legacy` import errors | Broken | Global test command is not green |
| Frontend unit tests | Fast UI logic safety net | `npm test` => no tests found | Broken | No effective unit-test safety net |
| Frontend E2E suite | End-to-end regression confidence | Playwright smoke fails with root-owned output dirs (`EACCES`) | Broken | E2E currently non-runnable in this environment |
| Contracts/truth docs alignment | Contracts reflect runnable truth | `TRUTH_TESTS.md` references non-existent test paths; `ROUTES.md` includes `/linking/*` while app uses `/supervision` and `/hod` | Broken | Documentation drift from code reality |
| Legacy code footprint | Non-active modules kept from harming execution | `_legacy` tests still discovered by pytest and fail imports | Partially done | Legacy code isolated from runtime but still breaks full CI-style test run |
