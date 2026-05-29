# PGSIMS Operations Guide

This document defines standard procedures for administrative operations, data backups, and routine maintenance of the PGSIMS application.

## 1. Database Backups

### Automated Backups
Database backups are configured in settings under `SIMS_SETTINGS["BACKUP_LOCATION"]` (defaulting to the `backups/` directory relative to project root).

### Manual Backup (CLI)
To perform a manual hot backup of the PostgreSQL database:
```bash
docker compose -f docker/docker-compose.yml exec -T db pg_dump -U sims_user sims_db > backups/db_backup_$(date +%F).sql
```

### Restoration from Backup
To restore a database dump:
1. Re-initialize a blank database:
   ```bash
   docker compose -f docker/docker-compose.yml exec -T db dropdb -U sims_user sims_db
   docker compose -f docker/docker-compose.yml exec -T db createdb -U sims_user sims_db
   ```
2. Inject the SQL file:
   ```bash
   docker compose -f docker/docker-compose.yml exec -T db psql -U sims_user sims_db < backups/db_backup.sql
   ```

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
