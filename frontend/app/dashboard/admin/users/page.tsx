'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';
import Link from 'next/link';

export default function AdminUsersPage() {
  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
            <p className="mt-2 text-gray-600">Manage system users</p>
          </div>

          <SectionCard title="User Management">
            <EmptyState
              title="User Management API Not Available"
              description="The user management REST API endpoint is not yet available. You can use the search functionality to locate users, or access user management through the Django admin interface."
              action={{
                label: 'Go to Search',
                onClick: () => {
                  window.location.href = '/dashboard/search';
                },
              }}
            />
            <div className="mt-6 space-y-2">
              <p className="text-sm text-gray-600">
                Alternative options:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>
                  <Link href="/dashboard/search" className="text-indigo-600 hover:text-indigo-800">
                    Use Search to find users
                  </Link>
                </li>
                <li>
                  <Link href="/dashboard/admin/audit-logs" className="text-indigo-600 hover:text-indigo-800">
                    View user activity in Audit Logs
                  </Link>
                </li>
              </ul>
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
