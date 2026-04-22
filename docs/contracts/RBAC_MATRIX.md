# RBAC Matrix (Locked Policy)

This contract defines authoritative backend authorization behavior. Frontend route guards are convenience only.

## Roles (locked)
- `pg`
- `supervisor`
- `admin` (technical recovery/admin ops)
- `utrmc_user` (read-only oversight)
- `utrmc_admin` (UTRMC governance + override approval)

## Scope Rule (locked)
- Supervisor scope is **Option A: supervisees-only**.
- Supervisors may only read/review records for PGs assigned to them.

## Resource Matrix

### Logbook (API)
- `pg`
  - List/detail/create/update/submit: **own entries only**
  - Edit allowed only when status in `draft`, `returned`
- `supervisor`
  - Pending queue: **assigned supervisees only**
  - Verify (`approved`/`returned`/`rejected`): **assigned supervisees only**
- `utrmc_user`
  - Pending queue read: **allowed (read-only)**
  - Verify/mutate: **forbidden**
- `utrmc_admin`
  - Pending queue read: **allowed (read-only governance view)**
  - Verify/mutate: **forbidden**
- `admin`
  - Pending queue read: **all**
  - Verify/mutate: **allowed (recovery/admin operations)**

### Rotations (API)
- `pg`
  - List/detail/create/update: **own rotations only** (where endpoints exist)
- `supervisor`
  - Read: supervisees-only (where endpoints exist)
  - Cannot approve UTRMC overrides
- `utrmc_user`
  - Read oversight endpoints only (where provided)
  - Cannot approve UTRMC overrides
- `utrmc_admin`
  - May approve inter-hospital overrides via `PATCH /api/rotations/<id>/utrmc-approve/`
  - Approval requires override policy validation
- `admin`
  - Read/admin recovery operations per endpoint policy
  - Does not replace `utrmc_admin` for override approval endpoint

### Active Feature Layer — Logbook / Leave / Dashboards
- `pg` / `resident`
  - `GET/POST/PATCH /api/logbook/*`: **own records only**
  - `POST /api/logbook/{id}/submit/`: **own records only**
  - `GET /api/logbook/my-threshold/`: **allowed**
  - `GET/POST /api/leaves/`: **own training record only**
  - `GET /api/dashboard/resident/`: **allowed**
- `supervisor` / `faculty`
  - `GET /api/logbook/review-queue/`: **assigned/HOD-scope residents**
  - `POST /api/logbook/{id}/review/`: **assigned/HOD-scope residents**
  - `GET /api/utrmc/approvals/leaves/`: **assigned/HOD-scope residents**
  - `POST /api/leaves/{id}/approve|reject/`: **assigned/HOD-scope residents**
  - `GET /api/dashboard/supervisor/`: **allowed**
  - `GET /api/dashboard/hod/`: **allowed only with active HOD assignment**
- `utrmc_user`
  - Dashboards and org/userbase reads: **read-only allowed**
  - Mutations and approval/verification actions: **forbidden**
  - `GET /api/dashboard/utrmc/`: **allowed**
- `utrmc_admin`
  - Full cross-department review visibility
  - Submission verify and certificate issuance: **allowed**
  - Rotation completion verification: **allowed**
  - Dashboard endpoints: **all**
- `admin`
  - Same mutation/read capabilities as `utrmc_admin` on feature-layer workflows
  - Used for technical recovery and controlled administrative operations

### Deferred Feature Layer — Rotations / Synopsis / Thesis
- Endpoint-level RBAC remains implemented for internal verification.
- These workflows are not active release-gated UI surfaces as of 2026-04-21.
- Do not expose navigation, dashboard CTAs, or active-gate expectations for these workflows until their inactive-depth tests are promoted.

### Analytics (API + Admin Dashboard)
- Default: `admin` only
- `supervisor`: allowed only if feature flag `ANALYTICS_SUPERVISOR_ACCESS_ENABLED=true`
- Legacy alias accepted: `ANALYTICS_ALLOW_SUPERVISOR_ACCESS=true`
- `pg`, `utrmc_user`, `utrmc_admin`: forbidden
- `POST /api/analytics/events/` follows same role rule and is additionally gated by
  `ANALYTICS_UI_INGEST_ENABLED`

### Reference Data (API)
#### Department (`academics.Department`)
- Read (`list`, `retrieve`): any authenticated role
- Write (`create`, `update`, `delete`): `admin` only (`utrmc_admin` read-only)

#### Hospital (`rotations.Hospital`)
- Read (`list`, `retrieve`): any authenticated role
- Write (`create`, `update`, `delete`): `admin` only (`utrmc_admin` read-only)

#### HospitalDepartment (`rotations.HospitalDepartment`)
- Read (`list`, `retrieve`): any authenticated role
- Write (`create`, `update`, `delete`): `utrmc_admin` primary; `admin` allowed for incident recovery

### Userbase + Org Graph (API)
#### User management (`/api/users/*`)
- `admin`, `utrmc_admin`
  - list/create/update userbase users: **allowed**
- `supervisor`, `faculty`, `pg`/`resident`, `utrmc_user`
  - list/read own user row only: **allowed**
  - create/update userbase users: **forbidden**
  - retrieve own user record only: **allowed**
  - `GET /api/users/` returns the caller's own user row only when they are not a manager
  - detail requests for other user IDs are not exposed in the queryset and resolve as `404`

#### Profiles (`/api/residents/*`, `/api/staff/*`)
- `admin`, `utrmc_admin`: full CRUD scope
- non-manager users: retrieve own profile only

#### Membership/assignment/linking
- `/api/department-memberships/*`
- `/api/hospital-assignments/*`
- `/api/supervision-links/*`
- `/api/hod-assignments/*`
  - `admin`, `utrmc_admin`: **allowed**
  - other roles: **forbidden**

#### Roster reads (`/api/departments/{id}/roster/`)
- `admin`, `utrmc_admin`, `utrmc_user`: **allowed**
- `supervisor`, `faculty`: **allowed** for own active department memberships
- `pg`/`resident`: **allowed** for own active resident membership departments

## Notes
- Backend queryset scoping + object-level checks are the source of truth.
- Frontend middleware redirects improve UX but do not grant access.
