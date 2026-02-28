'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

export default function DataAdminLinksPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Supervision Links</h1>
            <p className="mt-1 text-gray-500">Import / export Supervision Links data.</p>
          </div>
          <ImportExportPanel
            entity="supervision-links"
            label="Supervision Links"
            templateFile="supervisor_resident_links.csv"
            exportResource="supervision_links"
          />
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
