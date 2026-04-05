import type { BrowserContext, Page } from '@playwright/test';

export type E2ERole = 'pg' | 'supervisor' | 'admin' | 'utrmc_user' | 'utrmc_admin';

type AuthPayload = {
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

const CREDENTIALS: Record<E2ERole, { username: string; password: string }> = {
  pg: { username: 'e2e_pg', password: 'Pg123456!' },
  supervisor: { username: 'e2e_supervisor', password: 'Supervisor123!' },
  admin: { username: 'e2e_admin', password: 'Admin123!' },
  utrmc_user: { username: 'e2e_utrmc_user', password: 'Utrmc123!' },
  utrmc_admin: { username: 'e2e_utrmc_admin', password: 'UtrmcAdmin123!' },
};

const authCache = new Map<E2ERole, AuthPayload>();

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

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function applyAuthPayload(
  context: BrowserContext,
  page: Page,
  appBaseURL: string,
  payload: AuthPayload
) {
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

export async function loginAs(context: BrowserContext, page: Page, role: E2ERole) {
  const appBaseURL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
  const apiCandidates = Array.from(
    new Set(
      [
        process.env.E2E_API_URL ?? 'http://127.0.0.1:8014',
        appBaseURL,
      ].filter((value): value is string => Boolean(value && value.trim()))
    )
  );
  const credentials = CREDENTIALS[role];
  const cachedPayload = authCache.get(role);

  if (cachedPayload && parseExp(cachedPayload.access) > Math.floor(Date.now() / 1000) + 60) {
    await applyAuthPayload(context, page, appBaseURL, cachedPayload);
    return;
  }

  let response: Awaited<ReturnType<typeof page.request.post>> | null = null;
  let lastError: unknown = null;

  for (const apiBaseURL of apiCandidates) {
    try {
      for (let attempt = 0; attempt < 3; attempt += 1) {
        response = await page.request.post(`${apiBaseURL}/api/auth/login/`, {
          data: credentials,
        });
        if (response.ok()) {
          break;
        }
        if (response.status() === 429) {
          const retryAfterHeader = response.headers()['retry-after'];
          const retrySeconds = Number.parseInt(retryAfterHeader ?? '3', 10);
          await sleep((Number.isNaN(retrySeconds) ? 3 : retrySeconds) * 1000);
          continue;
        }
        break;
      }
      if (response?.ok()) {
        break;
      }
      lastError = new Error(`Login failed via ${apiBaseURL}: ${response?.status()} ${await response?.text()}`);
    } catch (error: unknown) {
      lastError = error;
    }
  }

  if (!response || !response.ok()) {
    const reason = lastError instanceof Error ? lastError.message : String(lastError ?? 'unknown error');
    throw new Error(`Login failed for ${role}. Tried: ${apiCandidates.join(', ')}. Last error: ${reason}`);
  }
  const payload = (await response.json()) as AuthPayload;
  authCache.set(role, payload);
  await applyAuthPayload(context, page, appBaseURL, payload);
}
