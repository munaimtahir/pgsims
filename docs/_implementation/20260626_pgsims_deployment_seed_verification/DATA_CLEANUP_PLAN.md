# Data Cleanup Plan and Result

Date: 2026-06-26

## Backup

- Database type: PostgreSQL 15 container.
- Service/container: `db` / `pgsims_db`
- Backup command:

```bash
docker compose --env-file .env -f docker/docker-compose.yml exec -T db pg_dump -U sims_user sims_db > docs/_implementation/20260626_pgsims_deployment_seed_verification/pre_cleanup_backup.sql
```

- Backup path: `docs/_implementation/20260626_pgsims_deployment_seed_verification/pre_cleanup_backup.sql`
- Backup size: `694K`

## Cleanup Scope

- Preserve master hospital/department/matrix data.
- Do not delete backup/import/audit logic.
- Ensure exactly three active usable accounts:
  - `admin` / `admin`
  - `pgr001` / `pgfmu123`
  - `sup001` / `pgfmu123`
- Link `sup001 -> supervises -> pgr001`.
- Deactivate UTRMC hospital entry if present.

## Actions Taken

- Updated `admin` as active superuser/admin and reset password to `admin`.
- Created/updated `sup001` as active supervisor and reset password to `pgfmu123`.
- Created/updated `pgr001` as active resident and reset password to `pgfmu123`.
- Set `pgr001.supervisor = sup001`.
- Created active `SupervisorResidentLink`: `sup001 -> pgr001`, department `MED`.
- Created active resident profile, staff profile, department memberships, and sample training record.
- Deactivated/archived all other users instead of deleting, to preserve FK/audit integrity.
- Deactivated existing old supervision links; retained them inactive for audit/history context.
- Deactivated UTRMC hospital entry instead of deleting, to preserve hospital-department matrix consistency.
- Other hospitals were preserved.

## Result Evidence

```text
kept_active [('admin', 'admin'), ('pgr001', 'resident'), ('sup001', 'supervisor')]
deactivated_count 26
supervisor_fk True
active_link 33 sup001 pgr001 True
utrmc_action deactivated:4:UTRMC Teaching Hospital
other_hospitals [('AH', 'Allied Hospital', False), ('DHQ', 'DHQ Hospital', False), ('GGH', 'Govt General Hospital Ghulam Muhammadabad', False)]
```

Security note: these are temporary pilot/demo credentials only and must be changed before real production use.

