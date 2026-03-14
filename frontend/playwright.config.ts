import { defineConfig, devices } from '@playwright/test';

/**
 * PGSIMS Playwright Configuration
 *
 * Target app: Next.js frontend (canonical local Docker URL: http://127.0.0.1:8082)
 * Test suites:
 *   - smoke    Fast sanity checks on public pages and role dashboards (no setup dep)
 *   - critical Full user-flow tests requiring pre-authenticated storageState
 *
 * Run commands (see package.json for scripts):
 *   npm run test:e2e:smoke    — smoke suite only (fast, good for CI)
 *   npm run test:e2e:workflow — promoted workflow gate
 *   npm run test:e2e          — smoke + critical suites
 *   npm run test:e2e:headed   — run with visible browser
 *   npm run test:e2e:ui       — interactive Playwright UI
 *
 * Environment variables:
 *   E2E_BASE_URL   Frontend base URL (default: http://127.0.0.1:8082)
 *   E2E_API_URL    Backend API URL (default: http://127.0.0.1:8014)
 *
 * App startup: The app is NOT started automatically. Start the Docker stack before running:
 *   docker compose -f docker/docker-compose.yml --env-file .env up -d
 *   (or `make up` from repo root)
 * For non-Docker local runs (optional), set both:
 *   E2E_BASE_URL=http://127.0.0.1:3000 E2E_API_URL=http://127.0.0.1:8000
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
    ['html', { outputFolder: '../output/playwright/report', open: 'never' }],
    ['list'],
  ],

  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    // Use a separate output dir to avoid conflict with jest test-results
    testIdAttribute: 'data-testid',
  },

  outputDir: '../output/playwright/results',

  projects: [
    // Auth setup — saves admin storageState for the critical suite
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },

    // Smoke suite — fast, self-contained; no storageState dependency
    {
      name: 'smoke',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /smoke\/.*\.spec\.ts/,
    },

    // Workflow gate — small deterministic contract-critical browser flows
    {
      name: 'workflow-gate',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /workflow-gate\/.*\.spec\.ts/,
    },

    // Auth/session suite
    {
      name: 'auth',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /auth\/.*\.spec\.ts/,
    },

    // RBAC/access control suite
    {
      name: 'rbac',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /rbac\/.*\.spec\.ts/,
    },

    // Navigation suite
    {
      name: 'navigation',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /navigation\/.*\.spec\.ts/,
    },

    // Dashboard suite
    {
      name: 'dashboard',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /dashboard\/.*\.spec\.ts/,
    },

    // Workflow tests
    {
      name: 'workflows',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /workflows\/.*\.spec\.ts/,
    },

    // Negative/validation tests
    {
      name: 'negative',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /negative\/.*\.spec\.ts/,
    },

    // Critical suite — full user-flow tests; requires setup to have run
    {
      name: 'critical',
      use: { ...devices['Desktop Chrome'], storageState: 'e2e/.auth/admin.json' },
      dependencies: ['setup'],
      testMatch: /critical\/.*\.spec\.ts/,
    },

    // Screenshot tour — captures every screen/workflow for every role
    {
      name: 'screenshots',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1400, height: 900 },
        screenshot: 'on',
      },
      testMatch: /screenshots\/.*\.spec\.ts/,
    },
  ],
});
