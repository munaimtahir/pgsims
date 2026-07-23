# Production Settings Review - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

A detailed review of `backend/sims_project/settings.py` was conducted to ensure production hardening rules are met:

## Parameters Reviewed & Validated
1. **DEBUG Mode**: Configured to load from env variables (defaults to `False`). Verified that `DEBUG=True` is restricted to local development/test environments.
2. **Host Constraints**: `ALLOWED_HOSTS` resolves explicit domains and blocks spoofed HTTP host headers.
3. **CORS Rules**: Restricts cross-origin scripts to approved origins (`CORS_ALLOWED_ORIGINS` is loaded dynamically and is not set to `*`).
4. **CSRF Protection**: CSRF trusted origins list resolves explicit domain patterns (`CSRF_TRUSTED_ORIGINS` mapped).
5. **Secure Cookies**: HTTPS secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) are enabled in production compose contexts.
6. **Logging Engine**: Confirms logs are directed to stdout and structured log files under `logs/`, capturing warn/error frames without writing plain credentials or secrets.
