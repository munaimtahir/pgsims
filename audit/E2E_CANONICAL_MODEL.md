# Canonical Local E2E Model

## Objective

Define one deterministic local model for browser smoke verification.

## Runtime model (canonical)

### Backend runtime

- Service: Docker `backend`
- URL: `http://127.0.0.1:8014`
- Start command:
  ```bash
  docker compose -f docker/docker-compose.yml --env-file .env up -d db redis backend
  ```
- Health check:
  ```bash
  curl -sSf http://127.0.0.1:8014/healthz/
  ```

### Frontend runtime

- Service: Docker `frontend`
- URL: `http://127.0.0.1:8082`
- Start command:
  ```bash
  docker compose -f docker/docker-compose.yml --env-file .env up -d frontend
  ```
- Health check:
  ```bash
  curl -sSf http://127.0.0.1:8082/login
  ```

## Auth/data fixtures (deterministic)

- Seed command:
  ```bash
  docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
  ```
- Command is idempotent (`update_or_create`) and establishes canonical smoke users:
  - `e2e_utrmc_admin / UtrmcAdmin123!`
  - `e2e_utrmc_user / Utrmc123!`
  - `e2e_admin / Admin123!`
  - `e2e_supervisor / Supervisor123!`
  - `e2e_pg / Pg123456!`

## Playwright contract for canonical local smoke

- `E2E_BASE_URL` default: `http://127.0.0.1:8082`
- `E2E_API_URL` default: `http://127.0.0.1:8014`
- `loginAs()` helper no longer uses `localhost:8000` fallback.

## Canonical smoke scope

Keep smoke minimal and meaningful:

- public pages + auth redirect guards
- login form success/invalid flows (real UI login)
- dashboard reachability for seeded roles (UTRMC admin, supervisor, PG)

## Canonical run command

```bash
cd frontend && npm run test:e2e:smoke:local
```

This is the repo-standard browser smoke baseline for local reproducibility.
