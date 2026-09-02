# Active Surface Map

| Feature / Workflow | Claimed in docs | Nav visible | FE page exists | BE exists | FE-BE linked | Runtime reachable | Classification | Notes |
|---|---|---:|---:|---:|---:|---:|---|---|
| Authentication (JWT login, forgot password) | Yes | N/A | Yes | Yes | Yes | Yes | Active | Verified by frontend tests and build routes. |
| UTRMC master data (hospitals/departments/matrix/users/supervision/HOD) | Yes | Yes | Yes | Yes | Yes | Yes | Active | CRUD and listing routes present and wired. |
| Resident training dashboard (summary/progress/schedule) | Yes | Yes | Yes | Yes | Yes | Yes | Active | Uses `/api/residents/me/summary/` and progress endpoints. |
| Research workflow (resident + supervisor approval) | Yes | Yes | Yes | Yes | Yes | Yes | Active but Partial | Core actions work; broader policy/UX hardening remains. |
| Thesis workflow | Yes | Yes | Yes | Yes | Yes | Yes | Active but Partial | Submit path wired; limited verification scope. |
| Workshops workflow | Yes | Yes | Yes | Yes | Yes | Yes | Active but Partial | Record/delete wired; no broad E2E in this pass. |
| Eligibility monitor | Yes | Yes | Yes | Yes | Yes | Yes | Active | Canonical `reasons` contract gates passing. |
| Postings workflow | Yes | Yes | Yes | Yes | Yes | Yes | Active but Partial | Resident/UTRMC pages + endpoints active. |
| Logbook workflow | Historically yes | No | No | Legacy-only | No | No | Deferred | Legacy code exists but not active runtime include/app binding. |
| Cases workflow | Historically yes | No | No | Legacy-only | No | No | Deferred | Same boundary as logbook. |
| Legacy analytics modules | Historically yes | No | No | Legacy-only | No | No | Legacy | Not part of active app include set. |

## Evidence
- Backend app activation: `backend/sims_project/settings.py` (`INSTALLED_APPS`).
- Backend route exposure: `backend/sims_project/urls.py`.
- Frontend nav exposure: `frontend/lib/navRegistry.ts`.
- Frontend route/build inventory: `npm run build` route output (captured in `05-build-and-runtime-verification.md`).
