import { defineConfig, devices } from '@playwright/test';

// Discovery-only config to run audit-local specs without touching the
// application's committed Playwright suite configuration.
export default defineConfig({
  testDir: '.',
  timeout: 30_000,
  retries: 0,
  workers: 1,
  reporter: [['list']],
  outputDir: './playwright_output',
  use: {
    ...devices['Desktop Chrome'],
    trace: 'off',
    screenshot: 'off',
    video: 'off',
  },
});
