const COOKIE_MAX_AGE = 60 * 60 * 24; // mirror short-lived access session only (1 day max)
const ACCESS_EXP_COOKIE = 'pgsims_access_exp';
const ACCESS_COOKIE = 'pgsims_access_token';
const ROLE_COOKIE = 'pgsims_user_role';

function cookieSecurityAttrs() {
  // `Secure` would block local http://localhost cookies, so enable it outside local dev.
  const isBrowser = typeof window !== 'undefined';
  const isLocalhost =
    isBrowser &&
    (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
  return isLocalhost ? 'SameSite=Lax' : 'SameSite=Lax; Secure';
}

function setCookie(name: string, value: string, maxAge = COOKIE_MAX_AGE) {
  if (typeof document === 'undefined') return;
  document.cookie = `${name}=${encodeURIComponent(value)}; Path=/; Max-Age=${maxAge}; ${cookieSecurityAttrs()}`;
}

function clearCookie(name: string) {
  if (typeof document === 'undefined') return;
  document.cookie = `${name}=; Path=/; Max-Age=0; ${cookieSecurityAttrs()}`;
}

function decodeJwtPayload(token: string): Record<string, unknown> | null {
  const parts = token.split('.');
  if (parts.length < 2) return null;
  try {
    const payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    const padded = payload + '='.repeat((4 - (payload.length % 4)) % 4);
    const decoded = atob(padded);
    const parsed = JSON.parse(decoded);
    return parsed && typeof parsed === 'object' ? (parsed as Record<string, unknown>) : null;
  } catch {
    return null;
  }
}

function getAccessExpiryEpoch(accessToken: string): number | null {
  const payload = decodeJwtPayload(accessToken);
  const exp = payload?.exp;
  return typeof exp === 'number' && Number.isFinite(exp) ? exp : null;
}

export function syncAuthCookies(params: {
  accessToken?: string | null;
  role?: string | null;
}) {
  const { accessToken, role } = params;
  if (accessToken) {
    setCookie(ACCESS_COOKIE, accessToken);
    const exp = getAccessExpiryEpoch(accessToken);
    if (exp) {
      const ttl = Math.max(1, Math.min(COOKIE_MAX_AGE, exp - Math.floor(Date.now() / 1000)));
      setCookie(ACCESS_EXP_COOKIE, String(exp), ttl);
    } else {
      clearCookie(ACCESS_EXP_COOKIE);
    }
  } else {
    clearCookie(ACCESS_COOKIE);
    clearCookie(ACCESS_EXP_COOKIE);
  }

  if (role) {
    setCookie(ROLE_COOKIE, role);
  } else {
    clearCookie(ROLE_COOKIE);
  }
}

export function clearAuthCookies() {
  clearCookie(ACCESS_COOKIE);
  clearCookie(ACCESS_EXP_COOKIE);
  clearCookie(ROLE_COOKIE);
}
