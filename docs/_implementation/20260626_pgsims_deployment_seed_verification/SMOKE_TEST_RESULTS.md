# Smoke Test Results

Date: 2026-06-26

## Domain/Page Checks

```text
homepage/domain loads: https://pg.fmu.edu.pk/ -> HTTP/2 200
login page loads: https://pg.fmu.edu.pk/login -> HTTP/2 200
API route/proxy works: https://pg.fmu.edu.pk/api/ -> HTTP/2 401 unauthenticated
static file works: https://pg.fmu.edu.pk/static/admin/css/base.css -> HTTP/2 200
```

Protected route checks, unauthenticated:

```text
/dashboard/utrmc -> 307 /login
/dashboard/utrmc/users -> 307 /login
/dashboard/utrmc/onboarding -> 307 /login
/dashboard/utrmc/supervision -> 307 /login
/dashboard/utrmc/hod -> 307 /login
/dashboard/utrmc/programs -> 307 /login
/dashboard/utrmc/backup -> 307 /login
/dashboard/resident -> 307 /login
/dashboard/supervisor -> 307 /login
```

## Logs

Backend/frontend log scan:

```text
docker compose --env-file .env -f docker/docker-compose.yml logs --tail=300 backend frontend | rg " 500 |ERROR|Traceback|Internal Server Error|CRITICAL"
```

Result: no matching critical 500/error lines found.

## Backend Checks

```text
docker compose --env-file .env -f docker/docker-compose.yml exec -T backend python manage.py check
System check identified no issues (0 silenced).
```

Requested test command:

```text
python manage.py test sims.users.test_userbase_api sims.users.test_resident_onboarding
```

Result: failed because `sims.users.test_resident_onboarding` does not exist as a source file in `backend/sims/users/`; only stale `__pycache__` entries exist.

Focused existing userbase test:

```text
python manage.py test sims.users.test_userbase_api
Found 16 test(s).
Ran 16 tests in 1.824s
OK
```

## Frontend Checks

```text
cd frontend && npm run typecheck
tsc --noEmit --skipLibCheck
```

Result: passed after removing stale local generated `.next` files.

```text
cd frontend && npm test -- --runInBand
Test Suites: 39 passed, 39 total
Tests: 114 passed, 114 total
```

Note: Jest emitted a jsdom navigation not-implemented console error, but the suite passed.

