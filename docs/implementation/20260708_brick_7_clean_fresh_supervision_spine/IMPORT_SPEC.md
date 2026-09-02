# Import Spec

This document describes the supervision import surface for Brick 7.

## Scope

The supervision import endpoint is the canonical bulk entry point for mapping residents to supervisors.

## API

- `POST /api/supervision/import/`
- Supports dry-run and commit flows.
- Accepts supervision assignment rows with:
  - resident identifier
  - supervisor identifier
  - assignment type
  - start date
  - optional notes

## Behavior

1. Validate each row.
2. Enforce the same hospital and department match rules used by manual assignment creation.
3. Reject duplicate active assignments.
4. Reject a second active primary supervisor for the same resident.
5. In dry-run mode, return successes and failures without persisting.
6. In commit mode, persist valid rows and emit audit events.

## Notes

- This import surface belongs to the new `sims.supervision` app.
- Legacy supervision-link CSV imports still exist elsewhere in the codebase for backward compatibility, but they are not the Brick 7 supervision spine.
