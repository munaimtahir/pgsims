# Frontend Navigation Audit

Date: 2026-09-10
Branch: `fix/frontend-authenticated-shell-navigation`

## Executive Summary

The authenticated sidebar disappeared whenever an ADMIN/SUPERVISOR/RESIDENT navigated from
`/dashboard/*` to any of the top-level entity routes (`/residents`, `/users`, `/supervisors`,
`/academics/*`, `/supervision/*`, `/admins`, `/support-staff`, `/masters`, `/profile`). Root
cause confirmed and fixed: those routes are Next.js App Router siblings of `app/dashboard/`,
not descendants, so they never inherited `app/dashboard/layout.tsx`'s `DashboardLayout`/
`Sidebar`. Fixed by adding a thin `layout.tsx` to each affected top-level folder that renders
the same shared `DashboardLayout`. Verified live in a browser for ADMIN, SUPERVISOR and
RESIDENT logins; sidebar persists across navigation and page refresh, with correct
role-scoped nav content in every case.

While auditing, a second real bug (matching `docs/discovery/20260909_.../12_BUG_TECH_DEBT_REGISTER.md`
item WEB-7) was confirmed and fixed: Logbook, Evaluations, Monitoring, My Progress,
Supervisor Workload, Workflow Overview/Data-Quality, and the academics report pages were
fully built and wired to real APIs but absent from `navRegistry.ts` for every role — real
users could not reach them without a typed/bookmarked URL. Also found and fixed a genuine
dashboard-count bug (admin dashboard showed "0 Supervisors" / "0 Support Staff" despite
6/1 existing) caused by the stats code reading only page 1 (25 rows, default DRF page size)
of `/api/users/` instead of the paginated `count` field.

## Confirmed Root Cause

- `frontend/app/dashboard/layout.tsx` is the only place `DashboardLayout`
  (`frontend/components/layout/DashboardLayout.tsx`) → `Sidebar`
  (`frontend/components/layout/Sidebar.tsx`) was mounted.
- `frontend/lib/navRegistry.ts`'s `NAV_SECTIONS` links Admin/Supervisor/Resident nav to
  top-level folders (`app/residents`, `app/users`, `app/supervisors`, `app/academics/*`,
  `app/supervision/*`, `app/admins`, `app/admin`, `app/support-staff`, `app/masters`,
  `app/profile`) that are **not** children of `app/dashboard/` — a Next.js `layout.tsx`
  only wraps its own folder subtree, so these routes fell back to the bare
  `frontend/app/layout.tsx` (no shell).
- No route groups (`app/(authenticated)`, `app/(public)`) existed. `frontend/middleware.ts`'s
  matcher is `['/dashboard/:path*']` only, so these routes also relied solely on per-page
  client-side `ProtectedRoute` for auth — a related but separate finding (not the direct
  cause of the missing sidebar).

## Architecture Before

```
app/layout.tsx              (no shell)
app/dashboard/layout.tsx    -> DashboardLayout -> Sidebar   (only place shell exists)
app/residents/page.tsx      (no layout.tsx -> falls back to bare root layout, no shell)
app/users/page.tsx          (same)
app/academics/**            (same)
app/supervision/**          (same)
... etc.
```

## Architecture After

Added a `layout.tsx` (identical ~5-line pattern to `app/dashboard/layout.tsx`) to each
top-level folder with sidebar links pointing into it:

```
frontend/app/residents/layout.tsx
frontend/app/users/layout.tsx
frontend/app/supervisors/layout.tsx
frontend/app/support-staff/layout.tsx
frontend/app/admins/layout.tsx
frontend/app/admin/layout.tsx        (covers /admin/pending-supervisor-links)
frontend/app/masters/layout.tsx
frontend/app/academics/layout.tsx    (covers all /academics/* children automatically)
frontend/app/supervision/layout.tsx  (covers all /supervision/* children automatically)
frontend/app/profile/layout.tsx
```

Each renders `<DashboardLayout>{children}</DashboardLayout>` — the one existing shell
component, reused, not duplicated. Zero URL changes, zero file moves. `app/login`,
`app/register`, `app/forgot-password`, `app/reset-password`, `app/unauthorized`,
`app/change-password`, `app/complete-profile` intentionally were **not** given a layout —
they stay outside the authenticated shell.

Route groups (`app/(authenticated)/...`) were considered (the approach suggested in the
original task) and rejected: they would require physically moving ~10 folders and
re-verifying every relative import/test path across them for the same URL outcome, at much
higher regression risk than adding 10 small new files.

## Role Navigation Matrix (post-fix)

| Role | Sections | Top-level routes | Sidebar persists |
|---|---|---|---|
| ADMIN | Admin | Dashboard, Users, Residents, Document Requirements, Pending Supervisor Links, Supervisors, Support Staff, Admins, Masters, Data Quality, Backup Center, Supervision (5 sub-items), Academics (20 sub-items after WEB-7 fix) | ✅ verified live |
| SUPERVISOR | Supervisor | My Dashboard, My Residents, Supervision Ledger, Academic Review Queue, Logbook Review, Evaluations, Rotation Approvals, Leave Approvals, My Workload, 3 report links, My Profile | ✅ verified live |
| RESIDENT | Resident | My Dashboard, My Training, My Supervisor, My Documents, My Academic Summary, My Progress, My Logbook, My Evaluations, My Rotations, My Leave, 2 report links, My Profile | ✅ verified live |
| SUPPORT_STAFF | Support Staff | My Dashboard, My Profile | not verified live this session (browser extension disconnected mid-session — see Remaining Known Issues) |

Note: Supervisor's "My Dashboard"/"My Residents"/"Supervision Ledger" and Resident's "My
Dashboard"/"My Training"/"My Supervisor"/"My Academic Summary" intentionally all point at
the same single dashboard route today — that dashboard page already renders all of that
information in one view (verified live: supervisor dashboard shows assigned residents +
pending counts; resident dashboard shows training + supervisor + pending counts together).
Treated as **INTENTIONAL**, not dead/duplicate links, since splitting them would fragment a
page that already presents this data coherently; left unchanged per the plan's instruction
not to silently alter this without confirming intent.

## Frontend Route Audit

All 66 unique hrefs in `NAV_SECTIONS` were checked against the live `frontend/app/` route
tree and are enforced by an automated test (`frontend/lib/navRegistry.test.ts`, 129
assertions, all passing) that:
1. asserts every href resolves to a real `page.tsx`, and
2. asserts every href's top-level segment sits under a folder with a `layout.tsx` (i.e. is
   inside the authenticated shell).

This test runs as part of `npm test` and will fail CI if a future PR adds a dead nav item or
a nav item that bypasses the shell.

## Frontend → API → Backend Mapping (spot-checked, risk areas)

- **Pending Supervisor Links** (`/admin/pending-supervisor-links`) → backend
  `PendingSupervisorAssignment` model (`backend/sims/supervision/models.py`) via
  `backend/sims/supervision/urls.py`'s router (`assignments/`) and dedicated
  `change-primary/`, `options/`, `data-quality/`, `import/` endpoints. No route in this
  flow touches `/admin/`/Django-admin login — confirmed by reading the URL config directly.
- **Supervisor directory / assignments** → `ResidentSupervisorAssignment`
  (`backend/sims/supervision/models.py`), same router. Verified live: `/supervisors` lists
  6 real supervisor identities including the reconciled `supervisor` login (Prof. M. Tahir
  Bashir Malik), with the retired real-identity row correctly shown "Inactive".
- **Admin dashboard stats** (`userbaseApi.users.list()` → `/api/users/`, DRF
  `UserViewSet`, `PageNumberPagination`, `PAGE_SIZE=25`): confirmed the dashboard was
  reading only the first page of results and filtering client-side, undercounting any role
  whose rows didn't fit page 1. Fixed by adding `userbaseApi.users.count()` (reads the
  response's `count` field per role filter) and switching
  `frontend/app/dashboard/utrmc/page.tsx` to use it. Verified live: dashboard now correctly
  shows 6 Supervisors / 1 Support Staff instead of 0/0.

## Dead/Broken Links Found

None of the 66 registered hrefs were dead (all resolve to real pages) — the reported defect
was the missing shell, not missing pages. The WEB-7 gap (real pages with **no** nav entry at
all) is the inverse problem and is fixed above.

## Repairs Made

1. 10 new `layout.tsx` files mounting the shared `DashboardLayout` (shell fix).
2. `frontend/lib/navRegistry.ts`: added Logbook, Logbook Categories (moved into visible
   position), Evaluations, Monitoring, Workflow Overview, Workflow Data Quality, and 5
   report routes to the Admin/Supervisor/Resident sections, scoped per each page's actual
   `ProtectedRoute allowedRoles` (verified by reading each page file directly, not guessed).
3. `frontend/lib/api/userbase.ts` + `frontend/app/dashboard/utrmc/page.tsx`: fixed the
   supervisor/support-staff undercount (dashboard count bug, addendum section D.3/K).
4. `frontend/lib/navRegistry.test.ts`: new regression test (129 assertions).
5. `frontend/app/dashboard/utrmc/page.test.tsx`: updated existing test mock for the new
   `userbaseApi.users.count` call.

## Permission Findings

- Nav-level role scoping in `navRegistry.ts` for every newly-added item matches the
  corresponding page's `ProtectedRoute allowedRoles` exactly (checked by reading each page
  file's guard, not assumed) — no nav item is now visible to a role whose page would reject
  it.
- Confirmed (per earlier codebase exploration) that `SupportStaffProfile.department_ref`
  exists but is not enforced by any queryset/permission filtering anywhere in the backend —
  SUPPORT_STAFF access today is coarse (role-only gated, blocked-by-default on several
  academics endpoints, or full-access on rotation/leave inbox views). This is a pre-existing
  gap, not something this fix introduced or attempted to widen; see the demonstration
  readiness report for how the canonical `staff` account was scoped without touching backend
  permission logic.

## Supervisor-Link Findings

Live-verified end to end: `supervisor` login → Prof. M. Tahir Bashir Malik profile → 7
assigned residents → 2 pending Academic Review Queue items, one of which is the canonical
`resident` login (Dr. Jawad Saifullah), who in turn sees "Primary supervisor: M. Tahir
Bashir Malik" and "2 Pending Review Items" on their own dashboard. This confirms the
`reconcile_urology_supervisor_profiles` identity-swap (built in the concurrently-running
Urology demo sprint) is correct end-to-end through the fixed navigation shell.

## Academics Findings

All `/academics/*` pages (20 registered after the WEB-7 fix) now sit under
`app/academics/layout.tsx`, so every child route automatically inherits the shell without
needing its own layout file. Loading/empty/error states were not individually re-audited
this session beyond what the existing Jest/Playwright suites already cover.

## Automated Tests Added

- `frontend/lib/navRegistry.test.ts` (new) — static route-contract regression test, 129
  assertions, all passing.
- `frontend/app/dashboard/utrmc/page.test.tsx` (updated) — mock updated for the new
  `count()` API method.

## Manual Verification

Performed live via Chrome browser automation against a local dev stack
(Django `runserver` on sqlite + `next dev`), logged in through the real `/login` page:

- **ADMIN** (`admin`): dashboard loads with correct (now-fixed) counts; clicked Residents
  and Supervisors from the sidebar — shell persisted on both, correct data rendered.
- **SUPERVISOR** (`supervisor`, resolves to Prof. M. Tahir Bashir Malik): dashboard shows 7
  assigned residents + 2 pending items; clicked Academic Review Queue — shell persisted,
  both pending items shown with resident/supervisor links and Approve/Dismiss actions.
- **RESIDENT** (`resident`, resolves to Dr. Jawad Saifullah): dashboard shows training,
  primary supervisor, and pending-item count consistent with the supervisor's view.
- **SUPPORT_STAFF** (`staff`): account created and department-scoped to Urology
  Department, but live browser login was not completed — the Chrome extension disconnected
  mid-session (see Remaining Known Issues).
- Logout between roles was clean — no stale role's nav or data was visible after switching
  accounts.

## Remaining Known Issues

- SUPPORT_STAFF (`staff`) login/navigation was not verified live in a browser this session
  (tooling disconnect). The account exists, is `SUPPORT_STAFF`, and is linked to "Urology
  Department" via `SupportStaffProfile.department_ref` — but no backend queryset actually
  filters by that field yet (see Permission Findings), so this login today gets whatever the
  existing coarse SUPPORT_STAFF rules already grant, not a true Urology-scoped view. This is
  flagged, not silently fixed, since building real department-scoped filtering is a new,
  non-trivial RBAC change out of scope for a navigation fix.
- Full 4-role Playwright regression run (`npm run test:e2e:regression`) against the
  docker-composed stack was not executed this session (local dev used sqlite + `runserver`/
  `next dev` instead of the Docker stack, since no `.env` with DB/secret credentials was
  present in this environment). The static Jest suite (243 tests) and full production build
  were run and pass.
- Negative RBAC deep-link tests (resident → `/users`, etc.) were not exercised live this
  session; existing `frontend/e2e/rbac/access-control.spec.ts` covers this pattern and
  should be extended/run as a follow-up.
- **Environment note**: partway through this session another concurrent process/session was
  found to be committing directly to this same repository working directory (on a related
  "Urology identity linkage" sprint) and briefly left the working tree checked out on
  `main`. No work was lost — this branch's changes were uncommitted at the time and carried
  over cleanly on switching back — but this indicates the working directory is currently
  shared with at least one other active agent session; coordinate before further concurrent
  work here.

## Final Verdict

**CONDITIONAL GO** for the navigation-shell fix itself: the reported defect is fixed and
verified live for 3 of 4 roles, backed by a new regression test, with zero build/lint/
typecheck/test regressions. Full GO is withheld only pending: (1) live SUPPORT_STAFF
verification, (2) a full Playwright regression run against the Docker-composed stack, and
(3) a decision on SUPPORT_STAFF department-scoped backend filtering (currently absent by
design gap, not by this change).
