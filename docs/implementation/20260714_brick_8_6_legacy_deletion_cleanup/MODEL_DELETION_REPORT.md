# Model Deletion Report

- `SupervisorResidentLink` was fully deleted in Brick 8.6.
- Active runtime sync behavior had already been removed and the remaining command/test surfaces were migrated to `ResidentSupervisorAssignment`.
- Django admin registration remains removed.
- Django migration `backend/sims/users/migrations/0009_delete_supervisorresidentlink.py` drops the legacy table.
- Remaining repository references are historical migrations only.
- Final status: deleted.
