# Runtime Bringup

## Docker Status
`docker compose -f docker/docker-compose.yml --env-file .env ps` showed:
- `pgsims_db`: healthy
- `pgsims_redis`: healthy
- `pgsims_backend`: healthy before restart; health starting immediately after controlled restart
- `pgsims_frontend`: healthy
- worker/beat: running

## Curl Evidence
Stored at `OUT/prod_gate_artifacts/20260421T233708Z/curl/runtime_health_and_same_origin.txt`.

Observed:
- `GET http://127.0.0.1:8014/health/` -> `200 OK`
- `GET http://127.0.0.1:8014/healthz/` -> `200 OK`, database/cache/celery ok
- `GET http://127.0.0.1:8082/login` -> `200 OK`
- `GET http://127.0.0.1:8082/api/auth/profile/` -> backend `401 Unauthorized`, proving same-origin proxy reaches backend

## Logs
Backend/frontend log tail captured at `OUT/prod_gate_artifacts/20260421T233708Z/logs/docker_backend_frontend_tail.log`.

