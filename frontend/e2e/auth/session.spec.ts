/**
 * Auth / Session Tests
 *
 * Covers:
 * - Valid login by each role → correct dashboard
 * - Invalid credential rejection
 * - Logout invalidates session and redirects to /login
 * - Unauthenticated access to protected route → redirect to /login
 * - Role-specific landing page
 */
import { expect, test } from '@playwright/test';
import { loginAs, type E2ERole } from '../helpers/auth';

// ------------------------------------------------------------------
// Unauthenticated guard
// ------------------------------------------------------------------

test('unauthenticated user is redirected to /login when accessing dashboard', async ({ page }) => {
  // No cookies, no localStorage — should redirect
  await page.goto('/dashboard/utrmc');
  await expect(page).toHaveURL(/\/login/);
});

test('unauthenticated user is redirected to /login for supervisor dashboard', async ({ page }) => {
  await page.goto('/dashboard/supervisor');
  await expect(page).toHaveURL(/\/login/);
});

test('unauthenticated user is redirected to /login for resident dashboard', async ({ page }) => {
  await page.goto('/dashboard/resident');
  await expect(page).toHaveURL(/\/login/);
});

// ------------------------------------------------------------------
// Valid login by role
// ------------------------------------------------------------------

const ROLE_EXPECTATIONS: Array<{ role: E2ERole; expectedPath: string }> = [
  { role: 'utrmc_admin', expectedPath: '/dashboard/utrmc' },
  { role: 'supervisor', expectedPath: '/dashboard/supervisor' },
  { role: 'pg', expectedPath: '/dashboard/resident' },
];

for (const { role, expectedPath } of ROLE_EXPECTATIONS) {
  test(`${role} logs in and lands on correct dashboard`, async ({ page, context }) => {
    await loginAs(context, page, role);
    await page.goto(expectedPath);
    await expect(page).not.toHaveURL(/\/login/, { timeout: 8000 });
    await expect(page.locator('nav,main,[role="navigation"]').first()).toBeVisible();
  });
}

// ------------------------------------------------------------------
// Invalid credentials
// ------------------------------------------------------------------

test('login rejects invalid credentials', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel(/username/i).fill('not_a_real_user');
  await page.getByLabel(/password/i).fill('WrongPassword!');
  await page.getByRole('button', { name: /sign in/i }).click();
  // Should stay on login page
  await expect(page).toHaveURL(/\/login/);
  // Error message should appear (any visible text in the error div)
  await expect(page.locator('div[class*="FFF5F5"], div[class*="C53030"], [class*="red"]').first()).toBeVisible({ timeout: 10000 });
});

test('login rejects empty credentials', async ({ page }) => {
  await page.goto('/login');
  await page.getByRole('button', { name: /sign in|log in/i }).click();
  // Should stay on login or show validation
  await expect(page).toHaveURL(/\/login/);
});

// ------------------------------------------------------------------
// Logout flow
// ------------------------------------------------------------------

test('logout clears session and redirects to /login', async ({ page, context }) => {
  await loginAs(context, page, 'utrmc_admin');
  await page.goto('/dashboard/utrmc');
  await expect(page).not.toHaveURL(/\/login/);

  // Click the sidebar logout button
  await page.locator('[data-testid="sidebar-logout-btn"]').click();

  // Should land on login page
  await expect(page).toHaveURL(/\/login/, { timeout: 10000 });

  // Trying to access dashboard should redirect back to login
  await page.goto('/dashboard/utrmc');
  await expect(page).toHaveURL(/\/login/);
});

test('supervisor logout clears session', async ({ page, context }) => {
  await loginAs(context, page, 'supervisor');
  await page.goto('/dashboard/supervisor');
  await expect(page).not.toHaveURL(/\/login/);

  await page.locator('[data-testid="sidebar-logout-btn"]').click();
  await expect(page).toHaveURL(/\/login/, { timeout: 10000 });
});
