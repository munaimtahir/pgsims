# Logging and Error Handling - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

## Error Handling Design
1. **Frontend User Feedback**:
   - API call failures are captured by axio intercepts and displayed to the user using toast messages or error layouts instead of crash screens.
   - Route guards automatically catch invalid tokens and redirect to `/unauthorized` or `/login`.
2. **Backend Integrity**:
   - Validation failures (e.g. overlapping rotations, duplicate primary supervisors) raise explicit `ValidationError` responses.
   - DRF transforms these validation errors into structured JSON response messages.

## Logging Guidelines
- **Sensitive information**: Secrets, database passwords, user plain text passwords, and auth tokens are stripped from logs.
- **Audit Trails**: Security audits are routed to the `ActivityLog` model (covered in `sims/audit/` endpoints) detailing user, timestamp, actions, IP addresses, and payload state metadata.
