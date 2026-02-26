'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { getDashboardPathForRole } from '@/lib/rbac';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: ('pg' | 'supervisor' | 'admin' | 'utrmc_user' | 'utrmc_admin')[];
}

export default function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const router = useRouter();
  const { isAuthenticated, user, hasHydrated } = useAuthStore();

  const isRoleAllowed = !allowedRoles || !user || allowedRoles.includes(user.role) || user.role === 'admin';

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
    }
  }, [hasHydrated, isAuthenticated, user, isRoleAllowed, router]);

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

  return <>{children}</>;
}
