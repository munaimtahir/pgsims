import { expect, test } from '@playwright/test';

import { loginAsRole } from './helpers/session';

test.describe('Feature-layer regression smoke', () => {
  test('resident core pages still load', async ({ page, context }) => {
    await loginAsRole(context, page, 'resident_user');

    await page.goto('/dashboard/resident');
    await expect(page.getByRole('heading', { name: /My Training Dashboard/i })).toBeVisible();

    await page.goto('/dashboard/resident/progress');
    await expect(page.getByRole('heading', { name: /^Logbook$/i })).toBeVisible();

    await page.goto('/dashboard/resident/research');
    await expect(page.getByRole('heading', { name: /^Research$/i, level: 1 })).toBeVisible();
    await expect(page.getByText(/Deferred workflow/i)).toBeVisible();

    await page.goto('/dashboard/resident/thesis');
    await expect(page.getByRole('heading', { name: /Thesis/i, level: 1 })).toBeVisible();

    await page.goto('/dashboard/resident/workshops');
    await expect(page.getByRole('heading', { name: /Workshops/i })).toBeVisible();
  });

  test('supervisor and HOD entry routes still load', async ({ page, context }) => {
    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: /Supervisor Dashboard/i })).toBeVisible();

    await page.goto('/dashboard/supervisor/research-approvals');
    await expect(page.getByRole('heading', { name: /Research Approvals/i })).toBeVisible();

    await loginAsRole(context, page, 'hod_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: /Supervisor Dashboard/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: /Today’s attention/i })).toBeVisible();
  });

  test('UTRMC management pages still load', async ({ page, context }) => {
    await loginAsRole(context, page, 'utrmc_admin_user');

    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /UTRMC (Dashboard|Overview)/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page.getByRole('button', { name: /Add Hospital/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/departments');
    await expect(page.getByRole('button', { name: /Add Department/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/supervision');
    await expect(page.getByRole('heading', { name: /Supervision Links/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/eligibility-monitoring');
    await expect(page.getByRole('heading', { name: /Eligibility/i })).toBeVisible();
  });
});
