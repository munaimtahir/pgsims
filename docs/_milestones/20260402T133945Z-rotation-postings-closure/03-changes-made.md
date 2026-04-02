# Changes Made

## Backend

- `backend/sims/training/views.py`
  - Introduced shared supervisor/rotation scope helpers.
  - Extended supervisor-visible rotation query scope to direct supervised residents.
  - Allowed resident resubmission of returned rotations.
  - Preserved returned/rejected rotations in resident summary schedule payload.
- `backend/sims/training/tests.py`
  - Added direct-supervisor rotation visibility test.
  - Added supervisor pending rotation coverage test.
  - Added returned-rotation resubmission test.

## Frontend

- `frontend/lib/api/training.ts`
  - Added active rotation and leave client methods/types used by the promoted workflow.
- `frontend/app/dashboard/resident/schedule/page.tsx`
  - Now renders real resident rotations and leave requests.
  - Added resident submit/resubmit actions for rotations and leave submission actions.
  - Added returned/rejected rotation reason visibility.
- `frontend/app/dashboard/supervisor/page.tsx`
  - Added pending rotation section with approve/return actions.
- `frontend/app/dashboard/utrmc/page.tsx`
  - Added active rotation operations surface on the existing route.
- `frontend/app/dashboard/resident/postings/page.tsx`
  - Added `resident_training` payload wiring from resident summary.
  - Removed false draft/delete messaging.
  - Corrected status handling to real uppercase backend values.
- `frontend/app/dashboard/utrmc/postings/page.tsx`
  - Corrected status handling to real uppercase backend values.
  - Preserved read-only `utrmc_user` boundary.
- `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts`
  - Added end-to-end rotation closure coverage.
  - Added end-to-end postings closure coverage.

## Documentation

- `README.md`
- `docs/contracts/API_CONTRACT.md`
- `docs/contracts/ROUTES.md`

These now reflect the active verified rotation/postings surface instead of the previous partial status.
