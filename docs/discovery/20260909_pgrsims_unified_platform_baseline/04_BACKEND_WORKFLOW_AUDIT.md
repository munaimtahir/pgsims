# 04 — Backend Workflow State Audit

Scope: state machines for the major resident-facing workflows, verified against
`backend/sims/*/models.py` and `views.py`. Cross-reference `03_CANONICAL_DOMAIN_MODEL_MAP.md` for
the models involved.

## Onboarding / identity creation

```
/users/new (universal creation center, all 4 roles)
  → create_user_with_profile() [sims/users/services.py] inside transaction.atomic()
      creates User + role Profile + AuditLog together
  → must_change_password=True by default
  → first login: must_change_password → forces /change-password
  → missing required profile fields (declared server-side, e.g. via ResidentDocumentRequirement)
      → /complete-profile (dynamically rendered from backend-declared fields)
  → otherwise → role dashboard
```
`/api/auth/me/` (verified route in `sims.users.api_urls`) is the single source of truth for this
state machine, matching CLAUDE.md. No signal-based profile creation found — confirmed via grep for
`post_save` across `sims/users/` (only audit-adjacent signals exist, not identity creation).

## Rotation assignment (`training.RotationAssignment`)

```
draft → submit → HOD/UTRMC approve → active → complete
                → (return, with return_reason)
                → (reject, with reject_reason)
```
Exposed via `sims/training/urls.py`'s `rotations`, `my/rotations/`,
`utrmc/approvals/rotations/`, `supervisor/rotations/pending/` routes (confirmed present). Resident
can submit; HOD-designated supervisor or UTRMC admin can approve/return/reject; no `override_reason`
field exists (confirmed absent repo-wide). Real frontend exists at `/academics/rotation-assignments`
(per web fork, confirmed reachable and in nav).

## Leave requests (`training.LeaveRequest`)

Same draft→submit→approve/return/reject shape as rotations, confirmed by symmetrical model fields
and route structure. Frontend at `/academics/leave-requests`, confirmed in nav by web fork.

## Logbook entry lifecycle — **two parallel implementations, only one is the real product surface**

`academics.LogbookEntry` (the one actually driving the shipped product):
```
DRAFT → SUBMITTED → VERIFIED (supervisor verifies == UI "Approved" per TERMINOLOGY.md)
                   → RETURNED (revision requested)
                   → REJECTED
       (any pre-VERIFIED state) → CANCELLED
```
Actions confirmed by the API contract fork: `submit`, `verify`, `return_revision`, `reject`,
`cancel` — a real, complete workflow with distinct actor permissions (resident submits/cancels;
supervisor verifies/returns/rejects).

`training.LogbookEntry` (parallel, backend-internal-only lifecycle) uses a different status set
including `STATUS_APPROVED` and is written to only by the bulk-import pipeline
(`sims/bulk/services.py`) and read only by milestone-threshold logic
(`sims/training/views.py:_evaluate_logbook_thresholds`) and one legacy dashboard counter
(`sims/users/models.py:get_documents_pending_count`). **These two lifecycles never intersect** — no
code path copies data between them. See `03_CANONICAL_DOMAIN_MODEL_MAP.md` (BE-2) for the full
impact analysis; this is the most significant workflow-correctness finding of this pass.

## Notifications

`NotificationService` (`sims/notifications/services.py`) is confirmed the single construction path
for `Notification` objects — grep across active apps for direct `Notification.objects.create(`
outside `notifications/services.py` found no bypasses using legacy field names (`user=`, `message=`,
`type=`, `related_object_id=`), matching CLAUDE.md's binding rule.

## Legacy server-rendered dashboard views — still live, not the canonical UI

`sims/users/urls.py` mounts a full set of Django-template dashboard views at `/users/dashboard/`,
`/users/supervisor-dashboard/`, `/users/admin-dashboard/`, `/users/resident-dashboard/`
(`sims_project/urls.py:160`, confirmed mounted). These predate the Next.js frontend and are not
linked from it (the Next.js app talks only to `/api/*` routes) — but they are still real, reachable
URLs, still executing real (if partially stale — see BE-2) business logic, not stubs. This is a
architectural leftover worth an explicit decision (retire the routes entirely vs. leave them as an
emergency fallback) rather than indefinite dual-maintenance; filed as BE-3 (P3) in the tech-debt
register — no active harm today since nothing links to them, but they're a maintenance/confusion
surface and, per BE-2, currently produce misleading output if reached directly.

## Backup / disaster recovery workflow

`sims/backup_center/services.py` implements scheduled + on-demand backup creation, Google Drive
upload, and a disaster-recovery path. One real (environment-dependent) test failure was found here
in this pass — see `10_TEST_AND_CI_BASELINE.md` "## Backend Tests & CI" and BE-4 in the tech-debt
register: `create_disaster_recovery_backup()` doesn't ensure its target `backups/` directory exists
before writing, so it fails in any environment where that directory hasn't been pre-created
(observed locally; unknown whether production/CI environments happen to have it — worth confirming).
