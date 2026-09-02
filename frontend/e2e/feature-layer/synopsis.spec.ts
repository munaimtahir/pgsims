import { expect, test } from '@playwright/test';

import { expectTextEventually } from './helpers/assertions';
import { resetFeatureResidentSubmissionState } from './helpers/seed';
import { loginAsRole } from './helpers/session';
import { makeUploadFile } from './helpers/uploads';

test.describe('Feature-layer synopsis workflow', () => {
  test.beforeEach(() => {
    resetFeatureResidentSubmissionState();
  });

  test('resident submits complete synopsis package and UTRMC issues certificate', async ({
    page,
    context,
  }) => {
    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');

    const synopsisCard = page
      .locator('div.bg-white')
      .filter({ has: page.getByRole('heading', { name: /Synopsis Submission/i }) })
      .first();

    await expect(synopsisCard.getByText(/^Synopsis Proposal$/)).toBeVisible();
    await expect(synopsisCard.getByText(/^Synopsis Ethics Sheet$/)).toBeVisible();

    await synopsisCard.getByRole('button', { name: /Submit Synopsis Submission/i }).click();
    await expectTextEventually(page, /Failed to submit synopsis package\./i);

    await synopsisCard
      .locator('input[type="file"]')
      .nth(0)
      .setInputFiles(makeUploadFile('synopsis-proposal.pdf', 'Synopsis proposal draft'));
    await expectTextEventually(page, /synopsis document uploaded\./i);

    await synopsisCard.getByRole('button', { name: /Submit Synopsis Submission/i }).click();
    await expectTextEventually(page, /Failed to submit synopsis package\./i);

    await synopsisCard
      .locator('input[type="file"]')
      .nth(1)
      .setInputFiles(makeUploadFile('synopsis-ethics.pdf', 'Ethics compliance attachment'));
    await expectTextEventually(page, /synopsis document uploaded\./i);

    const submitSynopsisButton = synopsisCard.getByRole('button', { name: /Submit Synopsis Submission/i });
    await expect(submitSynopsisButton).toBeEnabled();
    await submitSynopsisButton.click({ timeout: 5_000 }).catch(() => {});
    await expect(synopsisCard).toContainText(/SUBMITTED|UNDER REVIEW/i);

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');

    const synopsisQueueCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Certificate Verification Queues/i }) })
      .locator('div.bg-white')
      .filter({ hasText: /Feature Resident/i })
      .filter({ hasText: /SYNOPSIS/i })
      .first();
    await expect(synopsisQueueCard).toBeVisible({ timeout: 15_000 });
    await synopsisQueueCard.getByRole('button', { name: /Verify & Issue/i }).click();
    await expectTextEventually(page, /synopsis submission verified\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');
    const verifiedSynopsisCard = page
      .locator('div.bg-white')
      .filter({ has: page.getByRole('heading', { name: /Synopsis Submission/i }) })
      .first();
    await expect(verifiedSynopsisCard).toContainText(/CERTIFICATE ISSUED/i);
  });
});
