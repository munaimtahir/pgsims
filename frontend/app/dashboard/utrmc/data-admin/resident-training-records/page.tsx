'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

export default function ImportResidentTrainingRecordsPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Import Resident Training Records</h1>
            <p className="mt-1 text-gray-500">Bulk enroll residents into training programs.</p>
          </div>
          <ImportExportPanel
            entity="resident-training-records"
            label="Resident Training Records"
            templateFile="resident_training_records.csv"
            exportResource="resident_training_records"
          />
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
