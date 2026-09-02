# RBAC Proof

## Requirements
- Super Admin only: connect/disconnect/folder/upload/verify/download/restore-ready
- UTRMC Admin: no Drive management actions unless explicitly allowed (default deny)
- Restricted roles: no Drive controls (existing Backup Center policy applies)

## Status
- Backend endpoints are guarded by `IsSuperAdmin` (superuser) for all Drive management operations.
- Callback endpoint is unauthenticated but requires a valid signed+cached OAuth state tied to a user id.
