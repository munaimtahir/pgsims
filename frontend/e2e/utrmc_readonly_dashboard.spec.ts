import { expect, test } from '@playwright/test';
import { seedAuth } from './helpers/auth';

test.describe('UTRMC Read-only Dashboard', () => {
  test('utrmc_user can load dashboard and sees no mutation UI', async ({ page, context }) => {
    await seedAuth(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc');

    await expect(page.getByTestId('utrmc-dashboard-title')).toBeVisible();
    await expect(page.getByTestId('utrmc-access-mode')).toContainText('Read-only oversight');
    await expect(page.getByTestId('utrmc-readonly-note')).toContainText(
      'Mutation actions are hidden'
    );

    await expect(page.getByRole('button', { name: /approve|return|reject|submit|save|delete/i })).toHaveCount(0);
  });

  test('utrmc_user is redirected away from supervisor route', async ({ page, context }) => {
    await seedAuth(context, page, 'utrmc_user');
    await page.goto('/dashboard/supervisor/logbooks');
    await page.waitForURL(/\/dashboard\/utrmc/);
    await expect(page.getByTestId('utrmc-dashboard-title')).toBeVisible();
  });
});

