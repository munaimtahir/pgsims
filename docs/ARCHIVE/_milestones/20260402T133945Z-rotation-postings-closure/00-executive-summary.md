# Rotation and Postings Closure — Executive Summary

## Starting Point

Recovery had already restored truth alignment and frontend/build baseline, but the active rotation/postings surface was still only partially closed:

- Rotations had strong backend support in `backend/sims/training/views.py` and `backend/sims/training/models.py`, but the frontend only exposed fragments across resident schedule, supervisor dashboard, and UTRMC overview.
- Resident postings UI still depended on incorrect assumptions about draft/delete behavior and did not satisfy the backend create payload contract.
- UTRMC postings UI still treated backend lifecycle statuses as lowercase client-only values, so approval/completion actions were not rendered for real API responses.

## What Was Corrected

- Rotation scope truth was aligned so supervisors can review rotations for directly supervised residents, not only department/HOD scope.
- Returned rotations can now be resubmitted by the resident, matching the active frontend journey.
- Resident schedule now shows real rotation records with return/reject reasons and submit/resubmit actions.
- Supervisor dashboard now includes a real pending rotation review section with approve/return actions.
- UTRMC overview now hosts the active rotation operations surface on the existing route:
  - create draft
  - see submitted/approved/active/returned/rejected/completed queues
  - activate approved rotations
  - complete active rotations
- Resident postings create flow now sends the required `resident_training` field.
- Resident and UTRMC postings pages now use the real uppercase backend status values.
- UTRMC postings explicitly preserves a read-only boundary for `utrmc_user`.

## What Is Now Truly Active

- Rotation workflow on the verified active surface:
  - UTRMC admin creates draft on `/dashboard/utrmc`
  - resident sees and submits from `/dashboard/resident/schedule`
  - supervisor approves from `/dashboard/supervisor`
  - UTRMC admin activates and completes from `/dashboard/utrmc`
- Postings workflow on the verified active surface:
  - resident creates posting request from `/dashboard/resident/postings`
  - UTRMC admin approves and completes from `/dashboard/utrmc/postings`
  - resident sees resulting completed state from `/dashboard/resident/postings`

## What Was Closed in This Pass

- Rotation workflow closure on the existing active routes
- Postings workflow closure on the existing active routes
- Runtime verification coverage for both workflows in the promoted workflow gate

## What Remains Unsafe or Incomplete

- Deferred legacy surfaces remain deferred:
  - logbook
  - cases
  - legacy analytics
- Rotation/postings edge coverage outside the promoted workflow gate remains partial:
  - rejected postings follow-up handling beyond visibility
  - non-seeded multi-resident operational depth
  - wider role-path permutations beyond the verified happy paths

## Milestone Verdict

This milestone is sufficient to upgrade rotations and postings from “active but partial” to “active and verified on the promoted active surface”.

Safe to continue to the next milestone: **Yes**, provided future work keeps legacy deferred surfaces deferred and uses this milestone pack plus `docs/contracts/` as the authority baseline.
