/**
 * Dashboard smoke tests — verifies that role-specific dashboards load correctly
 * after authentication. Uses the loginAs() helper to authenticate via the API
 * directly (faster than driving the form) then navigates to the dashboard pages.
 *
 * Roles covered: utrmc_admin, supervisor, pg/resident
 */
import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

// ─── UTRMC Admin ─────────────────────────────────────────────────────────────

test.describe('UTRMC Admin dashboards', () => {
  test.beforeEach(async ({ context, page }) => {
    await loginAs(context, page, 'utrmc_admin');
  });

  test('UTRMC overview loads with stat cards', async ({ page }) => {
    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: 'UTRMC Overview' })).toBeVisible({
      timeout: 15_000,
    });
    // Stat card labels live inside <main> — scope avoids matching sidebar nav links
    await expect(page.getByRole('main').getByText('Hospitals')).toBeVisible();
    await expect(page.getByRole('main').getByText('Departments')).toBeVisible();
    await expect(page.getByRole('main').getByText('Total Users')).toBeVisible();
  });

  test('users management page loads with Add User button', async ({ page }) => {
    await page.goto('/dashboard/utrmc/users');
    await expect(page.getByRole('heading', { name: 'Users' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole('button', { name: /add user/i })).toBeVisible();
  });

  test('hospitals management page loads with Add Hospital button', async ({ page }) => {
    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page.getByRole('button', { name: /add hospital/i })).toBeVisible({
      timeout: 15_000,
    });
  });

  test('departments management page loads', async ({ page }) => {
    await page.goto('/dashboard/utrmc/departments');
    await expect(page.getByRole('button', { name: /add department/i })).toBeVisible({
      timeout: 15_000,
    });
  });

  test('Hospital–Department matrix page loads', async ({ page }) => {
    await page.goto('/dashboard/utrmc/matrix');
    await expect(
      page.getByRole('heading', { name: /hospital.*department.*matrix/i })
    ).toBeVisible({ timeout: 15_000 });
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
    await expect(page.getByRole('heading', { name: /sign in to sims/i })).not.toBeVisible({
      timeout: 5_000,
    });
    // Note: "My Training Dashboard" heading is rendered only when a training record
    // exists for this user. A fresh e2e_pg user without a training record will see
    // a loading/error state instead. This is expected behaviour; deeper assertions
    // belong in the data-seeded critical suite, not the smoke suite.
  });
});
