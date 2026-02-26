import type { BrowserContext, Page } from '@playwright/test';

export type E2ERole = 'pg' | 'supervisor' | 'admin' | 'utrmc_user' | 'utrmc_admin';

function base64Url(input: string) {
  return Buffer.from(input)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
}

function fakeJwt(role: E2ERole) {
  const header = base64Url(JSON.stringify({ alg: 'none', typ: 'JWT' }));
  const payload = base64Url(
    JSON.stringify({
      sub: String(role === 'pg' ? 10 : role === 'supervisor' ? 20 : 30),
      role,
      exp: Math.floor(Date.now() / 1000) + 60 * 60,
    })
  );
  return `${header}.${payload}.sig`;
}

function parseJwtExp(token: string): number {
  const payload = JSON.parse(
    Buffer.from(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8')
  ) as { exp?: number };
  return payload.exp ?? Math.floor(Date.now() / 1000) + 3600;
}

function authStorage(role: E2ERole) {
  const user = {
    id: role === 'pg' ? 10 : role === 'supervisor' ? 20 : role === 'utrmc_user' ? 40 : 50,
    username: role,
    email: `${role}@example.com`,
    first_name: role.toUpperCase(),
    last_name: 'User',
    full_name: `${role.toUpperCase()} User`,
    role,
  };

  return {
    state: {
      user,
      accessToken: fakeJwt(role),
      refreshToken: 'mock-refresh',
      isAuthenticated: true,
    },
    version: 0,
  };
}

export async function seedAuth(context: BrowserContext, page: Page, role: E2ERole) {
  const store = authStorage(role);
  const accessToken = store.state.accessToken;
  const exp = parseJwtExp(accessToken);

  await context.addCookies([
    {
      name: 'pgsims_access_token',
      value: accessToken,
      url: 'http://localhost:3000',
    },
    {
      name: 'pgsims_user_role',
      value: role,
      url: 'http://localhost:3000',
    },
    {
      name: 'pgsims_access_exp',
      value: String(exp),
      url: 'http://localhost:3000',
    },
  ]);

  await page.addInitScript((payload) => {
    localStorage.setItem('auth-storage', JSON.stringify(payload));
    localStorage.setItem('access_token', payload.state.accessToken);
    localStorage.setItem('refresh_token', payload.state.refreshToken);
    localStorage.setItem('user', JSON.stringify(payload.state.user));
  }, store);
}
