# PGSIMS Operations Guide

This document defines standard procedures for administrative operations, data backups, and routine maintenance of the PGSIMS application.

## 1. Backups (Recommended)

PGSIMS supports **application data backups** via the Backup Center:
- **Regular System Backup** (`.pgsimsbak`): database + uploaded files + manifest + integrity checks
- **Full Server Recovery Backup** (`.pgsimsdr`): routine backup bundle plus recovery notes (no unencrypted secrets)

### UI
- Navigate to `/dashboard/utrmc/backup`

### CLI
```bash
cd backend
python3 manage.py create_system_backup --routine
python3 manage.py create_system_backup --disaster
python3 manage.py validate_system_backup /path/to/backup.pgsimsbak
python3 manage.py restore_system_backup /path/to/backup.pgsimsbak --dry-run
```

See `docs/BACKUP_AND_RESTORE.md` for operator workflow and restore safety rules.

## 2. Inspecting Logs
- **Django Logs**: `docker compose logs backend`
- **Celery Worker Logs**: `docker compose logs worker`
- **Frontend Logs**: `docker compose logs frontend`
- **Error Log File**: Located inside the container at `/app/logs/sims_error.log` (persistent on host if configured).

## 3. Reseed Baseline Command
To seed clean initial lookup values:
```bash
docker compose -f docker/docker-compose.yml exec backend python manage.py initialize_pgsims_baseline
```
