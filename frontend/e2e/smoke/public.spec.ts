/**
 * Public page smoke tests — no authentication required.
 * These tests verify that publicly accessible pages render correctly
 * and that unauthenticated access to protected routes redirects to /login.
 */
import { expect, test } from '@playwright/test';

test.describe('Public pages', () => {
  test('login page renders with form fields', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByRole('heading', { name: /sign in to sims/i })).toBeVisible();
    await expect(page.getByLabel('Username')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible();
    await expect(page.getByText(/registration is disabled/i)).toBeVisible();
  });

  test('register page shows disabled message with back link', async ({ page }) => {
    await page.goto('/register');
    await expect(page.getByRole('heading', { name: /registration is disabled/i })).toBeVisible();
    await expect(page.getByText(/new accounts are provisioned by administrators only/i)).toBeVisible();
    await expect(page.getByRole('link', { name: /back to login/i })).toHaveAttribute('href', '/login');
  });

  test('unauthenticated access to /dashboard/utrmc redirects to /login', async ({ page }) => {
    await page.goto('/dashboard/utrmc');
    await expect(page).toHaveURL(/\/login/);
    await expect(page.getByRole('heading', { name: /sign in to sims/i })).toBeVisible();
  });

  test('unauthenticated access to /dashboard/supervisor redirects to /login', async ({ page }) => {
    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/login/);
  });

  test('unauthenticated access to /dashboard/resident redirects to /login', async ({ page }) => {
    await page.goto('/dashboard/resident');
    await expect(page).toHaveURL(/\/login/);
  });
});
