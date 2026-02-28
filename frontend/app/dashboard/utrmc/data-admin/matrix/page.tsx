'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

export default function DataAdminMatrixPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">H-D Matrix</h1>
            <p className="mt-1 text-gray-500">Import / export H-D Matrix data.</p>
          </div>
          <ImportExportPanel
            entity="matrix"
            label="H-D Matrix"
            templateFile="hospital_departments.csv"
            exportResource="matrix"
          />
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
