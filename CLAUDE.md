# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PGSIMS (also called PGMS / PGR SIMS) is a Django + Next.js monorepo managing postgraduate medical
training at UTRMC: residents, supervisors, rotations, academic workflows, and administration.

**Read `AGENTS.md` before making any code, migration, frontend, backend, documentation, or test
changes.** It is the binding operating-rules file for this repo (an equivalent but older document,
`GEMINI.md`, covers the same ground for Gemini-based agents — treat `AGENTS.md` as authoritative).
`docs/CANONICAL_SOURCE_OF_TRUTH.md` is a short, current summary of roles, identity creation, and
canonical models/routes — check it when unsure whether something is still current.

**`README.md` and `docs/PROD_GATE_CLOSURE/` are largely historical.** They describe an earlier
"PG/Supervisor/Admin" role model and a since-superseded gate-closure sprint. The codebase has since
been rebuilt on a clean-room 4-role model (see below) and current work proceeds through numbered
"bricks" tracked under `docs/implementation/` and validated by `scripts/check_brick_*.sh`. When
README/docs conflict with what you find in `backend/sims/users/models.py` or `AGENTS.md`, trust the
code and `AGENTS.md`.

## Architecture

### Monorepo layout

```
backend/          Django REST API (Python 3.11+, Django 4.2)
  sims/            Active app modules (see below)
  sims/_legacy/    Deleted/deferred modules kept for reference only — NOT in INSTALLED_APPS
  sims_project/    Settings, urls, celery, wsgi/asgi, middleware
frontend/          Next.js 14 (App Router), TypeScript, Tailwind, React Query, Zustand
docs/              Documentation; docs/contracts/ is the authoritative integration spec
docs/implementation/  Per-"brick" delivery docs (DISCOVERY/DECISION_LOCK/CHANGES/TEST_RESULTS/FINAL_VERDICT)
scripts/           Gate-check scripts, backup/restore, local dev helpers
docker/            Compose files (docker-compose.yml, .prod.yml, .local.yml)
deploy/            Caddy config for the canonical production deployment path
```

### Active backend apps (`backend/sims/`)

`users`, `academics`, `rotations`, `audit`, `bulk`, `notifications`, `training`, `supervision`,
`backup_center` — these are the apps actually wired into `INSTALLED_APPS`
(`backend/sims_project/settings.py`). `sims/_legacy/` still contains `cases`, `certificates`,
`logbook`, `search`, `analytics`, `attendance`, `reports`, `results` — these are **not installed**
and are not part of the active surface; don't build on them without explicit instruction to revive
that brick.

### Roles and identity (clean-room model — current)

Only four roles exist: `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`
(`backend/sims/users/models.py`). Do not reintroduce legacy roles (`UTRMC_ADMIN`, `HOD`, `TEACHER`,
`STUDENT`, `PGR`, `TRAINEE`, `CLERK`, etc.) in backend choices, frontend dropdowns, fixtures, or docs.

- `/users/new` is the **universal identity creation center** for all four roles — there is no
  separate creation flow per role.
- User + role-specific profile (`AdminProfile` / `ResidentProfile` / `SupervisorProfile` /
  `SupportStaffProfile`) + `AuditLog` are created together via
  `create_user_with_profile(...)` in `backend/sims/users/services.py`, inside
  `transaction.atomic()`. Do not create profiles via implicit `post_save` signals.
- HOD is not a role/model/route — at most `SupervisorProfile.designation == "HOD"`.
- Login/onboarding state machine: `must_change_password` → `/change-password`; missing required
  profile fields → `/complete-profile` (dynamically rendered from backend-declared fields, not
  hardcoded); otherwise → dashboard. `/api/auth/me/` is the source of truth for this state.
- `scripts/check_update_0_identity_cleanup.sh` and `manage.py repair_identity_profiles` guard this
  model — rerun them after touching identity/profile code.

Full detail on the identity model, profile schema versioning, audit action names, and required
tests lives in `AGENTS.md` sections 4–20 — read it directly rather than relying on this summary for
anything nontrivial in that area.

### Canonical domain models — do not duplicate

- Exactly one `Department` model: `sims.academics.Department`.
- Exactly one `Hospital` model: `sims.rotations.Hospital`, linked to departments via
  `sims.rotations.HospitalDepartment` (a hospital ↔ department matrix, not a duplicate Department
  model). Never create things like `RotationDepartment` or `AcademicDepartment`.
- A resident's stable affiliation is `User.home_department` / `User.home_hospital`. Rotations to a
  different hospital require either an unavailable destination department at the home hospital, or
  an `override_reason` + UTRMC admin approval via the rotation's approve endpoint.
- Notifications always go through `NotificationService` (`backend/sims/notifications/services.py`)
  using the canonical field names `recipient`, `verb`, `body`, `metadata`. Never construct
  `Notification` objects with legacy keys (`user=`, `message=`, `type=`, `related_object_id=`).
- Audit trail relies on `django-simple-history` — don't remove it, and don't mutate
  approved/verified records outside the normal write path (that bypasses history).

### Contract-first integration

Backend↔frontend integration is driven by `docs/contracts/`:
`API_CONTRACT.md`, `DATA_MODEL.md`, `RBAC_MATRIX.md`, `ROUTES.md`, `TERMINOLOGY.md`,
`INTEGRATION_TRUTH_MAP.md`, `TRUTH_TESTS.md`. If a code change alters a payload shape, route, or
user-facing term, update the relevant contract file **in the same change** — don't ship silent
drift. `ROUTES.md` and `TERMINOLOGY.md` are frozen once pilot begins; changing them needs an
explicit version bump.

Status terminology differs between backend and UI, e.g. backend `pending` displays as "Submitted" in
the UI, and `supervisor_feedback` is aliased to `feedback` — see `docs/TERMINOLOGY.md`.

### Frontend structure

`frontend/app/` (Next.js App Router) is organized by top-level route family matching the canonical
routes in `docs/CANONICAL_SOURCE_OF_TRUTH.md`: `/users`, `/residents`, `/supervisors`,
`/support-staff`, `/admins`, `/masters`, `/supervision`, `/academics`, `/dashboard/{utrmc,resident,supervisor}`,
`/complete-profile`, `/change-password`. API client code lives in `frontend/lib/api/` (one file per
backend app, e.g. `academics.ts`, `supervision.ts`, `userbase.ts`), auth/session helpers in
`frontend/lib/auth/`, and RBAC-driven nav/route guarding in `frontend/lib/rbac.ts` and
`frontend/lib/navRegistry.ts`.

## Commands

### Backend (run from `backend/`)

```bash
python manage.py runserver 0.0.0.0:8000     # dev server
python manage.py migrate                     # apply migrations
python manage.py makemigrations              # create migrations
python manage.py makemigrations --check --dry-run   # verify no missing migrations
python manage.py check                       # system checks
python manage.py shell
python manage.py repair_identity_profiles    # identity/profile integrity repair

black sims/ --line-length 100                # format
flake8 sims/ --count --statistics            # lint (max-line-length=100, ignores E501/W503/E203)

pytest sims -v                               # run all backend tests
pytest sims/users/ -v                        # run one app's tests
pytest sims/academics/tests.py::SomeTestCase::test_name -v   # run a single test
```

Backend has **two pytest configs that disagree** — `backend/pytest.ini` (used automatically; sets
`DJANGO_SETTINGS_MODULE=sims_project.settings_test` and `--ignore=sims/_legacy
--ignore=sims/cases/tests.py --ignore=sims/certificates/tests.py --ignore=sims/logbook/tests.py`)
takes precedence over `backend/pyproject.toml`'s `[tool.pytest.ini_options]` (which points at
`sims_project.settings` and adds coverage flags with `--cov-fail-under=80`) because pytest prefers
`pytest.ini` when both exist. If coverage numbers look unexpectedly absent, that's why — pass
`-c pyproject.toml` or the explicit `--cov` flags if you need the coverage-enforcing config.

### Frontend (run from `frontend/`)

```bash
npm run dev                 # dev server
npm run build                # production build
npm run lint                 # ESLint
npm run typecheck            # tsc --noEmit --skipLibCheck
npm test                     # Jest unit tests
npm test -- path/to/file.test.ts   # single Jest test file
npm run test:coverage

npm run test:e2e:smoke:local       # Playwright smoke, against local servers (ports below)
npm run test:e2e:critical          # setup + critical projects
npm run test:e2e:regression        # setup + critical + workflows + negative + rbac
npm run test:e2e:full               # every Playwright project
```

Local E2E runs point at `E2E_BASE_URL=http://127.0.0.1:8082` (frontend) and
`E2E_API_URL=http://127.0.0.1:8014` (backend) — matching the Caddy-fronted local ports, not the raw
dev-server ports.

### Docker / gates / project-wide

```bash
docker compose -f docker/docker-compose.yml --env-file .env up -d   # local stack (or: make up)
docker compose -f docker/docker-compose.yml exec backend python manage.py migrate   # (or: make migrate)
make dev / make test / make up / make down / make logs / make shell / make seed / make build

bash scripts/check_all_pgms_gates.sh          # run every brick/identity/legacy gate check in sequence
bash scripts/check_brick_9_10_academic_workflows.sh
bash scripts/check_brick_11_dashboards_reports_monitoring.sh
bash scripts/check_brick_12_production_hardening.sh
bash scripts/check_pgms_health.sh
```

Production deploys via Docker Compose (`docker/docker-compose.prod.yml`) + a host Caddy reverse
proxy synced by `ops/caddy_sync_reload.sh`; see `docs/ARCHIVE/deploy/CADDY_ROUTINE.md` for the full
routine. Docker runtime needs `docker compose --env-file .env ...` — without it, backend startup
fails with a missing `SECRET_KEY` error, because the root `.env` isn't picked up implicitly by all
compose invocations.

## Definition of done (from `AGENTS.md` / copilot governance rules)

A task is complete only when: relevant tests pass, `docs/contracts/` is updated if the change
touches integration, no forbidden pattern is introduced (duplicate Department/Hospital models,
legacy notification keys, legacy roles, unauthorized route/terminology changes), and the work is
documented (brick work under `docs/implementation/<date>_brick_.../`, other work under
`docs/_audit/`).
