import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

test('admin live feed updates after PG logbook submit workflow', async ({ page, context }) => {
  test.setTimeout(120000);
  const caseTitle = `E2E live feed ${Date.now()}`;
  page.once('dialog', async (dialog) => {
    if (dialog.type() === 'confirm') {
      await dialog.accept();
      return;
    }
    await dialog.dismiss();
  });

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
  await expect(pgRow).toBeVisible();
  const submitResponsePromise = page.waitForResponse(
    (response) =>
      response.url().includes('/api/logbook/my/') &&
      response.url().includes('/submit/') &&
      response.request().method() === 'POST' &&
      response.status() === 200
  );
  await pgRow.getByRole('button', { name: 'Submit' }).click();
  const submitResponse = await submitResponsePromise;
  const submittedEntry = (await submitResponse.json()) as { id: number };
  await expect(page.getByText(/submitted for supervisor review/i)).toBeVisible();

  await loginAs(context, page, 'admin');
  await page.goto('/dashboard/admin/analytics');
  await page.getByTestId('analytics-tab-live').click();
  await expect(page.getByRole('heading', { name: 'Analytics' })).toBeVisible();

  const isFilteredLiveResponse = (response: { url: () => string; request: () => { method: () => string }; status: () => number }) => {
    if (
      !response.url().includes('/api/analytics/events/live') ||
      response.request().method() !== 'GET' ||
      response.status() !== 200
    ) {
      return false;
    }
    const url = new URL(response.url());
    return (
      url.searchParams.get('event_type_prefix') === 'logbook.case.submitted' &&
      url.searchParams.get('entity_type') === 'logbook_entry'
    );
  };
  const firstLiveResponsePromise = page.waitForResponse(
    (response) =>
      isFilteredLiveResponse(response)
  );
  await page.getByTestId('analytics-live-filter-event-prefix').fill('logbook.case.submitted');
  await page.getByTestId('analytics-live-filter-entity-type').fill('logbook_entry');
  const firstLiveResponse = await firstLiveResponsePromise;
  const firstPayload = (await firstLiveResponse.json()) as {
    events?: Array<{ entity_id?: string | number; event_type?: string }>;
  };

  await expect
    .poll(
      async () => {
        const foundInFirstPayload = (firstPayload.events || []).some(
          (event) =>
            String(event.entity_id ?? '') === String(submittedEntry.id) &&
            event.event_type === 'logbook.case.submitted'
        );
        if (foundInFirstPayload) return true;
        try {
          const response = await page.waitForResponse(
            (candidate) => isFilteredLiveResponse(candidate),
            { timeout: 8000 }
          );
          const payload = (await response.json()) as {
            events?: Array<{ entity_id?: string | number; event_type?: string }>;
          };
          return (payload.events || []).some(
            (event) =>
              String(event.entity_id ?? '') === String(submittedEntry.id) &&
              event.event_type === 'logbook.case.submitted'
          );
        } catch {
          return false;
        }
      },
      { timeout: 45000 }
    )
    .toBe(true);

  await expect(page.getByRole('columnheader', { name: /occurred at/i })).toBeVisible();
  await expect(page.getByRole('columnheader', { name: /event type/i })).toBeVisible();
  await expect(page.getByRole('columnheader', { name: /actor role/i })).toBeVisible();
  const submittedEventLink = page.getByRole('link', { name: String(submittedEntry.id), exact: true });
  await expect(submittedEventLink).toBeVisible({ timeout: 30000 });
});
