# Web Feature Matrix — frontend/ (Next.js 14 App Router)

Scope: web frontend only. Method: reconciled `docs/PORTAL_CURRENT_STATE.md`,
`docs/PORTAL_WEB_PARITY_MATRIX.md`, `docs/CANONICAL_FRONTEND_ROUTE_AUDIT.md`,
`docs/CANONICAL_FRONTEND_ROLE_MATRIX.md`, `docs/CANONICAL_ROUTE_MAP.md`,
`docs/FRONTEND_DELETE_CANDIDATES.md`, `docs/CANONICAL_SOURCE_OF_TRUTH.md` against current
`frontend/app/` source (`find frontend/app -maxdepth 2 -type d`, per-route file reads,
`frontend/lib/navRegistry.ts`, `frontend/lib/api/*`) on 2026-09-09.

## Headline doc/code contradiction

`docs/CANONICAL_ROUTE_MAP.md` and `docs/CANONICAL_FRONTEND_ROLE_MATRIX.md` are **stale**: they omit
an entire tier of built routes that exist in `frontend/app/academics/` today — `logbook`,
`logbook/new`, `logbook/[id]`, `logbook/[id]/review`, `evaluations`, `evaluations/new`,
`evaluations/[id]`, `evaluations/[id]/review`, `leave-requests`, `leave-requests/new`,
`leave-requests/[id]`, `rotation-assignments`, `rotation-assignments/new`,
`rotation-assignments/[id]`, `my-progress`, `monitoring`, `supervisor-workload`,
`reports/{data-quality,evaluations,logbook,resident-progress,resident-progress/[id],
supervisor-workload,supervisor-workload/[id]}`, `workflow-overview`, `workflow-data-quality`, plus
`admin/pending-supervisor-links` and `residents/document-requirements`. `CLAUDE.md` itself
correctly notes rotation-assignments/leave-requests frontends landed "as of 2026-07-25" — the
canonical-route docs were never updated after that brick. Trust the code
(`frontend/app/academics/*`, confirmed present in the `npm run build` route table) over
`CANONICAL_ROUTE_MAP.md`/`CANONICAL_FRONTEND_ROLE_MATRIX.md` for these routes.

**Bigger and more load-bearing**: of that missing tier, `logbook*`, `evaluations*`, `my-progress`,
`monitoring`, `supervisor-workload`, `reports/*`, `workflow-overview`, `workflow-data-quality` are
**absent from `frontend/lib/navRegistry.ts`** (full file read, 129 lines) for every role
(ADMIN/RESIDENT/SUPERVISOR/SUPPORT_STAFF), and are not linked from `app/dashboard/{resident,
supervisor,utrmc}/page.tsx` either (`grep -n "academics/logbook\|academics/evaluations\|...` over
`app/dashboard` and `components/layout` returned zero hits). Only `rotation-assignments` and
`leave-requests` made it into nav (`navRegistry.ts:62-63,80-81,94-95`). **Logbook and Evaluations —
fully built CRUD+review workflows — are currently unreachable by any in-app navigation; a user can
only reach them by typing the URL.** See `12_BUG_TECH_DEBT_REGISTER.md` WEB-1.

## Route inventory by canonical family (frontend/app/)

| Family | Status | Evidence |
|---|---|---|
| `/users`, `/users/new` | COMPLETE | Canonical per `CANONICAL_FRONTEND_ROUTE_AUDIT.md`; in nav (`navRegistry.ts:33`) |
| `/residents`, `/residents/[id]`, `/residents/document-requirements` | COMPLETE | In nav (`navRegistry.ts:34-35`) |
| `/supervisors`, `/supervisors/[id]` | COMPLETE | In nav (`navRegistry.ts:37`) |
| `/support-staff`, `/support-staff/[id]` | COMPLETE | In nav (`navRegistry.ts:38`) |
| `/admins`, `/admins/[id]` | COMPLETE | In nav (`navRegistry.ts:39`) |
| `/admin/pending-supervisor-links` | WORKING BUT NOT IN CANONICAL DOCS | 21-line page; in nav (`navRegistry.ts:36`); undocumented in `CANONICAL_ROUTE_MAP.md` |
| `/masters` | COMPLETE | In nav (`navRegistry.ts:40`) |
| `/supervision/*` (overview, assignments, assignments/new, assignments/[id], import, data-quality) | COMPLETE | All 5 subroutes in nav (`navRegistry.ts:47-51`) |
| `/academics` (overview, training-records, periods, rotation-templates, evaluation-templates, logbook-categories, review-queue, data-quality) | COMPLETE | In nav (`navRegistry.ts:58-67`) |
| `/academics/rotation-assignments*`, `/academics/leave-requests*` | WORKING BUT NEEDS HARDENING | Full CRUD present (102/98-line list pages + new/[id]); in nav for ADMIN/SUPERVISOR/RESIDENT; uses `WorkflowStatusBadge` (correct terminology mapping, `components/ui/WorkflowStatusBadge.tsx`) |
| `/academics/logbook*` | UI EXISTS, NAV MISSING (functionally PARTIAL) | 4 pages, full draft/submit/review flow (`academics.ts` `listLogbookEntries`/`submit`/`verify`/`return_revision`/`reject`); **not in `navRegistry.ts`, not linked from any dashboard** |
| `/academics/evaluations*` | UI EXISTS, NAV MISSING (functionally PARTIAL) | Same pattern as logbook: list/new/[id]/[id]/review, zero nav entry |
| `/academics/my-progress`, `/academics/monitoring`, `/academics/supervisor-workload` | UI EXISTS, NAV MISSING | Pages exist, zero nav entry, zero dashboard link |
| `/academics/reports/*` (data-quality, evaluations, logbook, resident-progress(+[id]), supervisor-workload(+[id])) | UI EXISTS, NAV MISSING | 7 report pages built, zero nav entry |
| `/academics/workflow-overview`, `/academics/workflow-data-quality` | UI EXISTS, NAV MISSING | Zero nav entry |
| `/dashboard/utrmc`, `/dashboard/resident`, `/dashboard/supervisor` | COMPLETE | Canonical shells, all in nav, all Jest-tested (`page.test.tsx` for each, passing) |
| `/complete-profile`, `/change-password` | COMPLETE | Canonical shared flows, Jest-tested |
| `/dashboard/change-password`, `/dashboard/pg*`, `/dashboard/resident/(progress\|schedule\|research\|thesis\|workshops\|postings)`, `/dashboard/supervisor/(research-approvals\|residents/[id]/progress)`, `/dashboard/utrmc/(users\|supervisors\|hospitals\|departments\|matrix\|programs\|backup\*\|eligibility-monitoring\|postings\|onboarding\|academics\|data-quality\|supervision)`, `/dashboard/utrmc/departments/[id]/roster` | LEGACY (redirect-only) | Confirmed 6-line `redirect()`-only stub bodies, e.g. `app/dashboard/resident/research/page.tsx` (verified by direct read); matches `CANONICAL_FRONTEND_ROUTE_AUDIT.md` |
| `/dashboard/utrmc/backup` | COMPLETE (exception to the redirect-only pattern) | 19.2 kB page in build output — this one legacy-looking path is NOT a stub; it's the live Backup Center, not in `navRegistry.ts` subItems but IS a top-level nav item (`navRegistry.ts:42`) |
| `/login`, `/forgot-password`, `/reset-password/[uid]/[token]` | COMPLETE | Jest-tested (`login/page.test.tsx`, `forgot-password/page.test.tsx`, `reset-password/[uid]/[token]/page.test.tsx`), all passing |
| `/register` | ORPHAN / PLACEHOLDER-BY-POLICY | 265-line self-registration page, zero inbound links anywhere in `app/` (`grep -rn "href=\"/register\""` → no hits outside `app/register` itself); calls `authApi.register()` → `POST /api/auth/register/` (`lib/api/auth.ts:142-143`) → `backend/sims/users/api_views.py:94` `register_view`, gated by `ENABLE_PUBLIC_REGISTRATION` env flag, **default `False`** (`backend/sims_project/settings.py:755-756`). Contradicts the "`/users/new` is the universal identity creation center" model in `CLAUDE.md`/`AGENTS.md`; backend gate mitigates security risk but the page is dead code in the default deployment. See `12_BUG_TECH_DEBT_REGISTER.md` WEB-2. |
| `/profile` | WORKING | 113 kB page, linked only from Resident nav (`navRegistry.ts:96`); note Supervisor/Support Staff "My Profile" nav items point at `/complete-profile` instead (`navRegistry.ts:82,104`) — inconsistent target for the same nav label across roles, not necessarily a bug (different roles, different flows) but worth flagging as inconsistent naming |
| `/unauthorized` | COMPLETE | Standard RBAC fallback page |

## WEB_FEATURE_MATRIX

| Domain | Backend Ready | Web UI | End-to-End Workflow | Tests | Production Verified | Defects |
|---|---|---|---|---|---|---|
| Authentication | Yes (`sims/users`, JWT) | Yes — `/login`, `/forgot-password`, `/reset-password/[uid]/[token]` | Plausible: forms post to `lib/api/auth.ts`, error handling present, rate-throttled login view (`CustomTokenObtainPairView`, `LoginRateThrottle`) | `login/page.test.tsx`, `forgot-password/page.test.tsx`, `reset-password/.../page.test.tsx`, `lib/api/auth.test.ts`, `store/authStore.test.ts` — all pass (`npm test` run 2026-09-09: 38 suites/114 tests passed) | Yes per `PORTAL_WEB_PARITY_MATRIX.md` ("Live staging verified") | `/register` page orphaned and gated off by default (WEB-2) |
| Onboarding | Yes | Yes — `/complete-profile` | Plausible: dynamic field rendering per `CLAUDE.md`'s "not hardcoded" rule; tested | `app/complete-profile/page.test.tsx` passes | Yes per parity matrix ("Live staging GET/PATCH verified") | Uses raw "Submitted" string literal directly in page (`grep -l "Submitted" app/complete-profile/page.tsx`) — consistent with terminology lock, not a defect |
| Profile | Yes | Yes — `/profile`, `/complete-profile` | Plausible | Covered indirectly via complete-profile test | Yes (parity matrix) | Two different profile routes reachable via nav depending on role (`/profile` for RESIDENT, `/complete-profile` for others) under the same "My Profile" label — inconsistent, not verified broken |
| Training | Yes (`sims.training`, `sims.academics` — two independent `ResidentTrainingRecord` models per `CLAUDE.md`) | Yes — `/academics/training-records*` (admin CRUD), `/dashboard/resident` summary card | Plausible for admin CRUD (in nav, tested: `training-records/page.test.tsx`); resident-facing summary is read-only inside dashboard | `academics/training-records/page.test.tsx` passes | Not documented for web specifically (parity matrix covers Android/Portal only) | The dual-model split noted in `CLAUDE.md`/`AUDIT_2026-07-23_PILOT_READINESS.md §12` is a backend concern, not reproduced here — flagged for awareness only |
| Rotations | Yes (`training.RotationAssignment`) | Yes — `/academics/rotation-assignments*` | Plausible: full draft→submit→approve lifecycle UI, in nav for ADMIN/SUPERVISOR/RESIDENT, uses `WorkflowStatusBadge` | No dedicated Jest test file found for `rotation-assignments` pages (only `lib/api/rotations.test.ts` for the API layer) | `PORTAL_WEB_PARITY_MATRIX.md` marks web Rotations "Yes" but doesn't specify staging verification depth (Portal/Android side explicitly "Deferred") | Page-level (UI) tests missing for this workflow — gap, not a break |
| Supervision | Yes (`ResidentSupervisorAssignment`) | Yes — `/supervision/*` | Plausible: assignment CRUD, import, data-quality all present and in nav | No dedicated page-level test files found under `app/supervision/` (checked directory listing) | Parity matrix: "Live staging active assignment verified" | Same as Rotations — no Jest coverage at page level |
| Documents | Yes | Yes — `/dashboard/resident/documents`, `/residents/document-requirements` | Plausible | Not enumerated in Jest suite list | Parity matrix: "Live staging list, review feedback, upload and resubmission verified" (covers Portal path; web path not separately confirmed) | None found, but web-specific document workflow lacks its own documented verification distinct from Portal's |
| Logbook | Yes (`sims.academics.LogbookEntry`, confirmed authoritative per `SPRINT_STATE.md`: "the active web logbook uses `academics.LogbookEntry`") | Yes — `/academics/logbook*`, full draft/submit/verify/return/reject flow (`lib/api/academics.ts` actions match `07_CONTRACT_DRIFT_REPORT.md` CD-1's confirmed real API shape) | **Broken by omission**: UI and API are functionally complete, but the route is unreachable from any nav or dashboard link — a real user cannot discover it without a bookmarked/typed URL | No page-level Jest test found for `academics/logbook/*` (searched, none present) | Not documented as web-verified anywhere (Portal parity marks Logbook "Deferred" for Portal, doesn't speak to web) | **WEB-1 (P1): unreachable via navigation** — see bug register |
| Assessments (Evaluations) | Yes (`EvaluationFormTemplate`) | Yes — `/academics/evaluations*`, `/academics/evaluation-templates` | Templates reachable (in nav); the resident/supervisor-facing `evaluations*` instance pages are **not** in nav | No page-level Jest test found for `academics/evaluations/*` | Not documented | Same unreachability defect as Logbook (WEB-1) |
| Research / thesis / workshops | Backend status not verified in this pass (out of scope — backend agent's lane) | **Deferred/legacy only** — `/dashboard/resident/{research,thesis,workshops}` are 6-line `redirect()`-only stubs to `/dashboard/resident`; `/dashboard/supervisor/research-approvals` likewise | Not implemented in web; matches `PORTAL_WEB_PARITY_MATRIX.md` ("Deferred") for the Portal side and `CANONICAL_FRONTEND_ROUTE_AUDIT.md`'s REDIRECT classification for web | N/A | Not verified | None — correctly retired, per `AGENTS.md`/route-audit intent |
| Leave Requests | Yes (`training.LeaveRequest`) | Yes — `/academics/leave-requests*` | Plausible, same shape as Rotations, in nav | No dedicated page-level Jest test found | Not documented specifically for web | No page-level test coverage |

## Terminology contract check (`docs/contracts/TERMINOLOGY.md`)

- `lib/ui/status.ts` implements the lock correctly for the generic 4-state model
  (`pending`→"Submitted", `returned`→"Returned", `rejected`→"Rejected", `approved`→"Approved") and is
  used together with `WorkflowStatusBadge` by Rotations/Leave Requests pages
  (`app/academics/rotation-assignments/page.tsx:71`, `app/academics/leave-requests/page.tsx:67`).
- **Logbook does not use either helper.** `app/academics/logbook/page.tsx:79-93` inline-renders the
  raw backend enum string (`entry.status`, one of `DRAFT/SUBMITTED/VERIFIED/RETURNED/REJECTED/
  CANCELLED` per `backend/sims/academics/models.py:598-608`) directly as the visible label. Backend
  `VERIFIED` is shown verbatim as "VERIFIED" instead of the locked term **"Approved"**
  (`docs/contracts/TERMINOLOGY.md`: "Approved: supervisor verifies entry"). This is consistent with
  `07_CONTRACT_DRIFT_REPORT.md` CD-4's finding that the terminology doc's `supervisor_feedback`→
  `feedback` alias doesn't match the real `supervisor_comments` field either — the Logbook feature
  was built against its own vocabulary (`SUBMITTED`/`VERIFIED`) that was never reconciled with the
  generic terminology lock file. Not a functional break, but a real terminology-contract violation.
  See `12_BUG_TECH_DEBT_REGISTER.md` WEB-3.
- `WorkflowStatusBadge` (`components/ui/WorkflowStatusBadge.tsx`) independently hardcodes its own
  `STATUS_COLORS` map keyed on raw uppercase backend values (`SUBMITTED`, `APPROVED`, etc.) rather
  than delegating to `lib/ui/status.ts`'s `getStatusLabel`/`getStatusBadgeClass` — two parallel,
  not-quite-consistent status-label systems exist in the same codebase (`lib/ui/status.ts` lowercase
  keys vs `WorkflowStatusBadge.tsx` uppercase keys). No observed mislabeling in Rotations/Leave
  Requests today, but the duplication is a latent-defect risk if the two ever diverge in behavior.
