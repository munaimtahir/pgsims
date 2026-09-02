'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuthStore } from '@/store/authStore';
import { getDashboardPathForRole } from '@/lib/rbac';

/**
 * Dashboard redirect hub - redirects to role-specific dashboard
 */
export default function DashboardPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const isSupportStaff = user?.role === 'SUPPORT_STAFF';

  useEffect(() => {
    if (user && user.role !== 'SUPPORT_STAFF') {
      router.replace(getDashboardPathForRole(user.role));
    }
  }, [user, router]);

  return (
    <ProtectedRoute>
      {isSupportStaff ? (
        <div className="pg-page space-y-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">Support Staff Dashboard</h1>
            <p className="mt-2 text-sm text-slate-600">
              Restricted support-staff shell. Administrative setup and canonical mutation modules remain hidden.
            </p>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="pg-card">
              <h2 className="pg-section-title">My Access</h2>
              <p className="mt-3 text-sm text-slate-600">
                This role is limited to profile completion and read-only operational support.
              </p>
            </div>
            <div className="pg-card">
              <h2 className="pg-section-title">Available Actions</h2>
              <div className="mt-3 flex flex-wrap gap-3">
                <Link href="/complete-profile" className="pg-btn-primary">Complete Profile</Link>
                <Link
                  href="/change-password"
                  className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700"
                >
                  Change Password
                </Link>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Redirecting to dashboard...</p>
          </div>
        </div>
      )}
    </ProtectedRoute>
  );
}
