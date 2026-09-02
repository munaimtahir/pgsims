# Project Structure and Architecture

## Architecture overview

- **Repository type**: monorepo (`backend/`, `frontend/`, `docker/`, `docs/`).
- **Backend**: Django 4.2 + DRF + JWT + Celery (`backend/requirements.txt`, `backend/sims_project/settings.py`).
- **Frontend**: Next.js 14 App Router + TypeScript + Zustand + React Query (`frontend/package.json`).
- **Database**: PostgreSQL in Docker; SQLite fallback in settings if DB env not supplied (`settings.py`).
- **Cache/queue**: Redis + Celery worker/beat (`docker-compose*.yml`).
- **Auth**: `rest_framework_simplejwt`, token refresh interceptors on frontend.
- **Deployment stack**: Docker Compose + reverse proxy docs (Caddy routine), services: `db redis backend frontend worker beat`.

## Repository layout (high-level)

- `backend/sims/` active apps: `users`, `academics`, `rotations`, `training`, `notifications`, `audit`, `bulk`.
- `backend/sims/_legacy/` modules still present: `logbook`, `cases`, `analytics`, `attendance`, `reports`, `results`, `search`, `certificates`.
- `frontend/app/` route groups: `/dashboard/{pg,resident,supervisor,utrmc}`, `/login`, `/forgot-password`, `/register`.
- `frontend/lib/api/`: `auth`, `userbase`, `training`, `users`, `notifications`, `bulk`, `audit`.
- `docs/contracts/`: API, RBAC, routes, terminology, truth tests.
- `docs/integration/`: additional truthmap/mismatch docs (non-contract namespace).

## Main route/module inventory

Backend root URL wiring (`backend/sims_project/urls.py`):

- Included: `api/auth`, `api/* userbase`, `api/users/*`, `api/* training`, `api/audit`, `api/bulk`, `api/notifications`.
- Not included: `_legacy/logbook/api_urls.py` in active URL tree.

Frontend App Router pages found:

- Present: resident research/progress/thesis/workshops/schedule/postings; supervisor home/research approvals/progress details; UTRMC hospitals/departments/matrix/users/supervision/hod/programs/postings/eligibility.
- Missing vs common contract/test references: `dashboard/pg/logbook`, `dashboard/supervisor/logbooks`, and other legacy-like pages.

## Tooling summary

- Backend tests: `pytest` with `pytest-django`; `_legacy` ignored in `backend/pytest.ini`.
- Frontend tests: Jest + Playwright multi-project.
- Build: `next build` (observed long/hanging trace finalization in this run).
- Package managers: `pip`, `npm`.
