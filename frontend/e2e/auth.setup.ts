import fs from 'fs';
import path from 'path';
import { expect, test as setup } from '@playwright/test';

import { loginAs } from './helpers/auth';

const authFile = 'e2e/.auth/admin.json';

setup('admin login and persist storage state', async ({ context, page }) => {
  await page.goto('/login');
  await loginAs(context, page, 'admin');
  await page.goto('/dashboard/utrmc');
  await expect(page).toHaveURL(/\/dashboard\/utrmc/);

  fs.mkdirSync(path.dirname(authFile), { recursive: true });
  await page.context().storageState({ path: authFile });
});
