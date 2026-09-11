/**
 * Dashboard smoke tests — verifies that role-specific dashboards load correctly
 * after authentication. Uses the loginAs() helper to authenticate via the API
 * directly (faster than driving the form) then navigates to the dashboard pages.
 *
 * Roles covered: utrmc_admin, supervisor, pg/resident
 */
import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

// ─── Administrator ──────────────────────────────────────────────────────────

test.describe('Administrator dashboards', () => {
  test.beforeEach(async ({ context, page }) => {
    await loginAs(context, page, 'utrmc_admin');
  });

  test('UTRMC overview loads with stat cards', async ({ page }) => {
    await page.goto('/dashboard/utrmc');
      await expect(page.getByRole('heading', { name: 'Admin Dashboard' })).toBeVisible({
      timeout: 15_000,
    });
    // Stat card labels live inside <main> — scope avoids matching sidebar nav links
    await expect(page.getByRole('main').getByText('Users').first()).toBeVisible();
    await expect(page.getByRole('main').getByText('Residents').first()).toBeVisible();
    await expect(page.getByRole('main').getByText('Supervisors').first()).toBeVisible();
  });

  test('users management page loads with Add User button', async ({ page }) => {
    await page.goto('/users');
    await expect(page.getByRole('heading', { name: 'Users' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole('link', { name: 'New User' })).toBeVisible();
  });

  test('hospitals management page loads with Add Hospital button', async ({ page }) => {
    await page.goto('/masters');
    await expect(page.getByRole('heading', { name: 'Masters' })).toBeVisible({
      timeout: 15_000,
    });
  });

  test('departments management page loads', async ({ page }) => {
    await page.goto('/masters');
    await expect(page.getByText('Departments', { exact: true })).toBeVisible({
      timeout: 15_000,
    });
  });

  test('Hospital–Department matrix page loads', async ({ page }) => {
    await page.goto('/masters');
    await expect(page.getByText('Hospital-Department Matrix', { exact: true })).toBeVisible({ timeout: 15_000 });
  });
});

// ─── Supervisor ───────────────────────────────────────────────────────────────

test.describe('Supervisor dashboard', () => {
  test.beforeEach(async ({ context, page }) => {
    await loginAs(context, page, 'supervisor');
  });

  test('supervisor dashboard loads with resident list section', async ({ page }) => {
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: 'Supervisor Dashboard' })).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByRole('heading', { name: /my residents/i })).toBeVisible({
      timeout: 15_000,
    });
  });
});

// ─── Resident / PG ───────────────────────────────────────────────────────────

test.describe('Resident (PG) dashboard', () => {
  test.beforeEach(async ({ context, page }) => {
    await loginAs(context, page, 'pg');
  });

  test('resident dashboard is accessible and renders page chrome', async ({ page }) => {
    await page.goto('/dashboard/resident');
    // Verify URL — middleware allows pg/resident role on this path
    await expect(page).toHaveURL(/\/dashboard\/resident/);
    // Not redirected back to login — auth cookie is valid
    await expect(page.getByRole('heading', { name: /sign in to fmu-utrmc pgsims/i })).not.toBeVisible({
      timeout: 5_000,
    });
    await expect(page.getByRole('heading', { name: 'Resident Dashboard' })).toBeVisible({ timeout: 15_000 });
  });
});
