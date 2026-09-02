import { expect, type Locator, test } from '@playwright/test';

import { expectTextEventually } from './helpers/assertions';
import { uniqueToken } from './helpers/data';
import { loginAsRole } from './helpers/session';
import { installDialogResponder } from './helpers/ui';

function toIsoDate(date: Date): string {
  return date.toISOString().slice(0, 10);
}

async function selectOptionByText(select: Locator, matcher: RegExp) {
  const value = await select.locator('option').evaluateAll(
    (options, sourcePattern) => {
      const pattern = new RegExp(sourcePattern, 'i');
      const found = options.find((opt) => pattern.test(opt.textContent || ''));
      return found instanceof HTMLOptionElement ? found.value : '';
    },
    matcher.source
  );
  expect(value, `No option matched ${matcher}`).toBeTruthy();
  await select.selectOption(value);
}

test.describe('Feature-layer rotations phase-1 workflow', () => {
  test('apply, return/approve decisions, activate, complete, and UTRMC verify completion', async ({
    page,
    context,
  }) => {
    test.setTimeout(60_000);

    const returnNote = uniqueToken('FL rotation return');
    const startA = new Date();
    startA.setUTCDate(startA.getUTCDate() - 45);
    const endA = new Date();
    endA.setUTCDate(endA.getUTCDate() - 15);

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /UTRMC (Dashboard|Overview)/i })).toBeVisible();

    const residentSelect = page.getByLabel('Resident');
    const placementSelect = page.getByLabel('Placement');

    await selectOptionByText(residentSelect, /Feature Resident/i);
    await selectOptionByText(placementSelect, /Medicine/i);
    await page.getByLabel('Start Date').fill(toIsoDate(startA));
    await page.getByLabel('End Date').fill(toIsoDate(endA));
    await page.getByLabel('Notes').fill(returnNote);
    await page.getByRole('button', { name: /Create Rotation Draft/i }).click();
    await expectTextEventually(page, /Rotation draft created\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/schedule');
    const returnTimelineCard = page.locator('div.rounded-xl').filter({ hasText: returnNote }).first();
    await expect(returnTimelineCard).toBeVisible({ timeout: 15_000 });
    await returnTimelineCard.getByRole('button', { name: /Submit for Review/i }).click();
    await expectTextEventually(page, /Rotation submitted for supervisor review\./i);

    installDialogResponder(page, ['Please rotate next month after current commitments.']);
    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');

    const returnQueueCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Pending Rotation Requests/i }) })
      .locator('div.bg-white')
      .filter({ hasText: returnNote })
      .first();
    await expect(returnQueueCard).toBeVisible({ timeout: 15_000 });
    await returnQueueCard.getByRole('button', { name: /Return to Resident/i }).click();
    await expectTextEventually(page, /Rotation returned to resident\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/schedule');
    const returnedScheduleCard = page.locator('div.rounded-xl').filter({ hasText: returnNote }).first();
    await expect(returnedScheduleCard).toContainText(/RETURNED/i);
    await expect(returnedScheduleCard).toContainText(/Please rotate next month/i);
    await returnedScheduleCard.getByRole('button', { name: /Submit for Review/i }).click();
    await expectTextEventually(page, /Rotation submitted for supervisor review\./i);

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    const approvedQueueCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Pending Rotation Requests/i }) })
      .locator('div.bg-white')
      .filter({ hasText: returnNote })
      .first();
    await expect(approvedQueueCard).toBeVisible({ timeout: 15_000 });
    await approvedQueueCard.getByRole('button', { name: /Approve Rotation/i }).evaluate((el) => {
      (el as HTMLButtonElement).click();
    });

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');

    const apiBaseURL = process.env.E2E_API_URL ?? 'http://127.0.0.1:8014';
    const accessToken = await page.evaluate(() => window.localStorage.getItem('access_token'));
    expect(accessToken).toBeTruthy();
    const authHeaders = { Authorization: `Bearer ${accessToken}` };

    const listResponse = await page.request.get(`${apiBaseURL}/api/rotations/`, {
      headers: authHeaders,
    });
    expect(listResponse.ok()).toBeTruthy();
    const listPayload = (await listResponse.json()) as {
      results?: Array<{ id: number; notes?: string | null }>;
    };
    const targetRotation = (listPayload.results || []).find((rotation) =>
      (rotation.notes || '').includes(returnNote)
    );
    expect(targetRotation, `Missing approved rotation for note ${returnNote}`).toBeTruthy();

    const utrmcApproveResponse = await page.request.post(
      `${apiBaseURL}/api/rotations/${targetRotation!.id}/utrmc-approve/`,
      { headers: authHeaders }
    );
    expect(utrmcApproveResponse.ok()).toBeTruthy();
    await page.reload();

    const approvedOpsCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Approved Rotations/i }) })
      .locator('div.bg-white')
      .filter({ hasText: returnNote })
      .first();
    await expect(approvedOpsCard).toBeVisible({ timeout: 15_000 });
    await approvedOpsCard.getByRole('button', { name: /Activate Rotation/i }).click();

    const activeOpsCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Active Rotations/i }) })
      .locator('div.bg-white')
      .filter({ hasText: returnNote })
      .first();
    await expect(activeOpsCard).toBeVisible({ timeout: 15_000 });
    const markCompleteButton = activeOpsCard.getByRole('button', { name: /Mark Complete/i });
    await expect(markCompleteButton).toBeVisible({ timeout: 15_000 });
    await markCompleteButton.click();

    const completionQueueCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Certificate Verification Queues/i }) })
      .locator('div.bg-white')
      .filter({ hasText: /Feature Resident/i })
      .first();
    await expect(completionQueueCard).toBeVisible({ timeout: 15_000 });
    await completionQueueCard.getByRole('button', { name: /Verify Completion/i }).click();
    await expectTextEventually(page, /Rotation completion verified\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/schedule');
    const completedScheduleCard = page.locator('div.rounded-xl').filter({ hasText: returnNote }).first();
    await expect(completedScheduleCard).toContainText(/COMPLETED/i);
    await expect(completedScheduleCard).toContainText(/Medicine/i);

    await page.goto('/dashboard/resident');
    await expect(page.getByText(/Rotations verified:\s*\d+\/1/i)).toBeVisible({ timeout: 15_000 });
  });
});
