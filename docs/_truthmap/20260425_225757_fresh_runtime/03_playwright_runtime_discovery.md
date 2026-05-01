# Stage 3: Role-Wise Playwright Runtime Discovery

Source evidence:

- `../_truthmap_docker_fix/20260425_223918/json/stage3_browser_proof.json`
- `../_truthmap_docker_fix/20260425_223918/screenshots/`

## Runtime Role Discovery

### Resident

- Login succeeded as `resident_user`
- Landing URL: `/dashboard/resident`
- Heading: `My Training Dashboard`
- Visible nav:
  - `My Dashboard`
  - `My Schedule`
  - `Logbook`

### Supervisor

- Login succeeded as `supervisor_user`
- Landing URL: `/dashboard/supervisor`
- Heading: `Supervisor Dashboard`
- Visible nav:
  - `Overview`
  - `My Residents`

### UTRMC Admin

- Login succeeded as `utrmc_admin_user`
- Landing URL: `/dashboard/utrmc`
- Heading: `UTRMC Overview`
- Visible nav:
  - `Overview`
  - `Hospitals`
  - `Departments`
  - `H-D Matrix`
  - `Users`
  - `Supervision Links`
  - `HOD Assignments`
  - `Programmes`
  - `Eligibility Monitor`

### UTRMC Read-Only

- Login succeeded as `utrmc_staff_user`
- Landing URL: `/dashboard/utrmc`
- Same nav family as the UTRMC overview shell

### Admin

- Login succeeded as `e2e_admin`
- Landing URL: `/dashboard/utrmc`
- Same nav family as UTRMC admin

## Discovery Verdict

- The rebuilt frontend is serving the current dashboard shell and current role nav.
- Previous blanket claims that “all dashboards 404” are false after fresh runtime validation.
- The runtime-discovered role surfaces align with `frontend/lib/navRegistry.ts`.
