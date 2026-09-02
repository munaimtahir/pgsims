import type { BrowserContext, Page } from '@playwright/test';

import { loginAsFeatureUser, type FeatureLayerUserKey } from '../../helpers/auth';

export type FeatureRole = FeatureLayerUserKey;
const APP_BASE_URL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';

export const FEATURE_ROLE_HOME: Record<FeatureRole, string> = {
  resident_user: '/dashboard/resident',
  supervisor_user: '/dashboard/supervisor',
  hod_user: '/dashboard/supervisor',
  utrmc_admin_user: '/dashboard/utrmc',
  utrmc_staff_user: '/dashboard/utrmc',
  negative_role_user: '/dashboard/resident',
};

export async function loginAsRole(
  context: BrowserContext,
  page: Page,
  role: FeatureRole
) {
  await context.clearCookies();
  await page.goto(APP_BASE_URL, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => {
    window.localStorage.clear();
    window.sessionStorage.clear();
  });
  await loginAsFeatureUser(context, page, role);
}
