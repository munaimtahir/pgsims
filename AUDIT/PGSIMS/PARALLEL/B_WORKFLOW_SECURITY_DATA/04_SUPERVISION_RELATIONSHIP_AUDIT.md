# SUPERVISION RELATIONSHIP AUDIT

The Resident-Supervisor relationship governs a vast majority of the access in PGSIMS.

### Implementation details:
* Handled canonically by `sims.supervision.models.ResidentSupervisorAssignment`.
* Database-level uniqueness constraints prevent a resident from having more than one `PRIMARY` active supervisor simultaneously.
* An attempt to create a duplicate active `PRIMARY` assignment dynamically raised a PostgreSQL `IntegrityError` in test scripts, proving the constraint works properly.

### Legacy Overlaps & Residual Risk
* The `User` model still contains a `supervisor` foreign key.
* While primarily deprecated, some legacy permissions (`sims/common_permissions.py`) occasionally check `user.id == obj.pg.supervisor_id`.
* **Residual Risk:** If a user assignment is updated via the canonical `ResidentSupervisorAssignment` but the legacy `User.supervisor` field is not synchronized or cleansed, legacy views (like `CanVerifyLogbookEntry`) may still use the stale legacy field to evaluate authorization logic. This leaves a minor discrepancy window where authorization logic relies on technical debt instead of the current state of truth.
* **Mitigation / Next Step:** The application should deprecate the `User.supervisor` field and refactor all references in `common_permissions.py` to utilize `ResidentSupervisorAssignment` directly.
