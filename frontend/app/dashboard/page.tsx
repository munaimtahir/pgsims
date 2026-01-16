'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuthStore } from '@/store/authStore';

/**
 * Dashboard redirect hub - redirects to role-specific dashboard
 */
export default function DashboardPage() {
  const router = useRouter();
  const { user } = useAuthStore();

  useEffect(() => {
    if (user) {
      const role = user.role;
      if (role === 'admin') {
        router.replace('/dashboard/admin');
      } else if (role === 'supervisor') {
        router.replace('/dashboard/supervisor');
      } else if (role === 'pg') {
        router.replace('/dashboard/pg');
      } else {
        router.replace('/unauthorized');
      }
    }
  }, [user, router]);

  return (
    <ProtectedRoute>
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecting to dashboard...</p>
        </div>
      </div>
    </ProtectedRoute>
  );
}
