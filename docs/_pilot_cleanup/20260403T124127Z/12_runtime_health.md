# Runtime Health

Current compose service state:

| Service | Status | Notes |
| --- | --- | --- |
| `pgsims_backend` | healthy | bound to `127.0.0.1:8014` |
| `pgsims_frontend` | healthy | bound to `127.0.0.1:8082` |
| `pgsims_db` | healthy | postgres 15 |
| `pgsims_redis` | healthy | redis 7 |
| `pgsims_worker` | running | celery worker |
| `pgsims_beat` | running | celery beat |

Backend health:

```json
{"status": "healthy", "checks": {"database": "ok", "cache": "ok", "celery": "ok"}}
```

Frontend health:
- Root page returned HTTP `200`

Admin auth verification:
- `admin` login: `True`
- Current total user count: `1`

Important runtime caution:
- Email backend in the live container is still `django.core.mail.backends.console.EmailBackend`.
- That is acceptable for technical verification, but real outbound email workflows are not production-ready until email settings are configured.

