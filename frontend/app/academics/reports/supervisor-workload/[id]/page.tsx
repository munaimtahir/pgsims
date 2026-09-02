'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi } from '@/lib/api/academics';
import apiClient from '@/lib/api/client';

interface SupervisedResident {
  resident_id: number;
  name: string;
  username: string;
  program_name: string | null;
  training_year: number | null;
  training_status: string | null;
  training_record_id: number | null;
}

interface ReviewQueueRow {
  id: number;
  resident_name: string;
  queue_type: string;
  due_date: string | null;
  notes: string;
}

interface WorkloadReport {
  supervisor?: {
    id: number;
    name: string;
    username: string;
    email: string;
    department_name: string | null;
    hospital_name: string | null;
  };
  workload?: {
    assigned_residents_count: number;
    pending_evaluation_reviews_count: number;
    pending_logbook_reviews_count: number;
    overdue_reviews_count: number;
    assigned_residents?: SupervisedResident[];
    review_queue?: ReviewQueueRow[];
  };
}

export default function SupervisorWorkloadReportDetailPage() {
  const params = useParams();
  const supervisorId = Number(params.id);

  const [report, setReport] = useState<WorkloadReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getSupervisorWorkloadReportDetail(supervisorId)
      .then((data) => setReport(data as unknown as WorkloadReport))
      .catch(() => setReport(null))
      .finally(() => setLoading(false));
  }, [supervisorId]);

  if (loading) {
    return <div className="text-center py-8 text-sm text-slate-500">Loading workload report...</div>;
  }

  if (!report || !report.supervisor || !report.workload) {
    return (
      <div className="text-center py-8 text-sm text-red-500">
        Supervisor workload report is not available. Please verify active supervisor profile.
      </div>
    );
  }

  const sup = report.supervisor;
  const wl = report.workload;
  const assigned = wl.assigned_residents || [];
  const queue = wl.review_queue || [];

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title={`${sup.name}'s Workload Report`}
            description="Detail workload audit for teaching supervisor including assigned rosters and pending queues."
          />
          <a
            href={`${apiClient.defaults.baseURL || ''}/api/academics/reports/supervisor-workload/export.csv?supervisor_id=${sup.id}`}
            target="_blank"
            rel="noreferrer"
            className="pg-btn-secondary border-indigo-300 text-indigo-700 hover:bg-indigo-50"
          >
            Export Workload CSV
          </a>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Identity Card */}
          <div className="pg-card space-y-3">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-1.5">Supervisor Profile</h2>
            <div className="space-y-1.5 text-sm">
              <div>
                <span className="text-slate-500 font-medium">Full Name:</span>{' '}
                <span className="font-semibold text-slate-800">{sup.name}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Username:</span>{' '}
                <span className="font-semibold text-slate-850">{sup.username}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Email:</span>{' '}
                <span className="font-semibold text-slate-800">{sup.email}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Department:</span>{' '}
                <span className="font-semibold text-slate-850">{sup.department_name || '—'}</span>
              </div>
            </div>
          </div>

          {/* Core Metrics */}
          <div className="grid gap-4 grid-cols-2">
            <MetricCard label="Residents" value={wl.assigned_residents_count || 0} />
            <MetricCard
              label="Pending Evals"
              value={wl.pending_evaluation_reviews_count || 0}
              tone={wl.pending_evaluation_reviews_count > 0 ? 'warning' : 'default'}
            />
            <MetricCard
              label="Pending Logbooks"
              value={wl.pending_logbook_reviews_count || 0}
              tone={wl.pending_logbook_reviews_count > 0 ? 'warning' : 'default'}
            />
            <MetricCard
              label="Overdue Reviews"
              value={wl.overdue_reviews_count || 0}
              tone={wl.overdue_reviews_count > 0 ? 'warning' : 'default'}
            />
          </div>
        </div>

        {/* Assigned Residents Roster */}
        <div className="pg-card space-y-4">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Assigned Residents</h2>
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">Resident Name</th>
                  <th className="px-4 py-3 text-left">Program</th>
                  <th className="px-4 py-3 text-left">Training Year</th>
                  <th className="px-4 py-3 text-left">Record Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {assigned.map((res) => (
                  <tr key={res.resident_id}>
                    <td className="px-4 py-3 font-semibold text-slate-855">{res.name} ({res.username})</td>
                    <td className="px-4 py-3">{res.program_name || '—'}</td>
                    <td className="px-4 py-3">Year {res.training_year || '—'}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                          res.training_status === 'ACTIVE'
                            ? 'bg-green-50 text-green-700'
                            : 'bg-yellow-50 text-yellow-700'
                        }`}
                      >
                        {res.training_status || '—'}
                      </span>
                    </td>
                  </tr>
                ))}
                {assigned.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={4}>
                      No supervised residents assigned to this supervisor.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pending Review Queue Items */}
        <div className="pg-card space-y-4">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Pending Review Queue</h2>
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">Resident</th>
                  <th className="px-4 py-3 text-left">Review Type</th>
                  <th className="px-4 py-3 text-left">Due Date</th>
                  <th className="px-4 py-3 text-left">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {queue.map((item) => (
                  <tr key={item.id}>
                    <td className="px-4 py-3 font-medium text-slate-900">{item.resident_name}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                          item.queue_type === 'EVALUATION_REVIEW'
                            ? 'bg-blue-50 text-blue-700'
                            : 'bg-purple-50 text-purple-700'
                        }`}
                      >
                        {item.queue_type}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-slate-600">{item.due_date || '—'}</td>
                    <td className="px-4 py-3 text-slate-500 max-w-xs truncate">{item.notes || '—'}</td>
                  </tr>
                ))}
                {queue.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={4}>
                      All review queue items verified.
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
