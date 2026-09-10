# SECURITY AUDIT

## CLASSIFICATION MATRIX

| Security Domain | Method | Status / Comments |
|-----------------|--------|-------------------|
| Authentication | STATICALLY_REVIEWED | Configured securely via DRF SimpleJWT. |
| Authorization | DYNAMICALLY_TESTED | Role constraints enforced correctly via `IsManager` / API endpoints. |
| Object-level authorization (IDOR/BOLA) | DYNAMICALLY_TESTED | Querysets block cross-record data retrieval strictly. |
| Privilege escalation | STATICALLY_REVIEWED | `SelfProfileUpdateSerializer` prevents `role` or `is_staff` modification. |
| CSRF | STATICALLY_REVIEWED | Environment-driven `CSRF_TRUSTED_ORIGINS`, relies on Django default CSRF protection for web-based forms. |
| CORS | STATICALLY_REVIEWED | `CORS_ALLOWED_ORIGINS` accurately reads from ENV, defaulting to safe limits. |
| XSS | STATICALLY_REVIEWED | Relies on React/NextJS auto-escaping frontend constraints, DRF endpoints output unescaped JSON data (standard). |
| SQL injection risk | STATICALLY_REVIEWED | ORM securely parameterizes all standard queries. No raw SQL usage identified. |
| Command injection risk | STATICALLY_REVIEWED | No `os.system` / `subprocess` calls on untrusted inputs found. |
| Unsafe file upload | STATICALLY_REVIEWED | `ResidentDocumentViewSet` correctly restricts upload formats using `ALLOWED_EXTENSIONS`. |
| File download authorization | STATICALLY_REVIEWED | Restricted implicitly by `ResidentDocumentViewSet.retrieve` validating owner. |
| Path traversal | STATICALLY_REVIEWED | Relies on Django's underlying `FileField` protection mechanisms. |
| Secret exposure | STATICALLY_REVIEWED | No exposed keys found in production path logic. Mock keys exist in test setups. |
| Production DEBUG/error exposure | STATICALLY_REVIEWED | Derived correctly by `os.environ.get("DEBUG")`. `DEBUG=False` masks internal exceptions appropriately. |

## Secrets Exposure Details
A static review of the repository found no production secrets hardcoded in the codebase. Keys like database passwords and OAuth client secrets are safely extracted via environment variables in `settings.py` and `services.py`. Some mock secrets were found in test files.

## Network Security (CORS & CSRF)
Cookie security (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) is forced on in production when requested via environment or implicitly driven off the Debug flag.

## Authentication Details
DRF SimpleJWT is used. Refresh tokens are explicitly blacklisted upon logout (`api_views.logout_view`).
