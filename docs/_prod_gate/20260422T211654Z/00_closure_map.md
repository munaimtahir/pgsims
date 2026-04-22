# Closure Map

Timestamp (UTC): 20260422T211654Z

Source evidence:
- `docs/_prod_gate/20260421T233708Z/`
- `OUT/prod_gate_summary.md`
- `OUT/prod_gate_results.json`
- `OUT/prod_gate_code_coverage.json`
- `OUT/prod_gate_scope_coverage.json`
- `OUT/prod_gate_role_matrix.json`

## Required Closure Items

| Gate | Prior Actual | Required | Closure target |
|---|---:|---:|---|
| Active routes tested | 76% | 100% | add runtime/page tests for every mounted active route below |
| Active APIs tested | 80% | 100% | add backend/API tests for endpoints below |
| Visible CTAs tested | 51% | 100% | add Playwright CTA tests or explicit non-actionable proof |
| Invalid transitions tested | 75% | 100% critical scope | add direct API denial/state tests |
| Unauthorized access tests | 90% | 100% active scope | add role-denial tests for remaining active APIs/routes |
| Backend line coverage | 53.53% | >=95% | meaningful tests for low-coverage active modules |
| Backend branch coverage | 27.75% | >=90% | branch tests for permissions/transitions/serializers |
| Frontend line coverage | 3.77% | >=90% | component tests for mounted pages/components/API layer |
| Frontend branch coverage | 3.10% | >=85% | loading/error/empty/action branch tests |
| Schema gate | blocked | passing | wire `drf-spectacular` schema endpoint/command |

## Untested / Partially Tested Active Routes

| Route | Path | Required test target |
|---|---|---|
| Supervisor resident progress | `frontend/app/dashboard/supervisor/residents/[id]/progress/page.tsx` | Playwright route render and backend `GET /api/supervisors/residents/{id}/progress/` response shape/denial |
| UTRMC department roster | `frontend/app/dashboard/utrmc/departments/[id]/roster/page.tsx` | Playwright route render and backend `GET /api/departments/{id}/roster/` shape/denial |
| UTRMC HOD assignments | `frontend/app/dashboard/utrmc/hod/page.tsx` | visible page plus assign/edit CTA path and read-only denial |
| UTRMC data quality | `frontend/app/dashboard/utrmc/data-quality/page.tsx` | recompute/patch CTA path and role denial |
| UTRMC programs | `frontend/app/dashboard/utrmc/programs/page.tsx` | templates/policy/milestone CTA path and role denial |
| UTRMC supervision | `frontend/app/dashboard/utrmc/supervision/page.tsx` | add/edit link CTA path and role denial |
| UTRMC matrix | `frontend/app/dashboard/utrmc/matrix/page.tsx` | toggle matrix cell CTA and read-only denial |
| UTRMC users | `frontend/app/dashboard/utrmc/users/page.tsx` | add user CTA validation/success path and read-only denial |
| UTRMC hospitals | `frontend/app/dashboard/utrmc/hospitals/page.tsx` | add hospital CTA validation/success path and read-only denial |
| UTRMC departments | `frontend/app/dashboard/utrmc/departments/page.tsx` | add department CTA validation/success path and read-only denial |
| UTRMC eligibility monitor | `frontend/app/dashboard/utrmc/eligibility-monitoring/page.tsx` | filter/state assertions and endpoint shape |

Deferred mounted routes remain non-release blockers only if they keep rendering deferred notices and stay off navigation:
- `frontend/app/dashboard/resident/{research,thesis,workshops,postings}/page.tsx`
- `frontend/app/dashboard/supervisor/research-approvals/page.tsx`

## Untested / Partially Tested Active APIs

| API | Required backend test target |
|---|---|
| `GET /api/departments/{id}/roster/` | response shape for UTRMC admin/user; resident/supervisor denial |
| `GET /api/hospitals/{id}/departments/` | response shape and role matrix |
| `/api/hod-assignments/` | list/create/update, read-only denial |
| `/api/supervision-links/` | list/create/update, read-only denial |
| `/api/hospital-departments/` | matrix list/update, read-only denial |
| `/api/programs/`, `/api/program-templates/`, `/api/programs/{id}/policy/`, `/api/programs/{id}/milestones/` | shape/mutation/denial |
| `/api/admin/data-quality/*` | summary/recompute/patch audit shape and denial |
| `/api/utrmc/eligibility/` | lock UTRMC read-only behavior to expected `200`, not `200 or 403` |
| `/api/supervisors/residents/{id}/progress/` | assigned supervisor allowed; unrelated supervisor/resident denied |
| `/api/users/` | UTRMC user object-level scope retrieval denial/allowance matrix |

## Visible CTAs Still Needing Evidence

| Screen | CTA/control | Required test |
|---|---|---|
| UTRMC overview | bulk import dry-run/apply, data-quality CTA, rotation/admin action controls | execute or prove deferred/non-actionable |
| UTRMC hospitals | Add Hospital | validation + create/update + read-only hidden/denied |
| UTRMC departments | Add Department | validation + create/update + read-only hidden/denied |
| UTRMC matrix | matrix toggle | mutation + read-only hidden/denied |
| UTRMC users | Add User | validation + create + read-only hidden/denied |
| UTRMC supervision | add/edit supervision link | mutation + read-only hidden/denied |
| UTRMC HOD | assign HOD | mutation + read-only hidden/denied |
| UTRMC programs | template/policy/milestone actions | mutation + read-only hidden/denied |
| UTRMC data quality | recompute/patch actions | mutation + denial |
| Supervisor resident progress | Back/detail links | route navigation |

## Missing Invalid-Transition Tests

| Workflow | Missing invalid/denial target |
|---|---|
| Leave | approve non-submitted leave; reject non-submitted leave; resident creating leave for another training record |
| Logbook | submit approved/returned entry incorrectly; review draft entry; unrelated supervisor review denial |
| UTRMC admin cluster | read-only `utrmc_user` direct API mutations for every visible write endpoint |
| Userbase | supervisor/UTRMC user object retrieval outside allowed scope |

## Missing Unauthorized-Access Tests

| Surface | Missing test target |
|---|---|
| UTRMC roster/org endpoints | resident/supervisor direct API denial |
| UTRMC admin mutations | UTRMC read-only direct API denial |
| Supervisor progress endpoint | resident and unrelated supervisor denial |
| Data-quality endpoints | non-admin denial |

## Backend Modules Dragging Coverage Down

These are from `OUT/prod_gate_artifacts/20260421T233708Z/coverage/backend_coverage.json`.

| Module | Prior coverage | Active-scope relevance |
|---|---:|---|
| `sims/training/views.py` | 57.80% line / 41.53% branch | active dashboards, leave, logbook, UTRMC eligibility, supervisor progress |
| `sims/training/eligibility.py` | 62.50% line / 53.85% branch | active eligibility/readiness summaries |
| `sims/training/serializers.py` | 90.54% line / low partial branches | active leave/logbook/program serializers |
| `sims/users/userbase_views.py` | 68.63% line / 51.19% branch | active UTRMC users/org graph |
| `sims/users/userbase_serializers.py` | 72.58% line / 14.29% branch | active UTRMC users/org graph |
| `sims/users/data_quality.py` | 83.33% line / partial branches | active data-quality CTA |
| `sims/bulk/views.py` | 51.44% line / 37.50% branch | active bulk import/export UI |
| `sims/bulk/userbase_engine.py` | 56.11% line / 39.66% branch | active unified userbase import |
| `sims/bulk/services.py` | 11.23% line / 5.31% branch | active only where mounted bulk templates/imports call it; needs scoped coverage decision |
| `sims/common_permissions.py` | 26.48% line / 4.84% branch | active permission policy helpers |
| `sims/users/models.py` | 69.77% line / 30.77% branch | active user/role/org entities |

Clearly inactive/template/legacy modules should be excluded only if not used by mounted active runtime; active files must remain in coverage.

## Frontend Mounted Files Dragging Coverage Down

| File | Prior coverage | Required test style |
|---|---:|---|
| `frontend/app/dashboard/utrmc/page.tsx` | 0% | render dashboard with mocked API, exercise visible CTA branches |
| `frontend/app/dashboard/utrmc/data-quality/page.tsx` | 0% | render loading/error/success and recompute/patch actions |
| `frontend/app/dashboard/utrmc/programs/page.tsx` | 0% | render data and exercise template/policy controls |
| `frontend/app/dashboard/supervisor/page.tsx` | 0% | render queues, approve/reject/return branches |
| `frontend/app/dashboard/resident/schedule/page.tsx` | 0% | render leave form, validation, submit branches |
| `frontend/app/dashboard/resident/progress/page.tsx` | 0% | render logbook, draft/submit/error branches |
| `frontend/app/dashboard/utrmc/{hospitals,departments,matrix,users,supervision,hod,eligibility-monitoring}/page.tsx` | 0% | render and CTA/empty/error branch tests |
| `frontend/lib/api/{client,training,userbase,bulk,auth}.ts` | low/0% | API wrapper tests for path/payload/error behavior |
| `frontend/components/layout/Sidebar.tsx` | 0% | role nav visibility tests |
| `frontend/components/ui/ImportExportPanel.tsx` | 0% | dry-run/apply/error tests |

## Schema / OpenAPI Gap

`backend/requirements.txt` includes `drf-spectacular>=0.29.0`, but prior evidence found:
- no `drf_spectacular` app in `INSTALLED_APPS`
- no `DEFAULT_SCHEMA_CLASS`
- no `/api/schema/` route
- no reproducible schema-generation command in docs/package scripts

Required closure:
- add `drf_spectacular` to `INSTALLED_APPS`
- set `REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"`
- add `SpectacularAPIView` route, preferably `/api/schema/`
- add a backend schema smoke test
- document command: `cd backend && SECRET_KEY=test-secret python3 manage.py spectacular --file ../OUT/prod_gate_artifacts/<timestamp>/schema/openapi.yaml --validate`

