'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';
import Link from 'next/link';

export default function SupervisorPGsPage() {
  return (
    <ProtectedRoute allowedRoles={['supervisor']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My PGs</h1>
            <p className="mt-2 text-gray-600">View assigned postgraduate trainees</p>
          </div>

          <SectionCard title="Assigned PGs">
            <EmptyState
              title="Assigned PG Listing API Not Available"
              description="The API endpoint for listing assigned PGs is not yet available. You can use the search functionality to find PGs."
              action={{
                label: 'Search for PGs',
                onClick: () => {
                  window.location.href = '/dashboard/search';
                },
              }}
            />
            <div className="mt-6">
              <Link
                href="/dashboard/search"
                className="text-sm text-indigo-600 hover:text-indigo-800"
              >
                Use Search to find PGs →
              </Link>
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
