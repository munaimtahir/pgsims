'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

export default function ImportTrainingProgramsPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Import Training Programs</h1>
            <p className="mt-1 text-gray-500">Bulk import training program definitions.</p>
          </div>
          <ImportExportPanel
            entity="training-programs"
            label="Training Programs"
            templateFile="training_programs.csv"
            exportResource="training_programs"
          />
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
