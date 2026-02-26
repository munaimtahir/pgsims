import { expect, test } from '@playwright/test';
import { loginAs } from './helpers/auth';

test('Admin import + reports export + UTRMC KPI dashboard', async ({ page, context }) => {
  const suffix = `${Date.now()}`.slice(-6);
  const supervisorUsername = `e2e_sup_${suffix}`;
  const residentUsername = `e2e_pg_${suffix}`;
  const departmentCode = `E2E${suffix}`;

  await loginAs(context, page, 'admin');
  await page.goto('/dashboard/admin/bulk-import');

  await page.selectOption('select', 'departments');
  await page.locator('input[type="file"]').setInputFiles({
    name: 'departments.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from(`code,name,description,active\n${departmentCode},E2E Department ${suffix},E2E import,true\n`),
  });
  await page.getByRole('button', { name: /^import$/i }).click();
  await expect(page.getByText(/import completed/i)).toBeVisible();

  await page.selectOption('select', 'supervisors');
  await page.locator('input[type="file"]').setInputFiles({
    name: 'supervisors.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from(
      `name,username,specialty,email\nSupervisor ${suffix},${supervisorUsername},Surgery,${supervisorUsername}@example.com\n`
    ),
  });
  await page.getByRole('button', { name: /^import$/i }).click();
  await expect(page.getByText(/import completed/i)).toBeVisible();

  await page.selectOption('select', 'residents');
  await page.locator('input[type="file"]').setInputFiles({
    name: 'residents.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from(
      `name,username,year,specialty,supervisor_username,email\nResident ${suffix},${residentUsername},1,Surgery,${supervisorUsername},${residentUsername}@example.com\n`
    ),
  });
  await page.getByRole('button', { name: /^import$/i }).click();
  await expect(page.getByText(/import completed/i)).toBeVisible();

  await page.goto('/dashboard/admin/reports');
  await page.selectOption('select', 'residents-roster');
  await page.getByRole('button', { name: /^run$/i }).click();
  await expect(page.getByText(residentUsername)).toBeVisible();

  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: /^csv$/i }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toContain('residents-roster');

  await loginAs(context, page, 'utrmc_user');
  await page.goto('/dashboard/utrmc');
  await expect(page.getByTestId('utrmc-dashboard-title')).toBeVisible();
  await expect(page.getByText('Pending Logbook Queue')).toBeVisible();
});
