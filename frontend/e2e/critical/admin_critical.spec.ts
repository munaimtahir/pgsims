import { expect, test } from '@playwright/test';

test('admin dashboard loads with key widgets', async ({ page }) => {
  await page.goto('/dashboard/admin');
  await expect(page.getByRole('heading', { name: 'Admin Dashboard' })).toBeVisible();
  await expect(page.getByText('Quick Actions')).toBeVisible();
  await expect(page.getByText('Unread Notifications')).toBeVisible();
});

test('admin can open reports catalog and run preview', async ({ page }) => {
  await page.goto('/dashboard/admin/reports');
  await expect(page.getByRole('heading', { name: 'Admin Reports' })).toBeVisible();

  const options = page.locator('select option');
  expect(await options.count()).toBeGreaterThan(0);

  await page.getByRole('button', { name: /^run$/i }).click();
  await expect(page.getByRole('heading', { name: 'Preview' })).toBeVisible();
});
