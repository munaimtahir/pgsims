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
| `/masters` (now the live `BulkSetupWorkspace` bulk import/export screen — was a static description page as of the initial 2026-07-23 pass, fixed same day, see audit §4.6/Step 5) | `POST /api/bulk/import/<entity>/<action>/`, `GET /api/bulk/templates/<resource>/`, `GET /api/bulk/exports/<resource>/`, plus `/api/bulk/flexible/*` for the custom column-mapping mode | WORKING — covers hospitals, departments, matrix, training-programs, faculty-supervisors, residents, supervision-links, and rotation-assignments. |

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
**DECIDED 2026-07-24: in scope for this pilot.** Leave request/approval is confirmed a real,
wanted feature — needs a resident-facing submit/list form and a supervisor/admin approval inbox,
comparable in size to the bulk-import gap. **Not started yet, by explicit instruction**: build this
after the remaining open decisions (§7.3/§7.5/§7.6 below) are finalized, not before.

### 7.3 MIXED — a second "masters" API: two dead ViewSets, five with real (untested-by-frontend) test coverage
`sims/academics/urls.py` registers a DRF router (`InstitutionViewSet`, `HospitalViewSet`,
`DepartmentViewSet`, `TrainingProgramViewSet`, `SpecialtyViewSet`, `DesignationViewSet`,
`AcademicSessionViewSet` — all from `sims/academics/views.py`), mounted **twice** in
`sims_project/urls.py`: at `api/masters/` (line 156) and again at `academics/api/` (line 158). No
frontend page or component calls either prefix (confirmed by grep across `frontend/app`,
`frontend/components`, `frontend/lib`, `frontend/e2e`).

**Correction to an earlier version of this finding**: an initial pass classified this whole cluster
as dead/legacy and attempted to relocate it out of the live app — that relocation was executed,
tested, and then **reverted** in the same session, because `sims/tests/test_masters_brick6.py::
test_master_apis_rbac` hits `/api/masters/institutions/` directly by URL string (not by importing
the view class, which is why the initial grep-based dead-code check missed it) to verify admin-write
/ resident-read-only RBAC on this exact endpoint. That test is real, intentional, and currently
passing — this is not abandoned code by that measure.

Breaking it down by model:
- **`HospitalViewSet`, `DepartmentViewSet`** — genuinely redundant: `sims.users.userbase_views` (§3)
  exposes the same canonical `Hospital`/`Department` models at `/api/hospitals/`/`/api/departments/`,
  which **is** what the frontend and the bulk-import screen actually use. These two duplicate an
  already-working path.
- **`InstitutionViewSet`, `SpecialtyViewSet`, `DesignationViewSet`, `AcademicSessionViewSet`,
  `TrainingProgramViewSet`** — **not** duplicated elsewhere. `Institution`/`Specialty`/
  `Designation`/`AcademicSession` data is read (but not written) elsewhere, via
  `IdentityOptionsView` (`/api/identity/options/`, confirmed working — powers the dropdown option
  lists on `/complete-profile` and `/users/new`) and populated via the `seed_pilot_masters`
  management command. The **write/CRUD path** for these five master-data types has real,
  RBAC-tested backend support and genuinely **no frontend UI** — this reads more like the leave
  management gap (§7.2: real capability, no way to reach it) than like confirmed-dead code.

**DECIDED AND EXECUTED 2026-07-24**: given the choice per model —
- **Academic Session**: real, structurally required (`ResidentProfile.academic_session_ref` is a
  live foreign key set during profile completion, alongside `hospital`/`department_ref`/
  `program_ref`, all of which already had a working admin path). Built via the same pattern as
  Training Program (§4.6/Step 5): a new `import_academic_sessions` bulk-import method
  (`sims/bulk/services.py`), wired into the unified import endpoint, template, and export; a new
  "Academic Sessions" panel added to `BulkSetupWorkspace.tsx` at `/masters` (Step 5 of 9 in that
  workflow now). 4 new backend tests.
- **Institution, Specialty, Designation**: confirmed not structurally needed (not real foreign keys
  anywhere — `User.specialty` and `*Profile.designation` are free-text fields, not FKs to these
  tables) — no UI built, per the decision.
- **The entire dead cluster removed**: `sims/academics/urls.py` (all 7 ViewSets:
  `InstitutionViewSet`, `HospitalViewSet`, `DepartmentViewSet`, `TrainingProgramViewSet`,
  `SpecialtyViewSet`, `DesignationViewSet`, `AcademicSessionViewSet`) deleted along with the two
  dead URL mounts in `sims_project/urls.py`. The `Institution`/`Specialty`/`Designation`/
  `AcademicSession` **models** were kept — still used by Django admin, `IdentityOptionsView` (the
  read-only dropdown source for `/complete-profile`/`/users/new`), the `seed_pilot_masters`
  management command, and (for `Institution`) a foreign key in `sims/rotations/models.py`. Only the
  duplicate REST API onto them was removed.
- Retired `sims/tests/test_masters_brick6.py::test_master_apis_rbac` (the only test depending on the
  removed routes, found this time by checking both `reverse()` names and literal URL strings before
  touching anything — no surprises, unlike §7.3's first attempt). Its sibling tests in the same file
  (`test_identity_options_endpoint`, `test_onboarding_profile_completion_resolves_master_foreign_keys`,
  `test_data_quality_endpoint`, `test_seed_pilot_masters_command`) all still pass unchanged.

Verified: `pytest sims` 439 passed / 8 skipped / 0 failed, `manage.py check` clean,
`check_all_pgms_gates.sh` all pass, zero remaining references to any removed class/route anywhere in
the backend.

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

### 7.5 CORRECTED — not confirmed-dead: `sims/training`'s "operational dashboard" + "logbook" implementation has real backend test coverage
`sims/training/urls.py` and `sims/training/views.py` contain a second, complete implementation of
logbook entries (`LogbookEntryViewSet`, `LogbookThresholdConfigViewSet` at bare `/api/logbook/`) and
role dashboards (`ResidentOperationalDashboardView`, `SupervisorOperationalDashboardView`,
`UTRMCOperationalDashboardView` at `/api/dashboard/*`). **No production frontend code calls it** —
that part of the original finding holds. But an attempt to verify this as safe to relocate found it
is exercised extensively by the **backend** test suite via direct URL strings (not by importing the
view class, which is why the initial class-name-based check missed it): `sims/training/tests.py`,
`sims/training/test_feature_layer_ops.py`, `sims/test_schema_gate.py`, and several files under
`sims/tests/` collectively make dozens of calls to `/api/logbook/...` and `/api/dashboard/...`
directly. This is real, substantial, currently-passing test coverage, not incidental.
**Corrected assessment**: this is not "confirmed dead code" in the same sense as §7.6 below — it's a
working, tested backend implementation with no current frontend consumer.

**DECIDED AND EXECUTED 2026-07-24: removed.** Confirmed genuinely superseded by
`sims.academics`'s logbook/dashboards (§4) — deleted `LogbookEntryViewSet`,
`LogbookThresholdConfigViewSet`, `LogbookReviewQueueView`, `LogbookMyThresholdView`,
`ResidentOperationalDashboardView`, `SupervisorOperationalDashboardView`,
`UTRMCOperationalDashboardView` and their URL registrations from `sims/training/views.py` /
`urls.py`. The `LogbookEntry`/`LogbookThresholdConfig` **models** were left untouched — they're
genuinely used elsewhere (`sims/bulk/services.py`'s bulk review/assignment feature,
`sims/users/models.py`'s dashboard stat calculations) — only the duplicate API surface onto them
was removed. Retired/repurposed the ~15 backend tests that specifically exercised this dead surface
across 7 files (some tests were fully removed, some had only their dead-endpoint assertions
stripped while keeping coverage of other, unrelated things in the same test method). Verified: full
`pytest sims` suite green (436 passed / 8 skipped / 0 failed), `check_all_pgms_gates.sh` all pass,
zero remaining references to any of the removed routes/names anywhere in the backend. Chose plain
deletion over the "move to `_deprecated_candidates`" pattern used elsewhere in this document — unlike
§7.3's cluster, this code was tightly coupled to private helper functions shared with other live
views, making a clean standalone relocated copy impractical; git history is the recovery path if
ever needed.

**Not fixed, flagged as a follow-up**: three Playwright e2e spec files still reference the now-removed
routes (`frontend/e2e/feature-layer/permissions.spec.ts`,
`frontend/e2e/critical/admin_analytics_live_feed.spec.ts`,
`frontend/e2e/smoke/ui_pilot_readiness.spec.ts`). These need a running server to execute and
weren't run as part of this change's verification (which used `pytest`/`npm test`/gate scripts, not
full e2e) — fixing them blind without being able to run them risks guessing wrong. Two of the three
appear to be response-mocking/interception code that would likely just go unreached rather than
fail; `permissions.spec.ts` makes a real request to the removed endpoint and would fail if run.

### 7.6 CORRECTED (twice) — the "stats"/"analytics" views in `sims/users/views.py` also have real test coverage
`UserSearchAPIView`, `SupervisorsBySpecialtyAPIView`, `UserStatsAPIView`, `UserStatisticsAPIView`,
`UserPerformanceAPIView`, `admin_stats_api`, and the four `"coming soon"` analytics stub views from
§4.4 — all in `sims/users/views.py`/`sims/users/urls.py` under the `users:` namespace. First pass
(class/function-name grep): flagged as confirmed dead. Second pass (literal URL-string grep, done
after §7.3/§7.5 were caught): still showed zero hits and was reported here as "the one candidate
that's actually safe to relocate." That was still wrong — a **third**, closer check (grepping for
the actual `reverse("users:<url-name>")` calls, e.g. `reverse("users:admin_analytics")`,
`reverse("users:user_stats_api", kwargs={"pk": ...})`) found real, passing test coverage for
**every single view in this cluster**, in `sims/tests/test_users_views_final_push.py` and
`sims/tests/test_users_views.py`. No relocation was attempted for this cluster — it was caught by
this third check immediately before any file was touched, unlike §7.3 which had to be relocated,
tested, found broken, and reverted.

**DECIDED 2026-07-24**: leave the old analytics stubs/stats views as-is (planned for a future
version, not this pilot). The underlying real gap this cluster surfaced — the `/users`,
`/residents`, `/supervisors`, `/support-staff` directory pages have no search or filter of any kind
— **has been built**: the backend already fully supported `search`/`active`/`department` query
params on `UserViewSet` (`sims/users/userbase_views.py`), so this was a pure frontend addition — a
debounced search box (name/username/email) and an active/inactive status filter added to
`RoleDirectoryPage.tsx`, the shared component behind all four directory pages. New test coverage in
`RoleDirectoryPage.test.tsx` (4 tests). Verified: `npm run build/typecheck/lint` clean, `npm test`
35/35 suites (up from 34).

### 7.3/7.5/7.6 — a note on methodology (read before acting on anything in this document)
The original Step 0 reverse-check searched for backend view **class and function names** across the
frontend and backend. That method has a real, three-times-demonstrated blind spot:
`django.urls.reverse("app:route_name")` calls and direct URL-string test/API calls reference the URL
**name** or the literal **path**, neither of which contains the view class name. **Every single one**
of the three clusters originally reported in this document as "confirmed dead legacy code" turned
out, on progressively closer inspection, to have real, substantial, currently-passing test coverage.
One (§7.3) was actually relocated, broke a test, and had to be reverted. Given that track record,
**no other "zero references" claim in this document should be treated as verified for relocation
purposes** without first checking for `reverse("<app>:<url-name>")` calls specifically — class-name
and literal-path checks alone were not sufficient. §7.2 (leave management) and the frontend-facing
findings (§4.6, §7.4, §7.8) are a different, more reliable category — they were checked by asking
"does any frontend code call this," which doesn't have this particular blind spot, though it should
still be treated as a strong signal rather than absolute proof. A systematic re-check by URL *name*
(every `name="..."` in every `urls.py`, cross-referenced against every `reverse(...)` call) has not
been done end-to-end for every entry in this document, only for the specific clusters investigated
in §7.3-§7.6.

**Update 2026-07-24**: of the two dead-code clusters, one (§7.5) has been decided and removed; §7.3
and §7.6 remain as documented above pending further decisions or are resolved as noted inline.
Separately, the real gap this cluster's investigation surfaced — no search/filter on the user
directory pages — has been built; see the note at the end of §7.6.

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
academic workflow, dashboards/reports, backup/restore, and — as of the same-day fix — bulk import)
are confirmed **WORKING**. Beyond the bulk-import gap (found and fixed, §4.6/Step 5), this pass
found **one real, undecided feature gap** (leave management, §7.2 — real backend, no frontend at
all), **one deliberately-retired feature set** confirmed intentional (§7.4 — thesis/research/
workshops/postings, no action needed), and **three backend clusters that were investigated as
possible dead code and, on progressively closer checking, all turned out to have real, currently
passing backend test coverage despite having no frontend consumer** (§7.3, §7.5, §7.6 — see the
methodology note at the end of §7.6 for what went wrong and why). **None of the three were
relocated** — one was relocated, found to break a test, and reverted; the other two were caught by
closer checking before any file was touched. All three are left exactly as they were before this
audit, flagged for a human decision on each (product scope for §7.3's untested-by-frontend
CRUD surface; whether §7.5/§7.6 are genuinely obsolete duplicates whose tests should be retired, or
still meaningfully relied upon) rather than any further static-analysis-driven cleanup attempt. A
handful of small items remain to confirm by hand during the pre-launch smoke test (§6 backup
actions, §7.8).
