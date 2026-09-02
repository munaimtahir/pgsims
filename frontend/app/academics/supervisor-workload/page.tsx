'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi } from '@/lib/api/academics';

interface SupervisedResidentRow {
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

interface WorkloadData {
  assigned_residents_count?: number;
  pending_evaluation_reviews_count?: number;
  pending_logbook_reviews_count?: number;
  assigned_residents?: SupervisedResidentRow[];
  review_queue?: ReviewQueueRow[];
}

export default function SupervisorWorkloadPage() {
  const [workload, setWorkload] = useState<WorkloadData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getSupervisorAcademicWorkload()
      .then((data) => setWorkload(data as unknown as WorkloadData))
      .catch(() => setWorkload(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading workload metrics...</div>;
  }

  if (!workload) {
    return (
      <div className="text-center py-6 text-sm text-red-500">
        Supervisor workload data is not available. Please verify you have a supervisor profile.
      </div>
    );
  }

  const assigned = workload.assigned_residents || [];
  const queue = workload.review_queue || [];

  return (
    <ProtectedRoute allowedRoles={['SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Supervisor Academic Workload"
          description="Track pending verification items, evaluation requests, and progress metrics for your assigned residents."
        />

        <div className="pg-kpi-grid md:grid-cols-3">
          <MetricCard label="Assigned Residents" value={workload.assigned_residents_count || 0} />
          <MetricCard
            label="Pending Evaluations"
            value={workload.pending_evaluation_reviews_count || 0}
            tone={workload.pending_evaluation_reviews_count && workload.pending_evaluation_reviews_count > 0 ? 'warning' : 'default'}
          />
          <MetricCard
            label="Pending Logbooks"
            value={workload.pending_logbook_reviews_count || 0}
            tone={workload.pending_logbook_reviews_count && workload.pending_logbook_reviews_count > 0 ? 'warning' : 'default'}
          />
        </div>

        {/* Assigned Residents Roster */}
        <div className="pg-card space-y-4">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Supervised Residents</h2>
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">Resident Name</th>
                  <th className="px-4 py-3 text-left">Program</th>
                  <th className="px-4 py-3 text-left">Training Year</th>
                  <th className="px-4 py-3 text-left">Record Status</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {assigned.map((res) => (
                  <tr key={res.resident_id}>
                    <td className="px-4 py-3 font-medium text-slate-900">{res.name} ({res.username})</td>
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
                    <td className="px-4 py-3">
                      <Link
                        href={`/academics/training-records/${res.training_record_id}`}
                        className="text-sm font-medium text-indigo-600 hover:underline"
                      >
                        Open Record
                      </Link>
                    </td>
                  </tr>
                ))}
                {assigned.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={5}>
                      No supervised residents assigned to your roster.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Review Queue Items */}
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
                  <th className="px-4 py-3 text-left">Actions</th>
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
                    <td className="px-4 py-3">
                      {item.queue_type === 'EVALUATION_REVIEW' ? (
                        <Link
                          href={`/academics/evaluations`}
                          className="text-sm font-medium text-indigo-600 hover:underline"
                        >
                          Go to Evaluations
                        </Link>
                      ) : (
                        <Link
                          href={`/academics/logbook`}
                          className="text-sm font-medium text-indigo-600 hover:underline"
                        >
                          Go to Logbook
                        </Link>
                      )}
                    </td>
                  </tr>
                ))}
                {queue.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={5}>
                      All review queue tasks completed! Nice job.
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
