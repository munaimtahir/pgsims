# Supervisor Android — API Capability Matrix

Scope: **Supervisor — action-capable**, fulfilling the "advanced supervisor actions" milestone
(M7) that `docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md` originally deferred out of
the LIMITED MVP. Supervisors can view and act on (approve / reject / return for revision) pending
Logbook, Leave, Rotation and Research items directly from Android, in addition to the original
MVP's authentication, own info, assigned residents, and resident training/progress status.

All read endpoints below were exercised against the live production backend
(`https://android.pgsims.alshifalab.pk/`) on 2026-09-10 with a real seeded Urology supervisor
account and matched the shapes this document describes. The action endpoints below were already
verified against `docs/contracts/API_CONTRACT.md` and production `views.py` source at the time they
were wired; re-verify against a seeded staging account before shipping.

| Capability | Existing API | Method | Endpoint | Android action |
| --- | --- | --- | --- | --- |
| Current user + role | Yes | GET | `/api/auth/me/` | Role-based routing (`SUPERVISOR` → `SupervisorPane`); reused unchanged from the resident flow |
| Assigned residents (list) | Yes | GET | `/api/supervisors/me/summary/` | `SupervisorResidentsContent` — name, programme, current rotation, IMM/Final eligibility, research status |
| Own pending-approval counts (rotation/leave/research) | Yes | GET | `/api/supervisors/me/summary/` (`pending.*`) | Workflow pending counts on `SupervisorHomeContent` |
| Assigned-residents count + logbook/evaluation pending counts | Yes | GET | `/api/academics/monitoring/supervisor-dashboard/` | Workflow pending counts on `SupervisorHomeContent` |
| Resident detail (training, current posting, research, thesis, workshops, eligibility) | Yes | GET | `/api/supervisors/residents/{resident_id}/progress/` | `SupervisorResidentDetailScreen`, fetched on demand when a resident is opened |
| Logbook pending queue | Yes | GET | `/api/academics/logbook-entries/` (shared with the resident flow, already supervisor-scoped; client filters to `status == "SUBMITTED"`) | `SupervisorWorkflowQueueScreen(LOGBOOK)`. **Not** `/api/academics/review-queue/` — that endpoint's item `id` is a queue-row id, not the logbook entry id the action endpoints need, and it mixes in unrelated `EVALUATION_REVIEW` rows; caught during live verification against `supervisor`/production on 2026-09-10 (queue row 44 referenced entry 28 only in free-text `notes`). |
| Approve logbook entry | Yes | POST | `/api/academics/logbook-entries/{id}/verify/` | **Wired.** `SupervisorWorkflowQueueScreen` → Approve |
| Return/reject logbook entry | Yes | POST | `/api/academics/logbook-entries/{id}/return_revision/`, `.../reject/` (payload: `supervisor_comments`; required for return) | **Wired.** → Return for revision / Reject |
| Leave pending queue | Yes | GET | `/api/utrmc/approvals/leaves/` (auto-scopes to the caller's own supervised residents for a supervisor account, despite the `utrmc` path segment) | `SupervisorWorkflowQueueScreen(LEAVE)` |
| Approve/reject leave request | Yes | POST | `/api/leaves/{id}/approve/`, `.../reject/` (payload: `reason`) | **Wired.** → Approve / Reject |
| Rotation pending queue | Yes | GET | `/api/supervisor/rotations/pending/` | `SupervisorWorkflowQueueScreen(ROTATION)` |
| Approve/reject/return rotation | Yes | POST | `/api/rotations/{id}/hod-approve/`, `.../reject/`, `.../returned/` (payload: `reason`) | **Wired.** → Approve / Reject / Return for revision. Correcting a prior note in this doc: rotation reject and return DO exist (`docs/contracts/API_CONTRACT.md`), it was not approve-only. |
| Research pending queue | Yes | GET | `/api/supervisor/research-approvals/` | `SupervisorWorkflowQueueScreen(RESEARCH)` |
| Approve/return research submission | Yes | POST | `/api/my/research/action/supervisor-approve/`, `.../supervisor-return/` (payload: `project_id`, `feedback`) | **Wired.** → Approve / Return for revision |
| Document review (approve/reject) | **No** — `ResidentDocument.review()` is hard-coded admin-only today | — | `/api/resident-documents/{id}/review/` | **Not available to supervisors at all**, on web or Android. Out of scope until the backend adds a supervisor path. |
| WBA / competency / portfolio assessment | **Not implemented anywhere in the backend** | — | — | Not built — there is nothing to surface |

## Architecture notes

- No backend changes were needed for this build — every endpoint above already existed and already
  scopes its response to the calling supervisor's own active `ResidentSupervisorAssignment` rows.
- Android changes stayed inside the existing `app-companion` module's flat-Composable, no-ViewModel,
  no-Hilt, no-Navigation-Compose style (see `InstitutionalRepository.kt`, `InstitutionalScreen.kt`,
  `SupervisorScreens.kt`, `SupervisorWorkflowScreens.kt`):
  - `InstitutionalApi` gained four queue GETs and eight action POSTs, all following the existing
    `submitLogbook`/`supervisorResidentProgress` templates.
  - The four workflow queues are fetched **on-demand** only when a supervisor opens that workflow —
    they are not part of `InstitutionalSnapshot`/`snapshot()`, to avoid inflating the cold-start
    fetch fan-out for a feature most sessions won't touch every load.
  - `SupervisorWorkflowScreens.kt` (new file) holds `SupervisorWorkflowQueueScreen`, its item detail
    `AlertDialog`, and a reusable `ReasonConfirmDialog` for reject/return actions, mirroring the
    dialog patterns already in `ResidentWorkflowScreens.kt`.
  - `SupervisorScreens.kt`'s `SupervisorPane` gained a `selectedWorkflow` local-state slot alongside
    the existing `selectedResidentId` drill-down, same mutual-exclusivity pattern, no new navigation
    library introduced. The Home screen's workflow rows are now tappable and route into the queue
    screen; the former "not yet available on Android" disclaimer was removed.
  - After a successful action, the queue screen removes the item locally and calls the existing
    `onRefresh` (`InstitutionalWorkspace`'s `reloadKey`) so Home's pending counts resync from the
    server.

## Deferred (still out of scope)

Document review (`/api/resident-documents/{id}/review/`) remains admin-only in the backend — adding
a supervisor path there is a backend change, not something this Android build can do on its own.
