import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('UTRMC Read-only Dashboard', () => {
  test('utrmc_user can load dashboard and sees no mutation UI', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc');

    await expect(page.getByTestId('utrmc-dashboard-title')).toBeVisible();
    await expect(page.getByTestId('utrmc-access-mode')).toContainText('Read-only oversight');
    await expect(page.getByTestId('utrmc-readonly-note')).toContainText(
      'Mutation actions are hidden'
    );

    await expect(page.getByText(/pending logbook queue/i)).toBeVisible();
  });

  test('utrmc_user is redirected away from supervisor route', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/supervisor/logbooks');
    await page.waitForURL(/\/dashboard\/utrmc/);
    await expect(page.getByTestId('utrmc-dashboard-title')).toBeVisible();
  });
});
