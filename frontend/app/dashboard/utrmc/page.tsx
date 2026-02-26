'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuthStore } from '@/store/authStore';

export default function UTRMCDashboardPage() {
  const { user } = useAuthStore();
  const isReadOnly = user?.role === 'utrmc_user';

  return (
    <ProtectedRoute allowedRoles={['utrmc_user', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 data-testid="utrmc-dashboard-title" className="text-3xl font-bold text-gray-900">UTRMC Dashboard</h1>
          <p className="text-gray-600">
            Oversight dashboard area is enabled. Pages will be added without changing route structure.
          </p>
          <div data-testid="utrmc-access-panel" className="rounded-md border border-gray-200 bg-white p-4">
            <p data-testid="utrmc-access-mode" className="text-sm font-medium text-gray-900">
              Access Mode: {isReadOnly ? 'Read-only oversight' : 'UTRMC admin'}
            </p>
            <p data-testid="utrmc-readonly-note" className="mt-1 text-sm text-gray-600">
              {isReadOnly
                ? 'Mutation actions are hidden for utrmc_user accounts.'
                : 'Admin approvals are handled in workflow-specific pages or backend/admin tools. This dashboard remains non-mutating.'}
            </p>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
