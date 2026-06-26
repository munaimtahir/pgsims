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
Create a `.env` file in the root directory based on `.env.template` with configuration values:
```ini
DEBUG=False
SECRET_KEY=your-production-django-secret-key
ALLOWED_HOSTS=api.pgsims.alshifalab.pk,pg.fmu.edu.pk,pgsims.alshifalab.pk,localhost,127.0.0.1
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8082,https://pg.fmu.edu.pk,https://pgsims.alshifalab.pk
```

### 2. Launch or Refresh Services
Run the following commands to build and recreate all services in detached mode:
```bash
docker compose -f docker/docker-compose.yml up -d --build --force-recreate
```

### 3. Apply Migrations and Static assets
Run migrations inside the backend container and collect static assets:
```bash
docker compose -f docker/docker-compose.yml exec backend python manage.py migrate
docker compose -f docker/docker-compose.yml exec backend python manage.py collectstatic --noinput
```

### 4. Create Super Admin Account
Initialize the admin credentials:
```bash
docker compose -f docker/docker-compose.yml exec backend python manage.py create_superadmin
```

### 5. Public Proxy Refresh
When code or containers change, refresh the live proxy after the rebuild so the public URL serves the latest container set:
```bash
./ops/deploy_live_update.sh
```
