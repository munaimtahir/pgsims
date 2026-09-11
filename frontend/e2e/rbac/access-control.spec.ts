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

  test('supervisor can access the canonical review queue', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/academics/review-queue');
    await expect(page).toHaveURL(/\/academics\/review-queue/);
    await expect(page).not.toHaveURL(/\/login/);
  });
});

// ------------------------------------------------------------------
// UTRMC Admin RBAC
// ------------------------------------------------------------------

test.describe('Admin role access control', () => {
  test('admin can access supervisor dashboard', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/dashboard\/supervisor/, { timeout: 10000 });
  });

  test('admin can resolve the legacy resident entry route', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/pg');
    await expect(page).toHaveURL(/\/dashboard\/resident/, { timeout: 10000 });
  });

  test('admin can access canonical administration pages', async ({ page, context }) => {
    const pages = [
      '/dashboard/utrmc',
      '/masters',
      '/users',
      '/residents',
      '/supervisors',
      '/support-staff',
      '/admins',
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

test.describe('Support staff access control', () => {
  test('support staff can access the administration overview', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('nav').first()).toBeVisible();
  });

  test('support staff cannot access supervisor area — redirected', async ({ page, context }) => {
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
