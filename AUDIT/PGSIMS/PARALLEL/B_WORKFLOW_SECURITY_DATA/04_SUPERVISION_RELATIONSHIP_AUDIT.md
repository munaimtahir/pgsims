# SUPERVISION RELATIONSHIP AUDIT

The Resident-Supervisor relationship governs a vast majority of the access in PGSIMS.

### Implementation details:
* Handled canonically by `sims.supervision.models.ResidentSupervisorAssignment`.
* Database-level uniqueness constraints prevent a resident from having more than one `PRIMARY` active supervisor simultaneously.
* An attempt to create a duplicate active `PRIMARY` assignment dynamically raised a PostgreSQL `IntegrityError` in test scripts, proving the constraint works properly.

### Legacy Overlaps
* The `User` model still contains a `supervisor` foreign key. While primarily deprecated, some legacy permissions (`sims/common_permissions.py`) occasionally check `user.id == obj.pg.supervisor_id`.
* **Risk:** None currently, as new endpoints rely purely on the modern `ResidentSupervisorAssignment`.
