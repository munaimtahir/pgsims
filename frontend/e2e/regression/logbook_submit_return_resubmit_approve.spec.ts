import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test('PG -> Supervisor return -> PG resubmit -> approve workflow', async ({ page, context }) => {
  const caseTitle = `E2E logbook ${Date.now()}`;
  const promptReplies = ['Please add more details.', 'Approved.'];

  page.on('dialog', async (dialog) => {
    if (dialog.type() === 'confirm') {
      await dialog.accept();
      return;
    }
    if (dialog.type() === 'prompt') {
      await dialog.accept(promptReplies.shift() ?? '');
      return;
    }
    await dialog.dismiss();
  });

  await loginAs(context, page, 'pg');
  await page.goto('/dashboard/pg/logbook');
  await page.getByTestId('logbook-form-case-title').fill(caseTitle);
  await page.getByTestId('logbook-form-date').fill('2026-02-26');
  await page.getByTestId('logbook-form-location').fill('Ward A');
  await page.getByTestId('logbook-form-history').fill('Post-op review');
  await page.getByTestId('logbook-form-management').fill('Management plan draft');
  await page.getByTestId('logbook-form-topic').fill('Surgery');
  await page.getByTestId('logbook-save-button').click();
  await expect(page.getByText(/draft logbook entry created successfully/i)).toBeVisible();
  const pgRow = page.locator('tr', { hasText: caseTitle }).first();
  await expect(pgRow).toBeVisible();
  await pgRow.getByText('Submit').click();
  await expect(page.getByText(/submitted for supervisor review/i)).toBeVisible();

  await loginAs(context, page, 'supervisor');
  await page.goto('/dashboard/supervisor/logbooks');
  const supervisorRow = page.locator('tr', { hasText: caseTitle }).first();
  await expect(supervisorRow).toBeVisible();
  await supervisorRow.getByText('Return').click();

  await loginAs(context, page, 'pg');
  await page.goto('/dashboard/pg/logbook');
  const returnedRow = page.locator('tr', { hasText: caseTitle }).first();
  await expect(returnedRow).toContainText('Returned');
  await expect(returnedRow).toContainText('Please add more details.');
  await returnedRow.getByText('Edit').click();
  await page.getByTestId('logbook-form-management').fill('Updated management action with details.');
  await page.getByTestId('logbook-save-button').click();
  await page.locator('tr', { hasText: caseTitle }).first().getByText('Submit').click();

  await loginAs(context, page, 'supervisor');
  await page.goto('/dashboard/supervisor/logbooks');
  await page.locator('tr', { hasText: caseTitle }).first().getByText('Approve').click();

  await loginAs(context, page, 'pg');
  await page.goto('/dashboard/pg/logbook');
  const approvedRow = page.locator('tr', { hasText: caseTitle }).first();
  await expect(approvedRow).toContainText('Approved');
  await expect(approvedRow.getByText('Edit')).toHaveCount(0);
});
