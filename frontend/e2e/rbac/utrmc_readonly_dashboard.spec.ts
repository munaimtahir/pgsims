import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('UTRMC read-only oversight', () => {
  test('utrmc_user sees read-only boundaries on active UTRMC pages', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_user');

    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page.getByRole('heading', { name: 'Hospitals' })).toBeVisible();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.getByRole('button', { name: /\+ add hospital/i })).toHaveCount(0);
    await expect(page.getByRole('button', { name: /^edit$/i })).toHaveCount(0);

    await page.goto('/dashboard/utrmc/departments');
    await expect(page.getByRole('heading', { name: 'Departments' })).toBeVisible();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.getByRole('button', { name: /\+ add department/i })).toHaveCount(0);

    await page.goto('/dashboard/utrmc/users');
    await expect(page.getByRole('heading', { name: 'Users' })).toBeVisible();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.getByRole('button', { name: /\+ add user/i })).toHaveCount(0);

    await page.goto('/dashboard/utrmc/matrix');
    await expect(page.getByRole('heading', { name: 'Hospital–Department Matrix' })).toBeVisible();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.locator('tbody button').first()).toBeDisabled();

    await page.goto('/dashboard/utrmc/supervision');
    await expect(page.getByRole('heading', { name: 'Supervision Links' })).toBeVisible();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.getByRole('button', { name: /\+ add link/i })).toHaveCount(0);

    await page.goto('/dashboard/utrmc/hod');
    await expect(page.getByRole('heading', { name: 'HOD Assignments' })).toBeVisible();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.getByRole('button', { name: /\+ add hod/i })).toHaveCount(0);

    await page.goto('/dashboard/utrmc/programs');
    await expect(page.getByRole('heading', { name: 'Programmes' })).toBeVisible();
    await page.locator('ul.space-y-1 > li button').first().click();
    await expect(page.getByTestId('readonly-notice')).toBeVisible();
    await expect(page.getByRole('button', { name: /save policy/i })).toHaveCount(0);
    await expect(page.getByRole('button', { name: /\+ add template/i })).toHaveCount(0);
  });

  test('utrmc_user is redirected away from supervisor route', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/supervisor/research-approvals');
    await page.waitForURL(/\/dashboard\/utrmc/);
    await expect(page).toHaveURL(/\/dashboard\/utrmc/);
  });
});
