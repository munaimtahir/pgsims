'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi } from '@/lib/api/academics';
import apiClient from '@/lib/api/client';

interface SupervisorReportRow {
  id: number;
  name: string;
  username: string;
}

export default function SupervisorWorkloadReportsListPage() {
  const [supervisors, setSupervisors] = useState<SupervisorReportRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getSupervisorWorkloadReportList()
      .then((data) => setSupervisors(data as unknown as SupervisorReportRow[]))
      .catch(() => setSupervisors([]))
      .finally(() => setLoading(false));
  }, []);

  const handleExportCSV = () => {
    const url = `${apiClient.defaults.baseURL || ''}/api/academics/reports/supervisor-workload/export.csv`;
    window.open(url, '_blank');
  };

  if (loading) {
    return <div className="text-center py-8 text-sm text-slate-500">Loading supervisor reports...</div>;
  }

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Supervisor Workload Reports"
            description="Audit assigned resident counts, pending evaluation review queues, and verification metrics for teaching supervisors."
          />
          <button
            onClick={handleExportCSV}
            className="pg-btn-secondary border-indigo-300 text-indigo-700 hover:bg-indigo-50"
          >
            Export Workload CSV
          </button>
        </div>

        <div className="pg-card space-y-4">
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-xs uppercase text-slate-600 font-semibold">
                <tr>
                  <th className="px-4 py-3 text-left">Supervisor Name</th>
                  <th className="px-4 py-3 text-left">Username</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {supervisors.map((sup) => (
                  <tr key={sup.id}>
                    <td className="px-4 py-3 font-semibold text-slate-800">{sup.name}</td>
                    <td className="px-4 py-3 text-slate-600">{sup.username}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center space-x-3">
                        <Link
                          href={`/academics/reports/supervisor-workload/${sup.id}`}
                          className="text-sm font-semibold text-indigo-600 hover:underline"
                        >
                          View Workload
                        </Link>
                        <span className="text-slate-350">|</span>
                        <a
                          href={`${apiClient.defaults.baseURL || ''}/api/academics/reports/supervisor-workload/export.csv?supervisor_id=${sup.id}`}
                          target="_blank"
                          rel="noreferrer"
                          className="text-sm font-medium text-slate-650 hover:underline"
                        >
                          Export CSV
                        </a>
                      </div>
                    </td>
                  </tr>
                ))}
                {supervisors.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-center text-slate-500" colSpan={3}>
                      No supervisor workload reports found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
