# Env Fixes

File changed:

- `.env`

## Added Local Runtime Values

- `DB_NAME=sims_db`
- `DB_USER=sims_user`
- Localhost and `127.0.0.1` entries for `CSRF_TRUSTED_ORIGINS`
- Localhost and `127.0.0.1` entries for `CORS_ALLOWED_ORIGINS`
- `SESSION_COOKIE_SECURE=False`
- `CSRF_COOKIE_SECURE=False`
- `USE_PROXY_HEADERS=False`
- `LOGIN_RATE_LIMIT=30/min`

## Why

The Docker compose workflow uses `--env-file .env`. These values prevent local HTTP runtime, login, seed, and browser smoke tests from being blocked by production-oriented defaults.

