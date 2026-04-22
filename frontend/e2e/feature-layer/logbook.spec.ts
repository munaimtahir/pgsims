import { expect, test } from '@playwright/test';

import { expectKpiCardValue, expectTextEventually } from './helpers/assertions';
import { uniqueToken } from './helpers/data';
import { loginAsRole } from './helpers/session';
import { installDialogResponder } from './helpers/ui';

test.describe('Feature-layer logbook workflow', () => {
  test('resident draft -> submit -> supervisor return -> resident resubmit -> supervisor approve', async ({
    page,
    context,
  }) => {
    const uniquePatientId = uniqueToken('FL-LOG');
    installDialogResponder(page, [
      'Please add clearer management detail.',
      'Approved after resubmission.',
    ]);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');

    const draftSection = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Logbook Entry \(Draft\)/i }) })
      .first();

    await draftSection.getByPlaceholder(/Patient ID number/i).fill(uniquePatientId);
    await draftSection.locator('input[type="datetime-local"]').first().fill('2026-06-15T09:30');
    await draftSection.getByPlaceholder(/Patient name/i).fill('Feature Layer Patient');
    await draftSection.locator('input[placeholder="Age"]').fill('42');
    await draftSection.getByPlaceholder('Diagnosis').fill('Complicated appendicitis');
    await draftSection.getByPlaceholder('Management plan').fill('Initial conservative management.');
    await draftSection.getByRole('button', { name: /Save Logbook Draft/i }).click();

    await expectTextEventually(page, /Logbook draft saved\./i);

    const residentEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /My Logbook Entries/i }) })
      .locator('.pg-card-muted')
      .filter({ hasText: uniquePatientId })
      .first();
    await expect(residentEntry).toBeVisible();
    await residentEntry.getByRole('button', { name: /^Submit$/i }).click();
    await expectTextEventually(page, /Logbook entry submitted\./i);
    await expect(residentEntry).toContainText(/SUBMITTED/i);

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');

    const supervisorEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Pending Logbook Reviews/i }) })
      .locator('.pg-card')
      .filter({ hasText: uniquePatientId })
      .first();
    await expect(supervisorEntry).toBeVisible({ timeout: 15_000 });
    await supervisorEntry.getByRole('button', { name: /Return with Feedback/i }).click();
    await expectTextEventually(page, /Logbook entry returned\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');
    const returnedEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /My Logbook Entries/i }) })
      .locator('.pg-card-muted')
      .filter({ hasText: uniquePatientId })
      .first();
    await expect(returnedEntry).toContainText(/RETURNED/i);
    await expect(returnedEntry).toContainText(/Please add clearer management detail\./i);
    await returnedEntry.getByRole('button', { name: /^Submit$/i }).click();
    await expectTextEventually(page, /Logbook entry submitted\./i);

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    const resubmittedEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Pending Logbook Reviews/i }) })
      .locator('.pg-card')
      .filter({ hasText: uniquePatientId })
      .first();
    await expect(resubmittedEntry).toBeVisible({ timeout: 15_000 });
    await resubmittedEntry.getByRole('button', { name: /^Approve$/i }).click();
    await expectTextEventually(page, /Logbook entry approved\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');
    const approvedEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /My Logbook Entries/i }) })
      .locator('.pg-card-muted')
      .filter({ hasText: uniquePatientId })
      .first();
    await expect(approvedEntry).toContainText(/APPROVED/i);

    await expectKpiCardValue(page, 'Approved', /\d+/);
    await expect(
      page
        .locator('section')
        .filter({ has: page.getByRole('heading', { name: /Logbook Threshold Progress/i }) })
        .getByText(/E2E Logbook Threshold Per 30 Days/i)
    ).toBeVisible();
  });
});
