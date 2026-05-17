# Local Env And Runtime Fix

## Problem

Local backend commands failed before schema generation:

```text
RuntimeError: SECRET_KEY environment variable is required
sqlite3.OperationalError: no such table: users_user
```

A separate runtime warning appeared because `backend/logs/sims_error.log` is owned by another OS user and is not writable by the current user.

## Fix

Created gitignored local file:

- `backend/.env`

Added local-only values:

- `SECRET_KEY`: generated local development secret.
- `DEBUG=True`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `USE_PROXY_HEADERS=False`
- `SECURE_SSL_REDIRECT=False`
- `SESSION_COOKIE_SECURE=False`
- `CSRF_COOKIE_SECURE=False`
- `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`
- `CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache`
- `LOGIN_RATE_LIMIT=30/min`
- `ENABLE_FILE_LOGGING=False`

`ENABLE_FILE_LOGGING=False` avoids the unwritable local log artifact without changing production settings.

## Migration Result

Command:

```bash
cd backend && python3 manage.py migrate --noinput
```

Result:

```text
Applied all migrations for academics, admin, audit, auth, bulk, contenttypes,
django_celery_beat, notifications, rotations, sessions, training, and users.
Exit code: 0
```

