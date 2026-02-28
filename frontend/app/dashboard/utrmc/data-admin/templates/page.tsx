'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';

const TEMPLATES = [
  { name: 'Hospitals', file: 'hospitals.csv', columns: 'hospital_code*, hospital_name*, active' },
  { name: 'Departments', file: 'departments.csv', columns: 'department_code*, department_name*, active' },
  { name: 'H-D Matrix', file: 'hospital_departments.csv', columns: 'hospital_code*, department_code*, active' },
  { name: 'Supervisors', file: 'supervisors.csv', columns: 'email*, full_name*, phone, role, department_code*, hospital_code, active' },
  { name: 'Residents', file: 'residents.csv', columns: 'email*, full_name*, phone, role, pgr_id, training_start, department_code*, hospital_code, active' },
  { name: 'Supervision Links', file: 'supervisor_resident_links.csv', columns: 'supervisor_email*, resident_email*, department_code, start_date, end_date, active' },
];

export default function DataAdminTemplatesPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Import Templates</h1>
            <p className="mt-1 text-gray-500">Download CSV templates for bulk import. Fields marked * are required.</p>
          </div>
          <SectionCard title="Available Templates">
            <div className="divide-y divide-gray-200">
              {TEMPLATES.map((t) => (
                <div key={t.file} className="py-4 flex items-start justify-between gap-4">
                  <div>
                    <p className="font-medium text-gray-900">{t.name}</p>
                    <p className="text-sm text-gray-500 mt-0.5">{t.columns}</p>
                  </div>
                  <a
                    href={`/templates/${t.file}`}
                    download
                    className="flex-shrink-0 px-3 py-1.5 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700"
                  >
                    ⬇ Download
                  </a>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
