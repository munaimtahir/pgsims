'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function PGNotificationsPage() {
  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
            <p className="mt-2 text-gray-600">View system notifications.</p>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <p className="text-gray-500">No notifications at this time.</p>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
