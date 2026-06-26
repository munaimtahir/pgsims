# Fix Log

## Backend

- Added user account actions on the backend:
  - reset password to `pgfmu123`
  - deactivate
  - archive/delete alias
- Added user filtering by supervisor and programme.
- Kept user archive behavior safe by preferring soft-deactivate/archive instead of hard delete.
- Ensured resident training records expose a proper CRUD surface for programme assignment.

## Frontend

- Reworked the UTRMC dashboard into a monitoring page.
- Added the resident programme assignment page and nav link.
- Expanded the Users page with:
  - role filter
  - department filter
  - active status filter
  - supervisor filter
  - programme filter
  - reset password action
  - deactivate action
  - delete/archive action
- Updated Supervision Links:
  - department selector
  - backend validation feedback
  - robust supervisor/resident name fallback
- Updated HOD Assignments:
  - candidate pool excludes admin users
  - backend validation feedback is shown
  - empty state for no eligible candidates

## Contracts

- Updated route and API contracts to match the new visible workflow:
  - users actions
  - resident training CRUD
  - resident programme assignment route

## Tests

- Added and updated backend tests for:
  - user filters
  - reset password
  - deactivate
  - archive
- Added and updated frontend tests for:
  - dashboard monitoring view
  - users page filters and row actions
  - supervision link creation
  - HOD assignment creation
  - resident programme assignment CRUD
  - sidebar link visibility
