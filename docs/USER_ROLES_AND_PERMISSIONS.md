# PGSIMS User Roles and Permissions

This document outlines the Role-Based Access Control (RBAC) matrix for PGSIMS, matching the
current clean-room identity model (`AGENTS.md`, `docs/CANONICAL_SOURCE_OF_TRUTH.md`,
`backend/sims/users/models.py`).

**Superseded note**: an earlier version of this document described a seven-role model (Super
Admin, UTRMC Admin, UTRMC User/Viewer, HOD, Supervisor/Faculty, Resident/PG, Data Entry/Clerk).
That model no longer exists in the code — `AGENTS.md` explicitly forbids reintroducing HOD,
CLERK/DATA_ENTRY, or a separate super-admin/UTRMC-admin split as roles. If you find other docs or
code still describing that model, treat it as stale and flag it the same way.

## Roles

Exactly four roles exist:

1. **`ADMIN`** — full system access: manage hospitals/departments/matrix, onboard all account
   types, assign supervisors, run bulk imports, approve inter-hospital rotation overrides.
2. **`SUPERVISOR`** — reviews and approves logbook entries and evaluations for assigned residents;
   `SupervisorProfile.designation` can hold a free-text value like `"HOD"`, but that is a display
   label only, not a distinct role, permission tier, or route.
3. **`RESIDENT`** — submits logbook entries and evaluations, views own training record, rotation
   placements, and progress/eligibility status.
4. **`SUPPORT_STAFF`** — restricted, mostly read-only access; profile completion and limited
   operational support only. Does not create or mutate users, masters data, or academic records.

## Permissions & Scope Matrix

| Action | Admin | Supervisor | Resident | Support Staff |
| :--- | :---: | :---: | :---: | :---: |
| Create any account (`/users/new`) | Yes | No | No | No |
| Manage hospitals/departments/matrix/programs (`/masters`) | Yes | No | No | No |
| Bulk import rosters | Yes | No | No | No |
| Assign resident↔supervisor links | Yes | No | No | No |
| Create rotation placements | Yes | No | No (view own only) | No |
| Approve inter-hospital rotation overrides | Yes | No | No | No |
| Submit logbook entries / evaluations | No | No | Yes (own) | No |
| Review/approve/return logbook entries & evaluations | No | Yes (assigned residents) | No | No |
| View dashboards & reports (own scope) | Yes (all) | Yes (assigned residents) | Yes (own) | Limited |
| Backup/restore | Yes | No | No | No |

All of the above is enforced server-side (see `backend/sims/common_permissions.py` and each app's
`permissions.py`) — frontend route guarding (`frontend/lib/rbac.ts`) is a UX convenience, not the
security boundary.
