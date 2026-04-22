import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

test.describe('Workflow gate — stabilized contract-critical flows', () => {
  test('forgot-password submits via real UI path and returns success response', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.getByLabel('Email address').fill('e2e_pg@pgsims.local');
    await page.getByRole('button', { name: /send reset link/i }).click();

    await expect(page.getByText(/password reset email sent|if an account with that email exists/i)).toBeVisible({
      timeout: 15_000,
    });
  });

  test('resident leave draft can be submitted and approved from supervisor dashboard', async ({
    context,
    page,
  }) => {
    test.setTimeout(60_000);
    const leaveReason = `Workflow leave ${Date.now()}`;

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    await expect(page.getByRole('heading', { name: 'My Schedule' })).toBeVisible({ timeout: 15_000 });
    await page.getByLabel('Leave Type').selectOption('study');
    await page.getByLabel('Start Date').fill('2026-04-10');
    await page.getByLabel('End Date').fill('2026-04-12');
    await page.getByLabel('Reason').fill(leaveReason);
    await page.getByRole('button', { name: 'Save Draft' }).click();

    await expect(page.getByText(/Leave request saved as draft\./i)).toBeVisible({ timeout: 15_000 });

    const residentLeaveCard = page.locator('.pg-card-muted').filter({ hasText: leaveReason }).first();
    await expect(residentLeaveCard).toBeVisible({ timeout: 15_000 });
    await residentLeaveCard.getByRole('button', { name: /submit for review/i }).click();
    await expect(page.getByText(/Leave request submitted for review\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');

    const supervisorLeaveCard = page.locator('.pg-card').filter({ hasText: leaveReason }).first();
    await expect(supervisorLeaveCard).toBeVisible({ timeout: 15_000 });
    await supervisorLeaveCard.getByRole('button', { name: 'Approve' }).click();
    await expect(page.getByText(/Leave request approved\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    const approvedLeaveCard = page.locator('.pg-card-muted').filter({ hasText: leaveReason }).first();
    await expect(approvedLeaveCard).toBeVisible({ timeout: 15_000 });
    await expect(approvedLeaveCard.getByText('APPROVED')).toBeVisible({ timeout: 15_000 });
  });
});
