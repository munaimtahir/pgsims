import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

test.describe('Workflow gate — bulk setup workspace', () => {
  test('utrmc overview no longer exposes the bulk setup workspace', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');

    await expect(page.getByRole('heading', { name: /UTRMC (Dashboard|Overview)/ })).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByText('Bulk Setup & Import/Export')).toHaveCount(0);
    await expect(page.getByText('Open onboarding tools')).toHaveCount(0);
  });
});
