# Route Freeze (Next.js App Router)

Router: Next.js App Router (`app/`).

Stable role areas:
- `/login`
- `/dashboard/pg/*` (legacy compatibility area; canonical resident area is `/dashboard/resident/*`)
- `/dashboard/resident/*`
- `/dashboard/supervisor/*`
- `/dashboard/utrmc/*`

Admin users are routed to `/dashboard/utrmc/*` in the current implementation.

Compatibility route:
- `/dashboard/pg`
  - Redirect shim only
  - Canonical resident area is `/dashboard/resident/*`

Current userbase/org graph screens under frozen area:
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/departments/[id]/roster`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/hod`

Do not rename these paths after pilot begins.

---

## Phase 6 — Academic Core Routes (2026-03-01)

### Resident / PG
- `/dashboard/resident` — resident command-center dashboard
- `/dashboard/resident/schedule` — schedule timeline, leave workflow, and resident rotation review/submission
- `/dashboard/resident/progress` — Academic progress + eligibility snapshot
- `/dashboard/resident/research` — Synopsis workflow (create, submit, track)
- `/dashboard/resident/thesis` — Thesis submission
- `/dashboard/resident/workshops` — Workshop completion recording
- `/dashboard/resident/postings` — Resident deputation posting request workflow

### Supervisor
- `/dashboard/supervisor` — supervisor dashboard with leave and rotation approval inboxes
- `/dashboard/supervisor/research-approvals` — Inbox: approve/review synopses

### UTRMC Admin
- `/dashboard/utrmc` — UTRMC overview, active rotation operations surface, and admin-only bulk setup/import-export workspace
- `/dashboard/utrmc/programs` — Programme definitions, policy editor, milestone viewer
- `/dashboard/utrmc/eligibility-monitoring` — Eligibility monitoring with filters
- `/dashboard/utrmc/postings` — UTRMC deputation posting approval/completion surface

These routes are frozen after pilot begins.

UX freeze note:
- 2026-04-02 approved change: added an admin-only bulk setup/import-export workspace inside the existing `/dashboard/utrmc` page.
- No route or sidebar label change was introduced.
