# 72 — Frontend Userbase UI

## Implemented Screens (frozen `/dashboard/*` namespace)
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/departments/[id]/roster`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/users/new`
- `/dashboard/utrmc/users/[id]`
- `/dashboard/utrmc/linking/supervision`
- `/dashboard/utrmc/linking/hod`
- Resident-access roster view:
  - `/dashboard/pg/departments/[id]/roster`

## UI Behavior
- Role guard:
  - management pages: `utrmc_admin` + `admin`
  - UTRMC roster page: `utrmc_user|utrmc_admin|admin`
  - resident roster page: `pg|resident`
- New navigation links added in `DashboardLayout` for UTRMC admin workflows.
- Added quick-action sections:
  - assign department membership
  - assign hospital-department site
  - create supervision link
  - assign HOD

## API Wiring
- New API client: `frontend/lib/api/userbase.ts`
- Client calls remain same-origin `/api/...` only.
- Key calls:
  - hospitals/departments/matrix CRUD
  - users list/create/update
  - memberships + hospital assignments
  - supervision + HOD linking
  - department roster fetch

## Compatibility Updates
- Frontend RBAC role typing now includes:
  - `resident`, `faculty`
- Middleware/dashboard routing maps:
  - resident -> `/dashboard/pg`
  - faculty -> `/dashboard/supervisor`
