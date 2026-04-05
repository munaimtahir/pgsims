import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

test.describe('Workflow gate — bulk setup workspace', () => {
  test('utrmc admin can dry-run hospital import from the overview workspace', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');

    await expect(page.getByRole('heading', { name: 'UTRMC Overview' })).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByRole('heading', { name: 'Bulk Setup & Import/Export' })).toBeVisible({
      timeout: 15_000,
    });

    const hospitalsCard = page
      .locator('div.rounded-2xl')
      .filter({ has: page.getByRole('heading', { name: 'Hospitals' }) })
      .first();

    await expect(hospitalsCard.getByText('Step 1')).toBeVisible();
    await expect(hospitalsCard.getByText('hospital_code *')).toBeVisible();
    await expect(hospitalsCard.getByText('hospital_name *')).toBeVisible();

    const csvBuffer = Buffer.from(
      'hospital_code,hospital_name,address,phone,email,active\nWFH,Workflow Hospital,Faisalabad,0410000000,wfh@example.com,true\n'
    );

    await hospitalsCard.locator('input[type="file"]').setInputFiles({
      name: 'hospitals.csv',
      mimeType: 'text/csv',
      buffer: csvBuffer,
    });

    await Promise.all([
      page.waitForResponse((response) =>
        response.url().includes('/api/bulk/import/hospitals/dry-run/') &&
        response.request().method() === 'POST'
      ),
      hospitalsCard.getByRole('button', { name: /dry run/i }).click(),
    ]);

    await expect(hospitalsCard.getByText(/Dry-run complete: 1 rows OK, 0 errors\./i)).toBeVisible({
      timeout: 15_000,
    });
  });
});
