import fs from 'fs';
import path from 'path';
import { expect, test as setup } from '@playwright/test';

const authFile = 'e2e/.auth/admin.json';

setup('admin login and persist storage state', async ({ page }) => {
  const username = process.env.E2E_ADMIN_USERNAME ?? 'e2e_admin';
  const password = process.env.E2E_ADMIN_PASSWORD ?? 'Admin123!';

  await page.goto('/login');
  await page.getByLabel('Username').fill(username);
  await page.getByLabel('Password').fill(password);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL(/\/dashboard\//, { timeout: 20000 });
  await expect(page).toHaveURL(/\/dashboard\/admin/);

  fs.mkdirSync(path.dirname(authFile), { recursive: true });
  await page.context().storageState({ path: authFile });
});
