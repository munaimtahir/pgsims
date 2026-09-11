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

  test('resident leave draft can be submitted and approved from canonical leave workflow', async ({
    context,
    page,
  }) => {
    test.setTimeout(60_000);
    const leaveReason = `Workflow leave ${Date.now()}`;

    await loginAs(context, page, 'pg');
    await page.goto('/academics/leave-requests/new');

    await expect(page.getByRole('heading', { name: 'New Leave Request' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText('Training Record', { exact: true })).toBeVisible({ timeout: 15_000 });
    await page.locator('select').nth(0).selectOption({ index: 1 });
    await page.locator('select').nth(1).selectOption('study');
    await page.locator('input[type="date"]').nth(0).fill('2026-04-10');
    await page.locator('input[type="date"]').nth(1).fill('2026-04-12');
    await page.locator('textarea').fill(leaveReason);
    await page.getByRole('button', { name: /Create Leave Request \(DRAFT\)/i }).click();

    await expect(page.getByRole('heading', { name: /Leave Request #/ })).toBeVisible({ timeout: 15_000 });
    const leaveUrl = page.url();
    const leaveId = leaveUrl.split('/').pop();
    expect(leaveId).toMatch(/^\d+$/);

    await page.getByRole('button', { name: 'Submit for Approval' }).click();
    await expect(page.getByText('SUBMITTED')).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'supervisor');
    await page.goto(`/academics/leave-requests/${leaveId}`);

    await expect(page.getByRole('heading', { name: /Leave Request #/ })).toBeVisible({ timeout: 15_000 });
    await page.getByRole('button', { name: 'Approve' }).click();
    await expect(page.getByText('APPROVED')).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'pg');
    await page.goto(`/academics/leave-requests/${leaveId}`);

    await expect(page.getByText('APPROVED')).toBeVisible({ timeout: 15_000 });
  });
});
