import { expect, type Locator, test } from '@playwright/test';

import { expectTextEventually } from './helpers/assertions';
import { uniqueToken } from './helpers/data';
import { loginAsRole } from './helpers/session';
import { installDialogResponder } from './helpers/ui';

async function readNumericCardValue(card: Locator): Promise<number> {
  const raw = (await card.locator('p').first().textContent()) || '0';
  const parsed = Number(raw.replace(/[^\d]/g, ''));
  return Number.isNaN(parsed) ? 0 : parsed;
}

test.describe('Feature-layer role-aware dashboards', () => {
  test('resident, supervisor, HOD, and UTRMC dashboards surface updated operational counters', async ({
    page,
    context,
  }) => {
    const uniquePatientId = uniqueToken('FL-DASH');
    installDialogResponder(page, ['Approved for dashboard refresh.']);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');

    const residentMetricSection = page.locator('section').filter({ hasText: /Logbook Total/i }).first();
    const approvedBeforeCard = residentMetricSection.locator('div').filter({ hasText: /Approved/i }).first();
    const approvedBefore = await readNumericCardValue(approvedBeforeCard);

    const draftSection = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Logbook Entry \(Draft\)/i }) })
      .first();
    await draftSection.getByPlaceholder(/Patient ID number/i).fill(uniquePatientId);
    await draftSection.locator('input[type="datetime-local"]').first().fill('2026-07-10T10:00');
    await draftSection.getByPlaceholder('Diagnosis').fill('Dashboard consistency case');
    await draftSection.getByPlaceholder('Management plan').fill('Observe and approve for counter checks');
    await draftSection.getByRole('button', { name: /Save Logbook Draft/i }).click();
    await expectTextEventually(page, /Logbook draft saved\./i);

    const residentEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /My Logbook Entries/i }) })
      .locator('div.border')
      .filter({ hasText: uniquePatientId })
      .first();
    await residentEntry.getByRole('button', { name: /^Submit$/i }).click();
    await expectTextEventually(page, /Logbook entry submitted\./i);

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: /Supervisor Dashboard/i })).toBeVisible();
    await expect(page.getByText('Assigned Residents', { exact: true })).toBeVisible();
    await expect(page.getByText('Pending Logbook', { exact: true })).toBeVisible();
    await expect(page.getByText('Pending Rotations', { exact: true })).toBeVisible();

    const queueEntry = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Pending Logbook Reviews/i }) })
      .locator('div.bg-white')
      .filter({ hasText: uniquePatientId })
      .first();
    await queueEntry.getByRole('button', { name: /^Approve$/i }).click();
    await expectTextEventually(page, /Logbook entry approved\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');
    const approvedAfterCard = page
      .locator('section')
      .filter({ hasText: /Logbook Total/i })
      .first()
      .locator('div')
      .filter({ hasText: /Approved/i })
      .first();
    const approvedAfter = await readNumericCardValue(approvedAfterCard);
    expect(approvedAfter).toBeGreaterThanOrEqual(approvedBefore + 1);

    await page.goto('/dashboard/resident');
    await expect(page.getByText(/Operational Readiness/i)).toBeVisible();
    await expect(page.getByText(/Logbook threshold:/i)).toBeVisible();

    await loginAsRole(context, page, 'hod_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByText(/Operational Snapshot \(HOD Scope\)/i)).toBeVisible();
    await expect(page.getByText('Pending Logbook', { exact: true })).toBeVisible();
    await expect(page.getByText('Pending Synopsis', { exact: true })).toBeVisible();

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /UTRMC Overview/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: /Cross-Department Readiness/i })).toBeVisible();
    await expect(page.getByText(/Pending Synopsis Reviews/i)).toBeVisible();
    await expect(page.getByText(/Pending Thesis Reviews/i)).toBeVisible();
    await expect(page.getByText(/Pending Rotation Verifications/i)).toBeVisible();
  });
});
