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

## Active Surface Routes (truth-hardened 2026-04-21)

### Resident / PG
- `/dashboard/resident` — resident command-center dashboard
- `/dashboard/resident/schedule` — schedule timeline and leave workflow
- `/dashboard/resident/progress` — logbook draft/submit and threshold snapshot

### Supervisor
- `/dashboard/supervisor` — supervisor dashboard with leave approvals and logbook review queue

### UTRMC Admin
- `/dashboard/utrmc` — UTRMC overview and read-only oversight surface for `utrmc_user`
- `/dashboard/utrmc/programs` — Programme definitions, policy editor, milestone viewer
- `/dashboard/utrmc/eligibility-monitoring` — Eligibility monitoring with filters

These routes are frozen after pilot begins.

UX freeze note:
- 2026-04-02 approved change: added an admin-only bulk setup/import-export workspace inside the existing `/dashboard/utrmc` page.
- No route or sidebar label change was introduced.
- 2026-04-21 approved truth-hardening change: resident sidebar label `/dashboard/resident/progress` changed from "Academic Progress" to "Logbook"; inactive resident research/thesis/workshops/postings and supervisor research approvals were removed from active navigation. Routes still exist but are not active release-gated surfaces.

## Deferred Routes (not active release truth)
- `/dashboard/resident/research`
- `/dashboard/resident/thesis`
- `/dashboard/resident/workshops`
- `/dashboard/resident/postings`
- `/dashboard/supervisor/research-approvals`
- `/dashboard/utrmc/postings`
