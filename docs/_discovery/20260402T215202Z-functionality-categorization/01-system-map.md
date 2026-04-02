# System Map

## Major User Roles

- Public / unauthenticated
  - `/`
  - `/login`
  - `/forgot-password`
  - `/register` returns an explicit disabled-registration boundary
- Resident / PG
  - `/dashboard/resident/*`
  - compatibility shim `/dashboard/pg` -> `/dashboard/resident`
- Supervisor / Faculty
  - `/dashboard/supervisor/*`
- Admin / UTRMC admin / UTRMC user
  - `/dashboard/utrmc/*`

## Active Runtime Route Surface

### Public

- `/`
- `/login`
- `/forgot-password`
- `/register`
- `/unauthorized`

### Resident / PG

- `/dashboard/resident`
- `/dashboard/resident/schedule`
- `/dashboard/resident/progress`
- `/dashboard/resident/research`
- `/dashboard/resident/thesis`
- `/dashboard/resident/workshops`
- `/dashboard/resident/postings`

### Supervisor

- `/dashboard/supervisor`
- `/dashboard/supervisor/research-approvals`
- `/dashboard/supervisor/residents/[id]/progress`

### UTRMC / Admin

- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/departments/[id]/roster`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/postings`
- `/dashboard/utrmc/eligibility-monitoring`

## Active Backend Include Surface

From `backend/sims_project/urls.py`:

- `users/`
- `rotations/`
- `api/audit/`
- `api/bulk/`
- `api/notifications/`
- `api/` -> userbase routes
- `api/users/`
- `api/` -> training routes
- `academics/`
- `api/auth/`

From `backend/sims/training/urls.py`, the active training workflow endpoints include:

- programs, templates, milestones, policies
- resident training records
- rotations
- leaves
- postings
- research
- thesis
- workshops
- eligibility
- supervisor approvals
- resident/supervisor summary endpoints

From `backend/sims/users/userbase_urls.py`, the active org/userbase endpoints include:

- hospitals
- departments
- hospital-departments
- residents
- staff
- department memberships
- hospital assignments
- supervision links
- HOD assignments

## Deferred / Legacy Surface

These modules exist on disk under `backend/sims/_legacy/*` but are not in the active URL include set:

- analytics
- attendance
- cases
- certificates
- logbook
- reports
- results
- search

There are also no active Next.js dashboard routes for logbook, cases, certificates, search, or legacy analytics.

## Workflow Map

### Verified Active Workflows

1. Forgot-password request
   - Public page -> `/api/auth/password-reset/`
2. Resident dashboard summary and eligibility
   - Resident dashboard -> `/api/residents/me/summary/`
3. Leave workflow
   - Resident schedule draft/create/submit -> supervisor approve
4. Research supervisor-review workflow
   - Resident research submission -> supervisor return/approve
5. Rotation lifecycle
   - UTRMC create draft -> resident submit -> supervisor approve -> UTRMC activate/complete
6. Postings lifecycle
   - Resident submit -> UTRMC approve/complete

### Active But Only Lightly Verified

1. Hospitals / departments CRUD
2. Users CRUD
3. Matrix toggling
4. Supervision link creation
5. HOD assignment creation
6. Programme policy / milestones / template admin
7. Thesis submission surface
8. Workshop completion surface
9. Resident progress and UTRMC eligibility monitor
10. Supervisor resident progress detail

### Deferred / Not Active

1. Logbook
2. Cases
3. Legacy analytics dashboards
4. Legacy certificates
5. Legacy global search/history
6. Legacy reports/results/attendance modules
