# Seed and Reset Policy - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

To protect production data and define how setup and demo environments operate, the following policies are set:

## Seed & Setup Commands
1. **seed_pilot_masters**: Idempotent. Inserts departments, hospitals, and rotation templates. Can be executed safely on initial deployment.
2. **seed_pilot_supervision**: Connects initial supervision assignments. Must not be executed in production after manual roster creation starts.
3. **seed_pilot_academics**: Configures default training records and academic sessions. Restricted to test environments.
4. **seed_pilot_academic_workflows**: Seeds dummy evaluations and logbooks. **Forbidden in production**.

## Reset Operations
- **`reset_demo_data` command**: Cleans up pilot test logs. Safe flags (`--dry-run` and `--confirm`) are enforced to avoid accidental execution on live servers.
- **Migration Policy**: Seed commands are isolated from migrations and must never run automatically as part of `python manage.py migrate`. They must only be invoked explicitly via the CLI.
