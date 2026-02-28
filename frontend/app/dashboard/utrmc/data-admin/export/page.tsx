'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ImportExportPanel from '@/components/ui/ImportExportPanel';

const EXPORT_ENTITIES = [
  { entity: 'hospitals', label: 'Hospitals', exportResource: 'hospitals' },
  { entity: 'departments', label: 'Departments', exportResource: 'departments' },
  { entity: 'matrix', label: 'H-D Matrix', exportResource: 'matrix' },
  { entity: 'supervisors', label: 'Supervisors', exportResource: 'supervisors' },
  { entity: 'residents', label: 'Residents', exportResource: 'residents' },
  { entity: 'links', label: 'Supervision Links', exportResource: 'supervision_links' },
];

export default function DataAdminExportPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Export Data</h1>
            <p className="mt-1 text-gray-500">Download full data exports as CSV or Excel.</p>
          </div>
          {EXPORT_ENTITIES.map(({ entity, label, exportResource }) => (
            <ImportExportPanel
              key={entity}
              entity={entity}
              label={label}
              templateFile={`${entity}.csv`}
              exportResource={exportResource}
            />
          ))}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
