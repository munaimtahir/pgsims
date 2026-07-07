# Onboarding Completion Rules — Update 0

## Rule System
Onboarding is verified on every login request.

### Redirection Hierarchy:
1. If `must_change_password` is `True`, redirect the user to `/change-password`.
2. If there are missing fields returned by `get_missing_profile_fields()`, redirect the user to `/complete-profile`.
3. If both of the above checks pass, redirect the user to their dashboard:
   - `ADMIN` -> `/dashboard/utrmc`
   - `RESIDENT` -> `/dashboard/resident`
   - `SUPERVISOR` -> `/dashboard/supervisor`
   - `SUPPORT_STAFF` -> `/dashboard/utrmc` (or scope dashboard)
