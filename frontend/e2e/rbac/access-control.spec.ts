/**
 * RBAC / Access Control Tests
 *
 * Verifies each role can only access allowed routes.
 * Cross-role access must redirect to role home (not 403 in Next.js — middleware redirects).
 */
import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

// ------------------------------------------------------------------
// PG / Resident RBAC
// ------------------------------------------------------------------

test.describe('PG role access control', () => {
  test('pg cannot access UTRMC admin area — redirected to resident dashboard', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/utrmc');
    // Middleware redirects pg to /dashboard/pg → which redirects to /dashboard/resident
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 10000 });
  });

  test('pg cannot access supervisor area — redirected to resident dashboard', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 10000 });
  });

  test('pg cannot access UTRMC admin subroutes — redirected', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/utrmc/programs');
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 8000 });
  });

  test('pg can access own resident dashboard', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/);
    await expect(page.locator('nav').first()).toBeVisible();
  });
});

// ------------------------------------------------------------------
// Supervisor RBAC
// ------------------------------------------------------------------

test.describe('Supervisor role access control', () => {
  test('supervisor cannot access UTRMC area — redirected to supervisor home', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/utrmc');
    await expect(page).toHaveURL(/\/dashboard\/supervisor/, { timeout: 10000 });
  });

  test('supervisor cannot access pg/resident area', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/pg');
    await expect(page).toHaveURL(/\/dashboard\/supervisor/, { timeout: 10000 });
  });

  test('supervisor can access supervisor dashboard', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/dashboard\/supervisor/);
    await expect(page.locator('nav').first()).toBeVisible();
  });

  test('supervisor can access research approvals page', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/research-approvals');
    await expect(page).toHaveURL(/\/dashboard\/supervisor\/research-approvals/);
    // Should not redirect away
    await expect(page).not.toHaveURL(/\/login/);
  });
});

// ------------------------------------------------------------------
// UTRMC Admin RBAC
// ------------------------------------------------------------------

test.describe('UTRMC Admin role access control', () => {
  test('utrmc_admin cannot access supervisor area — redirected', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/dashboard\/utrmc/, { timeout: 10000 });
  });

  test('utrmc_admin cannot access pg area — redirected', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/pg');
    await expect(page).toHaveURL(/\/dashboard\/utrmc/, { timeout: 10000 });
  });

  test('utrmc_admin can access UTRMC dashboard pages', async ({ page, context }) => {
    const pages = [
      '/dashboard/utrmc',
      '/dashboard/utrmc/hospitals',
      '/dashboard/utrmc/departments',
      '/dashboard/utrmc/users',
      '/dashboard/utrmc/supervision',
      '/dashboard/utrmc/programs',
    ];
    for (const href of pages) {
      await loginAs(context, page, 'utrmc_admin');
      await page.goto(href);
      await expect(page).not.toHaveURL(/\/login/, { timeout: 8000 });
      await expect(page).not.toHaveURL(/\/dashboard\/supervisor/);
    }
  });
});

// ------------------------------------------------------------------
// UTRMC User (read-only) RBAC
// ------------------------------------------------------------------

test.describe('UTRMC User (read-only) access control', () => {
  test('utrmc_user can access UTRMC overview', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('nav').first()).toBeVisible();
  });

  test('utrmc_user cannot access supervisor area — redirected', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/dashboard\/utrmc/, { timeout: 10000 });
  });
});

// ------------------------------------------------------------------
// Direct URL access for unauthenticated users
// ------------------------------------------------------------------

test.describe('Direct URL access when unauthenticated', () => {
  const protectedRoutes = [
    '/dashboard/utrmc',
    '/dashboard/supervisor',
    '/dashboard/resident',
    '/dashboard/utrmc/hospitals',
    '/dashboard/utrmc/users',
  ];

  for (const route of protectedRoutes) {
    test(`unauthenticated access to ${route} redirects to /login`, async ({ page }) => {
      await page.goto(route);
      await expect(page).toHaveURL(/\/login/, { timeout: 8000 });
    });
  }
});
