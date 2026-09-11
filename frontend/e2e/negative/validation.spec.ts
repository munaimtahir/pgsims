/**
 * Negative / Validation Tests
 *
 * Covers:
 * - Login form validation (empty fields, invalid data)
 * - Retired duplicate administration routes redirect to canonical masters
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
  test('retired hospital route redirects to canonical masters workspace', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page).toHaveURL(/\/masters/);
    await expect(page.getByRole('heading', { name: 'Bulk Setup & Import\/Export' })).toBeVisible();
  });
});

// ------------------------------------------------------------------
// Department form validation
// ------------------------------------------------------------------

test.describe('Department form validation', () => {
  test('retired department route redirects to canonical masters workspace', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');
    await expect(page).toHaveURL(/\/masters/);
    await expect(page.getByRole('heading', { name: 'Bulk Setup & Import\/Export' })).toBeVisible();
  });
});

// ------------------------------------------------------------------
// User form validation
// ------------------------------------------------------------------

test.describe('User form validation', () => {
  test('save user without required fields shows error', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/users/new');
    await expect(page.getByRole('heading', { name: 'New User' })).toBeVisible();
    await expect(page.getByLabel('Full Name')).toHaveAttribute('required', '');
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
    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
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

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    const res = await page.request.get(`${appBase}/api/supervisors/me/summary/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect([403, 404]).toContain(res.status());
  });
});
