# 01_CONFIG_FIXES

## What changed

### 1) Playwright normalized for production + serial execution
- Updated `frontend/playwright.config.ts`:
  - `use.baseURL = "https://pgsims.alshifalab.pk"`
  - `workers = 1`
  - `retries = 1`
  - `trace = "on-first-retry"`
  - `screenshot = "only-on-failure"`
  - `video = "retain-on-failure"`
  - HTML reporter output redirected to `OUT/E2E_REMEDIATION/playwright-report`
  - `fullyParallel = false`

### 2) Stabilized scope to critical serial pack
- Configured `testMatch` to run only `e2e/critical/*.spec.ts` in the chromium project.
- Added setup project (`auth.setup.ts`) that runs first.

### 3) Storage state authentication workflow (Option A: UI login once)
- Added `frontend/e2e/auth.setup.ts`:
  - Performs UI login with admin seeded account.
  - Asserts redirect to admin dashboard.
  - Saves storage state to `frontend/e2e/.auth/admin.json`.
- Reused storage state in chromium project (`use.storageState`).
- Added `frontend/.gitignore` entry for `/e2e/.auth/`.

### 4) Minimal critical E2E tests (2–4 tests)
- Added `frontend/e2e/critical/admin_critical.spec.ts`:
  - Admin dashboard widgets load.
  - Admin reports catalog opens and run action executes.
- Added `frontend/e2e/critical/secondary_role_optional.spec.ts`:
  - Verifies a non-admin dashboard using seeded secondary-role credentials when available.

## Why
- Removed localhost coupling.
- Reduced flakiness by serial execution + scoped critical path.
- Ensured reusable auth state and deterministic setup.
- Produced report/log artifacts in required remediation output directory.
