# 10 Runtime Health

## Compose Status

All services up:

- `pgsims_backend` (healthy)
- `pgsims_frontend` (healthy)
- `pgsims_db` (healthy)
- `pgsims_redis` (healthy)
- `pgsims_worker` (up)
- `pgsims_beat` (up)

## Endpoint Health

- Backend health endpoint:
  - `GET http://127.0.0.1:8014/healthz/`
  - response: healthy with database/cache/celery checks
- Frontend HTTP status:
  - `GET http://127.0.0.1:8082`
  - `HTTP/1.1 200 OK`

## Runtime/Env Verification

- Backend container env confirms:
  - non-debug mode (`DEBUG=False`)
  - expected `DATABASE_URL` to postgres `sims_db`
  - expected host/origin/trusted-origin values
  - expected Redis/Celery broker settings

