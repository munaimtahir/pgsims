import { expect, test } from '@playwright/test';

import { loginAsRole } from './helpers/session';

test.describe('Feature-layer regression smoke', () => {
  test('resident core pages still load', async ({ page, context }) => {
    await loginAsRole(context, page, 'resident_user');

    await page.goto('/dashboard/resident');
    await expect(page.getByRole('heading', { name: /Resident Dashboard/i })).toBeVisible();

    await page.goto('/dashboard/resident/progress');
    await expect(page).toHaveURL(/\/dashboard\/resident$/);
  });

  test('supervisor entry routes still load', async ({ page, context }) => {
    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: /Supervisor Dashboard/i })).toBeVisible();

    await page.goto('/dashboard/supervisor/research-approvals');
    await expect(page).toHaveURL(/\/dashboard\/supervisor$/);
  });

  test('UTRMC management pages still load', async ({ page, context }) => {
    await loginAsRole(context, page, 'utrmc_admin_user');

    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /Admin Dashboard/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page.getByRole('button', { name: /Add Hospital/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/departments');
    await expect(page.getByRole('button', { name: /Add Department/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/supervision');
    await expect(page).toHaveURL(/\/supervision$/);

    await page.goto('/dashboard/utrmc/eligibility-monitoring');
    await expect(page).toHaveURL(/\/dashboard\/utrmc$/);
  });
});
