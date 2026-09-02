# Audit Log Verification - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

The PGMS system implements a dedicated database audit trail using the `ActivityLog` (or `django-simple-history` where configured).

## Auditable Actions Verified
1. **User Accounts**: Logs user creation (`USER_CREATED`), edits, and password updates.
2. **Supervision Spine**: Logs creation, updates, and terminations of assignments (`SUPERVISION_ASSIGNED`, `SUPERVISION_ENDED`).
3. **Training Records**: Logs initialization and closure of resident training records.
4. **Evaluation Workflows**: Logs submissions, reviews, revisions, approvals, and rejections.
5. **Logbooks & Procedures**: Logs clinical entries, verifications, and comment additions.

## Audit Command
To inspect recent audit activities via CLI, run:
```bash
python manage.py check --deploy
```
Or query `/api/audit/logs/` (requires Admin permissions).
