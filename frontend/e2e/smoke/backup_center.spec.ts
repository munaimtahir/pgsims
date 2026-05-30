import { test, expect } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('[smoke] Backup Center', () => {
  test('utrmc_admin can open Backup & Restore Center and see key controls', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    await page.goto(`${appBase}/dashboard/utrmc/backup`);

    await expect(page.getByRole('heading', { name: 'Backup & Restore Center' })).toBeVisible();
    await expect(page.getByText('Create Regular System Backup')).toBeVisible();
    await expect(page.getByText('Create Full Server Recovery Backup')).toBeVisible();
    await expect(page.getByText('Backup History')).toBeVisible();
    await expect(page.getByText('Restore Wizard')).toBeVisible();
    await expect(page.getByText('Restore is Super Admin only.')).toBeVisible();
    await expect(page.getByText('Audit Log')).toBeVisible();
  });
});
