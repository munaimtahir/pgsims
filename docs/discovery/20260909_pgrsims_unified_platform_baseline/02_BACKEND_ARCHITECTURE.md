# 02 — Backend Architecture

## Framework and stack

Verified against `backend/requirements.txt` and `backend/sims_project/settings.py`:

```
Framework:        Django >=4.2,<5.0
API framework:     Django REST Framework >=3.14, drf-spectacular (OpenAPI schema at /api/schema/)
Auth:               djangorestframework-simplejwt >=5.3 (JWT) + SessionAuthentication as fallback
                     (settings.py:292-296) — token blacklist app installed for logout revocation
DB:                 PostgreSQL (psycopg2-binary), via django.contrib.postgres
Cache/broker:       django-redis, celery >=5.3, django-celery-beat (periodic tasks)
Audit:              django-simple-history >=3.5 (do not remove — CLAUDE.md binding rule)
CORS:                django-cors-headers, explicit allow-list (not wildcard) — see
                     `11_SECURITY_RBAC_REVIEW.md`
Static:              whitenoise
Import/export:       django-import-export (bulk app)
```

`AUTH_USER_MODEL = "users.User"` (custom user model, `sims/users/models.py`).

## Installed apps (verified `sims_project/settings.py:67-99`)

```
Active SIMS apps:
  sims.users
  sims.academics
  sims.rotations
  sims.audit
  sims.bulk
  sims.notifications
  sims.training
  sims.supervision
  sims.backup_center (via BackupCenterConfig)
```
This matches CLAUDE.md's documented active-app list exactly — no drift found here. `sims/_legacy/`
(`cases`, `certificates`, `logbook`, `search`, `analytics`, `attendance`, `reports`, `results`) is
confirmed **not** in `INSTALLED_APPS` — CLAUDE.md's claim is current and accurate.

## REST framework defaults (settings.py:290-310)

```python
DEFAULT_AUTHENTICATION_CLASSES = [JWTAuthentication, SessionAuthentication]
DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]   # secure-by-default; no endpoint is open unless
                                                   # explicitly overridden
DEFAULT_PAGINATION_CLASS = PageNumberPagination (PAGE_SIZE=25, env-overridable)
DEFAULT_FILTER_BACKENDS = [DjangoFilterBackend, SearchFilter, OrderingFilter]
DEFAULT_THROTTLE_CLASSES = [AnonRateThrottle, UserRateThrottle]
```
Sound, secure-by-default configuration — no P0/P1 architecture concerns here.

## Service layer pattern

Business logic is deliberately kept out of views/serializers and centralized in per-app
`services.py` modules (`sims/users/services.py`, `sims/academics/services.py`,
`sims/bulk/services.py`, `sims/backup_center/services.py`, `sims/rotations/services.py`,
`sims/supervision/services.py`). The canonical example, matching CLAUDE.md's binding rule, is
`create_user_with_profile(...)` in `sims/users/services.py`, which creates User + role-specific
profile + AuditLog together inside `transaction.atomic()` — confirmed present and is the only
identity-creation path referenced from `sims/users/onboarding_api.py` and the admin identity-center
views. No `post_save` signal is used for profile creation (grep for `post_save` in
`sims/users/` finds only audit/history-adjacent signals in `sims/audit/signals.py` and
`sims/training/signals.py`, not profile creation).

## URL architecture (verified `sims_project/urls.py`)

```
/users/                    → sims.users.urls (legacy server-rendered Django template views —
                              login, dashboards, admin-dashboard; still mounted and reachable,
                              NOT the canonical UI, see 04_BACKEND_WORKFLOW_AUDIT.md)
/cases/, /logbook/,
/certificates/             → sims.users.*_dummy_urls (explicitly named "dummy" — placeholder
                              redirects for the retired legacy PG/Supervisor/Admin model, not real
                              functionality)
/api/                       → sims.users.userbase_urls (org-graph: departments, hospitals, etc.)
/api/users/                 → sims.users.api_user_urls
/api/auth/                  → sims.users.api_urls (JWT login/refresh/me)
/api/                       → sims.training.urls (rotations, leave, logbook via training app,
                              workshops, research — see 03/04)
/api/academics/              → sims.academics.workflow_urls (NOT sims.academics.urls — see
                              resolution note below)
/api/audit/, /api/bulk/,
/api/notifications/,
/api/supervision/,
/api/backup_center/          → one file per app, matches CLAUDE.md's "one API-client file per
                              backend app" convention on the frontend side
/api/dashboard/resident/     → standalone APIView, not app-namespaced
/api/schema/                 → drf-spectacular OpenAPI schema
```

**Resolved: the web-fork-flagged "`sims/academics/` has no `urls.py`" question.** It does have a
`urls.py`, but that file is **deliberately unmounted** — `sims_project/urls.py:174-180` mounts
`sims.academics.workflow_urls` instead, with an inline comment explaining that `sims.academics.urls`
was "a second, unreachable 'masters' API onto the same canonical Department/Hospital/TrainingProgram
models already served at `api/hospitals/`, `api/departments/`, etc via `sims.users.userbase_urls`" and
was intentionally removed 2026-07-24 (`docs/truth-map/FRONTEND_BACKEND_TRUTH_MAP.md §7.3`, referenced
in the comment — not independently verified in this pass but the code-level intent is unambiguous).
**Not a defect** — this is resolved, documented-in-code architecture, not an oversight.

## Deployment structure

Docker Compose based (`docker/docker-compose.yml`, `.prod.yml`, `.local.yml` per root `CLAUDE.md`),
fronted by a host Caddy reverse proxy in production (confirmed live in `09_PRODUCTION_BASELINE.md`).
`SECRET_KEY` is required at import time (`settings.py:41`, `RuntimeError` if unset) — fails hard
rather than silently defaulting, good practice, confirmed by this pass's own local-check setup
needing an explicit `SECRET_KEY` env var to even run `manage.py check`.

## Local system checks (this pass, via a throwaway venv — no repo/CI config changed)

```
$ pip install -r backend/requirements.txt         → clean install, no conflicts
$ DJANGO_SETTINGS_MODULE=sims_project.settings_test python manage.py check
  → System check identified no issues (0 silenced)
$ python manage.py makemigrations --check --dry-run
  → No changes detected
```
No local Postgres was stood up for this check (not required for `check`/`makemigrations --check`,
which operate against code/migration state, not a live DB). See `10_TEST_AND_CI_BASELINE.md` for the
full pytest run, which does exercise a real (SQLite/test) database per `settings_test.py`.

## Doc-drift note

`pytest.ini`'s actual `addopts` (verified by reading the file directly) is:
```
--verbose --tb=short --disable-warnings --ignore=sims/_legacy --ignore=sims/cases/tests.py
--ignore=sims/certificates/tests.py --ignore=sims/logbook/tests.py
--cov=sims --cov-report=term-missing:skip-covered --cov-fail-under=70
```
Root `CLAUDE.md` states `pytest.ini` carries **no** coverage flags and that only `pyproject.toml`
enforces `--cov-fail-under=80`, framing the two configs as disagreeing on whether coverage is
enforced at all. That is stale: `pytest.ini` (the one that actually wins, confirmed by this pass's
test run using it automatically) already enforces coverage itself, just at a lower bar (70, not 80).
Low-priority (P3) doc correction — filed in `12_BUG_TECH_DEBT_REGISTER.md` "## Backend".
