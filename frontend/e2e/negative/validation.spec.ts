/**
 * Negative / Validation Tests
 *
 * Covers:
 * - Login form validation (empty fields, invalid data)
 * - UTRMC hospital form validation (empty required fields)
 * - UTRMC department form validation (empty required fields)
 * - Direct URL cross-role access blocked
 * - Invalid API payloads rejected
 */
import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

// ------------------------------------------------------------------
// Login form validation
// ------------------------------------------------------------------

test.describe('Login form validation', () => {
  test('empty username shows validation or stays on login', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/password/i).fill('somepassword');
    await page.getByRole('button', { name: /sign in|log in/i }).click();
    await expect(page).toHaveURL(/\/login/);
  });

  test('empty password shows validation or stays on login', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/username/i).fill('someuser');
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page).toHaveURL(/\/login/);
  });

  test('wrong password for valid user shows error', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/username/i).fill('e2e_admin');
    await page.getByLabel(/password/i).fill('WrongPassword999!');
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page).toHaveURL(/\/login/);
    // Red error div should appear
    await expect(page.locator('div[class*="FFF5F5"], div[class*="C53030"], [class*="red"]').first()).toBeVisible({ timeout: 10000 });
  });

  test('nonexistent user shows error', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/username/i).fill('this_user_does_not_exist_xyz');
    await page.getByLabel(/password/i).fill('SomePass123!');
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page).toHaveURL(/\/login/);
    // Red error div should appear
    await expect(page.locator('div[class*="FFF5F5"], div[class*="C53030"], [class*="red"]').first()).toBeVisible({ timeout: 10000 });
  });
});

// ------------------------------------------------------------------
// Hospital form validation
// ------------------------------------------------------------------

test.describe('Hospital form validation', () => {
  test('save without name is blocked or shows error', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/hospitals');

    await page.getByRole('button', { name: /add hospital/i }).click();
    await expect(page.getByRole('heading', { name: /add hospital/i })).toBeVisible();

    // Click Save without filling anything
    await page.getByRole('button', { name: /^save$/i }).click();

    // Either the modal stays open OR an error is shown
    const modalOpen = await page.getByRole('heading', { name: /add hospital/i }).isVisible().catch(() => false);
    const errorShown = await page.getByText(/required|error|failed/i).first().isVisible().catch(() => false);

    expect(modalOpen || errorShown).toBe(true);

    // Clean up
    const cancelBtn = page.getByRole('button', { name: /cancel/i });
    if (await cancelBtn.isVisible()) await cancelBtn.click();
  });
});

// ------------------------------------------------------------------
// Department form validation
// ------------------------------------------------------------------

test.describe('Department form validation', () => {
  test('save without name is blocked or shows error', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/departments');

    await page.getByRole('button', { name: /add department/i }).click();
    await expect(page.getByRole('heading', { name: /add department/i })).toBeVisible();

    await page.getByRole('button', { name: /^save$/i }).click();

    const modalOpen = await page.getByRole('heading', { name: /add department/i }).isVisible().catch(() => false);
    const errorShown = await page.getByText(/required|error|failed/i).first().isVisible().catch(() => false);

    expect(modalOpen || errorShown).toBe(true);

    const cancelBtn = page.getByRole('button', { name: /cancel/i });
    if (await cancelBtn.isVisible()) await cancelBtn.click();
  });
});

// ------------------------------------------------------------------
// User form validation
// ------------------------------------------------------------------

test.describe('User form validation', () => {
  test('save user without required fields shows error', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');

    await page.getByRole('button', { name: /add user/i }).click();
    await expect(page.getByRole('heading', { name: /add user/i })).toBeVisible();

    await page.getByRole('button', { name: /^save$/i }).click();

    const modalOpen = await page.getByRole('heading', { name: /add user/i }).isVisible().catch(() => false);
    const errorShown = await page.getByText(/required|error|failed/i).first().isVisible().catch(() => false);

    expect(modalOpen || errorShown).toBe(true);

    const cancelBtn = page.getByRole('button', { name: /cancel/i });
    if (await cancelBtn.isVisible()) await cancelBtn.click();
  });
});

// ------------------------------------------------------------------
// Cross-role URL access blocked
// ------------------------------------------------------------------

test.describe('Cross-role URL access blocked', () => {
  test('pg cannot access UTRMC admin routes directly', async ({ page, context }) => {
    await loginAs(context, page, 'pg');

    const utrmcRoutes = [
      '/dashboard/utrmc/hospitals',
      '/dashboard/utrmc/departments',
      '/dashboard/utrmc/users',
    ];

    for (const route of utrmcRoutes) {
      await page.goto(route);
      // Should be redirected to resident/pg dashboard, not stay on UTRMC route
      await expect(page).not.toHaveURL(route, { timeout: 8000 });
    }
  });

  test('supervisor cannot access UTRMC admin routes directly', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');

    await page.goto('/dashboard/utrmc/users');
    await expect(page).not.toHaveURL('/dashboard/utrmc/users', { timeout: 8000 });
  });
});

// ------------------------------------------------------------------
// API unauthorized access
// ------------------------------------------------------------------

test.describe('API unauthorized access', () => {
  test('calling users API without auth returns 401', async ({ page }) => {
    const appBase = process.env.E2E_BASE_URL ?? 'https://pgsims.alshifalab.pk';
    const res = await page.request.get(`${appBase}/api/users/`);
    expect([401, 403]).toContain(res.status());
  });

  test('calling supervisor summary API as pg returns 403', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
      return parsed.state?.accessToken ?? '';
    });

    const appBase = process.env.E2E_BASE_URL ?? 'https://pgsims.alshifalab.pk';
    const res = await page.request.get(`${appBase}/api/supervisors/me/summary/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect([403, 404]).toContain(res.status());
  });
});
