/**
 * Navigation Tests
 *
 * Verifies sidebar navigation renders correct items per role and key
 * pages can be reached through the nav menu.
 */
import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

// ------------------------------------------------------------------
// UTRMC Admin navigation
// ------------------------------------------------------------------

test.describe('UTRMC Admin sidebar navigation', () => {
  test('shows all Program Administration nav sections', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');

    const nav = page.locator('nav').first();
    await expect(nav.getByText('Hospitals')).toBeVisible();
    await expect(nav.getByText('Departments')).toBeVisible();
    await expect(nav.getByText('H-D Matrix')).toBeVisible();
    await expect(nav.getByText('Users')).toBeVisible();
    await expect(nav.getByText('Supervision Links')).toBeVisible();
    await expect(nav.getByText('Programmes')).toBeVisible();
  });

  test('sidebar Hospitals link navigates to hospitals page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.locator('nav').first().getByText('Hospitals').click();
    await expect(page).toHaveURL(/\/dashboard\/utrmc\/hospitals/);
  });

  test('sidebar Departments link navigates to departments page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.locator('nav').first().getByText('Departments').click();
    await expect(page).toHaveURL(/\/dashboard\/utrmc\/departments/);
  });

  test('sidebar Users link navigates to users page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.locator('nav').first().getByText('Users').click();
    await expect(page).toHaveURL(/\/dashboard\/utrmc\/users/);
  });

  test('sidebar Supervision Links navigates to supervision page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.locator('nav').first().getByText('Supervision Links').click();
    await expect(page).toHaveURL(/\/dashboard\/utrmc\/supervision/);
  });

  test('sidebar Programmes navigates to programs page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.locator('nav').first().getByText('Programmes').click();
    await expect(page).toHaveURL(/\/dashboard\/utrmc\/programs/);
  });

  test('UTRMC admin does NOT see Supervisor or Resident nav sections', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    const nav = page.locator('nav').first();
    await expect(nav.getByText('My Dashboard')).not.toBeVisible();
    await expect(nav.getByText('My Residents')).not.toBeVisible();
  });

  test('sidebar collapse button toggles sidebar width', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    // Sidebar is expanded by default
    await expect(page.getByText('PGSIMS')).toBeVisible();
    // Click collapse
    await page.getByRole('button', { name: /collapse sidebar/i }).click();
    // PGSIMS text should hide when collapsed
    await expect(page.getByText('PGSIMS')).not.toBeVisible({ timeout: 3000 });
  });
});

// ------------------------------------------------------------------
// Supervisor navigation
// ------------------------------------------------------------------

test.describe('Supervisor sidebar navigation', () => {
  test('shows Supervisory Dashboard sections', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');

    const nav = page.locator('nav').first();
    await expect(nav.getByText('Overview').first()).toBeVisible();
    await expect(nav.getByText('Research Approvals')).toBeVisible();
    await expect(nav.getByText('My Residents')).toBeVisible();
  });

  test('supervisor does NOT see Program Administration nav', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    const nav = page.locator('nav').first();
    await expect(nav.getByText('H-D Matrix')).not.toBeVisible();
    await expect(nav.getByText('Supervision Links')).not.toBeVisible();
  });

  test('Research Approvals link navigates correctly', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    await page.locator('nav').first().getByText('Research Approvals').click();
    await expect(page).toHaveURL(/\/dashboard\/supervisor\/research-approvals/);
  });
});

// ------------------------------------------------------------------
// Resident navigation
// ------------------------------------------------------------------

test.describe('Resident sidebar navigation', () => {
  test('shows Resident Portfolio sections', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    const nav = page.locator('nav').first();
    await expect(nav.getByText('My Dashboard')).toBeVisible();
    await expect(nav.getByText('My Schedule')).toBeVisible();
    await expect(nav.getByText('Academic Progress')).toBeVisible();
    await expect(nav.getByText('Research')).toBeVisible();
    await expect(nav.getByText('Thesis')).toBeVisible();
    await expect(nav.getByText('Workshops')).toBeVisible();
  });

  test('resident does NOT see UTRMC admin nav', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    const nav = page.locator('nav').first();
    await expect(nav.getByText('H-D Matrix')).not.toBeVisible();
    await expect(nav.getByText('Hospitals')).not.toBeVisible();
  });

  test('My Schedule link navigates to schedule page', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await page.locator('nav').first().getByText('My Schedule').click();
    await expect(page).toHaveURL(/\/dashboard\/resident\/schedule/);
  });

  test('Research link navigates to research page', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await page.locator('nav').first().getByText('Research').click();
    await expect(page).toHaveURL(/\/dashboard\/resident\/research/);
  });
});
