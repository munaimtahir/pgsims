# Runbook (Truth Map)

## Local Development Setup

### 1. Backend (Django)
- **Root**: `backend/`
- **Environment**: Python 3.11+
- **Steps**:
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver
  ```
- **Port**: 8000
- **Required Env Vars**:
  - `SECRET_KEY`
  - `DEBUG=True`
  - `DATABASE_URL` (or `DB_*` vars)
  - `REDIS_URL`
- **Default Credentials**: `admin` / `admin123` (Dev only)

### 2. Frontend (Next.js)
- **Root**: `frontend/`
- **Steps**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
- **Port**: 3000
- **Required Env Vars**:
  - `NEXT_PUBLIC_API_URL=http://localhost:8000` (in `.env.local`)

### 3. Background Workers
- **Steps**:
  ```bash
  celery -A sims_project worker -l info
  celery -A sims_project beat -l info
  ```

## Docker Management (Monorepo)
The root contains a `Makefile` and `docker/` folder.
- **Start All**: `make up` (uses `docker/docker-compose.yml`)
- **Stop All**: `make down`
- **Seed Data**: `make seed`
- **Migrations**: `make migrate`

## Missing Configs
- **Env Template**: No `.env.example` found at the root (though mentioned in README).
- **SSL**: No local SSL setup (standard for dev).

## Known Unknowns
- Compatibility with Node.js version (likely 18+ or 20+).

## Immediate Next Actions
1. Create a root `.env.example` covering both Backend and Frontend needs.
2. Verify `make seed` works without existing data.
