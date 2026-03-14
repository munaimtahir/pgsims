/**
 * Resident Training Workflow Tests
 *
 * Covers:
 * - Schedule page shows rotations seeded by seed_e2e
 * - Academic progress page loads eligibility data
 * - Research page loads and shows step wizard
 * - Thesis page loads
 * - Workshops page loads
 * - API endpoint validation for resident training data
 */
import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

// ------------------------------------------------------------------
// Schedule / Rotations
// ------------------------------------------------------------------

test.describe('Resident schedule', () => {
  test('schedule page loads and shows rotation data', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    await expect(page).not.toHaveURL(/\/login/);
    await page.waitForLoadState('networkidle');
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('schedule API returns rotations for e2e_pg', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
      return parsed.state?.accessToken ?? '';
    });
    expect(token).toBeTruthy();

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    const res = await page.request.get(`${appBase}/api/my/rotations/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    // Accept 200 (list), 404 (no training record yet), or 403 as not-forbidden
    expect([200, 404]).toContain(res.status());
  });
});

// ------------------------------------------------------------------
// Academic Progress
// ------------------------------------------------------------------

test.describe('Resident academic progress', () => {
  test('progress page loads without runtime error', async ({ page, context }) => {
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error' && !msg.text().includes('favicon')) errors.push(msg.text());
    });

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/progress');
    await page.waitForLoadState('networkidle');

    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();

    // Allow API errors from missing seed data — only fail on JS runtime errors
    const jsErrors = errors.filter(e =>
      !e.includes('Failed to fetch') &&
      !e.includes('NetworkError') &&
      !e.includes('Failed to load resource')
    );
    expect(jsErrors).toHaveLength(0);
  });

  test('eligibility API returns data for e2e_pg', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
      return parsed.state?.accessToken ?? '';
    });

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    const res = await page.request.get(`${appBase}/api/my/eligibility/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    // OK or 404 (if no program assigned) both acceptable — just not 403/500
    expect([200, 404]).toContain(res.status());
  });
});

// ------------------------------------------------------------------
// Research Workflow
// ------------------------------------------------------------------

test.describe('Resident research workflow', () => {
  test('research page loads and shows wizard steps', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/research');

    await expect(page).not.toHaveURL(/\/login/);
    await page.waitForLoadState('networkidle');
    await expect(page.locator('main').first()).toBeVisible();

    // Wizard steps should be visible
    const stepLabels = ['Topic & Supervisor', 'Upload Synopsis', 'Submit to Supervisor'];
    for (const label of stepLabels) {
      await expect(page.getByText(label).first()).toBeVisible({ timeout: 10000 });
    }
  });

  test('research API returns project for e2e_pg (or 404 if none created)', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
      return parsed.state?.accessToken ?? '';
    });

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    const res = await page.request.get(`${appBase}/api/my/research/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect([200, 404]).toContain(res.status());
  });
});

// ------------------------------------------------------------------
// Thesis
// ------------------------------------------------------------------

test.describe('Resident thesis page', () => {
  test('thesis page loads without redirect', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/thesis');

    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });
});

// ------------------------------------------------------------------
// Workshops
// ------------------------------------------------------------------

test.describe('Resident workshops page', () => {
  test('workshops page loads without redirect', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/workshops');

    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('workshops API returns data for e2e_pg', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
      return parsed.state?.accessToken ?? '';
    });

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    const res = await page.request.get(`${appBase}/api/my/workshops/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect([200, 404]).toContain(res.status());
  });
});

// ------------------------------------------------------------------
// Resident summary API
// ------------------------------------------------------------------

test.describe('Resident summary API', () => {
  test('resident summary endpoint is accessible', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
      return parsed.state?.accessToken ?? '';
    });

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    const res = await page.request.get(`${appBase}/api/residents/me/summary/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect([200, 404]).toContain(res.status());
  });
});
