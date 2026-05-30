import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test.describe('Flexible Column Mapping Import E2E', () => {
  const residentEmail = `flex.resident.${Date.now()}@example.com`;

  test.afterAll(async () => {
    // Phase 11: Cleanup dummy data after test using django management/shell
    const { execSync } = require('child_process');
    try {
      execSync(
        `docker compose --env-file ../.env -f ../docker/docker-compose.yml exec -T backend python manage.py shell -c "from sims.users.models import User; User.objects.filter(email='${residentEmail}').delete(); print('Cleaned up flex resident.')"`
      );
      console.log('Successfully cleaned up E2E resident dummy data.');
    } catch (e: any) {
      console.error('Failed to clean up E2E resident dummy data:', e.message);
    }
  });

  test('utrmc admin can import residents via flexible column mapping', async ({
    page,
    context,
  }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/onboarding');

    await expect(page.getByRole('heading', { name: 'Bulk Setup & Import/Export' })).toBeVisible({
      timeout: 15_000,
    });

    // 1. Select the new Flexible mapping tab
    await page.getByRole('button', { name: 'Upload Custom File & Map Columns' }).click();
    await expect(page.getByText('Flexible Column Mapping Import')).toBeVisible();

    // 2. Select target from dropdown
    const targetSelect = page.locator('[data-testid="select-import-target"]');
    await expect(targetSelect).toBeVisible();
    await targetSelect.selectOption('residents');

    // 3. Upload a custom CSV file
    const csvContent = [
      'CustomEmail,CustomName,CustomSpecialty,CustomYear,CustomStart,CustomHospital,CustomDept,CustomSupervisor',
      `${residentEmail},Dr. E2E Flex Resident,medicine,1,2026-01-01,AH,MED,supervisor_user@pgsims.local`,
    ].join('\n');

    const csvBuffer = Buffer.from(csvContent);
    await page.locator('input[type="file"]').setInputFiles({
      name: 'custom_residents_e2e.csv',
      mimeType: 'text/csv',
      buffer: csvBuffer,
    });

    // Wait for header detection
    await expect(page.getByText(/File "custom_residents_e2e.csv" successfully parsed/i)).toBeVisible({
      timeout: 15_000,
    });

    // 4. Continue to mapping
    await page.getByRole('button', { name: /Continue to Mapping/i }).click();
    await expect(page.getByText('PGSIMS Field')).toBeVisible();

    // 5. Select mapping dropdowns
    // Auto-suggestions should match email -> CustomEmail, full_name -> CustomName
    const emailSelect = page.locator('[data-testid="select-mapping-email"]');
    await expect(emailSelect).toHaveValue('CustomEmail');

    const nameSelect = page.locator('[data-testid="select-mapping-full_name"]');
    await expect(nameSelect).toHaveValue('CustomName');

    // Map remaining required fields manually
    await page.locator('[data-testid="select-mapping-specialty"]').selectOption('CustomSpecialty');
    await page.locator('[data-testid="select-mapping-year"]').selectOption('CustomYear');
    await page.locator('[data-testid="select-mapping-training_start"]').selectOption('CustomStart');
    await page.locator('[data-testid="select-mapping-hospital_code"]').selectOption('CustomHospital');
    await page.locator('[data-testid="select-mapping-department_code"]').selectOption('CustomDept');
    await page.locator('[data-testid="select-mapping-supervisor_email"]').selectOption('CustomSupervisor');

    // Verify mapping validation state says ready
    await expect(page.getByText('Mapping Valid & Ready to Preview')).toBeVisible();

    // 6. Execute dry run
    await Promise.all([
      page.waitForResponse((res) =>
        res.url().includes('/api/bulk/flexible/dry-run/') && res.request().method() === 'POST'
      ),
      page.getByRole('button', { name: /Execute Dry-Run & Preview/i }).click(),
    ]);

    // 7. Verify dry run results & preview
    await expect(page.getByText('Dry-Run Validation Summary')).toBeVisible();
    await expect(page.locator('span.block.text-2xl').nth(1)).toHaveText('1'); // Valid rows
    await expect(page.locator('span.block.text-2xl').nth(2)).toHaveText('0'); // Failures

    // Verify preview row
    await expect(page.getByText(residentEmail)).toBeVisible();

    // 8. Strict mode and Final import
    await page.locator('[data-testid="radio-mode-strict"]').check();
    
    // Set up alert dialog confirm before clicking
    page.once('dialog', async (dialog) => {
      expect(dialog.message()).toContain('final import');
      await dialog.accept();
    });

    // Run import apply
    await Promise.all([
      page.waitForResponse((res) =>
        res.url().includes('/api/bulk/flexible/apply/') && res.request().method() === 'POST'
      ),
      page.getByRole('button', { name: /Apply Final Import/i }).click(),
    ]);

    // Verify final success banner
    await expect(page.getByText(/Import succeeded! Successfully imported 1 records./i)).toBeVisible({
      timeout: 15_000,
    });

    // 9. Navigate to users list and verify imported user appears
    await page.goto('/dashboard/utrmc/users');
    await expect(page.getByText(residentEmail).first()).toBeVisible({ timeout: 15_000 });
  });
});
