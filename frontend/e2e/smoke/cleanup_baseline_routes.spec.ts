import { expect, test, type BrowserContext, type Page } from '@playwright/test';

type AuthPayload = {
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    full_name: string;
    role: string;
  };
  access: string;
  refresh: string;
};

function parseExp(token: string): number {
  try {
    const [, payload] = token.split('.');
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized + '='.repeat((4 - (normalized.length % 4)) % 4);
    const decoded = JSON.parse(Buffer.from(padded, 'base64').toString('utf-8')) as { exp?: number };
    return decoded.exp ?? Math.floor(Date.now() / 1000) + 3600;
  } catch {
    return Math.floor(Date.now() / 1000) + 3600;
  }
}

async function loginAsAdmin(context: BrowserContext, page: Page) {
  const response = await fetch('http://127.0.0.1:8014/api/auth/login/', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin123' }),
  });
  if (!response.ok) {
    throw new Error(`Admin login failed: ${response.status} ${await response.text()}`);
  }
  const payload = (await response.json()) as AuthPayload;
  const exp = parseExp(payload.access);
  await context.addCookies([
    { name: 'pgsims_access_token', value: payload.access, url: 'http://127.0.0.1:8082' },
    { name: 'pgsims_user_role', value: payload.user.role, url: 'http://127.0.0.1:8082' },
    { name: 'pgsims_access_exp', value: String(exp), url: 'http://127.0.0.1:8082' },
  ]);
  await page.addInitScript((authPayload) => {
    localStorage.setItem(
      'auth-storage',
      JSON.stringify({
        state: {
          user: authPayload.user,
          accessToken: authPayload.access,
          refreshToken: authPayload.refresh,
          isAuthenticated: true,
        },
        version: 0,
      })
    );
    localStorage.setItem('access_token', authPayload.access);
    localStorage.setItem('refresh_token', authPayload.refresh);
    localStorage.setItem('user', JSON.stringify(authPayload.user));
  }, payload);
}

test.describe('Cleanup baseline routes', () => {
  test('canonical UTRMC pages render with only the baseline admin account', async ({ page, context }) => {
    await loginAsAdmin(context, page);

    await page.goto('/dashboard/utrmc');
    await expect(page).not.toHaveURL(/\/login/);
    await expect(page.locator('main').first()).toBeVisible();

    await page.goto('/dashboard/utrmc/hospitals');
    await expect(page.getByRole('button', { name: /add hospital/i })).toBeVisible({ timeout: 10_000 });

    await page.goto('/dashboard/utrmc/departments');
    await expect(page.getByRole('button', { name: /add department/i })).toBeVisible({ timeout: 10_000 });

    await page.goto('/dashboard/utrmc/users');
    await expect(page.getByRole('button', { name: /add user/i })).toBeVisible({ timeout: 10_000 });

    await page.goto('/dashboard/utrmc/matrix');
    await expect(page.getByRole('heading', { name: /matrix/i })).toBeVisible({ timeout: 10_000 });

    await page.goto('/dashboard/utrmc/programs');
    await expect(page.getByRole('heading', { name: /programs/i })).toBeVisible({ timeout: 10_000 });

    await page.goto('/dashboard/utrmc/eligibility-monitoring');
    await expect(page.getByRole('heading', { name: /eligibility monitoring/i })).toBeVisible({ timeout: 10_000 });
  });
});
