'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';

export default function PGLogbookPage() {
  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Logbook</h1>
            <p className="mt-2 text-gray-600">Manage your logbook entries</p>
          </div>

          <SectionCard title="Logbook Entries">
            <EmptyState
              title="PG Logbook CRUD API Not Available"
              description="The REST API endpoints for creating, editing, and listing PG logbook entries are not yet available. Currently, only supervisor verification endpoints exist."
            />
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-2">
                Available features:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Supervisors can verify pending logbook entries</li>
                <li>View pending verifications (supervisor view)</li>
              </ul>
              <p className="text-sm text-gray-600 mt-4 mb-2">
                When the PG logbook API is available, this page will support:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Creating new logbook entries</li>
                <li>Editing draft entries</li>
                <li>Viewing your submitted entries</li>
                <li>Submitting entries for verification</li>
              </ul>
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
