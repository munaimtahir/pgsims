# Decision Lock - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

## Architecture Decisions Locked
1. **API Health endpoint**: Registered on the `/api/health/` path, checks active connection status of PostgreSQL database and returns json meta stats.
2. **Hardened environment configuration**:
   - `DEBUG` is set strictly to `False` in production context.
   - `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` are loaded explicitly from the environment.
3. **Command safety**:
   - Seed operations are idempotent.
   - `reset_demo_data` command is shielded with validation checks, dry-run flags, and prevents deletion of master metadata during production setup.
4. **Scoping security boundaries**:
   - Residents are restricted to self-profile scopes on evaluations, logbooks, progress summaries, and CSV reports.
   - Supervisors can only query or reviews items of postgraduate assignments corresponding to active `ResidentSupervisorAssignment` links.
   - Support staff is restricted from Mutating academic/supervision spine setups by default.
5. **Database dumps**: Executable backup, restore, and verify scripts created under `scripts/` using RFC standard checksum file assertions.
