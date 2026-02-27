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

### Analytics (API + Admin Dashboard)
- Default: `admin` only
- `supervisor`: allowed only if feature flag `ANALYTICS_ALLOW_SUPERVISOR_ACCESS=true`
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

## Notes
- Backend queryset scoping + object-level checks are the source of truth.
- Frontend middleware redirects improve UX but do not grant access.
