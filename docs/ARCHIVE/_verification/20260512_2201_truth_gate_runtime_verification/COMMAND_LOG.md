# Command Log

## Baseline

- `pwd`
- `git branch --show-current`
- `git status --short`
- `git log -1 --oneline`
- `docker compose -f docker/docker-compose.yml ps`
- `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"`
- `find . -maxdepth 3 -name '.env*' -type f -print`

## Environment

- `docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py shell`

## Runtime restore and seed

- `docker compose -f docker/docker-compose.yml --env-file .env up -d`
- `./scripts/e2e_seed.sh`
- direct `seed_e2e` rerun inside backend container

## Backend

- `docker compose -f docker/docker-compose.yml --env-file .env exec -T backend pytest sims -q`
- `docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py check`
- `docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py makemigrations --check --dry-run`

## Frontend

- `cd frontend && npm test -- --watch=false`
- `cd frontend && npm run lint`
- `cd frontend && npm run typecheck`
- `cd frontend && npm run build`

## E2E

- `cd frontend && E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npm run test:e2e:smoke:local`
- `cd frontend && E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npm run test:e2e:active-surface:local`
- `cd frontend && npm run test:e2e`
- `cd frontend && E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npm run test:e2e:critical`

## Supporting checks

- inspected `frontend/package.json`
- inspected `frontend/playwright.config.ts`
- inspected `scripts/e2e_seed.sh`
- inspected `frontend/e2e/helpers/auth.ts`
- inspected `frontend/app/dashboard/resident/research/page.tsx`
- inspected `frontend/e2e/critical/admin_critical.spec.ts`
- inspected `frontend/e2e/regression/README.md`
