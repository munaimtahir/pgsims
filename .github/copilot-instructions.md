# PGSIMS Copilot Instructions

PGSIMS is a Django + Next.js monorepo for managing postgraduate medical training at UTRMC.

## Critical Governance Rules

**Read `AGENTS.md` before making ANY changes.** Key rules:

1. **Contract-First (Non-Negotiable)**: Backend ↔ Frontend integration MUST be driven by `docs/contracts/`. If code changes require contract changes, update contracts in the same run. No "quick fixes" that silently change payload shapes.

2. **Frozen UX Rule**: Do NOT change route structure, navigation labels, or terminology once pilot begins. Changes require explicit approval and version bump in `docs/contracts/ROUTES.md` and `docs/contracts/TERMINOLOGY.md`.

3. **Canonical Data Model (Critical)**: 
   - There is exactly ONE canonical Department entity (`academics.Department`)
   - There is exactly ONE canonical Hospital entity (`rotations.Hospital`)
   - A hospital hosts departments via `HospitalDepartment` matrix table
   - Do NOT create duplicate Department models (e.g., "RotationDepartment", "AcademicDepartment")

4. **Audit Integrity**: All state transitions must be auditable. Do not remove `django-simple-history`. Never silently mutate approved/verified records.

5. **Notifications**: Must use canonical schema: `recipient`, `verb`, `body`, `metadata`. Do not use legacy keys (`user`, `message`, `type`, `related_object_id`). Use `NotificationService` helper (`sims/notifications/services.py`).

6. **Definition of Done**: A task is complete only when:
   - Relevant tests pass
   - Contracts updated (if applicable)
   - No drift introduced (scan forbidden patterns)
   - Work documented under `docs/_audit/`

## Build, Test, and Lint Commands

### Backend (Django)

```bash
# Local development
cd backend && python manage.py runserver 0.0.0.0:8000
# Or: make dev

# Run all tests with coverage
cd backend && pytest sims --cov=sims --cov-report=html --cov-report=term-missing -v
# Or: make test

# Run specific test
cd backend && pytest sims/logbook/test_api.py::PGLogbookEntryAPITests::test_submit_return_feedback_visible_and_resubmit_approve_flow -v

# Run tests for specific app
cd backend && pytest sims/users/ -v

# Format with Black
cd backend && black sims/ --line-length 100

# Lint with Flake8
cd backend && flake8 sims/ --count --statistics

# Database migrations
cd backend && python manage.py migrate
cd backend && python manage.py makemigrations

# Django shell
cd backend && python manage.py shell

# Seed demo data
cd backend && python manage.py sims_seed_demo

# Custom management commands
cd backend && python manage.py create_superadmin
cd backend && python manage.py import_trainees <csv_file>
```

**Truth Tests** (must always pass): See `docs/contracts/TRUTH_TESTS.md`
- Phase 1 Gate: `test_submit_return_feedback_visible_and_resubmit_approve_flow`
- Run drift gate checks for forbidden patterns (duplicate Department models, legacy Notification keys)

### Frontend (Next.js)

```bash
# Development server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Start production server
cd frontend && npm start

# Lint
cd frontend && npm run lint

# Unit tests
cd frontend && npm test
cd frontend && npm run test:watch
cd frontend && npm run test:coverage

# E2E tests (Playwright)
cd frontend && npm run test:e2e
```

### Docker

```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d
# Or: make up

# View logs
docker compose -f docker/docker-compose.yml logs -f
# Or: make logs

# Run migrations in container
docker compose -f docker/docker-compose.yml exec backend python manage.py migrate
# Or: make migrate

# Stop all services
docker compose -f docker/docker-compose.yml down
# Or: make down

# Build images
docker compose -f docker/docker-compose.yml build --no-cache
# Or: make build
```

## Architecture Overview

### Monorepo Structure

```
pgsims/
├── backend/            # Django REST API (Python 3.11+, Django 4.2)
│   ├── sims/           # Core app modules (users, logbook, rotations, etc.)
│   ├── sims_project/   # Project config (settings, urls, celery)
│   └── manage.py
├── frontend/           # Next.js 14 frontend (TypeScript, Tailwind, React Query)
│   ├── app/            # Next.js App Router
│   ├── components/     # React components
│   └── lib/            # Utilities and API client
├── docs/               # Consolidated documentation
│   └── contracts/      # Contract-first integration specs (authoritative)
├── docker/             # Docker Compose configurations
└── scripts/            # Maintenance and demo data utilities
```

### Backend Architecture

**Django App Structure**:
- `sims/users/` - User management and authentication (JWT via `djangorestframework-simplejwt`)
- `sims/logbook/` - Digital logbook entries with supervisor review workflow
- `sims/rotations/` - Rotation management with inter-hospital policy validation
- `sims/academics/` - Canonical Department model and academic configurations
- `sims/certificates/` - Certificate tracking
- `sims/cases/` - Clinical case submissions
- `sims/notifications/` - Notification delivery via `NotificationService`
- `sims/analytics/` - Statistics and reporting
- `sims/search/` - Global cross-module search
- `sims/audit/` - Activity logging and audit trail
- `sims/domain/` - Business rules and validators (`domain/validators.py`)

**Key Patterns**:
- **Contract-driven APIs**: All backend ↔ frontend integration specs live in `docs/contracts/API_CONTRACT.md`
- **Role-based access control**: Defined in `docs/contracts/RBAC_MATRIX.md`. Roles: `pg`, `supervisor`, `admin`, `utrmc_user`, `utrmc_admin`
- **Supervisor scope**: Option A (supervisees-only) - supervisors only see records for assigned PGs
- **Audit trail**: Uses `django-simple-history` for automatic historical tracking
- **Background tasks**: Celery with Redis broker for async operations
- **NotificationService**: Centralized notification helper at `sims/notifications/services.py`

**Status Terminology** (see `docs/TERMINOLOGY.md`):
- Backend status `pending` → UI displays "Submitted"
- `supervisor_feedback` → UI alias `feedback`
- Status flow: `draft` → `pending` (UI: Submitted) → `returned`/`rejected`/`approved`

### Frontend Architecture

**Tech Stack**:
- Next.js 14 with App Router
- TypeScript with strict mode
- Tailwind CSS for styling
- React Query (`@tanstack/react-query`) for server state
- Zustand for client state
- Axios for API client
- Playwright for E2E tests

**Key Patterns**:
- API client configuration in `lib/`
- Route structure locked per `docs/contracts/ROUTES.md`
- UI terminology locked per `docs/contracts/TERMINOLOGY.md`
- Components organized by feature/module

## Contract-First Integration

**Authoritative sources** (always check these first):
- `docs/contracts/API_CONTRACT.md` - API payload shapes and endpoints
- `docs/contracts/DATA_MODEL.md` - Canonical entity definitions and relationships
- `docs/contracts/RBAC_MATRIX.md` - Authorization rules per role
- `docs/contracts/ROUTES.md` - Frontend route structure (frozen after pilot)
- `docs/contracts/TERMINOLOGY.md` - User-facing terms (frozen after pilot)
- `docs/contracts/INTEGRATION_TRUTH_MAP.md` - Integration checkpoints
- `docs/contracts/TRUTH_TESTS.md` - Gate tests that must always pass

**Integration workflow**:
1. Check contract docs BEFORE changing backend/frontend integration
2. If code change requires contract change, update contract in same run
3. Update both backend implementation AND frontend client/types
4. Run truth tests to verify gates pass
5. Document changes in `docs/_audit/`

## Key Conventions

### Department/Hospital Canonical Model

**Critical**: There is ONE canonical Department model and ONE canonical Hospital model.

```python
# ✅ CORRECT - Use canonical models
from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment

# Create rotation with canonical entities
rotation = Rotation.objects.create(
    pg=user,
    department=department,      # FK to academics.Department
    hospital=hospital,          # FK to rotations.Hospital
    start_date=start,
    end_date=end
)

# ❌ FORBIDDEN - Do NOT create duplicate Department models
class RotationDepartment(models.Model):  # NEVER DO THIS
    name = models.CharField(...)
```

**Trainee home affiliation** (stable until graduation):
- `User.home_department` (FK to `academics.Department`)
- `User.home_hospital` (FK to `rotations.Hospital`)

**Inter-hospital rotation policy**:
- If `rotation.hospital != user.home_hospital`:
  - Allowed if destination department NOT available in home hospital (missing `HospitalDepartment` row), OR
  - Requires `override_reason` + approval by `utrmc_admin`
- If `rotation.department == user.home_department` AND `rotation.hospital != user.home_hospital`:
  - Always requires override + approval (rare exception)

### Notification Pattern

Always use `NotificationService` for consistency:

```python
# ✅ CORRECT - Use NotificationService
from sims.notifications.services import NotificationService

service = NotificationService(actor=supervisor)
service.send(
    recipient=pg_user,
    verb="returned_logbook_entry",
    title="Logbook Entry Returned",
    template="notifications/logbook_returned.html",
    context={"entry": entry, "feedback": feedback},
    channels=[Notification.CHANNEL_IN_APP, Notification.CHANNEL_EMAIL]
)

# ❌ FORBIDDEN - Do NOT use legacy keys
Notification.objects.create(
    user=recipient,                    # WRONG - use 'recipient'
    message="...",                     # WRONG - use 'body'
    type="info",                       # WRONG - use 'verb'
    related_object_id=entry.id         # WRONG - use 'metadata'
)
```

### Edit Permissions by Status

**Logbook entries**:
- PG can edit only when status in `draft`, `returned`
- Supervisors verify via `PATCH /api/logbook/<id>/verify/` with payload: `action` (`approved`/`returned`/`rejected`), `feedback`

**Rotations**:
- UTRMC admins approve overrides via `PATCH /api/rotations/<id>/utrmc-approve/`

### Test Organization

- Backend: Tests live in each app's `tests.py` or `test_*.py` files
- Use pytest with Django plugin (`pytest-django`)
- Test settings: `sims_project/settings_test.py`
- Fixtures in `sims/conftest.py` and per-app `conftest.py`
- Coverage target: 80% (see `pyproject.toml`)
- Ignored test files in pytest config: `sims/cases/tests.py`, `sims/certificates/tests.py`, `sims/logbook/tests.py` (legacy - use `test_*.py` pattern)

### Code Quality Standards

**Backend**:
- Black formatter: 100 character line length
- Flake8 linter: max-line-length=100, ignore E501/W503/E203
- Python 3.11+ features allowed
- Django 4.2 patterns

**Frontend**:
- ESLint with Next.js config
- TypeScript strict mode
- Tailwind CSS for styling
- Prefer server components where appropriate

## Environment Configuration

- Backend: `.env` file at project root (see `.env.example`)
- Frontend: `.env.local` in `frontend/` directory (see `.env.local.example`)
- Docker: Environment-specific compose files in `docker/`
- Localhost templates: `.env.localhost`, `frontend/.env.localhost`
- VPS templates: `.env.vps`, `frontend/.env.vps`

**Key env vars**:
- `SECRET_KEY` - Django secret (required for production)
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Comma-separated hostnames
- `DATABASE_URL` - PostgreSQL connection (format: `postgresql://user:pass@host:port/db`)
- `REDIS_URL` - Redis connection for cache
- `CELERY_BROKER_URL` - Celery broker (Redis)
- `CORS_ALLOWED_ORIGINS` - Frontend origins for CORS

## Celery Background Tasks

**Worker**: Processes async tasks
```bash
cd backend && celery -A sims_project worker -l info
```

**Beat**: Scheduled task scheduler
```bash
cd backend && celery -A sims_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

**Configuration**: `sims_project/celery.py`

## Deployment

**Production deployment**: See `docs/DEPLOY_COOLIFY_TRAEFIK.md` for recommended Coolify/Traefik setup

**Docker services**:
- `db` - PostgreSQL database
- `redis` - Redis cache and message broker
- `backend` - Django app (Gunicorn)
- `worker` - Celery worker
- `beat` - Celery beat scheduler
- `nginx` - Reverse proxy (or omit for Coolify/Traefik)

**Health checks**: All services include health checks. Check status: `docker compose ps`

## Documentation

Start with `docs/README.md` for index of all guides.

**Key references**:
- `docs/PROJECT_STRUCTURE.md` - Directory layout
- `docs/FEATURES_STATUS.md` - Feature completeness tracking
- `docs/SYSTEM_STATUS.md` - System health tracking
- `docs/TROUBLESHOOTING.md` - Common issues and remediation

**Contract specs** (authoritative):
- `docs/contracts/` - All integration contracts
- `docs/_audit/` - Work documentation (add here after completing tasks)

## Forbidden Patterns

Scanner should fail if these appear:

1. **Duplicate Department models**: e.g., `RotationDepartment`, `AcademicDepartment`
2. **Legacy Notification keys**: `user=`, `message=`, `type=`, `related_object_id=`
3. **Breaking API payloads without updating contracts**
4. **Direct DB edits for state changes** (bypass audit trail)
5. **UX changes without updating** `docs/contracts/ROUTES.md` or `docs/contracts/TERMINOLOGY.md`

## Phase Gates

**Current status**: Production-ready for pilot deployment (90% complete)

**Must-pass tests** (from `docs/contracts/TRUTH_TESTS.md`):
- Phase 1 Gate: `sims.logbook.test_api.PGLogbookEntryAPITests.test_submit_return_feedback_visible_and_resubmit_approve_flow`
- Migration Gate: Department/Hospital/Rotation creation with policy validation
- Drift Gate: No forbidden patterns appear

Run gates before considering any phase "done".
