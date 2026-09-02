/**
 * Navigation helper — go to canonical page for each role.
 */
import type { Page } from '@playwright/test';
import { expect } from '@playwright/test';

export const ROLE_HOME: Record<string, string> = {
  admin: '/dashboard/utrmc',
  utrmc_admin: '/dashboard/utrmc',
  utrmc_user: '/dashboard/utrmc',
  supervisor: '/dashboard/supervisor',
  faculty: '/dashboard/supervisor',
  pg: '/dashboard/resident',
  resident: '/dashboard/resident',
};

export const ROLE_FORBIDDEN: Record<string, string[]> = {
  pg: ['/dashboard/utrmc', '/dashboard/supervisor'],
  supervisor: ['/dashboard/utrmc', '/dashboard/pg'],
  utrmc_user: ['/dashboard/supervisor', '/dashboard/pg'],
  utrmc_admin: ['/dashboard/supervisor', '/dashboard/pg'],
  admin: [], // admin can access all
};

export async function gotoHome(page: Page, role: string) {
  const home = ROLE_HOME[role] ?? '/dashboard';
  await page.goto(home);
}

export async function expectPageHeading(page: Page, text: string | RegExp) {
  await expect(page.getByRole('heading', { level: 1 }).or(page.getByRole('heading', { level: 2 })).first()).toContainText(text);
}

export async function expectNoConsoleErrors(page: Page) {
  const errors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  return errors;
}
