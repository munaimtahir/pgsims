import { expect, test } from '@playwright/test';

test('login page renders and registration is disabled', async ({ page }) => {
  await page.goto('/login');
  await expect(page.getByRole('heading', { name: /sign in to sims/i })).toBeVisible();
  await expect(page.getByText(/registration is disabled/i)).toBeVisible();
  await page.goto('/register');
  await expect(page.getByRole('heading', { name: /registration is disabled/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /back to login/i })).toHaveAttribute('href', '/login');
});
