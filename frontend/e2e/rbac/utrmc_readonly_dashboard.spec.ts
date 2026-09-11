import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('Support staff administration boundaries', () => {
  test('support staff is redirected from retired duplicate administration pages', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_user');

    for (const route of ['/dashboard/utrmc/hospitals', '/dashboard/utrmc/departments', '/dashboard/utrmc/users']) {
      await page.goto(route);
      await expect(page).not.toHaveURL(route);
      await expect(page).not.toHaveURL(/\/login/);
    }

    await page.goto('/users');
    await expect(page).toHaveURL(/\/dashboard$/);
    await expect(page).not.toHaveURL(/\/login/);
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
