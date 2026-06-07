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
- `/dashboard/utrmc/supervisors`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/backup`

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
- `/dashboard/utrmc/backup` — Backup & Restore Center (Backup Center module)
- `/dashboard/utrmc/supervisors` — Supervisor and faculty management dashboard (designation, specialty, and contact details)

These routes are frozen after pilot begins.

UX freeze note:
- 2026-04-02 approved change: added an admin-only bulk setup/import-export workspace inside the existing `/dashboard/utrmc` page.
- No route or sidebar label change was introduced.
- 2026-04-21 approved truth-hardening change: resident sidebar label `/dashboard/resident/progress` changed from "Academic Progress" to "Logbook"; inactive resident research/thesis/workshops/postings and supervisor research approvals were removed from active navigation. Routes still exist but are not active release-gated surfaces.
- 2026-05-30 approved Backup Center module activation: added `/dashboard/utrmc/backup` as an admin-facing operational page under the already-frozen `/dashboard/utrmc/*` area. No existing route paths were renamed.
- 2026-06-01 approved additive update: added a “Google Drive Backup” panel inside `/dashboard/utrmc/backup` (no route or navigation label changes).
- 2026-06-06 approved change (UX/UI Debug & Update): Added route `/dashboard/utrmc/supervisors` for managing supervisor and faculty profiles. Exposed deletion actions for hospitals and departments. Unlocked UX freeze rules for UI/UX debugging and active iteration as explicitly requested by the administration.
- 2026-06-06 approved addition (Password Management & Onboarding): Activated self-registration form page at `/register`, added reset-password confirmation route at `/reset-password/[uid]/[token]`, and added change-password dashboard page at `/dashboard/change-password`.

## Deferred Routes (not active release truth)
- `/dashboard/resident/research`
- `/dashboard/resident/thesis`
- `/dashboard/resident/workshops`
- `/dashboard/resident/postings`
- `/dashboard/supervisor/research-approvals`
- `/dashboard/utrmc/postings`
