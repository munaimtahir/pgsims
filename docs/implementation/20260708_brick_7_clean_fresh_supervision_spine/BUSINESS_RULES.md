# Business Rules

This document summarizes the Brick 7 supervision rules.

## Core Rules

1. A resident can have only one active primary supervisor.
2. Co-supervisors are allowed.
3. Resident and supervisor profiles must match on hospital and department.
4. Assignments are soft-ended, not hard deleted.
5. Assignment creation and termination must be audited.

## Role Rules

- `ADMIN` can create and manage supervision assignments.
- `SUPERVISOR` can read assigned supervision data.
- `RESIDENT` can read own supervision data.
- `SUPPORT_STAFF` can read supervision data where permitted by the API policy.

## Change Primary

Changing a primary supervisor must:

1. End the current active primary assignment.
2. Create the new primary assignment atomically.
3. Preserve audit history.

## Validation

- Reject incomplete profiles.
- Reject duplicate active assignments.
- Reject invalid end-date combinations.
- Reject mismatched hospital or department links.
