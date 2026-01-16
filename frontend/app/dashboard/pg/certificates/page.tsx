'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';

export default function PGCertificatesPage() {
  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Certificates</h1>
            <p className="mt-2 text-gray-600">View and manage your certificates</p>
          </div>

          <SectionCard title="Certificates">
            <EmptyState
              title="Certificates API Not Available"
              description="The certificates REST API endpoint is not yet available. This feature will be implemented when the backend API is ready."
            />
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                When available, this page will display:
              </p>
              <ul className="list-disc list-inside mt-2 text-sm text-gray-600 space-y-1">
                <li>List of your certificates</li>
                <li>Certificate download links</li>
                <li>Certificate status and expiry dates</li>
                <li>Certificate compliance tracking</li>
              </ul>
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
