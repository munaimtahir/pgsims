'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { getDashboardPathForRole } from '@/lib/rbac';
import authApi from '@/lib/api/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: Array<'RESIDENT' | 'SUPERVISOR' | 'ADMIN' | 'SUPPORT_STAFF'>;
}

const ONBOARDING_ROUTES = ['/change-password', '/complete-profile'];

export default function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, user, hasHydrated } = useAuthStore();
  const [onboardingChecked, setOnboardingChecked] = useState(false);

  const isRoleAllowed = !allowedRoles || !user || allowedRoles.includes(user.role) || user.role === 'ADMIN';

  useEffect(() => {
    if (!hasHydrated) {
      return;
    }

    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    if (!isRoleAllowed) {
      router.push(getDashboardPathForRole(user.role));
      return;
    }

    if (ONBOARDING_ROUTES.includes(pathname)) {
      setOnboardingChecked(true);
      return;
    }

    authApi
      .me()
      .then((me) => {
        if (ONBOARDING_ROUTES.includes(me.allowed_next_route) && me.allowed_next_route !== pathname) {
          router.push(me.allowed_next_route);
          return;
        }
        setOnboardingChecked(true);
      })
      .catch(() => setOnboardingChecked(true));
  }, [hasHydrated, isAuthenticated, user, isRoleAllowed, router, pathname]);

  if (!hasHydrated || !isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isRoleAllowed) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900">Redirecting</h1>
          <p className="mt-2 text-gray-600">Sending you to the correct dashboard for your role.</p>
        </div>
      </div>
    );
  }

  if (!onboardingChecked) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
