'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

export default function ImportRotationTemplatesPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Import Rotation Templates</h1>
            <p className="mt-1 text-gray-500">Bulk import rotation templates per training program.</p>
          </div>
          <ImportExportPanel
            entity="rotation-templates"
            label="Rotation Templates"
            templateFile="rotation_templates.csv"
            exportResource="rotation_templates"
          />
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
