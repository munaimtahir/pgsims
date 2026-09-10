# 03 — Canonical Domain Model Map

Scope: `backend/sims/*/models.py` for the 8 active apps only. Every entry below is verified against
current source, not carried forward from docs without a check.

## Identity / roles

| Model | App | Purpose | Canonical status |
|---|---|---|---|
| `User` | `users` | Custom user model (`AUTH_USER_MODEL`), role field ∈ {ADMIN, RESIDENT, SUPERVISOR, SUPPORT_STAFF} | CANONICAL |
| `AdminProfile`, `ResidentProfile`, `SupervisorProfile`, `SupportStaffProfile` | `users` | One-per-role profile, created together with `User` + `AuditLog` via `create_user_with_profile()` inside `transaction.atomic()` | CANONICAL |
| `ResidentDocumentRequirement`, `ResidentDocument` | `users` | Declared-required-document tracking for onboarding/`complete-profile` | CANONICAL |
| `ResidentOnboardingDeclaration` | `users` | Onboarding attestation record | CANONICAL |
| `DepartmentMembership`, `HospitalAssignment` | `users` | Cross-reference tables linking users to org units | CANONICAL |
| `DataCorrectionAudit` | `users` | Tracks corrections to identity/profile data post-creation | CANONICAL |

Confirms CLAUDE.md's 4-role model is exactly what's implemented — no 5th/legacy role field values
found in `User.role` choices.

## Org structure

| Model | App | Purpose | Canonical status |
|---|---|---|---|
| `Department` | `academics` | The one Department model repo-wide | CANONICAL (matches CLAUDE.md — no `RotationDepartment`/`AcademicDepartment` found anywhere) |
| `Hospital`, `HospitalDepartment` | `rotations` | Hospital↔Department matrix | CANONICAL (matches CLAUDE.md) |
| `Institution`, `Specialty`, `Designation`, `AcademicSession`, `AcademicPeriod` | `academics` | Supporting master data | CANONICAL |
| `TrainingProgram`, `ProgramRotationTemplate` | `training` | Program-level curriculum definition | CANONICAL |

## Training record — **RESOLVED, CLAUDE.md is stale here**

CLAUDE.md (root) states: *"Two independent `ResidentTrainingRecord` models exist and must each be
set up separately per resident: `sims.academics.ResidentTrainingRecord` ... and
`sims.training.ResidentTrainingRecord`."*

**This is no longer true.** Verified by direct source read:
- `class ResidentTrainingRecord` exists **only** in `sims/training/models.py:111`.
- `sims/academics/models.py` has **zero** `class ResidentTrainingRecord` definition — it only holds
  three string-FK *references* to `"training.ResidentTrainingRecord"` (lines 433, 475, 570), i.e.
  `academics` models point at the one canonical `training.ResidentTrainingRecord`, they don't
  duplicate it.
- The migration history confirms this was a deliberate, executed consolidation, not an accident:
  `sims/academics/migrations/0006_residenttrainingrecord_...` (created the now-removed duplicate) →
  `0010_link_training_record_new.py` → `0011_finalize_training_record_retarget.py` →
  `0012_drop_academics_resident_training_record.py` (dropped it).

**Action: update CLAUDE.md** to remove this warning — it currently tells every future agent to
treat a resolved duplicate as live, which risks reintroducing exactly the problem it was consolidated
to prevent, or wasting effort "setting up" a record that no longer exists. Filed as BE-1 (P2 — doc
correctness, not a code defect) in `12_BUG_TECH_DEBT_REGISTER.md`.

## LogbookEntry — **NEW finding: an *unresolved*, currently-live duplicate of the same shape**

Two independent, both-wired, both-actively-used `LogbookEntry` models exist today:

| | `sims.academics.LogbookEntry` (`models.py:563`) | `sims.training.LogbookEntry` (`models.py:986`) |
|---|---|---|
| Route | `/api/academics/logbook-entries/` (via `workflow_urls.py`) | Not directly URL-routed |
| Consumer | **The real, shipped resident logbook workflow** — this is what the Next.js web UI (`/academics/logbook`) and, per `SPRINT_STATE.md`, the Android app's Logbook screens read/write. Confirmed by `07_CONTRACT_DRIFT_REPORT.md`'s independent finding that the live route/fields are `academics.LogbookEntry`'s shape (`supervisor_comments`, `submit/verify/return_revision/reject/cancel` actions). | Used internally by: (a) `sims/training/views.py:2004` `_evaluate_logbook_thresholds()` — the function that computes whether a resident has hit logbook-count milestones/thresholds; (b) `sims/bulk/services.py` — the bulk-import pipeline creates/updates entries here (`LogbookEntry.objects.create(**payload, ...)` at line 290); (c) `sims/users/models.py:302` `get_documents_pending_count()` — a legacy dashboard "pending review" counter for supervisors and residents. |
| Status field | `DRAFT/SUBMITTED/VERIFIED/RETURNED/REJECTED/CANCELLED` (per `07_CONTRACT_DRIFT_REPORT.md` CD-4, reading `academics/models.py:598-608`) | Has its own `STATUS_APPROVED` constant and `SUBMITTED` status referenced in `training/views.py` and `users/models.py` — a parallel, not-identical status vocabulary |

**Why this matters (concrete failure scenario, not hypothetical):** a resident submits and a
supervisor verifies a logbook entry through the actual product (web or Android) — this writes to
`academics.LogbookEntry`. That entry is invisible to:
1. `_evaluate_logbook_thresholds()` in `training/views.py`, which only counts
   `training.LogbookEntry` rows with `status=STATUS_APPROVED` — so milestone/threshold eligibility
   computed from logbook volume can be silently wrong (under-counting real, verified entries).
2. `User.get_documents_pending_count()`, which queries `training.LogbookEntry` for
   `status="SUBMITTED"` to build supervisor "pending review" badge counts and resident "submitted"
   counts. This method is wired to a live URL (`sims/users/views.py:96`, reached via
   `/users/supervisor-dashboard/`, mounted in `sims_project/urls.py:160`) — a legacy
   server-rendered Django view, not the canonical Next.js UI, but still a reachable production URL
   that will always undercount/misreport real logbook activity. Both call sites wrap the query in
   a bare `except Exception: pass`, so this doesn't error — it fails silently, returning `0` instead
   of the true count.
3. Conversely, bulk-imported logbook entries (`sims/bulk/services.py`) land in
   `training.LogbookEntry` and are **not** visible on the resident's actual logbook page
   (`academics.LogbookEntry`-backed) — an imported entry would exist in the DB but never appear to
   the resident or supervisor who's supposed to review it.

This is the same *shape* of problem CLAUDE.md already flags for `ResidentTrainingRecord` (now
resolved) — a genuine single-source-of-truth violation, currently live, not previously documented
anywhere read in this pass (`AGENTS.md`, `docs/DATA_MODEL.md`, `docs/AUDIT_2026-07-23_PILOT_READINESS.md`
were all checked; none mention a LogbookEntry duplication). Filed as **BE-2, P1**, in
`12_BUG_TECH_DEBT_REGISTER.md` — this is the single most important backend finding of this
discovery pass and should weigh heavily on build-order sequencing for any further logbook/milestone
work (see `15_BUILD_ORDER_AND_ROADMAP.md`).

## Rotations, leave, deputation

| Model | App | Purpose | Canonical status |
|---|---|---|---|
| `RotationAssignment` | `training` | draft→submit→HOD/UTRMC approve→active→complete, `return_reason`/`reject_reason` | CANONICAL, matches CLAUDE.md exactly. No `override_reason` field found anywhere (`grep -r override_reason backend/` → zero hits) — CLAUDE.md's claim that no such field exists is confirmed current. |
| `LeaveRequest` | `training` | Same state-machine shape as rotations | CANONICAL |
| `DeputationPosting` | `training` | Temporary cross-institution posting | CANONICAL |
| `ProgramRotationRequirement`, `RotationCompletion`, `RotationCertificate` | `training` | Requirement tracking / completion evidence for rotations | CANONICAL |

## Research, workshops, submissions

| Model | App | Purpose |
|---|---|---|
| `Workshop`, `WorkshopBlock`, `WorkshopRun`, `ResidentWorkshopCompletion` | `training` | Workshop catalog + completion tracking |
| `ResidentResearchProject`, `ResidentThesis` | `training` | Research/thesis tracking |
| `SubmissionRequirementTemplate`, `ResidentSubmission`, `SubmissionDocument`, `SubmissionReview`, `SubmissionCertificate` | `training` | Generic document-submission workflow underlying research/workshop/synopsis requirements |
| `ProgramMilestone`, `ProgramMilestoneResearchRequirement`, `ProgramMilestoneWorkshopRequirement`, `ProgramMilestoneLogbookRequirement`, `ResidentMilestoneEligibility` | `training` | Milestone definitions and per-resident eligibility computation (the consumer of the LogbookEntry threshold logic above) |

All of these are backend-complete with no legacy duplicate found. Per the Android fork's finding
(`08_ANDROID_FEATURE_MATRIX.md`), the Android client currently only *reads* rollups of this data
(read-only summaries) — no authoring UI exists client-side yet. This is a client-side gap, not a
backend one; the backend surface here is real and available.

## Notifications, audit

| Model | App | Purpose | Canonical status |
|---|---|---|---|
| `Notification`, `NotificationPreference` | `notifications` | Canonical fields confirmed: `recipient` (FK), `verb`, `body`, `metadata` (JSONField) — `notifications/models.py:24-40`. No legacy `user=`/`message=`/`type=`/`related_object_id=` fields found anywhere in the model. | CANONICAL, matches CLAUDE.md exactly |
| `AuditLog` and `simple_history`-generated historical tables | `audit` + all apps via `simple_history` | Audit trail | CANONICAL |

## Backup/DR

| Model | App | Purpose |
|---|---|---|
| `BackupCenter` models (`sims/backup_center/models.py`) | `backup_center` | Backup job tracking, Google Drive connector state | CANONICAL — see `10_TEST_AND_CI_BASELINE.md` for one real test failure in this app (disaster-recovery backup path, environment-dependent, not a logic bug). |

## `sims/_legacy/` — confirmed dead, not installed

`cases`, `certificates`, `logbook`, `search`, `analytics`, `attendance`, `reports`, `results` — none
appear in `INSTALLED_APPS`. Grep for imports of `sims._legacy.*` or `sims.logbook`/`sims.cases`/
`sims.certificates` from **active** app code found only defensive `apps.is_installed(...)` guarded
branches (`sims/users/models.py:370-397`, `get_documents_submitted_count()`) that never execute in
the current deployment. Confirmed correctly dead — no accidental live dependency on `_legacy`.
