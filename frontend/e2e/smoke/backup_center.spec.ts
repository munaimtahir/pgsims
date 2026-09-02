import { test, expect } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('[smoke] Backup Center', () => {
  test('Super Admin (admin) can open Backup Center and see all controls', async ({ page, context }) => {
    await loginAs(context, page, 'admin');

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    await page.goto(`${appBase}/dashboard/utrmc/backup`);

    await expect(page.getByRole('heading', { name: 'Backup Center' })).toBeVisible();
    await expect(page.getByText('Create Regular System Backup')).toBeVisible();
    await expect(page.getByText('Create Full Server Recovery Backup')).toBeVisible();
    await expect(page.getByText('Google Drive Backup')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Connect Google Drive' })).toBeVisible();
    await expect(page.getByText('Backup History')).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Restore Wizard' })).toBeVisible();
    await expect(page.getByText('Audit Log')).toBeVisible();
  });

  test('UTRMC Admin can open Backup Center but cannot see restore or disaster recovery controls', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');

    const appBase = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
    await page.goto(`${appBase}/dashboard/utrmc/backup`);

    await expect(page.getByRole('heading', { name: 'Backup Center' })).toBeVisible();
    await expect(page.getByText('Create Regular System Backup')).toBeVisible();
    await expect(page.getByText('Create Full Server Recovery Backup')).not.toBeVisible();
    await expect(page.getByText('Restore Wizard')).not.toBeVisible();
    await expect(page.getByText('Google Drive Backup')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Connect Google Drive' })).not.toBeVisible();
    await expect(page.getByText('Backup History')).toBeVisible();
    await expect(page.getByText('Audit Log')).toBeVisible();
  });
});
