# Route Freeze (Next.js App Router)

Router: Next.js App Router (`app/`).

Stable role areas:
- `/login`
- `/dashboard/pg/*`
- `/dashboard/supervisor/*`
- `/dashboard/utrmc/*`

Admin users are routed to `/dashboard/utrmc/*` in the current implementation.

Current userbase/org graph screens under frozen area:
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/departments/[id]/roster`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/users/new`
- `/dashboard/utrmc/users/[id]`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/hod`

Do not rename these paths after pilot begins.

---

## Phase 6 — Academic Core Routes (2026-03-01)

### Resident / PG
- `/dashboard/resident/progress` — Academic progress + eligibility snapshot
- `/dashboard/resident/research` — Synopsis workflow (create, submit, track)
- `/dashboard/resident/thesis` — Thesis submission
- `/dashboard/resident/workshops` — Workshop completion recording

### Supervisor
- `/dashboard/supervisor/research-approvals` — Inbox: approve/review synopses

### UTRMC Admin
- `/dashboard/utrmc/programs` — Programme definitions, policy editor, milestone viewer
- `/dashboard/utrmc/eligibility-monitoring` — Eligibility monitoring with filters

These routes are frozen after pilot begins.
