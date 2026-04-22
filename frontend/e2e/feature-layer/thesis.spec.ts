import { expect, test } from '@playwright/test';

import { expectTextEventually } from './helpers/assertions';
import { resetFeatureResidentSubmissionState } from './helpers/seed';
import { loginAsRole } from './helpers/session';
import { makeUploadFile } from './helpers/uploads';

test.describe('Feature-layer thesis workflow', () => {
  test.beforeEach(() => {
    resetFeatureResidentSubmissionState();
  });

  test('resident submits complete thesis package and UTRMC issues certificate', async ({
    page,
    context,
  }) => {
    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');

    const thesisCard = page
      .locator('div.bg-white')
      .filter({ has: page.getByRole('heading', { name: /Thesis Submission/i }) })
      .first();

    await expect(thesisCard.getByText(/^Thesis Manuscript$/)).toBeVisible();
    await expect(thesisCard.getByText(/^Similarity Report$/)).toBeVisible();

    await thesisCard.getByRole('button', { name: /Submit Thesis Submission/i }).click();
    await expectTextEventually(page, /Failed to submit thesis package\./i);

    await thesisCard
      .locator('input[type="file"]')
      .nth(0)
      .setInputFiles(makeUploadFile('thesis-manuscript.pdf', 'Thesis manuscript v1'));
    await expectTextEventually(page, /thesis document uploaded\./i);

    await thesisCard.getByRole('button', { name: /Submit Thesis Submission/i }).click();
    await expectTextEventually(page, /Failed to submit thesis package\./i);

    await thesisCard
      .locator('input[type="file"]')
      .nth(1)
      .setInputFiles(makeUploadFile('thesis-similarity.pdf', 'Similarity report attachment'));
    await expectTextEventually(page, /thesis document uploaded\./i);

    const submitThesisButton = thesisCard.getByRole('button', { name: /Submit Thesis Submission/i });
    await expect(submitThesisButton).toBeEnabled();
    await submitThesisButton.click({ timeout: 5_000 }).catch(() => {});
    await expect(thesisCard).toContainText(/SUBMITTED|UNDER REVIEW/i);

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');

    const thesisQueueCard = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Certificate Verification Queues/i }) })
      .locator('div.bg-white')
      .filter({ hasText: /Feature Resident/i })
      .filter({ hasText: /THESIS/i })
      .first();
    await expect(thesisQueueCard).toBeVisible({ timeout: 15_000 });
    await thesisQueueCard.getByRole('button', { name: /Verify & Issue/i }).click();
    await expectTextEventually(page, /thesis submission verified\./i);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident/progress');
    const verifiedThesisCard = page
      .locator('div.bg-white')
      .filter({ has: page.getByRole('heading', { name: /Thesis Submission/i }) })
      .first();
    await expect(verifiedThesisCard).toContainText(/CERTIFICATE ISSUED/i);
  });
});
