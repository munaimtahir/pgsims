# PGSIMS Deep Review Audit — Pilot Readiness

**Date**: 2026-07-23
**Auditor**: Claude Code, working directly against the codebase (not summarizing prior docs)
**Method**: Read `AGENTS.md`/`GEMINI.md`/`docs/CANONICAL_SOURCE_OF_TRUTH.md`; ran the full backend
test suite with coverage, all gate scripts, and the full frontend build/typecheck/lint/unit-test
pipeline against the current working tree; cross-checked self-reported "brick" verdicts against
actual code and test output; grepped for stub/placeholder markers.

---

## 1. What this application is supposed to do

PGSIMS is the postgraduate medical training management system for UTRMC (University Teaching &
Research Medical Complex / affiliated hospitals). It exists to replace manual/paper tracking of:

- **Who residents and supervisors are**, and which hospital/department they belong to.
- **Rotations**: which resident is placed in which hospital-department for which date range, with
  approval workflow for cross-hospital placements.
- **Supervision**: which supervisor is responsible for which residents.
- **Academic workflow**: logbook entries (clinical procedures a resident performs) and evaluations,
  each going through a draft → submit → supervisor-review (approve/return) cycle.
- **Eligibility monitoring**: tracking whether a resident has met the requirements (logbook volume,
  thesis, workshops) to sit for milestone exams.
- **Reporting/dashboards**: role-specific views (Admin/UTRMC, Supervisor, Resident) summarizing the
  above, with CSV export.
- **Administration**: bulk import of rosters, backup/restore of the database, audit logging of
  every state change.

Target pilot scope (per `docs/APP_OVERVIEW.md`, itself somewhat dated — see §5): 1–2 hospitals,
~2 departments, ~10 supervisors, ~30 residents.

## 2. Current architecture (ground truth, verified against code — not docs)

- **Backend**: Django 4.2 + DRF, JWT auth, PostgreSQL, Celery/Redis for async work.
  Active apps (in `INSTALLED_APPS`): `users`, `academics`, `rotations`, `audit`, `bulk`,
  `notifications`, `training`, `supervision`, `backup_center`.
  Apps present in the tree but **not installed** (dead code, kept for reference only):
  `sims/_legacy/{cases,certificates,logbook,search,analytics,attendance,reports,results}`. None of
  these run in the live app — anything that references them is legacy, not a live gap.
- **Frontend**: Next.js 14 App Router, TypeScript, Tailwind, React Query, Zustand. ~90 routes.
- **Identity/roles**: exactly four roles — `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF` — with
  a single universal creation flow (`/users/new` → `create_user_with_profile()`), verified directly
  in `backend/sims/users/models.py` and `services.py`. This is the "clean-room" rebuild described in
  `AGENTS.md`, and it is what's actually running today.
- **Canonical domain model**: one `Department` (`academics.Department`), one `Hospital`
  (`rotations.Hospital`), joined by `HospitalDepartment`. No duplicate department/hospital models
  exist in the current codebase — verified by direct grep.
- **Delivery process**: work is organized into sequential "bricks" (Update 0 identity cleanup →
  Brick 6 masters/data-quality → Brick 7 supervision → Brick 8 academic foundation → Brick 9–10
  academic workflows → Brick 11 dashboards/reports → Brick 12 production hardening), each with a
  `docs/implementation/<date>_brick_.../FINAL_VERDICT.md` and a `scripts/check_brick_*.sh` gate
  script that CI/agents are expected to run before calling a brick done.

## 3. What has actually been built and verified working

I ran every check independently rather than trusting the "GO" verdicts in the brick docs. Results:

| Check | Result |
|---|---|
| Backend test suite (`pytest sims`) | **406 passed, 8 skipped, 0 failed** |
| Backend `manage.py check` | 0 issues |
| Backend `makemigrations --check --dry-run` | No changes detected (migrations in sync with models) |
| `scripts/check_all_pgms_gates.sh` (9 gate scripts: identity, masters, supervision, academic foundation, brick 9-10, brick 11, brick 12, canonical roles, legacy-delete-candidates) | **ALL PASS** |
| Frontend `npm run build` | Succeeds cleanly, ~90 routes compiled |
| Frontend `npm run typecheck` | 0 errors |
| Frontend `npm run lint` | 0 warnings/errors |
| Frontend `npm test` (Jest) | **90 passed, 7 failed, across 34 suites (5 failing)** — see §4 |

The 8 skipped backend tests are all intentional (Google Drive backup connector — explicitly
out-of-scope per Update 0/Brick 7 skip markers in the test file itself, not a bug).

Functionally working, end to end (backend endpoint + frontend page + passing tests), as of this
audit:

- Universal user/identity creation and the four-role model, onboarding/profile-completion flow.
- Hospital/department/matrix management (masters data).
- Resident–supervisor assignment (supervision spine), including CSV import and data-quality checks.
- Rotation placements with inter-hospital override/approval workflow.
- Academic workflow: logbook entries and procedure records, evaluation forms, submit → review →
  approve/return cycle, resident personal-progress view, supervisor workload view.
- Dashboards and CSV export/reporting for Admin, Supervisor, and Resident roles, with backend-side
  access scoping (residents see only their own data; supervisors see only assignees).
- Audit logging via `django-simple-history` on state-changing models.
- Backup/restore tooling (`scripts/backup_pgms_db.sh`, `verify_pgms_backup.sh`,
  `restore_pgms_db.sh`) and a `/api/health/` endpoint reporting DB connectivity.
- Bulk import engine for rosters (residents, supervisors, placements, assignments), including a
  "flexible column mapping" mode for non-standard spreadsheets with dry-run/preview and
  strict/partial import modes.
- Operating manuals for Admin, Resident, and Supervisor roles now exist
  (`docs/ADMIN_OPERATING_MANUAL.md`, `docs/RESIDENT_QUICK_GUIDE.md`, `docs/SUPERVISOR_QUICK_GUIDE.md`).

## 4. Built but needs debugging — cannot be fully trusted yet

These were found by actually running the test suites, not by reading status docs (the brick
"GO" verdicts did not catch any of these, because none of them ran the frontend Jest suite or a
coverage report):

### 4.1 Real defect — Resident dashboard can crash on incomplete training records (FIXED in this audit pass)

`frontend/app/dashboard/resident/page.tsx:67-71` reads nested fields like this:

```tsx
<p>Program: {trainingRecord?.program.name || 'Not linked yet'}</p>
<p>Academic session: {trainingRecord?.academic_session.name || 'Not set'}</p>
<p>Department: {trainingRecord?.department.name || 'Not set'}</p>
<p>Training site: {trainingRecord?.training_site.name || 'Not set'}</p>
```

The `?.` only guards `trainingRecord` itself. If a resident has a training record but any of
`program`, `academic_session`, `department`, or `training_site` is `null`/absent (a realistic state
during pilot onboarding, before every field is fully populated), the page throws
`TypeError: Cannot read properties of undefined (reading 'name')` and the resident's own dashboard —
their primary landing page — goes blank. This is exactly the scenario the failing test
`ResidentHomePage › renders the canonical resident dashboard summary` reproduces.
**Fix applied in this audit pass**: changed each to `trainingRecord?.program?.name`, etc.
(`frontend/app/dashboard/resident/page.tsx`), and corrected a related stale assertion in
`page.test.tsx` that used an exact-text match against text that only ever rendered as a substring
(`"Primary supervisor: Prof Supervisor"`, not `"Prof Supervisor"` alone) — that assertion was wrong
independent of this bug and would have failed regardless. `app/dashboard/resident/page.test.tsx`
now passes.

### 4.2 Backend test coverage is below the project's own gate (61% vs. 80% target)

`backend/pyproject.toml` sets `--cov-fail-under=80`, but `backend/pytest.ini` (which wins, since
pytest prefers `pytest.ini` over `pyproject.toml` when both exist) doesn't enforce coverage at all,
so this has been silently unenforced. Actual measured coverage: **61.13%** overall. Weakest spots
(effectively untested):
- `backend/sims/bulk/services.py` (39%), `userbase_engine.py` (65%), `views.py` (61%) — the bulk
  import engine, i.e. exactly the code path used to onboard real pilot rosters.
- `backend/sims/backup_center/providers.py` (0%), `services.py` (30%), `views.py` (39%) — most of
  backup/restore is exercised by shell-script smoke tests, not unit tests.
- `backend/sims/training/views.py` (66%) — the largest file in the app (1590 statements) is the
  academic-workflow API surface; a third of it is untested branches.
- Most `manage.py` management commands (import/seed/reset scripts) are at or near 0% — expected for
  scripts, but means their correctness rests on manual testing only.

This isn't proof of bugs, but it means large parts of the system most likely to be exercised during
a live pilot (bulk import, backup/restore) have the thinnest automated safety net.

### 4.3 Frontend unit tests: 5 of 34 suites fail — mostly stale tests, but worth cleaning up

- `lib/auth/cookies.test.ts` — expects the role cookie to be lowercase (`resident`); the app
  correctly stores it uppercase (`RESIDENT`), matching the real role enum. **Test is stale, app
  behavior is correct.**
- `components/layout/Sidebar.test.tsx` (3 failing assertions) — expects nav labels like "My
  Schedule", "Overview", "Hospitals", "Logbook" that no longer exist; the Sidebar was rebuilt during
  the brick 6–11 work and the test wasn't updated. It even asserts a "Logbook" nav item, which
  belongs to the legacy, uninstalled `logbook` app. **Test is stale.**
- `app/dashboard/utrmc/page.test.tsx`, `app/academics/page.test.tsx` — same pattern: assert old copy
  ("Canonical Modules", "Training Records" link text) that was renamed during later bricks.
- `app/dashboard/resident/page.test.tsx` — this one is real (see §4.1); it's failing for the right
  reason.

None of these represent a broad functional regression, but a red test suite normalizes ignoring
failures, and it means the safety net that should have caught §4.1 wasn't actually being watched.

### 4.4 Legacy dead code left in the tree

- `sims/_legacy/*` (cases, certificates, logbook, search, analytics, attendance, reports, results):
  not installed, not routed, not reachable — but still present, still show up in searches, and could
  confuse a future contributor into "fixing" something that isn't live.
- `backend/sims/users/views.py` has four analytics endpoints (`admin_analytics_view`,
  `supervisor_analytics_view`, `pg_analytics_view`, `admin_stats_api`) explicitly stubbed to return
  `"Analytics coming soon"` / `{"status": "coming soon"}`. These predate the Brick 11 dashboard
  rebuild, which replaced this functionality properly under `/academics/reports/*`. Need to confirm
  nothing in routing still points a real nav item at these stubs, then delete them.

### 4.5 Documentation drift (not a code defect, but will actively mislead the next person)

Several docs in the repo describe an **earlier data/role model** that no longer matches the code and
will actively confuse anyone who starts here instead of at `AGENTS.md`:

- `README.md` — describes three roles ("Admin/Supervisor/PG"), calls the product "Surgical
  Information Management System", and documents a `Digital Logbook`/`Clinical Cases` feature set
  that's in `_legacy` and not installed.
- `.github/copilot-instructions.md` — RBAC section lists roles `pg`, `supervisor`, `admin`,
  `utrmc_user`, `utrmc_admin` (lowercase, 5-role legacy model) and references `sims.logbook`,
  `sims.cases`, `sims.search`, `sims.analytics` as active apps; none of these are installed today.
- `docs/APP_OVERVIEW.md` and `docs/USER_ROLES_AND_PERMISSIONS.md` — describe roles `Super Admin`,
  `HOD`, `Data Entry/Clerk`, `UTRMC Admin/User/Viewer` — none of which exist in the current
  four-role model (`AGENTS.md` explicitly forbids `HOD` and `CLERK`/`DATA_ENTRY` as roles).
- `docs/CURRENT_FINAL_STATE.md` and `docs/KNOWN_ISSUES.md` are dated 2026-05-30, before the
  Update 0 clean-room rewrite and Bricks 9–12; their test counts and "next approved step" no longer
  reflect reality.
- `docs/PROD_GATE_CLOSURE/` (11-blocker sprint, "NO-GO" verdict, dated 2026-04-23) and
  `docs/ANTI_DRIFT_GUARDRAILS.md` describe a sprint that appears to have been superseded by the
  brick-based process — but nothing in the repo says so explicitly, so a new agent following
  `README.md`'s "read this first" instructions would start from a stale, contradicted worldview.

I did not rewrite these in this pass (out of scope for an audit), but they should be either updated
or explicitly marked superseded before pilot, per the remediation plan below.

## 5. What is remaining / not yet built

- **Coverage enforcement**: the 80% backend coverage gate is defined but not actually running
  (§4.2) — either wire it into the CI/gate path or lower the stated target to match reality.
- **Legacy cleanup**: `sims/_legacy/*` and the four `"coming soon"` analytics stubs should be
  deleted or the pages verified fully dead, per `docs/LEGACY_DELETE_CANDIDATES.md` /
  `docs/FRONTEND_DELETE_CANDIDATES.md` (these files exist already — this audit did not verify
  whether they've been fully executed against, but the stubs above are still present).
  Note: `scripts/check_legacy_delete_candidates.sh` passes, so from the gate's perspective this is
  considered handled — worth reconciling that the analytics stubs weren't caught by it.
  I did not delete anything as part of this audit — that's a scoped follow-up, not something to do
  silently inside an audit pass.
- **Pagination on large report listings** (documented limitation, Brick 11) — fine at pilot scale
  (~30 residents), will need addressing before scaling beyond pilot.
- **No automated PDF export** — reports rely on browser print, documented and accepted as sufficient
  for pilot.
- **Frontend test suite health** — 5 stale suites need updating to match current UI copy/nav (§4.3).
- **Documentation reconciliation** — README/copilot-instructions/APP_OVERVIEW/USER_ROLES docs need
  to be brought in line with the current 4-role model, or explicitly marked historical (§4.5).

## 6. Plan to reach pilot readiness

This is scoped as four short, sequential work windows — each independently shippable, matching the
repo's own "brick" discipline (one focused window, gate script + doc at the end).

**Step 1 — Fix the one real defect — DONE**
Fixed the optional-chaining bug in `frontend/app/dashboard/resident/page.tsx` and the related stale
test assertion; `app/dashboard/resident/page.test.tsx` is now green.

**Step 2 — Repair the remaining frontend test safety net (half a day)**
Update the 4 still-stale suites (`cookies.test.ts`, `Sidebar.test.tsx`, `dashboard/utrmc/page.test.tsx`,
`academics/page.test.tsx`) to match current copy/role casing/nav structure, so `npm test` is green
end to end and can be trusted as a regression gate going forward. Left untouched in this pass
deliberately — rewriting UI-copy assertions without confirming the intended current copy against
design/product intent risks locking in the wrong text.

**Step 3 — Close the coverage gap on the highest-risk pilot paths (2-4 days)**
Not all of the 19-point coverage gap needs closing before pilot — but the bulk-import engine
(`sims/bulk/services.py`, `userbase_engine.py`) is what onboards real resident/supervisor rosters,
and backup/restore (`backup_center/providers.py`, `services.py`) is the safety net if pilot data
goes wrong. Prioritize tests for those two areas specifically over chasing the 80% number
everywhere. Then either fix the pytest.ini/pyproject.toml mismatch so the coverage gate is actually
enforced, or explicitly lower the documented target.

**Step 4 — Documentation and dead-code reconciliation (1 day)**
- Update or archive-and-flag `README.md`, `.github/copilot-instructions.md`,
  `docs/APP_OVERVIEW.md`, `docs/USER_ROLES_AND_PERMISSIONS.md` to match the 4-role model.
- Mark `docs/PROD_GATE_CLOSURE/` and `docs/ANTI_DRIFT_GUARDRAILS.md` as superseded-by-brick-process,
  or delete if truly obsolete, so a fresh contributor/agent isn't misdirected by README's "read this
  first" pointer.
- Delete or route away the four `"coming soon"` analytics stub endpoints in `sims/users/views.py`,
  confirming no live nav item still points at them.

**After Steps 1–4**: run `bash scripts/check_all_pgms_gates.sh`, `pytest sims`, and
`npm test && npm run build` one more time as a final go/no-go check, then this system is genuinely
ready for the pilot scope described in §1 (1-2 hospitals, ~30 residents, ~10 supervisors) — the
backend, data model, and workflow logic are already solid; what's missing is polish, not
architecture.

## 7. Bottom line

The core system is in materially better shape than the stale docs in this repo suggest, and no
worse than the newest brick docs claim — **with one exception**: the brick verdicts never actually
ran the frontend unit test suite, so they missed a real crash bug on the resident dashboard and a
set of stale tests that would have caught it. Backend logic, gate discipline, and the overall
architecture are sound and pass every check I could run. The path to pilot is short and concrete:
one real bug fix, one test-suite cleanup, targeted coverage work on the two highest-risk pilot code
paths, and a documentation pass so the next person (human or agent) doesn't start from a stale
worldview.
