# Frontend-Backend Truth Map — PGMS Clean-Room Foundation

**Last independently verified**: 2026-08-02, a fresh from-scratch bidirectional audit (this
document supersedes the 2026-07-23 version in full — every claim below was re-checked against
current code, not carried over). Method: enumerated every `urlpatterns`/router registration in
`backend/sims/{users,academics,rotations,training,supervision,bulk,notifications,backup_center,audit}`
(the apps actually in `INSTALLED_APPS` — `sims/_legacy/` excluded), then for each one grepped for
the **literal URL path or api-client function name actually invoked** from a page/component under
`frontend/app/`, not merely defined in `frontend/lib/api/*.ts` — the api-client-file-exists check is
exactly the false-positive class that hid the 2026-07-23 bulk-import bug, so it was deliberately not
trusted here. Frontend→backend direction: every page under `frontend/app/` that performs an action
was checked against a real, non-stub backend route.

Status legend: **WORKING** (real frontend↔backend pair, actually invoked, verified) · **GAP** (real
backend capability, no frontend caller anywhere — a genuine hole) · **GAP-LOW** (real backend
capability with no frontend caller, but low severity — either functionally superseded by another
path the UI does use, or a narrow parameterized helper) · **BACKEND-ONLY** (deliberately no UI
needed) · **LEGACY** (dead/superseded code, confirmed unreachable, kept only for git history or
model reuse elsewhere).

---

## 1. Universal Identity & Profile Sync — WORKING

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/login` | `POST /api/auth/login/` | WORKING |
| `/change-password` | `POST /api/auth/change-password/` | WORKING |
| `/complete-profile` | `GET /api/auth/complete-profile/`, `GET /api/auth/me/` | WORKING |
| `/users/new` | `POST /api/users/` → `create_user_with_profile` | WORKING |
| `/register`, `/forgot-password`, `/reset-password/[uid]/[token]` | `/api/auth/register/`, `/api/auth/password-reset/`, `/api/auth/password-reset/confirm/` | WORKING |
| `/users`, `/residents`, `/supervisors`, `/support-staff`, `/admins` (shared `RoleDirectoryPage`, with search/active-filter added 2026-07-24) | `GET /api/users/` (role-filtered, `search`/`active`/`department` query params) | WORKING |
| `ProtectedRoute` onboarding gate (calls `authApi.me()` on every protected mount except `/change-password`/`/complete-profile`, redirects on `allowed_next_route`) | `GET /api/auth/me/` | WORKING — confirmed the 2026-07-24 fix (§7.9/7.9b of the prior version) is still in place; `must_change_password` is cleared by `change_password_view` on success. |

**Confirmed resolved since 2026-07-23**: Phase A (`User.specialty` → real `Specialty` FK, via
`SafeForeignKeyDescriptor` in `backend/sims/users/models.py`), Phase B (home-affiliation
reconciliation), and Phase C (unification of the two independent `ResidentTrainingRecord` models
onto `sims.training.ResidentTrainingRecord`, with `sims.academics.ResidentTrainingRecord` dropped
entirely — `backend/sims/academics/models.py` no longer defines this class) are all verified present
in current code, not just in commit messages. The `docs/CANONICAL_SOURCE_OF_TRUTH.md` /
`CLAUDE.md` prose describing "two independent `ResidentTrainingRecord` models" is now **stale** —
trust `backend/sims/academics/models.py` (no `ResidentTrainingRecord` class) and
`backend/sims/training/models.py:111` (the sole survivor) over that prose.

## 2. Supervision Spine — WORKING

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/supervision`, `/supervision/assignments[, /new, /[id]]` | `/api/supervision/assignments/` (list/create/detail/`end`) | WORKING |
| `/supervision/import` | `POST /api/supervision/import/` | WORKING |
| `/supervision/data-quality` | `GET /api/supervision/data-quality/` | WORKING |
| n/a | `POST /api/supervision/change-primary/` | **GAP** — real, RBAC-checked (`ADMIN`-only), atomic "rotate primary supervisor" endpoint (`change_primary_supervisor`, `backend/sims/supervision/views.py:148`) with a working api-client wrapper (`supervisionApi.changePrimary` in `frontend/lib/api/supervision.ts:93`) that is never called from any page or component. No UI exposes a "change primary supervisor" action anywhere under `/supervision/*`. See §9 open decisions. |

## 3. Core Masters & Bulk Import — WORKING

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/masters` (`BulkSetupWorkspace.tsx`, 9-step workflow: hospitals, departments, matrix, training-programs, academic-sessions, faculty-supervisors, residents, supervision-links, rotation-assignments) | `POST /api/bulk/import/<entity>/<action>/`, `GET /api/bulk/templates/<resource>/`, `GET /api/bulk/exports/<resource>/`, plus `/api/bulk/flexible/{schemas,detect-headers,validate-mapping,dry-run,apply,presets}/` (custom column-mapping mode, called directly via `apiClient` from `FlexibleMappingImport.tsx`, not through `frontend/lib/api/bulk.ts`) | WORKING — confirmed all 9 steps wired, all flexible-mapping sub-endpoints have a real caller. |
| n/a | `POST /api/bulk/review/`, `/assignment/`, `/import/`, `/import-trainees/`, `/import-supervisors/`, `/import-residents/`, `/import-departments/` | **LEGACY** — the pre-unified-import view set, confirmed zero frontend references (checked `frontend/app`, `frontend/lib`, `frontend/components`, `frontend/e2e`). Fully superseded by the unified `import/<entity>/<action>/` endpoint the workspace actually uses. Per the prior version's own methodology note (class/path checks alone don't prove backend-test-safety for removal — `reverse()`-name checks are also needed), **left in place, not removed**; flagged for a human decision only if backend cleanup is ever prioritized. |
| n/a | `sims/academics`'s duplicate masters ViewSets (`InstitutionViewSet`, `HospitalViewSet`, `DepartmentViewSet`, `TrainingProgramViewSet`, `SpecialtyViewSet`, `DesignationViewSet`, `AcademicSessionViewSet`) at `api/masters/`/`academics/api/` | **RESOLVED (already executed as of 2026-07-24, reconfirmed now)** — `backend/sims/academics/urls.py` no longer exists; `sims_project/urls.py` lines 157-161 are a comment recording the removal. Academic Session CRUD lives in the bulk-import workflow instead (§3 row above); Institution/Specialty/Designation confirmed not structurally needed (free-text fields, not FKs) and were not rebuilt. |

## 4. Academic Workflow (Rotations, Evaluations, Logbook) — WORKING

`/academics`, `/academics/training-records[/[id]]`, `/academics/periods`,
`/academics/rotation-templates` (scaffold), `/academics/evaluation-templates`,
`/academics/logbook-categories`, `/academics/review-queue`, `/academics/data-quality`,
`/academics/evaluations[/new, /[id], /[id]/review]`, `/academics/logbook[/new, /[id], /[id]/review]`,
`/dashboard/resident`, `/dashboard/supervisor`, `/residents/[id]`, `/supervisors/[id]` — spot-checked
against `sims/academics/workflow_urls.py`, all map to real, called `/api/academics/*` endpoints.
`ResidentTrainingRecord`-backed views now read/write the unified `sims.training` model (§1) — no
regression found from the Phase C migration.

### 4.1 Rotation Assignments — WORKING (new since 2026-07-23)
`/academics/rotation-assignments[, /new, /[id]]` calls `rotationsApi` (`frontend/lib/api/rotations.ts`)
against `POST/GET /api/rotations/` (create/list/detail), `.../submit/`, `.../hod-approve/`
(exposed in the UI as `reviewApplication` with `action: approve|defer|reject`),
`.../utrmc-approve/`, `.../activate/`, `.../complete/`, plus `/api/hospital-departments/`,
`/api/resident-training/`, `/api/programs/` for the create form's dropdowns. Confirmed real usage by
grepping `rotationsApi.*` call sites in `frontend/app/academics/rotation-assignments/**/*.tsx`, not
just the client file. Full draft → submit → HOD-approve → UTRMC-approve → activate → complete
lifecycle is reachable from the UI for admin/supervisor/resident roles per `ProtectedRoute`.

The dedicated "mine"/"inbox" endpoints (`GET /api/my/rotations/`, `/api/utrmc/approvals/rotations/`,
`/api/supervisor/rotations/pending/`) are **not** called — the list page instead calls the generic
`GET /api/rotations/` and relies on `RotationAssignmentViewSet.get_queryset()`'s own role-based
filtering (residents see only their own, supervisors see supervised + own-department, admins see
all), which produces materially the same result set. **GAP-LOW** — real, tested backend, genuinely
unreached, but not a functional hole since the UI achieves the same outcome another way.

### 4.2 Leave Requests — WORKING (new since 2026-07-23, closes the old §7.2 gap)
`/academics/leave-requests[, /new, /[id]]` calls `leaveApi` (`frontend/lib/api/leave.ts`) against
`POST/GET /api/leaves/` (create/list/detail), `.../submit/`, `.../approve/`, `.../reject/`.
Confirmed real usage in `frontend/app/academics/leave-requests/**/*.tsx`. Same pattern as rotations:
the list page uses the generic RBAC-filtered `GET /api/leaves/`, so `leaveApi.myLeaves()`
(`/api/my/leaves/`) and `leaveApi.approvalInbox()` (`/api/utrmc/approvals/leaves/`) are defined but
never called — **GAP-LOW**, same "superseded by an equivalent generic path" reasoning as §4.1.

**Prior open item (§7.2) formally resolved**: leave management now has a complete resident
submit/list/detail UI and a supervisor/admin approve-or-reject flow, live and reachable.

## 5. Dashboards, Reports & Exports — WORKING

`/academics/monitoring`, `/academics/supervisor-workload`, `/academics/my-progress`,
`/academics/reports/*` (resident progress, supervisor workload, evaluations, logbook, data-quality,
each with CSV export) — spot-checked, still map to real `/api/academics/monitoring/*` and
`/api/academics/reports/*` endpoints, unchanged from the prior audit.

`frontend/app/dashboard/supervisor/residents/[id]/progress/page.tsx` is a 3-line
`redirect('/dashboard/supervisor')` stub — confirmed deliberate (matches the same Brick 8.6
redirect-stub pattern as §6 below), backed by a real, unreached
`GET /api/supervisors/residents/<id>/progress/` (`SupervisorResidentProgressView`,
`sims/training/views.py`). **GAP-LOW**, same bucket as §6, not a new finding.

## 6. Backup & Restore — WORKING (regression found and fixed this pass)

**Regression found**: `frontend/app/dashboard/utrmc/backup/page.tsx` had been replaced with a 6-line
`redirect('/dashboard/utrmc')` stub in commit `129abaa` ("Update 0 through Brick 8.6 foundation and
cleanup", 2026-07-15) — **before** the 2026-07-23 audit that then reported this route as WORKING.
That prior WORKING verdict was a false positive: it was based on `components/backup/*.tsx` having
passing unit tests (true, but those tests render the components directly, not through the page
route) and never checked that the actual `/dashboard/utrmc/backup` route rendered them. There was
also no nav-registry link to the page. Net effect: the entire backup/restore/Google-Drive UI was
live in the codebase, fully tested, and completely unreachable by any real user for at least three
weeks.

**Fixed this pass**: restored `frontend/app/dashboard/utrmc/backup/page.tsx` to the full
`BackupCenterPage` implementation (git history at `129abaa~1`) — verified all four child components
(`BackupList`, `CreateBackupModal`, `RestoreModal`, `GoogleDrivePanel`) and UI primitives
(`MetricCard`, `SectionCard`, `ErrorBanner`, `SuccessBanner`) it depends on still exist with matching
prop signatures before restoring (no drift since the commit that disabled it). Added a "Backup
Center" entry to the Admin section of `frontend/lib/navRegistry.ts` (previously missing) so the page
is actually discoverable via the sidebar, not just directly-navigable by URL. Verified: `npm run
typecheck` clean, `npm run lint` clean, `npx jest frontend/components/backup` (3 suites / 6 tests)
passing.

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/dashboard/utrmc/backup` (now nav-linked) | `/api/backup_center/backups/` (list/detail/create-routine/create-disaster/delete/download/validate), `/restores/` (list/upload/validate/dry-run/confirm), `/audit-logs/`, and the full `google-drive/*` set (status/connect/disconnect/health-check/create-folder/list, plus per-backup upload/verify/download) | WORKING — every one of these paths has a real, invoked caller in `components/backup/{BackupList,CreateBackupModal,RestoreModal,GoogleDrivePanel}.tsx`, confirmed by literal-path grep, not just component test coverage. This resolves the prior version's GAP-LOW list for this section in full. |
| n/a | `GET /api/backup_center/google-drive/oauth/callback/` | BACKEND-ONLY — a server-side OAuth redirect target opened by Google's consent flow, not something frontend JS calls directly; the page's `?googleDrive=connected\|error` query-param handling is the frontend-side half of this flow. No action needed. |

## 7. Notifications — GAP (real backend, api-client wrapper exists, zero UI)

`sims/notifications/urls.py` exposes `GET /api/notifications/` (list, with `is_read`/
`notification_type`/`ordering` filters), `POST /api/notifications/mark-read/`,
`GET/PATCH /api/notifications/preferences/`, `GET /api/notifications/unread-count/`. A full,
reasonably careful api-client wrapper exists at `frontend/lib/api/notifications.ts`
(`notificationsApi`, including field-shape adapters like unwrapping backend's `{unread: n}` into
`{count: n}`), but **zero** page or component under `frontend/app`/`frontend/components` imports or
calls it — no notification bell, no dropdown, no preferences page, nothing. This is exactly the
"backend + api-client-file exists, but never actually wired to a UI" pattern the task brief warns
about — the api-client layer alone does not establish reachability. See §9 open decisions.

## 8. Audit Log Viewer — GAP (real backend, api-client wrapper exists, zero UI)

`sims/audit/urls.py` registers `ActivityLogViewSet` (`/api/audit/activity/`) and `AuditReportViewSet`
(`/api/audit/reports/`, list + create). `frontend/lib/api/audit.ts` wraps both. No page or component
calls either. This is a **different** audit surface from the backup-center's own audit log
(`/api/backup_center/audit-logs/`, §6 above, which **is** wired) — don't conflate the two; this
finding is specifically about the general-purpose `ActivityLog`/`AuditReport` models having no
viewer anywhere. See §9 open decisions.

## 9. Open product-scope decisions (not built this pass — genuinely non-trivial, needs a call)

Each item below is a real, currently-passing backend capability with **no** frontend path to reach
it, where either (a) no frontend UI exists at all today (not even a stub/redirect) so building one
is a real feature, not a wiring fix, or (b) closing it would require a product decision about
whether the capability is still wanted. None of these were built, per the instruction to leave
larger/decision-requiring gaps documented rather than guessed at.

1. **Notifications (§7)** — a notification bell/dropdown + preferences page would need: unread-count
   polling, a read/unread list view, mark-as-read interaction, and a preferences form, wired into
   `DashboardLayout.tsx` (which currently has no header region at all, only a sidebar) for all four
   roles. The api-client layer is ready; the UI is a genuine net-new feature, not a small wire-up —
   left undecided/unbuilt.
2. **Audit log viewer (§8)** — `ActivityLogViewSet`/`AuditReportViewSet` have no admin-facing page.
   Same shape as #1: api client exists, UI does not, and scope (which roles see it, what filters
   matter) needs a decision before building.
3. **Change primary supervisor (§2)** — `POST /api/supervision/change-primary/` is a real,
   admin-only, atomic "rotate a resident's primary supervisor with a reason and effective date"
   workflow with no UI trigger anywhere under `/supervision/*`. Needs a small form/modal (resident
   picker, new-supervisor picker, start date, reason) — plausible to build quickly, but it's a new
   interaction, not a toggle on an existing screen, so left as a documented decision rather than
   guessed at without the ability to click-test it live.
4. **Rotation completion / certificate verification (`sims.training.RotationCompletion`,
   `RotationCompletionsView`, `RotationCompletionVerifyView`)** — confirmed (via
   `grep -rn "RotationCompletion.objects.create\|RotationCompletion("` across `backend/sims`,
   production code only) that **no production code path ever creates a `RotationCompletion` row** —
   the model, list view, and admin-verify-with-certificate-issuance action are only ever exercised by
   tests constructing rows directly via the ORM. This is a bigger gap than a missing UI: even if a
   frontend were built today, there is no backend trigger (e.g. "mark rotation complete → create a
   completion record pending certificate verification") to make it meaningful. This needs a product
   decision on whether rotation completion/certificate issuance is in scope at all before any code
   (frontend or backend) is written — not something to guess at.
5. **`sims/training`'s thesis/research/workshops/postings/milestones cluster** — unchanged from the
   prior audit's §7.4: `frontend/app/dashboard/resident/{thesis,research,workshops,postings,schedule,progress}/page.tsx`
   and `.../dashboard/supervisor/research-approvals/page.tsx` remain deliberate
   `redirect(...)` stubs. Confirmed still true this pass (`grep` for `redirect(` in each). Backing
   endpoints (thesis/synopsis submission+review, research projects, workshop completions, deputation
   postings, program milestones, eligibility) remain real and tested but intentionally unreached.
   `SupervisorResidentProgressView` (§5) and `MilestoneResearchRequirementView` belong to this same
   deliberately-deferred cluster. No action needed unless pilot scope changes.

## 10. GAP-LOW — isolated parameterized endpoints, low severity

- `rotations/api/departments/<hospital_id>/` (`department_by_hospital_api`, hospital→department
  cascading-dropdown helper) — confirmed zero references anywhere in `frontend/` (previously also
  used by an e2e spec; that reference is gone too). Superseded by `/api/hospital-departments/`
  (the matrix endpoint `rotationsApi.listHospitalDepartments()` actually uses on the rotation-
  assignment create form). Harmless, no action.
- `GET /api/my/rotations/`, `/api/utrmc/approvals/rotations/`, `/api/supervisor/rotations/pending/`,
  `/api/my/leaves/`, `/api/utrmc/approvals/leaves/` — see §4.1/§4.2, functionally superseded by the
  generic RBAC-filtered list endpoints the actual UI calls.
- Pre-unified bulk-import endpoints (§3) — superseded by `import/<entity>/<action>/`.

---

## 11. Summary

Of the backend resource groups checked across `users`, `academics`, `rotations`, `training`,
`supervision`, `bulk`, `notifications`, `backup_center`, and `audit`: the large majority — core
identity, supervision assignments, masters/bulk-import, academic workflow (evaluations/logbook/
rotation-templates), rotation assignments, leave requests, dashboards/reports, and backup/restore —
are confirmed **WORKING** with a real, invoked frontend caller (not just an api-client definition).

**Newly confirmed WORKING that the prior document had as GAP**: leave management (§4.2, prior §7.2)
and rotation-assignment scheduling (§4.1, prior §7.10/§7.10a) both now have complete, wired,
end-to-end UIs. The prior document's §7.3 (duplicate masters ViewSets) is confirmed fully resolved
(code deleted, not just decided).

**Newly found regression, fixed this pass**: the Backup Center page (§6) had silently regressed to a
redirect stub three weeks before the prior audit ran, making its 2026-07-23 "WORKING" verdict a false
positive based on component-level test coverage rather than actual route behavior. Restored and
nav-linked; this is the single code fix made in this pass.

**Newly found gaps, not previously documented**: `sims/notifications` (§7) and the general-purpose
`sims/audit` activity-log/report viewer (§8) both have complete backend + api-client-wrapper layers
and precisely zero frontend UI — the same "wrapper exists, nothing calls it" shape the bulk-import
bug taught this project to check for explicitly, just not caught until this pass because no one had
previously grepped for real call sites of `notificationsApi`/`auditApi`. Also newly found: the
`change-primary` supervisor-rotation endpoint (§2) has the same shape.

**Left as open decisions** (§9): notifications UI, audit-log-viewer UI, change-primary-supervisor UI,
and — the most consequential — rotation completion/certificate issuance, which turns out to have no
production trigger at all (not just no UI), meaning it needs a scope decision before either backend
or frontend work continues. The thesis/research/workshops/milestones cluster remains confirmed
intentional dead UI (real backend, deliberate stub), unchanged from the prior audit.
