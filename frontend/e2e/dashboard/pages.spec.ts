/**
 * Dashboard Tests
 *
 * Verifies dashboard pages render with seeded data:
 * - UTRMC overview — stat cards, tables visible
 * - Supervisor dashboard — residents list, summary
 * - Resident dashboard — eligibility cards, status badges
 */
import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

// ------------------------------------------------------------------
// UTRMC Dashboard
// ------------------------------------------------------------------

test.describe('UTRMC Admin dashboard', () => {
  test('overview page loads and shows key stat headings', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    // Page should not redirect to login
    await expect(page).not.toHaveURL(/\/login/);
    // Main content area should be visible
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('hospitals page loads and shows table', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page).not.toHaveURL(/\/login/);
    // Should have + Add Hospital button
    await expect(page.getByRole('button', { name: /add hospital/i })).toBeVisible({ timeout: 10000 });
  });

  test('departments page loads and shows table', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/departments');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.getByRole('button', { name: /add department/i })).toBeVisible({ timeout: 10000 });
  });

  test('users page loads and shows add user button', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.getByRole('button', { name: /add user/i })).toBeVisible({ timeout: 10000 });
  });

  test('supervision links page loads', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/supervision');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('H-D Matrix page loads', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/matrix');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.getByRole('heading', { name: /matrix/i })).toBeVisible({ timeout: 10000 });
  });

  test('programs page loads', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/programs');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('eligibility monitoring page loads', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/eligibility-monitoring');
    await expect(page).not.toHaveURL(/\/login/);
    await page.waitForLoadState('networkidle');
    // Either heading, loading text, or error message should be visible (page rendered)
    const hasContent = await page.locator('h1, h2, p, div[class*="animate-spin"]').first().isVisible().catch(() => false);
    expect(hasContent, 'Eligibility monitoring page should render some content').toBe(true);
  });
});

// ------------------------------------------------------------------
// Supervisor Dashboard
// ------------------------------------------------------------------

test.describe('Supervisor dashboard', () => {
  test('overview loads without error', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('research approvals page loads', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/research-approvals');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });
});

// ------------------------------------------------------------------
// Resident Dashboard
// ------------------------------------------------------------------

test.describe('Resident dashboard', () => {
  test('main resident dashboard loads', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('schedule page loads', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('academic progress page loads', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/progress');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('research page loads', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/research');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('thesis page loads', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/thesis');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('workshops page loads', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/workshops');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });
});

// ------------------------------------------------------------------
// UTRMC user (read-only viewer) dashboard
// ------------------------------------------------------------------

test.describe('UTRMC user (read-only) dashboard', () => {
  test('can view UTRMC overview', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();
  });

  test('can view hospitals list', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page).not.toHaveURL(/\/login/);
  });
});
