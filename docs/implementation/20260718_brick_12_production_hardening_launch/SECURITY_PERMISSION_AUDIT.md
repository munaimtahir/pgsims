# Security and Permission Audit - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

## Permission Policies Enforced
1. **Anonymous / Public Block**: Anonymous users are blocked by default on all `/api/academics/` routes (including overview metrics, lists, templates, and submissions). Public access is restricted only to `/api/auth/login/` and the `/api/health/` connection status view.
2. **Resident self-scoping**:
   - Residents cannot access the reports listing (`/api/academics/reports/resident-progress/`).
   - Querying a specific resident progress detail endpoint (`/api/academics/reports/resident-progress/<id>/`) checks that the target ID matches the logged-in resident's ID, returning `403 Forbidden` for other residents' profiles.
3. **Supervisor scoped assignments**:
   - Supervisors can only query workload details corresponding to their own profile.
   - Supervisors can only fetch progress report details of residents with active `ResidentSupervisorAssignment` assignments. Accessing other postgraduates returns `403 Forbidden`.
4. **Support Staff restrictions**: Support staff profile access is restricted by default on all spine record and supervision mutations.
5. **No Legacy Regression**: No references to deleted legacy roles (`UTRMC_ADMIN`, `HOD`) are permitted.
