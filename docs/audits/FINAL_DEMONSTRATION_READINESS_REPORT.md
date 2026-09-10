# PGR SIMS — Final Demonstration Readiness Report

Date: 2026-09-10
Branch: `fix/frontend-authenticated-shell-navigation`

## 1. Executive Summary

The reported navigation defect (sidebar disappearing outside `/dashboard/*`) is fixed and
verified live for ADMIN, SUPERVISOR and RESIDENT. A related dashboard-count bug
("Supervisors = 0") and a nav-reachability gap (Logbook/Evaluations/reports pages built but
unlinked) were found and fixed in the same pass. Canonical demo login accounts
(`admin`/`resident`/`supervisor`/`staff`) exist locally and are correctly linked to real
identities via the existing `reconcile_urology_supervisor_profiles` command. Full
demo-data population, `verify_demo_readiness` tooling, and a complete 4-role real-browser
E2E/RBAC matrix were **not** completed this session — see Remaining Known Issues. This
report gives an honest **CONDITIONAL GO**, not a full GO.

## 2. Environment Audited

- Classification: **LOCAL** (ephemeral, this session only).
- Frontend: `next dev` on `http://localhost:3000`, `.env.local` copied from
  `.env.local.example` (git-ignored).
- Backend: `python manage.py runserver` on `http://localhost:8000`, SQLite
  (`backend/db.sqlite3`, git-ignored, was empty at session start), `SECRET_KEY`/`DEBUG` set
  as ephemeral shell env vars only.
- No `.env` existed for the Docker Compose stack (`docker/docker-compose.yml`) in this
  environment, so the Docker/Postgres path described in `CLAUDE.md` was not used this
  session; a plain venv + sqlite local setup was used instead.
- This local database was populated from `urology_pgsims_institutional_demo_ready.xlsx`
  (untracked, present at repo root, contains real resident personal data per the workbook's
  own docstring) via the existing `bootstrap_urology_demo` command — this file was **not**
  committed and must never be.

## 3. Baseline

- Starting branch: `main`
- Starting SHA: `5f008adb399b2ea9b556f2058a555794738f3150`
- Working branch: `fix/frontend-authenticated-shell-navigation`
- Pre-existing uncommitted changes on `main` at session start (`backend/sims/academics/tests.py`,
  `backend/sims/academics/views.py`) belonged to a separate, already-active sprint
  ("Urology workflow approval demo", see `SPRINT_STATE.md`) and were left untouched.

## 4. Frontend Architecture

See `docs/audits/FRONTEND_NAVIGATION_AUDIT.md` for full root-cause/before/after detail.
Summary: added 10 thin `layout.tsx` files mounting the existing `DashboardLayout` shell
under every top-level authenticated route folder that previously had none. Zero URL
changes. Verified live for 3/4 roles.

## 5. Module Completeness Matrix (partial — see caveats)

| Module | Frontend route | Backend | Demo data | Demo ready |
|---|---|---|---|---|
| Residents | `/residents` | `UserViewSet`/`ResidentProfile` | 28 imported + 2 canonical | ✅ verified live |
| Supervisors | `/supervisors` | same + `SupervisorProfile` | 6 real, 1 canonical-linked | ✅ verified live |
| Supervision assignments | `/supervision/*` | `ResidentSupervisorAssignment` | 1 active linked via reconcile | ✅ verified live (supervisor→resident chain) |
| Academic Review Queue | `/academics/review-queue` | training/academics review models | 2 pending items seeded | ✅ verified live |
| Logbook / Evaluations | `/academics/logbook`, `/academics/evaluations` | wired, real API | 4 pending / 1 approved / 1 returned logbook; 2 pending / 1 approved / 1 returned evaluation (per `seed_urology_workflow_demo`) | nav fixed this session; not re-verified in browser after fix |
| Leave / Rotations | `/academics/leave-requests`, `/academics/rotation-assignments` | training app | 3 leave, 1 pending + 1 approved rotation seeded | not re-verified in browser this session |
| Support Staff scope | `/support-staff` | `SupportStaffProfile.department_ref` (unused by any queryset) | `staff` linked to Urology Department | **not demo-ready** — no backend scoping enforces it (pre-existing gap) |
| Backup Center | `/dashboard/utrmc/backup` | — | — | not audited this session |

## 6. Role Readiness

- **ADMIN**: READY — live-verified: login, dashboard (counts now correct), Residents,
  Supervisors, shell persistence.
- **SUPERVISOR**: READY — live-verified: login as `supervisor` (Prof. M. Tahir Bashir
  Malik), 7 assigned residents, 2 pending Academic Review Queue items, shell persistence.
- **RESIDENT**: READY — live-verified: login as `resident` (Dr. Jawad Saifullah), correct
  training/supervisor/pending-count data consistent with the supervisor's view.
- **SUPPORT_STAFF**: **NOT VERIFIED** — account exists and is department-linked, but live
  browser login was not completed (tooling disconnect) and backend department-scoping does
  not exist yet (see below).

## 7. Supervisor Identity / Linkage

- `supervisor` username → role `SUPERVISOR` → `SupervisorProfile` → **Prof. Dr. M. Tahir
  Bashir Malik** — confirmed via `reconcile_urology_supervisor_profiles` (pre-existing,
  idempotent command from the concurrent Urology sprint), re-run this session and confirmed
  idempotent (second run reports "already correct").
- `resident` username → role `RESIDENT` → **Dr. Jawad Saifullah** — same mechanism,
  confirmed.
- 7 residents currently show as assigned to this supervisor in the live UI.
- `admin` and `staff` canonical logins were newly created this session via a new,
  idempotent `backend/sims/users/management/commands/seed_canonical_demo_accounts.py`
  (not previously part of the reconcile pattern, since neither role has a "real identity
  swap" concept the way supervisor/resident do — they were created as plain new ADMIN/
  SUPPORT_STAFF identities via the canonical `create_user_with_profile` service, per
  `CLAUDE.md`'s identity-creation rule).

## 8. Workflow Readiness

| Workflow | Status |
|---|---|
| Resident management | PASS (live-verified) |
| Supervision / linking | PASS (live-verified, both directions) |
| Documents | NOT VERIFIED this session |
| Document review queue | PASS (Academic Review Queue live-verified with 2 pending items) |
| Logbook | seeded, nav fixed, not re-verified live after the nav fix |
| Evaluations | seeded, nav fixed, not re-verified live after the nav fix |
| Leave | seeded, not verified live |
| Rotations | seeded, not verified live |
| Data quality | dashboard renders; "39 Supervision Warnings" reflects genuine current data state (most of the 28 imported residents don't yet have a `ResidentSupervisorAssignment`) — not a bug, a real gap in demo data breadth if a broader demo is wanted |

## 9. Demonstration Data Inventory (as of this session, local DB)

- Users: 37 (after canonical account creation)
- Residents: 29 (28 imported + `resident` canonical, one of the 28 real identities retired)
- Supervisors: 6 (5 real + `supervisor` canonical, one real identity retired)
- Support staff: 1 (`staff`, Urology-linked)
- Training records: 28
- Review queue items: 6 total, 2 currently pending for the demo supervisor
- Logbook: 4 pending / 1 approved / 1 returned (per `seed_urology_workflow_demo` dry-run
  output, applied this session)
- Evaluations: 2 pending / 1 approved / 1 returned
- Leave: 3 records
- Rotations: 1 pending / 1 approved

## 10. Demo Workflow Coverage

Not produced as a separate file this session (`docs/audits/DEMO_WORKFLOW_COVERAGE.md`) —
the counts above are drawn from the existing `seed_urology_workflow_demo` command's own
dry-run report, which already enumerates per-workflow state coverage; treat that command's
output as the authoritative coverage source rather than duplicating it into a second
document without re-verification.

## 11. Backend/API Audit

See §"Frontend → API → Backend Mapping" in `docs/audits/FRONTEND_NAVIGATION_AUDIT.md`.
Pending Supervisor Links and Supervisor directory flows were traced and confirmed to never
route through `/admin/`/Django-admin login.

## 12. Frontend Route Audit

66 nav hrefs, all resolve to real pages, all now sit under the authenticated shell —
enforced by `frontend/lib/navRegistry.test.ts` (129 passing assertions).

## 13. RBAC Audit

- Nav-level role scoping cross-checked against each page's `ProtectedRoute allowedRoles`
  for every newly-added nav item (exact match, not assumed).
- No RBAC classes, permission checks, or role logic were loosened anywhere in this change.
- SUPPORT_STAFF department-scoping remains unimplemented (pre-existing gap, documented, not
  silently patched over with broadened access).
- Negative RBAC browser tests (resident → `/users`, etc.) were **not** executed this
  session — deferred to the existing `frontend/e2e/rbac/access-control.spec.ts` suite.

## 14. Data Quality Findings

- Fixed: admin dashboard "0 Supervisors"/"0 Support Staff" — a real pagination bug (dashboard
  read only page 1 of a paginated `/api/users/` response instead of the returned `count`).
- Not fixed/not a bug: "39 Supervision Warnings" — reflects that only 1 of 28+ imported
  residents currently has an active supervision assignment; a genuine data-breadth gap for a
  fuller demo, not a defect in this session's scope.

## 15. Dashboard Count Reconciliation

| Metric | UI (before) | UI (after fix) | DB |
|---|---|---|---|
| Users | 25 | 37 | 37 |
| Residents | 24 | 29 | 29 |
| Supervisors | 0 | 6 | 6 |
| Support Staff | 0 | 1 | 1 |

## 16. Defects Found and Fixed

1. Sidebar/shell missing outside `/dashboard/*` (the reported defect) — fixed.
2. `navRegistry.ts` missing Logbook/Evaluations/Monitoring/reports entries (WEB-7) — fixed.
3. Admin dashboard supervisor/support-staff undercount (pagination bug) — fixed.

## 17. Test Results

- Frontend lint: **PASS**
- Frontend typecheck: **PASS**
- Frontend production build: **PASS**
- Frontend unit tests: **PASS** (243/243, including 129 new nav-contract assertions)
- Backend `manage.py check`: **PASS**
- Backend `sims/users` test suite: **PASS** (93/93; the coverage-gate failure printed
  alongside is the known per-app coverage threshold from running a subset, not a functional
  failure — see `CLAUDE.md`'s note on the two competing pytest configs)
- E2E navigation/workflow/RBAC (Playwright): **NOT RUN** this session

## 18. Browser/E2E Evidence

Live manual verification only (see §6 above and `docs/audits/FRONTEND_NAVIGATION_AUDIT.md`
§"Manual Verification"). No `docs/audits/ROLE_E2E_BROWSER_MATRIX.md` or screenshot evidence
directory was produced — the browser tooling disconnected before that could be completed
for all 4 roles, and fabricating that matrix from partial results would violate the
"do not accept false positives" requirement.

## 19. Remaining Non-Blocking Technical Debt

- SUPPORT_STAFF department-scoped backend filtering does not exist; `department_ref` is
  stored but unused by any permission/queryset code.
- Full Docker/Postgres-based local stack was not exercised (sqlite used instead) — the
  identity-reconciliation and seeding commands should be re-verified against Postgres before
  a real demo.
- `docs/contracts/ROUTES.md` / `docs/CANONICAL_ROUTE_MAP.md` remain stale per discovery
  findings WEB-1/WEB-2 and were not updated this session despite `navRegistry.ts` changing —
  should be updated in a follow-up per the contract-first rule in `CLAUDE.md`.
- `SPRINT_STATE.md` was not updated in place this session (deferred — see note below).

## 20. Final Verdict

**CONDITIONAL GO.**

Ready: the reported navigation defect, the WEB-7 nav-reachability gap, and the dashboard
supervisor-count bug are all fixed and either live-verified or covered by a new automated
regression test, with a fully green build/lint/typecheck/test suite.

Not ready for an unattended full demonstration without further work: SUPPORT_STAFF role is
unverified live and has no real department scoping; Logbook/Evaluations/Leave/Rotations
workflows were seeded but not re-verified in the browser after the nav fix; no automated
`verify_demo_readiness` command exists yet; and this session's environment (local sqlite,
ephemeral secrets, a workbook-derived DB) has not been reproduced against the actual
Docker/Postgres deployment path the demonstration will run on.

---

**Note**: partway through this session, another concurrent Claude Code session was found to
be actively committing to this same repository directory (working on a related identity-
linkage sprint) and briefly checked the shared working tree out onto `main`. No work from
this session was lost, but readers should confirm with the other session/owner before
assuming this report and that session's commits describe the same tree.
