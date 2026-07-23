# PGSIMS Application Overview

PGSIMS (Postgraduate SIMS / PGMS) is the system for training tracking, rotation management,
logbook/evaluation review, and programme monitoring for postgraduate medical residents at UTRMC.

**Superseded note**: an earlier version of this document described a different role model (Super
Admin, HOD, Supervisor/Faculty, Resident/PG, Data Entry/Clerk) and listed digital logbook / clinical
case features that predate the current clean-room rebuild. See `AGENTS.md` and
`docs/CANONICAL_SOURCE_OF_TRUTH.md` for the model actually in the code today, summarized below.

## Scope of the Pilot Rollout

1-2 university-affiliated training hospitals, ~2 pilot departments, ~10 supervisors/faculty
members, ~30 residents.

## Roles

Exactly four: `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF` — see
`docs/USER_ROLES_AND_PERMISSIONS.md` for the full matrix.

## Core Features (active surface)

1. **Universal identity & onboarding**: one creation flow (`/users/new`) for all four roles;
   dynamic first-login state machine (`must_change_password` → `/change-password`, missing profile
   fields → `/complete-profile`, otherwise → role dashboard).
2. **Masters & bulk import** (`/masters`): hospitals, departments, hospital-department matrix, and
   training programmes, plus bulk CSV/Excel import (with a flexible column-mapping mode) for
   hospitals, departments, matrix, programmes, supervisors, residents, resident-supervisor links,
   and rotation placements.
3. **Supervision** (`/supervision`): resident-to-supervisor assignment, with CSV import and
   data-quality checks.
4. **Rotations**: placements into a hospital-department pairing, with inter-hospital
   override/approval workflow when a resident is placed outside their home hospital.
5. **Academic workflow** (`/academics`): logbook entries and evaluation submissions, each following
   a draft → submit → supervisor review (approve/return/reject) cycle; training records, academic
   periods, rotation/evaluation templates, logbook categories.
6. **Dashboards, reports & exports** (`/academics/monitoring`, `/academics/reports/*`,
   `/dashboard/{utrmc,resident,supervisor}`): role-scoped summaries with CSV export.
7. **Backup & restore** (`/dashboard/utrmc/backup`): database backup/restore, including an optional
   Google Drive connector, plus a `/api/health/` endpoint.
8. **Audit trail**: `django-simple-history` on state-changing models plus an Activity Log API.

## Deferred / not in the active surface

Digital logbook, clinical case tracking, certificates, search, and legacy analytics dashboards exist
as code under `backend/sims/_legacy/` but are **not installed** (not in `INSTALLED_APPS`) and are
not reachable from the frontend. Resident thesis/research/workshop self-service pages and leave
management have real backend support but limited or no current frontend — see
`docs/truth-map/FRONTEND_BACKEND_TRUTH_MAP.md` §7 for the verified, current status of each.

## Technical Architecture

- **Backend**: Django 4.2 REST Framework, SimpleJWT auth, PostgreSQL, Celery/Redis for async work.
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, React Query, Zustand.
- **Deployment**: Docker Compose + a host Caddy reverse proxy.
