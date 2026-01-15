# SIMS Repository Audit Report

## 1) Executive Summary

### What the app is supposed to be
SIMS is a Django-based “Student (Postgraduate) Information Management System” for postgraduate medical training with role-based access for Admin, Supervisor (Faculty), and Postgraduate (Resident) users. It includes modules for rotations, certificates, logbooks, clinical cases, analytics, attendance, results, notifications, and reports, plus a JWT-backed API. The repository also contains a separate Next.js frontend intended for the same system.

### Current run status (observed)
- **Backend (Django)**: The settings file hard-requires `SECRET_KEY` (no default), which means a plain `python manage.py runserver` will fail unless a `.env` or environment variable is provided. The Docker compose files supply a development key, so Docker-based run should start when the env is configured.
- **Frontend (Next.js)**: The Next app boots, but only includes a landing page, login, register, and a single generic `/dashboard` page. Role-based routes and most of the dashboard navigation links are missing.

### Top 10 blockers (ranked)
1. **Frontend role routes missing**: `/dashboard/admin`, `/dashboard/supervisor`, `/dashboard/student` do not exist, but login redirects to them.
2. **Frontend navigation links point to missing pages**: `/dashboard/logbook`, `/dashboard/results`, `/dashboard/students`, `/dashboard/rotations` are linked but not implemented.
3. **Auth API mismatch (frontend vs backend)**: Frontend expects `/api/auth/me/`, `/api/token/refresh/`, `/api/token/verify/` which do not exist in backend routes.
4. **Register form cannot satisfy backend validation**: Backend registration requires PGs to submit `specialty`, `year`, and `supervisor`; the Next.js register form does not collect `specialty`, `year`, or `supervisor`.
5. **Missing frontend routes for password flows**: `/forgot-password` and `/unauthorized` are referenced but not implemented in the Next app.
6. **Docs claim `/api/schema/` but no schema endpoint is defined in URL routing.**
7. **Two “frontends” are not reconciled**: Django templates implement full role-based UIs while the Next app is skeletal and not integrated into the Django server.
8. **Production env requirements are strict**: `SECRET_KEY` is mandatory; misconfiguration prevents startup.
9. **Role-based authorization gaps in some DRF viewsets**: Many APIs only use `IsAuthenticated` without admin-only enforcement for create/update (e.g., academics/results) which can lead to over-permissive operations.
10. **API documentation vs code drift**: Several routes in docs do not match actual Django URL paths (logbook and rotations API examples differ).

### Fastest path to a stable demo
1. **Run the Django server only** (templates) with minimal env and SQLite for data.
2. **Use the Django role dashboards** (`/users/admin-dashboard/`, `/users/supervisor-dashboard/`, `/users/pg-dashboard/`) and built-in module screens for logbook, rotations, certificates, etc.
3. **Defer Next.js UI** until API contracts and role-based routes are aligned (see phased plan below).

## 2) Repo Map (“Truth Map”)

### Structure overview
- **Backend (Django)**: `sims/` (apps), `sims_project/` (settings, URLs, WSGI), `templates/`, `static/`, `manage.py`, `requirements.txt`.
- **Frontend (Next.js)**: `frontend/` (Next 14 app router), `frontend/app/`, `frontend/components/`, `frontend/lib/api/`.
- **Infrastructure**: `docker-compose*.yml`, `Dockerfile`, `Dockerfile.frontend`, `deployment/`.
- **Docs**: `docs/` with extensive setup and status documentation.

### Tech stack per service
- **Backend**: Python 3.11+, Django 4.2, Django REST Framework, JWT (SimpleJWT), PostgreSQL/SQLite, Redis, Celery.
- **Frontend**: Next.js 14, React 18, Tailwind CSS, React Query, Axios, Zustand.
- **Infra**: Docker, Docker Compose, Gunicorn, WhiteNoise.

### Entry points & env
- **Backend entry**: `manage.py` + `sims_project/settings.py` + `sims_project/urls.py`.
- **Frontend entry**: `frontend/app/page.tsx` for landing, `frontend/app/login/page.tsx`, `frontend/app/register/page.tsx`.
- **Environment**: `.env.example` documents required values (notably `SECRET_KEY`).

## 3) Runbook (from zero to running)

### Backend (Django) – local without Docker
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env to set SECRET_KEY at minimum
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Backend (Django) – local Docker
```bash
docker-compose -f docker-compose.local.yml up -d
# If needed
# docker-compose -f docker-compose.local.yml exec web python manage.py migrate
# docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Set `NEXT_PUBLIC_API_URL=http://localhost:8000` for local API usage.

### Required env vars (minimum)
- `SECRET_KEY` (required to boot Django)
- `DEBUG` (optional)
- DB configuration: either `DATABASE_URL` or `DB_*` set (optional if SQLite)

### Services
- **Database**: PostgreSQL (optional; SQLite default works)
- **Redis**: optional (for caching/Celery)
- **Celery**: optional

### Migrations / seed
- `python manage.py migrate`
- Optional seed: `python manage.py sims_seed_demo`

### Happy path
1. Start backend.
2. Login at `http://localhost:8000/users/login/` (Django template UI).
3. Use dashboards and module menus.

### Common failure points
- Missing `SECRET_KEY` → Django startup error.
- Frontend login redirects to missing Next.js routes.
- Registering PGs via API fails without `specialty`, `year`, and `supervisor`.
- CORS/CSRF misconfiguration if frontend domain not included.

## 4) Role-Based Frontend Audit (High Detail)

### Scope
This section audits the **Next.js frontend** only (separate from Django templates).

### Student (Postgraduate) role
**Existing pages/routes**
- `/` (landing)
- `/login`
- `/register`
- `/dashboard` (generic dashboard with placeholder counts)

**Completeness**
- `/dashboard` is a placeholder (static counts, no API integration).
- No PG-specific pages (`/dashboard/logbook`, `/dashboard/results`) are implemented.

**API calls**
- `POST /api/auth/login/` (login)
- `POST /api/auth/register/` (register)
- `POST /api/auth/logout/` (logout)
- `GET /api/auth/me/` (expected but not implemented in backend)
- `POST /api/token/refresh/` and `POST /api/token/verify/` (expected but not implemented in backend)

**Auth assumptions**
- JWT in `localStorage` with `Authorization: Bearer` header.

**Missing views for usability**
- Student logbook list & entry creation
- Results/scoreboards
- Rotations schedule
- Profile management

**UI/UX gaps**
- Navigation links lead to nonexistent pages.
- No role-specific dashboard or guards beyond client-side checks.

### Faculty (Supervisor) role
**Existing pages/routes**
- None beyond the generic `/dashboard` page.

**Completeness**
- Missing supervisor-specific dashboards and student lists.

**API calls**
- Same auth endpoints as above; no supervisor APIs wired.

**Missing views**
- Supervisor dashboard
- Assigned PG list and progress
- Review queues (logbook/cases/certificates)

**UI/UX gaps**
- Login redirects to `/dashboard/supervisor` which does not exist.

### Admin role
**Existing pages/routes**
- None beyond the generic `/dashboard` page.

**Completeness**
- Missing admin dashboard, user management, system analytics.

**API calls**
- Same auth endpoints; no admin APIs wired.

**Missing views**
- Admin dashboard
- User/role management
- Bulk operations, reports, system settings

**UI/UX gaps**
- Login redirects to `/dashboard/admin` which does not exist.

## 5) Backend Audit

### Auth model & roles
- Custom `User` model with roles: `admin`, `supervisor`, `pg`, plus specialty/year/supervisor relationships.
- Role-based dashboards implemented in Django views and templates.

### Core models/entities (examples)
- **Users**: Custom User with role and supervisor relationships.
- **Rotations**: Hospitals, Departments, Rotations.
- **Logbook**: Procedures, Diagnoses, logbook entries (not fully enumerated here).
- **Certificates**: CertificateType, Certificate.
- **Clinical Cases**: CaseCategory, ClinicalCase.
- **Academics**: Department, Batch, StudentProfile.
- **Results**: Exam, Score.
- **Attendance**: Session, AttendanceRecord, EligibilitySummary.

### API inventory (actual endpoints)
- **Auth**: `/api/auth/login/`, `/api/auth/refresh/`, `/api/auth/logout/`, `/api/auth/register/`, `/api/auth/profile/`, `/api/auth/profile/update/`, `/api/auth/password-reset/`, `/api/auth/password-reset/confirm/`, `/api/auth/change-password/`.
- **Analytics**: `/api/analytics/trends/`, `/api/analytics/comparative/`, `/api/analytics/performance/`, `/api/analytics/dashboard/overview/`, `/api/analytics/dashboard/trends/`, `/api/analytics/dashboard/compliance/`.
- **Audit**: `/api/audit/activity/`, `/api/audit/reports/` (via DRF routers).
- **Search**: `/api/search/`, `/api/search/history/`, `/api/search/suggestions/`.
- **Notifications**: `/api/notifications/`, `/api/notifications/mark-read/`, `/api/notifications/preferences/`, `/api/notifications/unread-count/`.
- **Reports**: `/api/reports/templates/`, `/api/reports/generate/`, `/api/reports/scheduled/`, `/api/reports/scheduled/<id>/`.
- **Bulk**: `/api/bulk/review/`, `/api/bulk/assignment/`, `/api/bulk/import/`, `/api/bulk/import-trainees/`.
- **Attendance**: `/api/attendance/upload/`, `/api/attendance/summary/`.
- **Logbook**: `/api/logbook/pending/`, `/api/logbook/<id>/verify/`.
- **Academics**: `/academics/api/departments/`, `/academics/api/batches/`, `/academics/api/students/`.
- **Results**: `/results/api/exams/`, `/results/api/scores/`.

### Serializers/validation issues
- Registration requires PGs to supply `specialty`, `year`, and `supervisor` (strict validation), but the Next.js registration form omits these fields.

### Permissions & security
- DRF defaults to `IsAuthenticated` for most APIs. Some viewsets allow any authenticated user to create/update resources where admin-only access is typically expected (e.g., academics/results).
- Attendance upload enforces supervisor/admin on upload, but other APIs lack role-based guards.

### Admin panel status
- Django Admin is configured and available at `/admin/`, with customized dashboards and templates.

### Seed/test data
- Demo data command exists: `python manage.py sims_seed_demo`.

## 6) Integration Audit (Frontend <-> Backend)

### Endpoint mismatch table
| Frontend expects | Backend provides | Status |
| --- | --- | --- |
| `POST /api/auth/login/` | `POST /api/auth/login/` | ✅ match |
| `POST /api/auth/register/` | `POST /api/auth/register/` | ✅ match |
| `POST /api/auth/logout/` | `POST /api/auth/logout/` | ✅ match |
| `GET /api/auth/me/` | `GET /api/auth/profile/` | ❌ mismatch |
| `POST /api/token/refresh/` | `POST /api/auth/refresh/` | ❌ mismatch |
| `POST /api/token/verify/` | **No URL defined** | ❌ missing |

### Contract fixes (minimal)
- Update frontend to call `/api/auth/profile/`, `/api/auth/refresh/`.
- Add `/api/token/verify/` in backend or remove frontend verify call.

### CORS/base URL integration
- Frontend uses `NEXT_PUBLIC_API_URL` or auto-detect logic; backend CORS is configured via `CORS_ALLOWED_ORIGINS`.

### File uploads/static
- Backend serves media at `/media/` in debug; static handled by WhiteNoise.

## 7) DevOps / Deployment Audit

### Docker/Compose status
- `docker-compose.yml` runs PostgreSQL, Redis, Django (Gunicorn), Celery worker/beat, and Next.js frontend.
- `docker-compose.local.yml` targets localhost dev and runs Django dev server on 8000 plus Next.js on 3000.

### Reverse proxy
- Deployment docs reference Caddy/Traefik; production compose exposes Django on 8014 and frontend on 8082 for proxying.

### Production readiness gaps
- `SECRET_KEY` is required but not defaulted; missing env prevents startup.
- Security flags are configurable via env, but need explicit production values.

### Logging/visibility
- Logging configured to file and console; logs directory is created automatically.

## 8) Quality & Maintainability Audit

- **Linting/testing**: pytest configured for Django; Jest/Playwright for frontend.
- **Dead code/duplication**: Some API docs and frontend routes appear outdated vs current URL routing.
- **Security**: JWT auth + session auth enabled; role-based checks inconsistent across APIs.
- **Dependencies**: Django pinned to `<5.0`, Next 14.2.33; no lockfile for Python.
- **Performance**: Some dashboards compute stats via repeated queries; caching is optional via Redis but not required.

## 9) Stabilization Plan (Phased)

### Phase 0 – Stable Demo (1–2 days)
- Use Django template UI only.
- Ensure `.env` is present with `SECRET_KEY`.
- Run migrations and seed data.

### Phase 1 – API Contract Alignment (2–4 days)
- Align frontend auth endpoints with backend URLs.
- Add missing `/api/token/verify/` or remove unused verify calls.
- Update Next register form to collect `specialty`, `year`, and `supervisor` or change backend validation policy.

### Phase 2 – Role-Based Next.js UI (1–2 weeks)
- Implement `/dashboard/admin`, `/dashboard/supervisor`, `/dashboard/student` routes.
- Build minimal pages for logbook, results, students, rotations.
- Add `/unauthorized` and `/forgot-password` pages.

### Phase 3 – Hardening & QA (1 week)
- Add role-based permission classes to critical viewsets (academics/results).
- Add tests for API contracts and frontend routing.
- Review CORS/CSRF config for deployment.

## 10) Priority List of Issues & Quick Wins

### Top issues
1. Frontend role routes missing.
2. Frontend ↔ backend auth endpoint mismatch.
3. Registration form missing required fields.
4. Missing role-based pages in Next.js.
5. Docs and routes out of sync.

### Quick wins
- Fix frontend auth endpoint paths.
- Add missing Next.js routes as placeholders (admin/supervisor/student dashboards).
- Add `/unauthorized` and `/forgot-password` pages.
- Update register form to include required PG fields or adjust backend validation.

---

# Appendix: Commands & Traceability

### Inventory commands used
- `ls`
- `find .. -name AGENTS.md -print`
- `rg "urlpatterns|path\(|re_path\(" -n sims sims_project`
- `find frontend/app -maxdepth 3 -type f -name 'page.tsx'`
- `sed -n '1,200p' <file>` on key files

