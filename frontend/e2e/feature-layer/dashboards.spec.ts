import { expect, test } from '@playwright/test';

import { loginAsRole } from './helpers/session';

test.describe('Feature-layer role-aware dashboards', () => {
  test('resident, supervisor, and admin dashboards surface canonical counters', async ({
    page,
    context,
  }) => {
    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident');
    await expect(page.getByRole('heading', { name: /Resident Dashboard/i })).toBeVisible();
    await expect(page.getByText(/My Training/i)).toBeVisible();
    await expect(page.getByText(/My Supervisor/i)).toBeVisible();

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: /Supervisor Dashboard/i })).toBeVisible();
    await expect(page.getByText(/My Residents/i)).toBeVisible();
    await expect(page.getByText(/Academic Review Queue/i)).toBeVisible();

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /Admin Dashboard/i })).toBeVisible();
    await expect(page.getByText(/Canonical Modules/i)).toBeVisible();
    await expect(page.getByText(/Training Records/i)).toBeVisible();
  });
});
