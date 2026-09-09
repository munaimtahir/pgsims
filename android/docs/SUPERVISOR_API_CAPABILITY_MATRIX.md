# Supervisor Android — API Capability Matrix

Scope: **Supervisor — LIMITED MVP** per
`docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md` — authentication, own info, assigned
residents, resident training/progress status, and per-workflow pending counts. No approve / reject /
revision actions from Android in this pass (explicitly deferred; see "Deferred" section below).

All endpoints below were exercised against the live production backend
(`https://android.pgsims.alshifalab.pk/`) on 2026-09-10 with a real seeded Urology supervisor
account and matched the shapes this document describes.

| Capability | Existing API | Method | Endpoint | Android action |
| --- | --- | --- | --- | --- |
| Current user + role | Yes | GET | `/api/auth/me/` | Role-based routing (`SUPERVISOR` → `SupervisorPane`); reused unchanged from the resident flow |
| Assigned residents (list) | Yes | GET | `/api/supervisors/me/summary/` | `SupervisorResidentsContent` — name, programme, current rotation, IMM/Final eligibility, research status |
| Own pending-approval counts (rotation/leave/research) | Yes | GET | `/api/supervisors/me/summary/` (`pending.*`) | Workflow pending counts on `SupervisorHomeContent` |
| Assigned-residents count + logbook/evaluation pending counts | Yes | GET | `/api/academics/monitoring/supervisor-dashboard/` | Workflow pending counts on `SupervisorHomeContent` |
| Resident detail (training, current posting, research, thesis, workshops, eligibility) | Yes | GET | `/api/supervisors/residents/{resident_id}/progress/` | `SupervisorResidentDetailScreen`, fetched on demand when a resident is opened |
| Approve logbook entry | Yes (web) | POST | `/api/academics/logbook-entries/{id}/verify/` | **Not wired.** Deferred — see below |
| Return/reject logbook entry | Yes (web) | POST | `/api/academics/logbook-entries/{id}/return_revision/`, `.../reject/` | **Not wired.** Deferred |
| Approve/return research submission | Yes (web) | POST | `/api/my/research/action/supervisor-approve/`, `.../supervisor-return/` | **Not wired.** Deferred |
| Approve/reject leave request | Yes (web) | POST | `/api/leaves/{id}/approve/`, `.../reject/` | **Not wired.** Deferred |
| Approve rotation (HOD level) | Yes (web) | POST | `/api/rotations/{id}/hod-approve/` | **Not wired.** Deferred (no confirmed "reject" action exists for rotations — approve-only even if built later) |
| Document review (approve/reject) | **No** — `ResidentDocument.review()` is hard-coded admin-only today | — | `/api/resident-documents/{id}/review/` | **Not available to supervisors at all**, on web or Android. Out of scope until the backend adds a supervisor path. |
| WBA / competency / portfolio assessment | **Not implemented anywhere in the backend** | — | — | Not built — there is nothing to surface |

## Why read-only for this pass

`docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md` scopes Supervisor Android as "LIMITED
MVP" and explicitly defers "advanced supervisor actions" (approve/reject/revision) to a later
milestone (M7). This build stays inside that scope: it shows the same residents, statuses, and
pending counts a supervisor would see on the web review queues, but every mutation
(approve/reject/revision) still happens on PGR SIMS web. The in-app copy on the Supervisor Home
screen says this explicitly.

## Architecture notes

- No backend changes were needed for this MVP — every endpoint above already existed and already
  scopes its response to the calling supervisor's own active `ResidentSupervisorAssignment` rows.
- Android changes stayed inside the existing `app-portal` module's flat-Composable, no-ViewModel,
  no-Hilt, no-Navigation-Compose style (see `InstitutionalRepository.kt`, `InstitutionalScreen.kt`):
  - `InstitutionalApi` gained three new `suspend` endpoints (`supervisorSummary`,
    `supervisorDashboard`, `supervisorResidentProgress`).
  - `InstitutionalRepository.snapshot()` branches on `me.role == "SUPERVISOR"` and fetches only the
    two supervisor-facing sections instead of the resident-only ones.
  - `SupervisorScreens.kt` (new file) holds `SupervisorPane` and its three tabs (Home, Residents,
    Profile), plus an in-file resident-detail drill-down using local `rememberSaveable` state — no
    new navigation library was introduced, consistent with the rest of the module.
  - `InstitutionalScreen.kt`'s `InstitutionalWorkspace` routes to `SupervisorPane` instead of
    `ConnectedPane` when the signed-in account's role is `SUPERVISOR`; the resident flow is
    untouched.

## Deferred (fast-follow scope, not built here)

Approve/reject/revision actions for Logbook, Research/Synopsis, Leave, and Rotation, plus a backend
extension to let a resident's assigned supervisor (not just admins) review documents. These were
explicitly scoped out for this pass per user decision; the endpoints they'd use are already
identified in the table above.
