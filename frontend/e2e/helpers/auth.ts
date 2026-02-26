import type { BrowserContext, Page } from '@playwright/test';

export type E2ERole = 'pg' | 'supervisor' | 'admin' | 'utrmc_user' | 'utrmc_admin';

const CREDENTIALS: Record<E2ERole, { username: string; password: string }> = {
  pg: { username: 'e2e_pg', password: 'Pg123456!' },
  supervisor: { username: 'e2e_supervisor', password: 'Supervisor123!' },
  admin: { username: 'e2e_admin', password: 'Admin123!' },
  utrmc_user: { username: 'e2e_utrmc_user', password: 'Utrmc123!' },
  utrmc_admin: { username: 'e2e_utrmc_admin', password: 'UtrmcAdmin123!' },
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

export async function loginAs(context: BrowserContext, page: Page, role: E2ERole) {
  const appBaseURL = process.env.E2E_BASE_URL ?? 'http://localhost:3000';
  const apiBaseURL = process.env.E2E_API_URL ?? 'http://localhost:8000';
  const credentials = CREDENTIALS[role];
  const response = await page.request.post(`${apiBaseURL}/api/auth/login/`, {
    data: credentials,
  });
  if (!response.ok()) {
    throw new Error(`Login failed for ${role}: ${response.status()} ${await response.text()}`);
  }
  const payload = (await response.json()) as {
    user: {
      id: number;
      username: string;
      email: string;
      first_name: string;
      last_name: string;
      full_name: string;
      role: E2ERole;
    };
    access: string;
    refresh: string;
  };

  const exp = parseExp(payload.access);
  await context.addCookies([
    { name: 'pgsims_access_token', value: payload.access, url: appBaseURL },
    { name: 'pgsims_user_role', value: payload.user.role, url: appBaseURL },
    { name: 'pgsims_access_exp', value: String(exp), url: appBaseURL },
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
