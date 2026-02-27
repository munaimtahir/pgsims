# 00_BASELINE

## Environment
- Repo: `/srv/apps/pgsims`
- Domain target: `https://pgsims.alshifalab.pk`

## Tool Versions (Phase 1)
- `node --version` → `v20.20.0`
- `npm --version` → `10.8.2`
- `npx playwright --version` → `Version 1.56.1`

## Playwright Discovery (Before Fixes)
- Config: `frontend/playwright.config.ts`
- Test folder: `frontend/e2e/`
- Dry listing command: `npx playwright test --list`

### `--list` output snapshot
- `[chromium] admin_analytics.spec.ts`
- `[chromium] cases_create_submit_review.spec.ts`
- `[chromium] import_reports_dashboard.spec.ts`
- `[chromium] logbook_submit_return_resubmit_approve.spec.ts`
- `[chromium] login.spec.ts`
- `[chromium] utrmc_readonly_dashboard.spec.ts` (2 tests)
- Total: `7 tests in 6 files`

## Initial Mismatch Identified
- `fullyParallel: true` (non-serial behavior)
- `baseURL` defaulted to `http://localhost:3000`
- Cookies/auth helpers in some tests used localhost URLs
- Existing suite mixed heavy workflow tests with environment-dependent seeded users
