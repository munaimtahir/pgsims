import { expect, type Page } from '@playwright/test';

export async function expectKpiCardValue(
  page: Page,
  label: string,
  matcher: RegExp | string
) {
  const card = page.locator('div').filter({ hasText: label }).first();
  await expect(card).toBeVisible();
  await expect(card).toContainText(matcher);
}

export async function expectTextEventually(page: Page, text: RegExp | string) {
  await expect(page.getByText(text)).toBeVisible({ timeout: 15_000 });
}
