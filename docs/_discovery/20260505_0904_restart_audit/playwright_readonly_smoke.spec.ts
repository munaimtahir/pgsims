import { test, expect } from '@playwright/test';

const FRONTEND_BASE = process.env.PGSIMS_FRONTEND_BASE ?? 'http://127.0.0.1:8082';
const BACKEND_BASE = process.env.PGSIMS_BACKEND_BASE ?? 'http://127.0.0.1:8014';

test.describe('PGSIMS readonly smoke (discovery audit)', () => {
  test('frontend landing page responds', async ({ page }) => {
    const res = await page.goto(`${FRONTEND_BASE}/`, { waitUntil: 'domcontentloaded' });
    expect(res?.status(), 'frontend / status').toBe(200);
    await expect(page).toHaveTitle(/SIMS|PGSIMS/i);
  });

  test('frontend login page responds', async ({ page }) => {
    const res = await page.goto(`${FRONTEND_BASE}/login`, { waitUntil: 'domcontentloaded' });
    expect(res?.status(), 'frontend /login status').toBe(200);
    await expect(page.locator('body')).toContainText(/sign in|login/i);
  });

  test('backend healthz responds', async ({ request }) => {
    const res = await request.get(`${BACKEND_BASE}/healthz/`);
    expect(res.status(), 'backend /healthz status').toBe(200);
    const body = await res.json();
    expect(body?.status).toBe('healthy');
  });

  test('backend OpenAPI schema responds', async ({ request }) => {
    const res = await request.get(`${BACKEND_BASE}/api/schema/`);
    expect(res.status(), 'backend /api/schema/ status').toBe(200);
    const text = await res.text();
    expect(text).toMatch(/^openapi:/m);
  });
});
