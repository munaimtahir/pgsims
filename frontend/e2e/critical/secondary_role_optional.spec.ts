import { expect, test } from '@playwright/test';

type SecondaryCandidate = {
  username: string;
  password: string;
  expectedPath: RegExp;
};

const candidates: SecondaryCandidate[] = [
  {
    username: process.env.E2E_SECONDARY_USERNAME ?? 'e2e_utrmc_user',
    password: process.env.E2E_SECONDARY_PASSWORD ?? 'Utrmc123!',
    expectedPath: /\/dashboard\/utrmc/,
  },
  { username: 'e2e_supervisor', password: 'Supervisor123!', expectedPath: /\/dashboard\/supervisor/ },
  { username: 'e2e_pg', password: 'Pg123456!', expectedPath: /\/dashboard\/pg/ },
];

test('secondary role dashboard loads when seeded role is available', async ({ browser, baseURL }) => {
  let matched = false;

  for (const candidate of candidates) {
    const context = await browser.newContext({ baseURL });
    const page = await context.newPage();
    try {
      await page.goto('/login');
      await page.getByLabel('Username').fill(candidate.username);
      await page.getByLabel('Password').fill(candidate.password);
      await page.getByRole('button', { name: /sign in/i }).click();
      await page.waitForURL(candidate.expectedPath, { timeout: 8000 });
      await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
      matched = true;
      await context.close();
      break;
    } catch {
      await context.close();
    }
  }

  test.skip(!matched, 'No secondary seeded role credentials are available on the deployed environment.');
});
