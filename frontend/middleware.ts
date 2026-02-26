import { NextRequest, NextResponse } from 'next/server';

type Role = 'pg' | 'supervisor' | 'admin' | 'utrmc_user' | 'utrmc_admin';

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

function getRoleHome(role?: string | null) {
  switch (role) {
    case 'pg':
      return '/dashboard/pg';
    case 'supervisor':
      return '/dashboard/supervisor';
    case 'admin':
      return '/dashboard/admin';
    case 'utrmc_user':
    case 'utrmc_admin':
      return '/dashboard/utrmc';
    default:
      return '/login';
  }
}

function roleAllowedForPath(pathname: string, role: string | null): boolean {
  if (!role) return false;
  if (pathname.startsWith('/dashboard/pg')) return role === 'pg' || role === 'admin';
  if (pathname.startsWith('/dashboard/supervisor')) return role === 'supervisor' || role === 'admin';
  if (pathname.startsWith('/dashboard/admin')) return role === 'admin';
  if (pathname.startsWith('/dashboard/utrmc')) {
    return role === 'utrmc_user' || role === 'utrmc_admin' || role === 'admin';
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

  if (typeof jwtRole !== 'string' || isExpired(effectiveExp)) {
    const response = NextResponse.redirect(new URL('/login', request.url));
    response.cookies.delete('pgsims_access_token');
    response.cookies.delete('pgsims_user_role');
    response.cookies.delete('pgsims_access_exp');
    return response;
  }

  const role = (jwtRole ?? cookieRole) as Role | null;

  if (!roleAllowedForPath(pathname, role)) {
    const redirectUrl = new URL(getRoleHome(role), request.url);
    return NextResponse.redirect(redirectUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
