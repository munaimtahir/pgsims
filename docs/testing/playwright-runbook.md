# PGSIMS Playwright Runbook

## Prerequisites

- Docker + Docker Compose installed
- `make` available (or run docker compose directly)
- Node.js 18+ for generating reports locally

## 1. Start the Application

```bash
# From repo root
docker compose -f docker/docker-compose.yml --env-file .env up -d

# Verify all services are healthy
docker compose -f docker/docker-compose.yml ps

# Check app is up
curl -sk https://pgsims.alshifalab.pk/login | grep -o 'PGSIMS'
```

## 2. Seed E2E Test Data

```bash
# Seed the 5 E2E role users + UTRMC hospital + departments + rotations
docker compose -f docker/docker-compose.yml exec backend \
  python manage.py seed_e2e

# (Optional) Seed full urology demo scenario
docker compose -f docker/docker-compose.yml exec backend \
  python manage.py seed_demo_data
```

## 3. Run the Suite

### Smoke only (fast, 17 tests, ~1 min)
```bash
cd frontend
npm run test:e2e:smoke
```

### Auth / Session tests
```bash
cd frontend
npm run test:e2e:auth
```

### RBAC / Access Control
```bash
cd frontend
npm run test:e2e:rbac
```

### Navigation
```bash
cd frontend
npm run test:e2e:navigation
```

### Dashboard pages
```bash
cd frontend
npm run test:e2e:dashboard
```

### Workflow tests
```bash
cd frontend
npm run test:e2e:workflows
```

### Negative / Validation
```bash
cd frontend
npm run test:e2e:negative
```

### Full regression suite (everything except smoke)
```bash
cd frontend
npm run test:e2e:regression
```

### All suites
```bash
cd frontend
npm run test:e2e:full
```

## 4. Headed / Debug Mode (local machine with display)

```bash
cd frontend
npm run test:e2e:headed         # Runs with visible browser
npm run test:e2e:ui             # Interactive Playwright UI
npm run test:e2e:debug          # Step-through debugger
```

## 5. Server Environment (no display) — Docker Execution

On the production server, run via the official Playwright Docker image which
includes all browser dependencies:

```bash
cd /srv/apps/pgsims

# Single suite
docker run --rm -it \
  -v "$(pwd)/frontend:/app" \
  -w /app \
  -e E2E_BASE_URL=https://pgsims.alshifalab.pk \
  mcr.microsoft.com/playwright:v1.56.1-jammy \
  npx playwright test --project=smoke

# All suites
docker run --rm -it \
  -v "$(pwd)/frontend:/app" \
  -w /app \
  -e E2E_BASE_URL=https://pgsims.alshifalab.pk \
  mcr.microsoft.com/playwright:v1.56.1-jammy \
  npx playwright test

# Specific spec file
docker run --rm -it \
  -v "$(pwd)/frontend:/app" \
  -w /app \
  -e E2E_BASE_URL=https://pgsims.alshifalab.pk \
  mcr.microsoft.com/playwright:v1.56.1-jammy \
  npx playwright test e2e/rbac/access-control.spec.ts
```

## 6. CI Execution

The smoke suite runs automatically on push/PR via `.github/workflows/pgsims_e2e_smoke.yml`.

For full suite CI, trigger manually or add to the workflow file.

## 7. Reports and Artifacts

| Artifact | Location |
|----------|----------|
| HTML report | `frontend/playwright-report/index.html` |
| Test results | `frontend/pw-test-results/` |
| Screenshots (on failure) | Inside `pw-test-results/` |
| Traces (on failure) | Inside `pw-test-results/` |
| Video (on failure) | Inside `pw-test-results/` |

### View HTML report
```bash
cd frontend
npm run test:e2e:report
# Opens browser at localhost:9323
```

Or open directly:
```bash
open frontend/playwright-report/index.html
```

## 8. Resetting Test State

If tests created data that interferes with re-runs (unique constraint violations), reset:

```bash
# Re-run seed_e2e — it uses update_or_create, so safe to repeat
docker compose -f docker/docker-compose.yml exec backend \
  python manage.py seed_e2e

# Nuclear option: full demo reset
docker compose -f docker/docker-compose.yml exec backend \
  python manage.py seed_demo_data --reset
```

## 9. Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `E2E_BASE_URL` | Frontend URL for tests | `https://pgsims.alshifalab.pk` |
| `E2E_API_URL` | Backend API URL | Falls back to E2E_BASE_URL then localhost:8000 |

Set in `.env.test` or pass inline:
```bash
E2E_BASE_URL=http://localhost:3000 npm run test:e2e:smoke
```
