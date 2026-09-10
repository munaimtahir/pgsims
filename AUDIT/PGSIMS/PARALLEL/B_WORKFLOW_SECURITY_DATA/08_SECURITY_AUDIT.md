# SECURITY AUDIT

## Secrets Exposure
A static review (grep/rg) of the repository found no production secrets hardcoded in the codebase. Keys like `SECRET_KEY`, `DATABASE_URL`, and OAuth client secrets are correctly loaded from environment variables in `settings.py` and `services.py`. Some secrets were found statically in test files (e.g. `test-secret`).

## Network Security (CORS & CSRF)
* `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` are dynamically loaded from environment variables in production.
* If `DEBUG=False` and the environment variables are empty, the lists explicitly default to empty (`[]`), ensuring secure-by-default behavior in production environments.
* Cookie security (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) is forced on in production when requested via environment or implicitly driven off the Debug flag.

## Authentication
DRF SimpleJWT is used. Refresh tokens are explicitly blacklisted upon logout (`api_views.logout_view`).
