import { expect, test } from '@playwright/test';
import { loginAs } from './helpers/auth';

test('PG creates/submits case and supervisor reviews', async ({ page, context }) => {
  const title = `E2E case ${Date.now()}`;

  await loginAs(context, page, 'pg');
  await page.goto('/dashboard/pg/cases');
  await page.getByPlaceholder('Case title').fill(title);
  await page.locator('input[name="date_encountered"]').fill('2026-02-26');
  await page.locator('input[name="patient_age"]').fill('32');
  await page.getByPlaceholder('Chief complaint').fill('Abdominal pain');
  await page.getByPlaceholder('History of present illness').fill('Pain for two days');
  await page.getByPlaceholder('Physical examination').fill('Tenderness in RLQ');
  await page.getByPlaceholder('Management plan').fill('Imaging and observation');
  await page.getByPlaceholder('Clinical reasoning').fill('Likely appendicitis');
  await page.getByPlaceholder('Learning points').fill('Correlate exam with imaging');
  await page.getByRole('button', { name: /^save$/i }).click();
  await expect(page.getByText(/case created as draft/i)).toBeVisible();
  const row = page.locator('div.flex.items-center.justify-between.rounded.border.bg-white.p-3', { hasText: title }).first();
  await expect(row).toBeVisible();
  await row.getByRole('button', { name: 'Submit' }).click();

  await loginAs(context, page, 'supervisor');
  await page.goto('/dashboard/supervisor/cases');
  page.once('dialog', async (dialog) => dialog.accept('Needs more detail.'));
  const pendingRow = page.locator('div.flex.items-center.justify-between.rounded.border.p-3', { hasText: title }).first();
  await pendingRow.getByRole('button', { name: 'Needs revision' }).click();

  await loginAs(context, page, 'pg');
  await page.goto('/dashboard/pg/cases');
  const pgRevisionRow = page.locator('div.flex.items-center.justify-between.rounded.border.bg-white.p-3', { hasText: title }).first();
  await expect(pgRevisionRow).toContainText('needs_revision');
  await pgRevisionRow.getByRole('button', { name: 'Submit' }).click();
  await expect(page.getByText(/case submitted for review/i)).toBeVisible();

  await loginAs(context, page, 'supervisor');
  await page.goto('/dashboard/supervisor/cases');
  page.once('dialog', async (dialog) => dialog.accept('Approved.'));
  await page.locator('div.flex.items-center.justify-between.rounded.border.p-3', { hasText: title }).first().getByRole('button', { name: 'Approve' }).click();
  await expect(page.getByText(/case approved/i)).toBeVisible();
});
