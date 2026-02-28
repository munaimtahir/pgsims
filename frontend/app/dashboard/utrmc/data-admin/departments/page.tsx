'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

export default function DataAdminDepartmentsPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Departments</h1>
            <p className="mt-1 text-gray-500">Import / export Departments data.</p>
          </div>
          <ImportExportPanel
            entity="departments"
            label="Departments"
            templateFile="departments.csv"
            exportResource="departments"
          />
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
