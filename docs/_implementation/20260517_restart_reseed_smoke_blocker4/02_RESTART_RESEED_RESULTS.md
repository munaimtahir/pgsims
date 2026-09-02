# Restart/Reseed Results

## Fresh Start

Commands:

```bash
docker compose --env-file .env -f docker/docker-compose.yml down
docker compose --env-file .env -f docker/docker-compose.yml build backend frontend worker beat
docker compose --env-file .env -f docker/docker-compose.yml up -d
```

Result:

```text
Images built:
- docker-backend
- docker-frontend
- docker-worker
- docker-beat

Services healthy:
- pgsims_backend
- pgsims_frontend
- pgsims_db
- pgsims_redis
```

## Reseed

Command:

```bash
./scripts/e2e_seed.sh
```

Result:

```text
seed_org_data completed.
seed_active_surface_baseline completed successfully.
seed_e2e completed successfully.
E2E cache cleared.
E2E seed completed.
Exit code: 0
```

## Health Checks

Backend:

```bash
curl -fsS http://127.0.0.1:8014/healthz/
```

Result:

```json
{"status": "healthy", "checks": {"database": "ok", "cache": "ok", "celery": "ok"}}
```

Frontend:

```bash
curl -fsS http://127.0.0.1:8082/
```

Result:

```text
frontend_home_ok
```

