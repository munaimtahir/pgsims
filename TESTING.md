# PGSIMS — Testing Guide

This document covers the Playwright end-to-end test setup for the PGSIMS application.

---

## What Playwright Is Used For

Playwright tests the **Next.js frontend** (`frontend/`) in a real browser, exercising full user workflows:

- Public page rendering (login, register-disabled)
- Authentication flows (login form → role-specific dashboard redirect)
- Role dashboards: UTRMC Admin, Supervisor, Resident/PG
- UTRMC management pages: users, hospitals, departments, matrix
- Critical multi-step flows: userbase CRUD, research eligibility

---

## Where Config and Tests Live

```
frontend/
├── playwright.config.ts          # Main Playwright config
└── e2e/
    ├── auth.setup.ts             # Auth setup — saves admin storageState
    ├── helpers/
    │   └── auth.ts               # loginAs() helper for all 5 roles
    ├── smoke/                    # Fast sanity suite (no setup dependency)
    │   ├── public.spec.ts        # Public pages & unauthenticated redirects
    │   ├── auth_flow.spec.ts     # Login form flows for each role
    │   └── dashboards.spec.ts    # Role dashboards via API login
    ├── critical/                 # Full user-flow tests (require auth setup)
    │   ├── userbase_foundation.spec.ts
    │   ├── secondary_role_optional.spec.ts
    │   ├── phase6_research_eligibility.spec.ts
    │   ├── admin_critical.spec.ts
    │   └── admin_analytics_live_feed.spec.ts
    └── regression/               # Pending — tests for not-yet-implemented features
        └── README.md             # Explains graduation process
```

---

## Prerequisites

1. **Node.js ≥ 18** installed
2. **Playwright browsers installed** (Chromium)
3. **PGSIMS app running** — Playwright does NOT start the app automatically

### Start the app (Docker)

```bash
# From repo root
docker compose -f docker/docker-compose.yml --env-file .env up -d
# Or: make up
```

### Or run frontend locally (dev server)

```bash
cd frontend
npm run dev
# App is at http://localhost:3000
# Backend must also be running (port 8014 or via docker)
```

---

## Install Steps After Cloning

```bash
# 1. Install Node dependencies
cd frontend
npm install

# 2. Install Playwright Chromium browser
npm run test:e2e:install
# Equivalent: npx playwright install chromium

# 3. Install system browser dependencies (requires sudo, Linux only)
sudo npx playwright install-deps chromium
# If you cannot use sudo, see the Docker execution method below.
```

### Running on a server without sudo (Docker execution)

If system libraries (`libatk`, `libXdamage`, `libcairo`, etc.) cannot be installed, run tests via the Playwright Docker image:

```bash
# From repo root
docker run --rm \
  --network=host \
  -v "$(pwd)/frontend:/app" \
  -w /app \
  -e E2E_BASE_URL=https://pgsims.alshifalab.pk \
  mcr.microsoft.com/playwright:v1.56.1-jammy \
  bash -c "npx playwright test --project=smoke"
```

Match `v1.56.1-jammy` to the `@playwright/test` version in `frontend/package.json`.

---

## Run Commands

All commands must be run from the `frontend/` directory.

### Smoke tests (recommended for CI and quick checks)

```bash
npm run test:e2e:smoke
```

Runs `e2e/smoke/*.spec.ts` — no pre-authentication setup required. Fastest suite.

### Full E2E suite (smoke + critical)

```bash
npm run test:e2e
```

Runs setup (saves auth state), then smoke + critical suites.

### Critical flows only

```bash
npm run test:e2e:critical
```

### Run with visible browser (local debugging)

```bash
npm run test:e2e:headed
```

### Interactive Playwright UI mode (local debugging)

```bash
npm run test:e2e:ui
```

### Debug a single test

```bash
npm run test:e2e:debug -- e2e/smoke/public.spec.ts
```

### Open HTML report after a run

```bash
npm run test:e2e:report
```

### Generate new test code interactively

```bash
npm run test:e2e:codegen
# Opens browser with code-generation recording
```

---

## Targeting a Specific App URL

By default tests run against `https://pgsims.alshifalab.pk`. Override with:

```bash
E2E_BASE_URL=http://localhost:3000 npm run test:e2e:smoke
```

If backend is on a different host (e.g. local docker):

```bash
E2E_BASE_URL=http://localhost:3000 E2E_API_URL=http://localhost:8014 npm run test:e2e:smoke
```

---

## App Startup Behaviour

**The app is NOT started automatically by Playwright.** You must start it before running tests.

| Environment | Start command |
|-------------|--------------|
| Docker (production-like) | `make up` or `docker compose -f docker/docker-compose.yml --env-file .env up -d` |
| Local dev | `cd frontend && npm run dev` (backend must be running separately) |

This is intentional — the Docker stack is complex (Django + Celery + Redis + Next.js) and starting it from within Playwright would be fragile. A future `webServer` config can be added for `npm run dev` once that startup path is verified stable.

---

## Where Artifacts Are Stored

| Artifact | Location |
|----------|----------|
| HTML report | `frontend/playwright-report/` |
| Test results (traces, screenshots, videos) | `frontend/test-results/` |
| Admin auth state (gitignored) | `frontend/e2e/.auth/admin.json` |

All artifact directories are in `.gitignore` and must NOT be committed.

---

## Authentication and Seeded Users

Tests use dedicated E2E accounts seeded into the database. These credentials are in `e2e/helpers/auth.ts` (non-production test accounts):

| Role | Username | Password |
|------|----------|----------|
| `admin` | `e2e_admin` | `Admin123!` |
| `utrmc_admin` | `e2e_utrmc_admin` | `UtrmcAdmin123!` |
| `utrmc_user` | `e2e_utrmc_user` | `Utrmc123!` |
| `supervisor` | `e2e_supervisor` | `Supervisor123!` |
| `pg` | `e2e_pg` | `Pg123456!` |

### Seeding E2E users (first-time setup or after DB wipe)

```bash
# From repo root, using the running backend container
docker compose -f docker/docker-compose.yml --env-file .env exec backend python manage.py shell
```

Then in the Django shell:

```python
from django.contrib.auth import get_user_model
User = get_user_model()

users = [
    {'username': 'e2e_admin',      'password': 'Admin123!',      'role': 'admin'},
    {'username': 'e2e_utrmc_admin','password': 'UtrmcAdmin123!', 'role': 'utrmc_admin'},
    {'username': 'e2e_utrmc_user', 'password': 'Utrmc123!',      'role': 'utrmc_user'},
    {'username': 'e2e_supervisor', 'password': 'Supervisor123!', 'role': 'supervisor'},
    {'username': 'e2e_pg',         'password': 'Pg123456!',      'role': 'pg'},
]
for u in users:
    obj, created = User.objects.get_or_create(username=u['username'], defaults={'role': u['role']})
    obj.set_password(u['password'])
    if not obj.role:
        obj.role = u['role']
    obj.save()
    print('created' if created else 'updated', obj.username)
```

---

## How to Add New Tests

1. **Smoke test** (fast, self-contained): Add a file to `e2e/smoke/`.
2. **Critical flow** (complex multi-step, needs auth state): Add to `e2e/critical/`.
3. **Use role-based auth**: Call `loginAs(context, page, 'role')` from `e2e/helpers/auth.ts`.
4. **Prefer accessible locators**: `getByRole`, `getByLabel`, `getByText`, `getByPlaceholder`.
5. **Avoid `data-testid`** unless the component explicitly exports them — the app currently has none.
6. **Do not hardcode production data** — use seeded E2E accounts and known seeded records.

---

## Troubleshooting

### Tests fail with "No active account found" on login

The E2E users are not seeded. Run the seeding shell commands above.

### Tests fail with "net::ERR_CONNECTION_REFUSED"

The app is not running. Start it with `make up` or `npm run dev`.

### Auth state is stale or expired

Delete `e2e/.auth/admin.json` and re-run. The `setup` project will recreate it.

```bash
rm -f e2e/.auth/admin.json
npm run test:e2e:critical
```

### Browser not installed

```bash
npm run test:e2e:install
# Or: npx playwright install --with-deps chromium
```

### Trace / screenshot inspection

After a failed run, open the HTML report:

```bash
npm run test:e2e:report
```

Traces can be viewed in the report or directly at [trace.playwright.dev](https://trace.playwright.dev).

---

## CI

A GitHub Actions workflow (`.github/workflows/pgsims_e2e_smoke.yml`) runs the smoke suite on push/PR, pointing at the production server `https://pgsims.alshifalab.pk`. The workflow:

1. Installs Node dependencies
2. Installs Playwright Chromium
3. Runs `npm run test:e2e:smoke`
4. Uploads HTML report artifact on failure

> **Note**: The CI smoke suite requires the production app to be running and the E2E user accounts to be seeded. It does NOT deploy the app — it tests the already-deployed production instance.
