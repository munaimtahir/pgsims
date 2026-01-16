'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';

export default function PGRotationsPage() {
  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Rotations</h1>
            <p className="mt-2 text-gray-600">View your rotation schedule and assignments</p>
          </div>

          <SectionCard title="Rotations">
            <EmptyState
              title="Rotations API Not Available"
              description="The rotations REST API endpoint is not yet available. This feature will be implemented when the backend API is ready."
            />
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                When available, this page will display:
              </p>
              <ul className="list-disc list-inside mt-2 text-sm text-gray-600 space-y-1">
                <li>Current and upcoming rotations</li>
                <li>Rotation calendar view</li>
                <li>Department assignments</li>
                <li>Rotation evaluations</li>
              </ul>
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
