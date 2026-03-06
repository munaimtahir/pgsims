/**
 * Authentication flow smoke tests — exercises the login UI form end-to-end.
 * Tests that valid credentials redirect to the correct role dashboard,
 * and that invalid credentials show an error without redirecting.
 *
 * These tests do NOT use the loginAs() helper — they drive the real browser form
 * to verify the complete login stack (form → Next.js API proxy → Django backend → redirect).
 */
import { expect, test } from '@playwright/test';

test.describe('Login form', () => {
  test('valid utrmc_admin credentials redirect to UTRMC dashboard', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('e2e_utrmc_admin');
    await page.getByLabel('Password').fill('UtrmcAdmin123!');
    await page.getByRole('button', { name: /sign in/i }).click();

    // Router.push('/dashboard/utrmc') — wait for navigation
    await expect(page).toHaveURL(/\/dashboard\/utrmc/, { timeout: 15_000 });
    await expect(page.getByRole('heading', { name: 'UTRMC Overview' })).toBeVisible({ timeout: 15_000 });
  });

  test('valid supervisor credentials redirect to supervisor dashboard', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('e2e_supervisor');
    await page.getByLabel('Password').fill('Supervisor123!');
    await page.getByRole('button', { name: /sign in/i }).click();

    await expect(page).toHaveURL(/\/dashboard\/supervisor/, { timeout: 15_000 });
    await expect(page.getByRole('heading', { name: 'Supervisor Dashboard' })).toBeVisible({
      timeout: 15_000,
    });
  });

  test('valid pg credentials redirect to resident dashboard', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('e2e_pg');
    await page.getByLabel('Password').fill('Pg123456!');
    await page.getByRole('button', { name: /sign in/i }).click();

    // pg/resident role always redirects to /dashboard/resident
    // The heading "My Training Dashboard" only appears when a training record exists —
    // it is data-dependent. Smoke test verifies auth redirect only.
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 15_000 });
    // Confirm we are NOT on the login page (auth worked)
    await expect(page.getByRole('heading', { name: /sign in to sims/i })).not.toBeVisible();
  });

  test('invalid credentials show error and stay on login page', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('nonexistent_user_xyz');
    await page.getByLabel('Password').fill('WrongPassword!');
    await page.getByRole('button', { name: /sign in/i }).click();

    // Expect an error message to appear — backend returns "No active account found..."
    // Frontend falls back to "Login failed. Please check your credentials."
    await expect(page.getByText(/login failed|no active account|invalid/i)).toBeVisible({
      timeout: 10_000,
    });
    // Should NOT have navigated away from login
    await expect(page).toHaveURL(/\/login/);
  });

  test('empty form submission shows browser validation (required fields)', async ({ page }) => {
    await page.goto('/login');
    // Both username and password are required — clicking submit should not navigate
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page).toHaveURL(/\/login/);
  });
});
