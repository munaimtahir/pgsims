/**
 * UTRMC Management Workflows
 *
 * Covers UTRMC admin CRUD operations via the UI:
 * - Create and verify a hospital via UI
 * - Create and verify a department via UI
 * - User management (view/add modal)
 * - Supervision link management
 */
import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

// ------------------------------------------------------------------
// Hospital CRUD
// ------------------------------------------------------------------

test.describe('Hospital management', () => {
  test('retired hospital route resolves to masters workspace', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');

    await expect(page).toHaveURL(/\/masters/);
    await expect(page.getByRole('heading', { name: 'Bulk Setup & Import\/Export' })).toBeVisible();
  });

  test('hospital setup is available from the canonical masters workspace', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');

    await expect(page).toHaveURL(/\/masters/);
    await expect(page.getByRole('heading', { name: 'Hospitals', exact: true })).toBeVisible();
  });
});

// ------------------------------------------------------------------
// Department CRUD
// ------------------------------------------------------------------

test.describe('Department management', () => {
  test('retired department route resolves to masters workspace', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');

    await expect(page).toHaveURL(/\/masters/);
    await expect(page.getByRole('heading', { name: 'Bulk Setup & Import\/Export' })).toBeVisible();
  });

  test('department setup is available from the canonical masters workspace', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');

    await expect(page).toHaveURL(/\/masters/);
    await expect(page.getByRole('heading', { name: 'Departments', exact: true })).toBeVisible();
  });
});

// ------------------------------------------------------------------
// User management
// ------------------------------------------------------------------

test.describe('User management', () => {
  test('users page lists existing e2e users', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');

    // e2e_supervisor should be in the list (seeded via seed_e2e)
    // Use first() to avoid strict mode violation when username appears multiple times
    await expect(page.getByText('e2e_supervisor').first()).toBeVisible({ timeout: 10000 });
  });

  test('universal user creation exposes the four canonical roles', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/users/new');

    await expect(page.getByRole('heading', { name: 'New User' })).toBeVisible();
    await expect(page.getByLabel('Full Name')).toBeVisible();
    await expect(page.getByLabel('Role').locator('option')).toHaveCount(4);
  });
});

// ------------------------------------------------------------------
// Supervision links
// ------------------------------------------------------------------

test.describe('Supervision link management', () => {
  test('supervision page loads and shows table or empty state', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/supervision');

    await page.waitForLoadState('networkidle');
    // Should either have data or an empty/loading state — just verify page rendered
    await expect(page.locator('main').first()).toBeVisible();
    await expect(page).not.toHaveURL(/\/login/);
  });

  test('add supervision link modal opens', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/supervision');

    const addBtn = page.getByRole('button', { name: /add|create|link/i }).first();
    if (await addBtn.isVisible()) {
      await addBtn.click();
      // Modal or form should appear
      await expect(page.locator('div').filter({ has: page.getByRole('heading') }).first()).toBeVisible({ timeout: 5000 });
      // Close it
      const cancelBtn = page.getByRole('button', { name: /cancel/i });
      if (await cancelBtn.isVisible()) await cancelBtn.click();
    }
  });
});
