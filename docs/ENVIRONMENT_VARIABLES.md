# PGMS Environment Variables Reference Guide

The following environment variables configure the PGMS / PGR SIMS clean-room postgraduate medical education management system.

## Core Django Configuration
- `SECRET_KEY`: Production-strength cryptographically secure key used for signing sessions and tokens.
- `DEBUG`: Set to `False` in production (e.g. `DEBUG=False`).
- `ALLOWED_HOSTS`: Comma-separated list of host/domain names that this Django site can serve (e.g. `ALLOWED_HOSTS=pg.fmu.edu.pk,localhost`).
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins for unsafe HTTP requests (e.g. `CSRF_TRUSTED_ORIGINS=https://pg.fmu.edu.pk`).

## Database Connectivity
- `DATABASE_URL`: Full PostgreSQL database connection string (e.g. `postgresql://sims_user:password@db:5432/sims_db`).
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Individual database connection settings (fallback/override).

## Frontend & CORS
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins for cross-origin AJAX queries (e.g. `CORS_ALLOWED_ORIGINS=https://pg.fmu.edu.pk`).
- `FRONTEND_PUBLIC_API_URL`: Root path or host for API calls made by Next.js components.

## Operational & Media Settings
- `STATIC_ROOT`: Path where collection of static files is stored (e.g. `/app/staticfiles`).
- `MEDIA_ROOT`: Path to media file uploads (e.g. `/app/media`).
- `BACKUP_DIR`: Directory where PostgreSQL timestamped SQL dumps are saved (defaults to `/home/munaim/srv/apps/pgsims/backend/backups`).
- `LOG_LEVEL`: Default stdout logging levels (e.g. `INFO` or `WARNING`).
