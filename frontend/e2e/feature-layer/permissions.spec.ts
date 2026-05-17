import { expect, test } from '@playwright/test';

import { uniqueToken } from './helpers/data';
import { loginAsRole } from './helpers/session';

test.describe('Feature-layer permission boundaries', () => {
  test('resident is blocked from supervisor and UTRMC surfaces', async ({ page, context }) => {
    await loginAsRole(context, page, 'resident_user');

    await page.goto('/dashboard/supervisor');
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 10_000 });

    await page.goto('/dashboard/utrmc');
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 10_000 });

    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page).toHaveURL(/\/dashboard\/(resident|pg)/, { timeout: 10_000 });
  });

  test('unauthenticated direct dashboard access redirects to login', async ({ page }) => {
    await page.goto('/dashboard/utrmc');
    await expect(page).toHaveURL(/\/login/, { timeout: 10_000 });
  });

  test('scope-limited supervisor cannot review unrelated resident logbook entry', async ({
    page,
    context,
  }) => {
    const unrelatedPatientId = uniqueToken('FL-PERM');
    const apiBaseURL = process.env.E2E_API_URL ?? 'http://127.0.0.1:8014';

    await loginAsRole(context, page, 'negative_role_user');
    await page.goto('/dashboard/resident/progress');
    const accessToken = await page.evaluate(() => window.localStorage.getItem('access_token'));
    expect(accessToken).toBeTruthy();

    const createResponse = await page.request.post(`${apiBaseURL}/api/logbook/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
      data: {
        patient_id_number: unrelatedPatientId,
        patient_name: 'Permission Scope Validation Case',
        age: 42,
        gender: 'M',
        disease_area: 'Medicine',
        diagnosis: 'Permission scope validation case',
        clinical_presentation: 'Direct API fixture',
        management_plan: 'Permission boundary fixture',
        resident_reflection: 'Validate queue isolation.',
        patient_seen_at: '2026-08-05T11:00:00Z',
      },
    });
    expect(createResponse.ok(), await createResponse.text()).toBeTruthy();

    const createdEntry = (await createResponse.json()) as { id: number };
    const submitResponse = await page.request.post(
      `${apiBaseURL}/api/logbook/${createdEntry.id}/submit/`,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
    expect(submitResponse.ok(), await submitResponse.text()).toBeTruthy();

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    const queue = page
      .locator('section')
      .filter({ has: page.getByRole('heading', { name: /Pending Logbook Reviews/i }) });
    await expect(queue.getByText(unrelatedPatientId)).toHaveCount(0);
  });

  test('UTRMC staff (read-only) cannot access admin-only mutation controls', async ({
    page,
    context,
  }) => {
    await loginAsRole(context, page, 'utrmc_staff_user');
    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /UTRMC (Dashboard|Overview)/i })).toBeVisible();
    await expect(page.getByText(/read-only for UTRMC users/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /Create Rotation Draft/i })).toHaveCount(0);
    await expect(page.getByRole('button', { name: /Verify & Issue/i })).toHaveCount(0);
  });
});
