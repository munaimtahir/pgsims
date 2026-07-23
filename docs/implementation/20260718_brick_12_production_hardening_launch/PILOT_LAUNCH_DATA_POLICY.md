# Pilot Launch Data Policy - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

This document outlines the data policy for first-stage pilot deployments:

## Data Reset Timeline
1. **Pre-Pilot Cleanse**: Before releasing login accounts to actual postgraduate residents and supervisor faculty, run:
   ```bash
   python manage.py reset_demo_data --confirm
   ```
   *Note: This removes all test/demo submissions and entries while retaining baseline master configurations.*
2. **Initial Bootstrap**: Create initial real data objects in the following order:
   - First Admin user (using `createsuperuser` command).
   - Core Masters (Hospitals, Departments) via `/masters`.
   - Supervisor Profiles via `/users/new` (setting Designation / designation text).
   - Resident Profiles via `/users/new` (linking them to their respective programs).
   - Supervision Assignment links.
   - Academic training spine records.

## Production Safety Constraints
- Do not run `seed_pilot_academics` or `seed_pilot_academic_workflows` on the pilot server after actual data entry begins.
- Take a database backup before making structural program configurations.
- Verify connections using `scripts/check_pgms_health.sh` periodically.
