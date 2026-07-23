# Frontend-Backend Truth Map — PGMS Clean-Room Foundation

**Last independently verified**: 2026-07-23, as part of the pilot-readiness audit
(`docs/AUDIT_2026-07-23_PILOT_READINESS.md`, §4.6-§4.8). Method: enumerated every backend URL
pattern via `backend/sims/_devtools/truthmap_extract.py` (1183 raw route/method rows → 223 distinct
resource groups after collapsing HTTP-method/format-suffix variants), then cross-referenced each
against every frontend page (`frontend/app/**/page.tsx`), component, and `frontend/lib/api/*.ts` API
client file — in **both directions**: does every frontend call reach a real backend route (forward),
and does every backend route have a real frontend caller, or is it deliberately backend-only
(reverse)? This supersedes the previous version of this document, which was self-reported by each
brick's own implementing agent, one-directional, and covered only bricks 0/6/7/8/8.6/9-10/11 — it
never checked `/users`/`/residents`/`/supervisors`/`/support-staff`/`/admins` directory CRUD, auth
flows beyond login, `sims/bulk`, `sims/audit`, `sims/notifications`, or `sims/backup_center`, and
never checked for orphaned backend code.

Status legend: **WORKING** (real frontend↔backend pair, verified) · **GAP** (real capability, no
way to reach it — needs a decision) · **BACKEND-ONLY** (deliberately no UI needed) · **LEGACY**
(dead code from a superseded implementation, confirmed unreachable and superseded by a working
replacement).

---

## 1. Universal Identity & Profile Sync (Update 0) — WORKING

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/login` | `POST /api/auth/login/` | WORKING |
| `/change-password` | `POST /api/auth/change-password/` | WORKING |
| `/complete-profile` | `GET /api/auth/complete-profile/` (form spec), `GET /api/auth/me/` | WORKING |
| `/users/new` | `POST /api/users/` (→ `create_user_with_profile`) | WORKING |
| `/register`, `/forgot-password`, `/reset-password/[uid]/[token]` | `/api/auth/register/`, `/api/auth/password-reset/`, `/api/auth/password-reset/confirm/` | WORKING |
| `/users`, `/residents`, `/supervisors`, `/support-staff`, `/admins` (shared `RoleDirectoryPage`) | `GET /api/users/` (role-filtered via `userbaseApi.users`) | WORKING |

## 2. Supervision Spine (Brick 7) — WORKING

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/supervision`, `/supervision/assignments[, /new, /[id]]` | `/api/supervision/assignments/`, `/api/supervision/options/` | WORKING |
| `/supervision/import` | `POST /api/supervision/import/` | WORKING |
| `/supervision/data-quality` | `GET /api/supervision/data-quality/` | WORKING |

## 3. Core Masters & Directory (Brick 6) — WORKING (via a different endpoint than originally documented)

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/masters` (currently a static description page, no live data yet — see §4.6/Step 5) | `GET /api/hospitals/`, `/api/departments/`, `/api/hospital-departments/`, `/api/department-memberships/`, `/api/hospital-assignments/` (all `sims.users.userbase_views`) | WORKING at the API layer; **no frontend calls these yet** — tracked as Step 5 in the audit, not a new finding here. |

## 4. Academic Workflow Foundation (Brick 8) & Workflows/Submissions (Brick 9-10) — WORKING

Unchanged from the previous version of this document — independently spot-checked and confirmed
still accurate: `/academics`, `/academics/training-records[/[id]]`, `/academics/periods`,
`/academics/rotation-templates`, `/academics/evaluation-templates`, `/academics/logbook-categories`,
`/academics/review-queue`, `/academics/data-quality`, `/academics/evaluations[/new, /[id],
/[id]/review]`, `/academics/logbook[/new, /[id], /[id]/review]`, `/dashboard/resident`,
`/dashboard/supervisor`, `/residents/[id]`, `/supervisors/[id]` all map to real, working
`/api/academics/*` endpoints.

## 5. Dashboards, Reports & Exports (Brick 11) — WORKING

Unchanged from the previous version — confirmed still accurate: `/academics/monitoring`,
`/academics/supervisor-workload`, `/academics/my-progress`, `/academics/reports/*` (resident
progress, supervisor workload, evaluations, logbook, data-quality, each with CSV export) all map to
real `/api/academics/monitoring/*` and `/api/academics/reports/*` endpoints.

## 6. Backup & Restore (Brick 12) — WORKING

| Frontend Page | Backend Endpoint | Status |
| :--- | :--- | :--- |
| `/dashboard/utrmc/backup` (`components/backup/*`) | `/api/backup_center/backups/`, `/restores/`, `create-routine`, `create-disaster`, `upload`, and the Google Drive connect/status/list endpoints | WORKING for the core flows exercised by `components/backup/BackupList.tsx`, `CreateBackupModal.tsx`, `RestoreModal.tsx`, `GoogleDrivePanel.tsx` (all have passing tests). |
| n/a | `DELETE /api/backup_center/backups/<pk>/delete/`, `GET .../download/`, `POST .../validate/`, `POST .../restores/<pk>/{confirm,dry-run,validate}/`, `.../google-drive/{download,upload,verify}/`, `.../google-drive/oauth/callback/` | **GAP-LOW** — no direct frontend caller found for these specific actions. Likely reachable through UI flows I didn't fully trace (e.g. a confirm step inside `RestoreModal`), but worth a manual click-through to confirm during Phase 7 (smoke test) rather than assuming. |

---

## 7. NEW FINDINGS — genuine gaps and dead code (2026-07-23 audit)

### 7.1 GAP — Bulk-import UI not wired to any route
Already fully documented in `docs/AUDIT_2026-07-23_PILOT_READINESS.md` §4.6 / Step 5. Backend fully
supports hospitals/departments/matrix/supervisors/residents/supervision-links/rotation-assignments/
training-programs import; frontend component (`BulkSetupWorkspace.tsx`) exists and is tested but
unmounted. Not re-detailed here — see the audit doc.

### 7.2 GAP — Leave management has a complete backend and *zero* frontend
`LeaveRequestViewSet` (`/api/leaves/`), `MyLeavesView` (`/api/my/leaves/`), and
`LeaveApprovalInboxView` (`/api/utrmc/approvals/leaves/`) are fully implemented, tested backend
endpoints. I found **zero** references to "leave" anywhere under `frontend/app/` — not a page, not
a stub, not a redirect. This is different from §7.4 below (which has deliberate redirect stubs
acknowledging the feature was retired) — leave management looks like backend work that was never
followed up with any frontend at all, rather than a feature that was deliberately removed.
`docs/APP_OVERVIEW.md` (itself a stale doc, see the main audit §4.5) lists "Leave Management" as a
core pilot feature, which suggests this may genuinely be expected to work.
**Needs a product decision**: is resident leave request/approval in scope for this pilot? If yes,
this is a real missing frontend (list/submit form for residents, approval inbox for
supervisors/admins) — comparable in size to the bulk-import gap. If no, it should be documented as
explicitly deferred, the same way thesis/research/workshops were.

### 7.3 LEGACY — A whole second "masters" API, parallel to the one actually used, with zero callers
`sims/academics/urls.py` registers a DRF router (`InstitutionViewSet`, `HospitalViewSet`,
`DepartmentViewSet`, `TrainingProgramViewSet`, `SpecialtyViewSet`, `DesignationViewSet`,
`AcademicSessionViewSet` — all from `sims/academics/views.py`) and that router is mounted **twice**
in `sims_project/urls.py`: at `api/masters/` (line 156) and again at `academics/api/` (line 158).
Neither prefix has a single frontend caller anywhere (not even in e2e specs). This is a **completely
different set of view classes** from the ones the app actually uses for hospitals/departments —
those live in `sims/users/userbase_views.py` and are mounted at the plain `/api/hospitals/`,
`/api/departments/`, `/api/hospital-departments/` (confirmed working, §3 above). Grepped the whole
backend: the `sims.academics` versions are referenced only by their own `urls.py`/`views.py` — no
other backend code, no tests, imports them.
**Assessment**: this looks like an earlier "masters" implementation that was superseded by the
`userbase_views` one during a rebuild, and the old router registrations were never removed. Low risk
to the running app (nothing calls it), but it's actively confusing — two different `DepartmentViewSet`
classes, two different `HospitalViewSet` classes, is exactly the kind of duplication `AGENTS.md`
tells agents to avoid, even though in this case it's dead rather than actively diverging data.
**Recommendation, not yet executed**: remove the two `path(..., include("sims.academics.urls"))`
lines from `sims_project/urls.py` and relocate `sims/academics/urls.py` plus the seven orphaned
ViewSet classes out of `sims/academics/views.py` into a clearly-marked deprecated-candidates
location. I did not do this yet in this pass — unlike moving a whole standalone file, this requires
editing a live, shared `urls.py` and a large, actively-used `views.py`, which I judged as a
"decide together" change rather than a purely mechanical relocation, consistent with the review
process for destructive/legacy changes agreed for this audit. Flagging for the batch decision.

### 7.4 LEGACY (confirmed intentional) — Thesis/research/workshops/postings self-service pages are deliberate redirect stubs
`frontend/app/dashboard/resident/{thesis,research,workshops,postings,schedule,progress}/page.tsx`
and `frontend/app/dashboard/supervisor/research-approvals/page.tsx` are each a 6-line
`redirect('/dashboard/resident')` (or `/dashboard/supervisor`) stub — this matches the documented
"Brick 8.6 Cleanup Rule" (§5 of the old version of this doc: "Old `/dashboard/pg*` ... subpages are
redirect-only compatibility routes"), so this is a **confirmed deliberate decision**, not an
oversight. The backing endpoints (`ThesisSubmissionView`/`SynopsisSubmissionView` + review-queue +
review-action + documents, `ResidentResearchProjectView` + `ResearchProjectActionView`,
`MyWorkshopCompletionsView`, `DeputationPostingViewSet`, `SupervisorResearchApprovalsView`,
`ProgramMilestoneViewSet`, `MilestoneResearchRequirementView`) are real, tested, and fully built —
just intentionally not reachable from the current UI. **No action needed** unless this pilot's scope
changes to include the fuller academic-lifecycle tracking (thesis/synopsis/research/workshops
milestones) beyond rotations/logbook/evaluations.

### 7.5 LEGACY (confirmed) — A second, older "operational dashboard" + "logbook" implementation in `sims/training`
`sims/training/urls.py` and `sims/training/views.py` contain a second, complete implementation of
logbook entries (`LogbookEntryViewSet`, `LogbookThresholdConfigViewSet` at bare `/api/logbook/`) and
role dashboards (`ResidentOperationalDashboardView`, `SupervisorOperationalDashboardView`,
`UTRMCOperationalDashboardView` at `/api/dashboard/*`). These are referenced **only** by old e2e
specs (`frontend/e2e/critical/admin_analytics_live_feed.spec.ts`,
`frontend/e2e/smoke/ui_pilot_readiness.spec.ts`, `frontend/e2e/feature-layer/permissions.spec.ts`),
never by production frontend code. The current, actually-used implementation is
`sims.academics.views.LogbookEntryViewSet` at `/api/academics/logbook-entries/` (§4 above) and the
academics-based dashboards at `/api/academics/residents/me/summary/` etc. (also §4). This is the
same pattern as §7.3: an earlier implementation, superseded, never cleaned up — except this one is
still exercised by e2e specs, which means **those specs are testing dead code and should be
retired or repointed**, not treated as evidence the feature is live.
**Recommendation, not yet executed**: same treatment as §7.3 — relocate, don't delete, decide later.

### 7.6 LEGACY (confirmed, matches earlier §4.4 finding) — Old class-based "stats" views in `sims/users/views.py`
`UserSearchAPIView`, `SupervisorsBySpecialtyAPIView`, `UserStatsAPIView`, `UserStatisticsAPIView`,
`UserPerformanceAPIView`, `admin_stats_api` (function view) sit in the same file and same
pre-rebuild era as the four `"coming soon"` analytics stub views already flagged in the main audit
(§4.4). Zero frontend callers found anywhere. Same recommendation as §4.4: extract into their own
file, relocate to deprecated-candidates, decide later.

### 7.7 BACKEND-ONLY (no action needed)
- `api/health` — infrastructure health check, used by Docker/monitoring, not meant to have a UI.
- `api/schema` — OpenAPI schema endpoint (drf-spectacular), tooling-only.
- The `cases/`, `logbook/`, `certificates/` dummy-redirect routes (`sims/users/{cases,logbook,certificates}_dummy_urls.py`) — deliberate backward-compatibility redirects for old bookmarked URLs, already documented, working as designed.
- `rotations/api/quick-stats` — same dummy-redirect pattern.

### 7.8 GAP-LOW — a few isolated parameterized endpoints without a confirmed caller
`api/rotations/completions/<id>/verify`, `api/supervisors/residents/<id>/progress`,
`api/milestones/<id>/requirements/research`, `rotations/api/departments/<hospital_id>` (a
hospital→departments cascading-dropdown helper, referenced only in an e2e spec). These are small
enough that a manual click-through during Phase 7 (smoke test) will confirm or refute them faster
than further static analysis — flagged here so they aren't forgotten, not treated as high-severity
findings.

---

## 8. Summary

Of ~200 distinct backend resource groups checked: the large majority (core identity, supervision,
academic workflow, dashboards/reports, backup/restore) are confirmed **WORKING**. Beyond the
already-known bulk-import gap, this pass found **one real, undecided feature gap** (leave management,
§7.2), **three confirmed-dead legacy clusters** left over from pre-rebuild implementations (§7.3,
§7.5, §7.6 — none of them risky to leave as-is, all worth relocating out of the live app directories
once there's time), **one deliberate, already-documented set of deferred features** (§7.4 — no
action needed), and **a handful of small items** to confirm by hand during the pre-launch smoke test
(§6 backup actions, §7.8). None of the legacy findings were relocated in this pass — they involve
edits to shared, live files (`urls.py`, `views.py`) rather than moving an isolated file, so they're
being surfaced for a batch decision rather than acted on unilaterally, consistent with how this audit
has handled destructive/legacy changes throughout.
