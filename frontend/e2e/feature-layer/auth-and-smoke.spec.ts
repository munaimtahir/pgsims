import { expect, test } from '@playwright/test';

import { FEATURE_ROLE_HOME, loginAsRole, type FeatureRole } from './helpers/session';
import { captureConsoleErrors } from './helpers/ui';

const ROLE_EXPECTATIONS: Array<{
  role: FeatureRole;
  heading: RegExp;
}> = [
  { role: 'resident_user', heading: /My Training Dashboard/i },
  { role: 'supervisor_user', heading: /Supervisor Dashboard/i },
  { role: 'hod_user', heading: /Supervisor Dashboard/i },
  { role: 'utrmc_admin_user', heading: /UTRMC (Dashboard|Overview)/i },
  { role: 'utrmc_staff_user', heading: /UTRMC (Dashboard|Overview)/i },
];

test.describe('Feature-layer auth and smoke', () => {
  test('core feature roles can login and reach their dashboard surfaces', async ({ page, context }) => {
    for (const { role, heading } of ROLE_EXPECTATIONS) {
      await loginAsRole(context, page, role);
      await page.goto(FEATURE_ROLE_HOME[role]);
      await expect(page).toHaveURL(new RegExp(FEATURE_ROLE_HOME[role].replace('/', '\\/')));
      await expect(page.getByRole('heading', { name: heading })).toBeVisible({ timeout: 15_000 });
    }
  });

  test('key feature-layer routes render without fatal console crashes', async ({ page, context }) => {
    const errors = captureConsoleErrors(page);

    await loginAsRole(context, page, 'resident_user');
    await page.goto('/dashboard/resident');
    await expect(page.getByRole('heading', { name: /My Training Dashboard/i })).toBeVisible();

    await page.goto('/dashboard/resident/progress');
    await expect(page.getByRole('heading', { name: /^Logbook$/i })).toBeVisible();

    await page.goto('/dashboard/resident/schedule');
    await expect(page.getByRole('heading', { name: /My Schedule/i })).toBeVisible();

    await loginAsRole(context, page, 'supervisor_user');
    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: /Supervisor Dashboard/i })).toBeVisible();

    await loginAsRole(context, page, 'utrmc_admin_user');
    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: /UTRMC (Dashboard|Overview)/i })).toBeVisible();

    await page.goto('/dashboard/utrmc/eligibility-monitoring');
    await expect(page.getByRole('heading', { name: /Eligibility/i })).toBeVisible();

    const fatalErrors = errors.filter((entry) => {
      if (/Failed to fetch RSC payload.*Falling back to browser navigation/i.test(entry)) {
        return false;
      }
      return /(TypeError|ReferenceError|Cannot read properties of|Unhandled runtime error)/i.test(entry);
    });
    expect(fatalErrors, `Fatal console errors detected:\n${fatalErrors.join('\n')}`).toEqual([]);
  });
});
