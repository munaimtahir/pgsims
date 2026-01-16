'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function PGResultsPage() {
  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Results</h1>
            <p className="mt-2 text-gray-600">View your exam results and grades.</p>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <p className="text-gray-500">Results functionality coming soon.</p>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
