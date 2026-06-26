import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('Flexible Column Mapping Import E2E', () => {
  test('legacy UTRMC onboarding route redirects to resident onboarding', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/onboarding');

    await expect(page).toHaveURL(/\/dashboard\/onboarding\/residents$/);
    await expect(page.getByRole('heading', { name: 'Resident Onboarding' })).toBeVisible({
      timeout: 15_000,
    });
  });
});
