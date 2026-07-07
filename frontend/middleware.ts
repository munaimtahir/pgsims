import { NextRequest, NextResponse } from 'next/server';

type Role =
  | 'ADMIN'
  | 'RESIDENT'
  | 'SUPERVISOR'
  | 'SUPPORT_STAFF';

function decodeJwtPayload(token: string | undefined): Record<string, unknown> | null {
  if (!token) return null;
  const parts = token.split('.');
  if (parts.length < 2) return null;

  try {
    const payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    const padded = payload + '='.repeat((4 - (payload.length % 4)) % 4);
    const json = atob(padded);
    return JSON.parse(json) as Record<string, unknown>;
  } catch {
    return null;
  }
}

function isExpired(expEpochSeconds: number | null): boolean {
  if (!expEpochSeconds) return true;
  return expEpochSeconds <= Math.floor(Date.now() / 1000);
}

function normalizeRole(role?: string | null): Role | null {
  switch (role) {
    case 'ADMIN':
    case 'admin':
    case 'utrmc_admin':
    case 'super_admin':
    case 'system_admin':
      return 'ADMIN';
    case 'RESIDENT':
    case 'resident':
    case 'pg':
    case 'pgr':
    case 'trainee':
      return 'RESIDENT';
    case 'SUPERVISOR':
    case 'supervisor':
    case 'faculty':
    case 'teacher':
      return 'SUPERVISOR';
    case 'SUPPORT_STAFF':
    case 'support_staff':
    case 'utrmc_user':
    case 'clerk':
    case 'office_staff':
    case 'data_entry':
      return 'SUPPORT_STAFF';
    default:
      return null;
  }
}

function getRoleHome(role?: Role | null) {
  switch (role) {
    case 'RESIDENT':
      return '/dashboard/resident';
    case 'SUPERVISOR':
      return '/dashboard/supervisor';
    case 'ADMIN':
    case 'SUPPORT_STAFF':
      return '/dashboard/utrmc';
    default:
      return '/login';
  }
}

function roleAllowedForPath(pathname: string, role: Role | null): boolean {
  if (!role) return false;
  if (pathname.startsWith('/dashboard/pg')) return role === 'RESIDENT' || role === 'ADMIN';
  if (pathname.startsWith('/dashboard/resident')) return role === 'RESIDENT' || role === 'ADMIN';
  if (pathname.startsWith('/dashboard/supervisor')) {
    return role === 'SUPERVISOR' || role === 'ADMIN';
  }
  if (pathname.startsWith('/dashboard/admin')) return role === 'ADMIN';
  if (pathname.startsWith('/dashboard/utrmc')) {
    return role === 'SUPPORT_STAFF' || role === 'ADMIN';
  }
  return true;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (!pathname.startsWith('/dashboard')) {
    return NextResponse.next();
  }

  const token = request.cookies.get('pgsims_access_token')?.value;
  if (!token) {
    const loginUrl = new URL('/login', request.url);
    return NextResponse.redirect(loginUrl);
  }

  const payload = decodeJwtPayload(token);
  const jwtRole = payload?.role ?? payload?.user_role;
  const jwtExp = typeof payload?.exp === 'number' ? payload.exp : null;
  const cookieRole = request.cookies.get('pgsims_user_role')?.value ?? null;
  const cookieExpRaw = request.cookies.get('pgsims_access_exp')?.value ?? null;
  const cookieExp = cookieExpRaw && /^-?\d+$/.test(cookieExpRaw) ? Number(cookieExpRaw) : null;
  const effectiveExp = jwtExp ?? cookieExp;

  const rawRole = typeof jwtRole === 'string' ? jwtRole : cookieRole;
  const role = normalizeRole(rawRole);

  if (!role || isExpired(effectiveExp)) {
    const response = NextResponse.redirect(new URL('/login', request.url));
    response.cookies.delete('pgsims_access_token');
    response.cookies.delete('pgsims_user_role');
    response.cookies.delete('pgsims_access_exp');
    return response;
  }

  if (!roleAllowedForPath(pathname, role)) {
    const redirectUrl = new URL(getRoleHome(role), request.url);
    return NextResponse.redirect(redirectUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
