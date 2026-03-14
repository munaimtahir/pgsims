# E2E Run Log

## 1) Runtime status check

```bash
cd /home/munaim/srv/apps/pgsims
docker compose -f docker/docker-compose.yml ps
```

Observed:
- `pgsims_backend` healthy on `127.0.0.1:8014`
- `pgsims_frontend` healthy on `127.0.0.1:8082`
- db/redis/worker/beat up

## 2) Health probes

```bash
curl -sS -o /dev/null -w 'backend_health:%{http_code}\n' http://127.0.0.1:8014/healthz/
curl -sS -o /dev/null -w 'frontend_login:%{http_code}\n' http://127.0.0.1:8082/login
```

Observed:
- `backend_health:200`
- `frontend_login:200`

## 3) Seed deterministic smoke users/data

```bash
docker compose -f docker/docker-compose.yml exec -T backend python manage.py seed_e2e
```

Observed:
- `seed_e2e completed successfully.`

## 4) Canonical local smoke run

```bash
cd frontend
npm run test:e2e:smoke:local -- --reporter=list
```

Observed:
- `17 passed`

## 5) Default smoke command determinism check

```bash
cd frontend
npm run test:e2e:smoke -- --reporter=line
```

Observed:
- `17 passed`
- Confirms updated defaults remove prior auth/env ambiguity for local baseline.
