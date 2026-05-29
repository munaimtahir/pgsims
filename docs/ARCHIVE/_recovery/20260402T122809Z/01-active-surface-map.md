# Active Surface Map

| Module / Workflow | Current classification | User role relevance | Frontend presence | Backend presence | Runtime truth | Notes |
|---|---|---|---|---|---|---|
| Authentication (login, forgot password, profile) | Active | All users | Login and password-reset pages are active | Active auth endpoints under `/api/auth/` | Verified in browser and API tests | Forgot-password now returns generic success on delivery failure. |
| Resident dashboard home | Active | Resident / PG | `/dashboard/resident` | `/api/residents/me/summary/`, `/api/my/eligibility/` | Verified | Current canonical resident landing surface. |
| Resident schedule and leave workflow | Active | Resident / PG | `/dashboard/resident/schedule` | `/api/residents/me/summary/`, `/api/my/leaves/`, `/api/leaves/{id}/submit/` | Verified | Leave request UI is now wired to live backend behavior. |
| Resident academic progress | Active | Resident / PG | `/dashboard/resident/progress` | Summary + eligibility endpoints | Verified | Browser-visible in active route set. |
| Resident research workflow | Active | Resident / PG | `/dashboard/resident/research` | `/api/my/research/`, `/api/my/research/action/*` | Verified | Workflow gate confirms supervisor-return path and resident name contract. |
| Resident thesis workflow | Active but Partial | Resident / PG | `/dashboard/resident/thesis` | `/api/my/thesis/`, `/api/my/thesis/submit/` | Reachable and built | Active page and backend exist; broader E2E remains limited. |
| Resident workshops workflow | Active but Partial | Resident / PG | `/dashboard/resident/workshops` | `/api/my/workshops/` | Reachable and built | Active and linked; not deeply re-verified in this pass. |
| Resident postings workflow | Active but Partial | Resident / PG | `/dashboard/resident/postings` | `/api/postings/` | Reachable and built | Backend support exists; broader journey remains partial. |
| Supervisor dashboard overview | Active | Supervisor / Faculty | `/dashboard/supervisor` | `/api/supervisors/me/summary/`, `/api/leaves/` | Verified | Pending leave approvals now visible and actionable. |
| Supervisor research approvals | Active | Supervisor / Faculty | `/dashboard/supervisor/research-approvals` | `/api/supervisor/research-approvals/`, research action endpoints | Verified | Browser workflow gate passes. |
| Supervisor resident progress | Active but Partial | Supervisor / Faculty | `/dashboard/supervisor/residents/[id]/progress` | `/api/supervisors/residents/{id}/progress/` | Reachable and built | Present in active route tree; not a closure focus in this pass. |
| UTRMC master data (hospitals, departments, matrix, users, supervision, HOD) | Active | Admin / UTRMC admin / UTRMC user | Active nav and pages under `/dashboard/utrmc/*` | Active userbase/org graph APIs | Verified by lint, typecheck, build, and route inventory | Typing/runtime issues on active admin pages were resolved. |
| UTRMC programs and eligibility monitor | Active | Admin / UTRMC admin / UTRMC user | `/dashboard/utrmc/programs`, `/dashboard/utrmc/eligibility-monitoring` | Active training APIs | Verified by build and backend tests | Part of the live training surface. |
| UTRMC postings | Active but Partial | Admin / UTRMC admin | `/dashboard/utrmc/postings` | `/api/postings/` | Reachable and built | Active, but not promoted to workflow-gate coverage yet. |
| Rotation workflow | Active but Partial | Resident / Supervisor / UTRMC admin | Schedule/progress/postings context only; no dedicated complete FE lifecycle | `/api/rotations/` and approval endpoints | Backend active, FE lifecycle partial | Strong backend foundation remains preserved. |
| Logbook | Deferred | Historical resident/supervisor scope | No active nav and no active page in current dashboard tree | Legacy code exists outside active runtime boundary | Not active | Do not treat historical docs as runtime truth. |
| Cases | Deferred | Historical resident/supervisor scope | No active nav and no active page in current dashboard tree | Legacy code exists outside active runtime boundary | Not active | Deferred rather than silently claimed. |
| Legacy analytics modules | Legacy | Historical admin scope | No active dashboard exposure in current frontend | Historical endpoint inventory exists | Not authoritative active surface | Active training dashboards remain separate from legacy analytics claims. |

## Evidence references
- Frontend route tree: `frontend/app/dashboard/*`
- Navigation exposure: `frontend/lib/navRegistry.ts`
- Backend include set: `backend/sims_project/urls.py`
- Training route exposure: `backend/sims/training/urls.py`
- Workflow verification: `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts`
