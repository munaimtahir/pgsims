'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function SupervisorPGsPage() {
  return (
    <ProtectedRoute allowedRoles={['supervisor']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My PGs</h1>
            <p className="mt-2 text-gray-600">View your assigned postgraduate students.</p>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <p className="text-gray-500">PG list functionality coming soon.</p>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
