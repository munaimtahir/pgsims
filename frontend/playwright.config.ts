import { defineConfig, devices } from '@playwright/test';

/**
 * PGSIMS Playwright Configuration
 *
 * Target app: Next.js frontend (pgsims.alshifalab.pk or localhost:3000)
 * Test suites:
 *   - smoke    Fast sanity checks on public pages and role dashboards (no setup dep)
 *   - critical Full user-flow tests requiring pre-authenticated storageState
 *
 * Run commands (see package.json for scripts):
 *   npm run test:e2e:smoke    — smoke suite only (fast, good for CI)
 *   npm run test:e2e          — smoke + critical suites
 *   npm run test:e2e:headed   — run with visible browser
 *   npm run test:e2e:ui       — interactive Playwright UI
 *
 * Environment variables:
 *   E2E_BASE_URL   Frontend base URL (default: https://pgsims.alshifalab.pk)
 *   E2E_API_URL    Backend API URL — if unset, loginAs() falls back to E2E_BASE_URL then localhost:8000
 *
 * App startup: The app is NOT started automatically. Start the Docker stack before running:
 *   docker compose -f docker/docker-compose.yml --env-file .env up -d
 *   (or `make up` from repo root)
 * For local dev: `cd frontend && npm run dev` (sets E2E_BASE_URL=http://localhost:3000)
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  timeout: 30_000,
  expect: { timeout: 10_000 },

  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['list'],
  ],

  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'https://pgsims.alshifalab.pk',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    // Use a separate output dir to avoid conflict with jest test-results
    testIdAttribute: 'data-testid',
  },

  outputDir: 'pw-test-results',

  projects: [
    // Auth setup — saves admin storageState for the critical suite
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },

    // Smoke suite — fast, self-contained; no storageState dependency
    // Each test that needs auth calls loginAs() directly
    {
      name: 'smoke',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /smoke\/.*\.spec\.ts/,
    },

    // Critical suite — full user-flow tests; requires setup to have run
    {
      name: 'critical',
      use: { ...devices['Desktop Chrome'], storageState: 'e2e/.auth/admin.json' },
      dependencies: ['setup'],
      testMatch: /critical\/.*\.spec\.ts/,
    },
  ],
});
