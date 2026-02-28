# 70 — Feature Spec Lock: User Base + Org Graph

## Phase 0 Baseline (No Code Changes)
- `git rev-parse HEAD`: `c816659d55b209ab1daa4b91c315c01105c3687e`
- `git status --short`: clean (no tracked changes at capture time)
- `docker compose -f docker/docker-compose.prod.yml ps`: backend/frontend/db/redis/worker/beat all running and healthy.

## Existing Inventory Snapshot

### Reusable (Matches/Partially Matches)
- Canonical entities already exist:
  - `sims.rotations.models.Hospital`
  - `sims.academics.models.Department`
  - `sims.rotations.models.HospitalDepartment` with unique `(hospital, department)`.
- Existing RBAC foundations:
  - `sims.common_permissions` includes read/write split helpers and UTRMC/admin role checks.
- Existing APIs:
  - `/api/rotations/hospitals/` (admin write)
  - `/api/rotations/hospital-departments/` (utrmc_admin/admin write)
  - `/academics/api/departments/` (admin write)
  - `/api/auth/login/`, `/api/auth/profile/`
- Existing UTRMC UI area:
  - `/dashboard/utrmc`, `/dashboard/utrmc/cases`, `/dashboard/utrmc/reports`
- Existing client wiring is compliant:
  - frontend client defaults to same-origin `/api/...`
  - SSR fallback supports `http://backend:8014`.

### Missing / Requires Replacement
- No canonical models for:
  - `StaffProfile`, `ResidentProfile`
  - `DepartmentMembership`, `HospitalAssignment`
  - `SupervisorResidentLink`, dated `HODAssignment`
- No required endpoints:
  - `/api/users/` CRUD+filters
  - `/api/residents/{id}/`, `/api/staff/{id}/`
  - `/api/department-memberships/`, `/api/hospital-assignments/`
  - `/api/supervision-links/`, `/api/hod-assignments/`
  - `/api/departments/{id}/roster/`, `/api/hospitals/{id}/departments/`
- No UTRMC userbase console screens for matrix/users/linking/rosters.

## Locked Canonical Data Model (Implementation Target)

### Core Master Data
- `Hospital` (existing canonical): `id, name, code, active/is_active, created_at`
- `Department` (existing canonical): `id, name, code, active, created_at`
- `HospitalDepartment` (existing canonical):
  - `id, hospital(FK), department(FK), active/is_active, created_at`
  - `UniqueConstraint(hospital, department)`

### Users and Profiles
- User role semantics must include:
  - `admin`, `utrmc_admin`, `utrmc_user`, `supervisor`, `resident(pg)`, `faculty`
- `StaffProfile`:
  - `user(O2O), designation, phone, active`
- `ResidentProfile`:
  - `user(O2O), pgr_id, training_start, training_end, training_level/year, active`

### Membership + Assignments
- `DepartmentMembership`:
  - `id, user(FK), department(FK), member_type(faculty|supervisor|resident), is_primary, active, start_date, end_date`
  - enforce member_type/role consistency
  - one active primary per user (recommended lock)
- `HospitalAssignment`:
  - `id, user(FK), hospital_department(FK), assignment_type(primary_training|posting|faculty_site), start_date, end_date, active`

### Linking
- `SupervisorResidentLink`:
  - `id, supervisor_user(FK), resident_user(FK), department(FK optional), start_date, end_date, active`
  - role constraint: supervisor_user in `{supervisor, faculty}`, resident_user in `{resident, pg}`
- `HODAssignment`:
  - `id, department(FK), hod_user(FK), start_date, end_date, active`
  - role constraint: hod_user in `{faculty, supervisor}`
  - only one active HOD per department.

### Auditability
- Add `created_by`, `updated_by` on linking/assignment models where applicable.

## Locked RBAC Rules (Implementation Target)
- Hospital/Department CRUD: **admin only**
- HospitalDepartment matrix writes: **utrmc_admin**, with **admin override**
- User creation + linking + membership/assignment: **utrmc_admin/admin**
- Residents/supervisors/faculty:
  - may view own profile only
  - roster read allowed when scoped to their own active department membership.
- UTRMC roles:
  - roster and management views per endpoint policy.

## Locked API Surface (Required)
- Auth:
  - `POST /api/auth/login/`
  - `GET /api/auth/me/` (or equivalent alias)
- Master:
  - `GET/POST /api/hospitals/`
  - `GET/PATCH /api/hospitals/{id}/`
  - `GET/POST /api/departments/`
  - `GET/PATCH /api/departments/{id}/`
  - `GET/POST /api/hospital-departments/`
  - `PATCH /api/hospital-departments/{id}/`
- Users/profiles:
  - `GET/POST /api/users/` (filters role/department/active/search)
  - `GET/PATCH /api/users/{id}/`
  - `GET/PATCH /api/residents/{id}/`
  - `GET/PATCH /api/staff/{id}/`
- Membership/assignments:
  - `POST /api/department-memberships/`
  - `PATCH/DELETE /api/department-memberships/{id}/` (soft deactivate supported)
  - `POST /api/hospital-assignments/`
  - `PATCH/DELETE /api/hospital-assignments/{id}/`
- Linking:
  - `GET/POST /api/supervision-links/`
  - `PATCH /api/supervision-links/{id}/`
  - `GET/POST /api/hod-assignments/`
  - `PATCH /api/hod-assignments/{id}/`
- Rosters:
  - `GET /api/departments/{id}/roster/`
  - `GET /api/hospitals/{id}/departments/`

## Locked UI Surface (UTRMC Console)
Under frozen route namespace (`/dashboard/utrmc/*`), implement:
- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/users/new`
- `/dashboard/utrmc/users/[id]`
- `/dashboard/utrmc/linking/supervision`
- `/dashboard/utrmc/linking/hod`
- `/dashboard/utrmc/departments/[id]/roster`

## Acceptance Criteria + Test Checklist
- [ ] Model layer complete with constraints/indexes and migrations applied.
- [ ] RBAC classes implemented and endpoint policies enforced.
- [ ] Required API endpoints available and contract documented.
- [ ] UTRMC console screens implemented with same-origin `/api/...` client calls.
- [ ] Role guard for admin/utrmc_admin on management screens.
- [ ] Backend tests added:
  - resident cannot create departments
  - supervisor cannot create users
  - utrmc_admin can create linking
  - one active HOD per department
  - unique hospital-department pair
  - link role constraints
- [ ] OpenAPI export refreshed into `OUT/openapi.json`.
- [ ] Playwright E2E flow added and executed.
- [ ] Cleanup dependency audit completed; obsolete same-category code removed when safe.
- [ ] Final verification gates pass (backend checks/tests/migrate, frontend build, e2e smoke).
