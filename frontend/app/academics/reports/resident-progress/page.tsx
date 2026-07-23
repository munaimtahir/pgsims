'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi } from '@/lib/api/academics';
import apiClient from '@/lib/api/client';

interface ResidentReportRow {
  id: number;
  name: string;
  username: string;
}

export default function ResidentProgressReportsListPage() {
  const [residents, setResidents] = useState<ResidentReportRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getResidentProgressReportList()
      .then((data) => setResidents(data as unknown as ResidentReportRow[]))
      .catch(() => setResidents([]))
      .finally(() => setLoading(false));
  }, []);

  const handleExportCSV = () => {
    const url = `${apiClient.defaults.baseURL || ''}/api/academics/reports/resident-progress/export.csv`;
    window.open(url, '_blank');
  };

  if (loading) {
    return <div className="text-center py-8 text-sm text-slate-500">Loading residents progress reports...</div>;
  }

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Resident Progress Reports"
            description="Access training spines, supervisor assignments, and logbook category counts for registered residents."
          />
          <button
            onClick={handleExportCSV}
            className="pg-btn-secondary border-indigo-300 text-indigo-700 hover:bg-indigo-50"
          >
            Export All Progress CSV
          </button>
        </div>

        <div className="pg-card space-y-4">
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-xs uppercase text-slate-600 font-semibold">
                <tr>
                  <th className="px-4 py-3 text-left">Resident Name</th>
                  <th className="px-4 py-3 text-left">Username</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {residents.map((res) => (
                  <tr key={res.id}>
                    <td className="px-4 py-3 font-semibold text-slate-800">{res.name}</td>
                    <td className="px-4 py-3 text-slate-600">{res.username}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center space-x-3">
                        <Link
                          href={`/academics/reports/resident-progress/${res.id}`}
                          className="text-sm font-semibold text-indigo-600 hover:underline"
                        >
                          View Report
                        </Link>
                        <span className="text-slate-350">|</span>
                        <a
                          href={`${apiClient.defaults.baseURL || ''}/api/academics/reports/resident-progress/export.csv?resident_id=${res.id}`}
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
                {residents.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-center text-slate-500" colSpan={3}>
                      No resident progress reports found.
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
