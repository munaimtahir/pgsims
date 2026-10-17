# PGSIMS Deployment Guide

PGSIMS runs inside isolated Docker containers managed via Docker Compose.

## Container Architecture
- `db`: PostgreSQL 15 database instance.
- `redis`: Redis cache and Celery broker.
- `backend`: Django REST API service.
- `worker`: Celery worker for processing background jobs.
- `beat`: Celery beat for scheduling periodic actions.
- `frontend`: Next.js frontend client.

## Standard Deployment Steps

### 1. Configure Environment File
Create a root `.env` file with the required runtime values. Use that file explicitly in compose commands so `SECRET_KEY` and `DB_PASSWORD` are always resolved:
```ini
DEBUG=False
SECRET_KEY=your-production-django-secret-key
ALLOWED_HOSTS=api.pgsims.alshifalab.pk,pg.vexel.pk,pgsims.alshifalab.pk,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://pg.vexel.pk,https://pgsims.alshifalab.pk
NEXT_PUBLIC_API_URL=/api
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=strong-db-password
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8082,https://pg.vexel.pk,https://pgsims.alshifalab.pk
```

### 2. Launch Services
Run the following command to build and run all services in detached mode:
```bash
docker compose --env-file .env -f docker/docker-compose.prod.yml up -d --build
```

### 3. Apply Migrations and Static assets
Run migrations inside the backend container and collect static assets:
```bash
docker compose --env-file .env -f docker/docker-compose.prod.yml exec backend python manage.py migrate
docker compose --env-file .env -f docker/docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

### 4. Existing production identities
Do not seed users or reset credentials during a redeployment. Manage identities
through the existing ADMIN account and universal identity service.

## Shared reverse proxy and domain verification

Canonical production address: **https://pg.vexel.pk** (changed 2026-10-17).
Use project `docker` for the existing production stack. Rebuild affected services
with `docker compose -p docker --env-file .env -f docker/docker-compose.prod.yml build
backend worker beat frontend`, then use `up -d --no-deps backend worker beat frontend`.
Preserve database and Redis volumes. The relative frontend `/api` setting avoids
embedding a deployment hostname in browser bundles.

Run `bash ops/caddy_sync_reload.sh` after reviewing `deploy/Caddyfile.pgsims`.
It replaces only the PGSIMS block in the maintained shared Caddyfile, validates
before installation, keeps backups and restores them if reload fails. Do not
copy the standalone site file over `/etc/caddy/Caddyfile`.
The canonical block sends `/healthz/`, `/api/`, `/admin/`, and protected `/media/`
to Django; the frontend uses port 8082 and Django uses port 8014.

Verify HTTPS certificate validity, `/login`, `/healthz/` (including database),
`/api/auth/me/` (401 without credentials), and frontend/static assets. Inspect
container health and logs, and verify existing alternative hostnames. Consult
`docs/implementation/20261017_domain_migration/REPORT.md` for migration evidence.
