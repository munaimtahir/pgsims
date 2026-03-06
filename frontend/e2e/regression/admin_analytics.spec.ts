import { expect, test } from '@playwright/test';

import { loginAs } from './helpers/auth';

test('admin live feed updates after PG logbook submit workflow', async ({ page, context }) => {
  const caseTitle = `E2E live feed ${Date.now()}`;

  await loginAs(context, page, 'admin');
  await page.goto('/dashboard/admin/analytics');
  await page.getByTestId('analytics-tab-live').click();
  await expect(page.getByText('Analytics')).toBeVisible();
  const beforeCount = await page.locator('text=logbook.case.submitted').count();

  await loginAs(context, page, 'pg');
  await page.goto('/dashboard/pg/logbook');
  await page.getByTestId('logbook-form-case-title').fill(caseTitle);
  await page.getByTestId('logbook-form-date').fill('2026-02-27');
  await page.getByTestId('logbook-form-location').fill('Ward A');
  await page.getByTestId('logbook-form-history').fill('Workflow event source');
  await page.getByTestId('logbook-form-management').fill('Submit for analytics live feed');
  await page.getByTestId('logbook-form-topic').fill('Surgery');
  await page.getByTestId('logbook-save-button').click();
  await expect(page.getByText(/draft logbook entry created successfully/i)).toBeVisible();
  const pgRow = page.locator('tr', { hasText: caseTitle }).first();
  await pgRow.getByText('Submit').click();
  await expect(page.getByText(/submitted for supervisor review/i)).toBeVisible();

  await loginAs(context, page, 'admin');
  await page.goto('/dashboard/admin/analytics');
  await page.getByTestId('analytics-tab-live').click();
  await page.getByTestId('analytics-live-filter-event-prefix').fill('logbook.case');
  await page.waitForTimeout(8000);

  const afterCount = await page.locator('text=logbook.case.submitted').count();
  expect(afterCount).toBeGreaterThan(beforeCount);
});
