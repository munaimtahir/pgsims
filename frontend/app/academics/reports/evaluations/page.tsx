'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi } from '@/lib/api/academics';
import apiClient from '@/lib/api/client';

interface EvaluationReportRow {
  id: number;
  resident_name: string;
  supervisor_name: string | null;
  template_name: string;
  program_name: string | null;
  status: string;
  score: string | null;
  max_score: string | null;
  pending_age: number | null;
}

export default function EvaluationReportPage() {
  const [reportData, setReportData] = useState<EvaluationReportRow[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters state
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  const load = () => {
    setLoading(true);
    const params: Record<string, string> = {};
    if (statusFilter) params.status = statusFilter;
    if (dateFrom) params.date_from = dateFrom;
    if (dateTo) params.date_to = dateTo;

    academicsApi
      .getEvaluationReport(params)
      .then((data) => setReportData(data as unknown as EvaluationReportRow[]))
      .catch(() => setReportData([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, dateFrom, dateTo]);

  const handleExportCSV = () => {
    const qparams = new URLSearchParams();
    if (statusFilter) qparams.append('status', statusFilter);
    if (dateFrom) qparams.append('date_from', dateFrom);
    if (dateTo) qparams.append('date_to', dateTo);

    const url = `${apiClient.defaults.baseURL || ''}/api/academics/reports/evaluations/export.csv?${qparams.toString()}`;
    window.open(url, '_blank');
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR', 'RESIDENT']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Evaluation & Review Reports"
            description="Audit evaluation scores, templates, departments, and pending review age metrics."
          />
          <button
            onClick={handleExportCSV}
            className="pg-btn-secondary border-indigo-300 text-indigo-700 hover:bg-indigo-50"
          >
            Export CSV
          </button>
        </div>

        {/* Filters Form */}
        <div className="pg-card flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="pg-input py-1.5 text-sm"
            >
              <option value="">All Statuses</option>
              <option value="DRAFT">DRAFT</option>
              <option value="SUBMITTED">SUBMITTED</option>
              <option value="UNDER_REVIEW">UNDER REVIEW</option>
              <option value="APPROVED">APPROVED</option>
              <option value="RETURNED">RETURNED</option>
              <option value="REJECTED">REJECTED</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Submitted Date From</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="pg-input py-1.5 text-sm"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Submitted Date To</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="pg-input py-1.5 text-sm"
            />
          </div>
        </div>

        {loading ? (
          <div className="text-center py-6 text-sm text-slate-500">Loading report data...</div>
        ) : (
          <div className="pg-card">
            <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-xs uppercase text-slate-600 font-semibold">
                  <tr>
                    <th className="px-4 py-3 text-left">Resident</th>
                    <th className="px-4 py-3 text-left">Supervisor</th>
                    <th className="px-4 py-3 text-left">Template</th>
                    <th className="px-4 py-3 text-left">Program</th>
                    <th className="px-4 py-3 text-left">Score</th>
                    <th className="px-4 py-3 text-left">Status</th>
                    <th className="px-4 py-3 text-left">Pending (Days)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {reportData.map((row) => (
                    <tr key={row.id}>
                      <td className="px-4 py-3 font-semibold text-slate-800">{row.resident_name}</td>
                      <td className="px-4 py-3">{row.supervisor_name || '—'}</td>
                      <td className="px-4 py-3">{row.template_name}</td>
                      <td className="px-4 py-3 text-xs text-slate-500">{row.program_name || '—'}</td>
                      <td className="px-4 py-3">
                        {row.score !== null ? `${row.score} / ${row.max_score}` : '—'}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-semibold ${
                            row.status === 'APPROVED'
                              ? 'bg-green-50 text-green-700'
                              : row.status === 'SUBMITTED' || row.status === 'UNDER_REVIEW'
                              ? 'bg-blue-50 text-blue-700'
                              : row.status === 'RETURNED'
                              ? 'bg-yellow-50 text-yellow-700'
                              : 'bg-slate-50 text-slate-700'
                          }`}
                        >
                          {row.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-medium text-slate-600">
                        {row.pending_age !== null ? row.pending_age : '0'}
                      </td>
                    </tr>
                  ))}
                  {reportData.length === 0 && (
                    <tr>
                      <td className="px-4 py-6 text-center text-slate-500" colSpan={7}>
                        No evaluation submissions matched the filter criteria.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
