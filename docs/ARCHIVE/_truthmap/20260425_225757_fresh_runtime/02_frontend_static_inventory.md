# Stage 2: Frontend Static Inventory

## Sources

- Next.js rebuild output from the fresh no-cache image build
- `frontend/lib/navRegistry.ts`
- `find frontend/app -name page.tsx`

## Build-Time Route Inventory Confirmed In Fresh Image

From the rebuilt image output:

- `/dashboard/resident`
- `/dashboard/resident/progress`
- `/dashboard/resident/schedule`
- `/dashboard/resident/workshops`
- `/dashboard/supervisor`
- `/dashboard/utrmc`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/data-quality`
- additional UTRMC pages: hospitals, departments, matrix, HOD, eligibility-monitoring, postings

## Static Page Files Present

Key page files on disk:

- `frontend/app/dashboard/resident/page.tsx`
- `frontend/app/dashboard/resident/progress/page.tsx`
- `frontend/app/dashboard/resident/schedule/page.tsx`
- `frontend/app/dashboard/resident/workshops/page.tsx`
- `frontend/app/dashboard/supervisor/page.tsx`
- `frontend/app/dashboard/utrmc/page.tsx`
- `frontend/app/dashboard/utrmc/users/page.tsx`
- `frontend/app/dashboard/utrmc/programs/page.tsx`
- `frontend/app/dashboard/utrmc/supervision/page.tsx`
- `frontend/app/dashboard/utrmc/data-quality/page.tsx`

## Sidebar Registry (Current Source Of Truth)

### Resident

- `My Dashboard` -> `/dashboard/resident`
- `My Schedule` -> `/dashboard/resident/schedule`
- `Logbook` -> `/dashboard/resident/progress`

### Supervisor

- `Overview` -> `/dashboard/supervisor`
- `My Residents` -> `/dashboard/supervisor`

### UTRMC/Admin

- `Overview`
- `Hospitals`
- `Departments`
- `H-D Matrix`
- `Users`
- `Supervision Links`
- `HOD Assignments`
- `Programmes`
- `Eligibility Monitor`

## Static Findings Relevant To Audit Questions

- Workshops route file exists, but workshops is not present in resident nav.
- Bulk UI is not a separate route; it is embedded inside `frontend/app/dashboard/utrmc/page.tsx` via `BulkSetupWorkspace`.
- Data Quality page exists in source and image build output.
- Programs page is a detail/management surface for existing programs; no separate static page for “create program” or “edit program”.
