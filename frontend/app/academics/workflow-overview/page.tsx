'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi } from '@/lib/api/academics';

interface StatsMap {
  total?: number;
  approved?: number;
  under_review?: number;
  returned?: number;
  rejected?: number;
  cancelled?: number;
  verified?: number;
  submitted?: number;
  pending?: number;
  in_progress?: number;
  done?: number;
  dismissed?: number;
}

interface OverviewData {
  total_active_residents?: number;
  residents_with_training_record?: number;
  residents_without_training_record?: number;
  evaluation_stats?: StatsMap;
  logbook_stats?: StatsMap;
  review_queue_stats?: StatsMap;
}

export default function AdminWorkflowOverviewPage() {
  const [overview, setOverview] = useState<OverviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [message, setMessage] = useState('');

  const load = () => {
    setLoading(true);
    academicsApi
      .getAdminAcademicWorkflowOverview()
      .then((data) => setOverview(data as unknown as OverviewData))
      .catch(() => setOverview(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSeed = async () => {
    setSeeding(true);
    setMessage('');
    try {
      const counts = await academicsApi.seedWorkflows();
      setMessage(
        `Pilot workflow data seeded: ${counts.evaluation_submissions} evaluations, ${counts.logbook_entries} logbooks.`
      );
      load();
    } catch (err: unknown) {
      setMessage('Failed to seed workflows: ' + ((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || (err as Error).message));
    } finally {
      setSeeding(false);
    }
  };

  if (loading && !overview) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading overview...</div>;
  }

  const evalStats = overview?.evaluation_stats || {};
  const logStats = overview?.logbook_stats || {};
  const reviewStats = overview?.review_queue_stats || {};

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Academic Workflow Dashboard"
            description="High-level dashboard monitoring evaluation submissions, logbooks verification pipeline, and review workload."
          />
          <button
            onClick={handleSeed}
            disabled={seeding}
            className="pg-btn-secondary border-indigo-300 text-indigo-700 hover:bg-indigo-50 disabled:opacity-50"
          >
            {seeding ? 'Seeding...' : 'Seed Pilot Workflows'}
          </button>
        </div>

        {message && (
          <div className="rounded-lg border border-indigo-200 bg-indigo-50 p-3 text-sm text-indigo-700">
            {message}
          </div>
        )}

        <div className="pg-kpi-grid md:grid-cols-4">
          <MetricCard label="Active Residents" value={overview?.total_active_residents || 0} />
          <MetricCard label="Records Registered" value={overview?.residents_with_training_record || 0} />
          <MetricCard
            label="Residents Pending Record"
            value={overview?.residents_without_training_record || 0}
            tone={overview?.residents_without_training_record && overview.residents_without_training_record > 0 ? 'warning' : 'default'}
          />
          <MetricCard label="Pending Reviews" value={reviewStats.pending || 0} tone="info" />
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {/* Evaluations Stats Card */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Rotation Evaluations</h2>
            <div className="space-y-2 text-sm text-slate-700">
              <div className="flex justify-between">
                <span>Total Submissions</span>
                <span className="font-semibold text-slate-900">{evalStats.total || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Approved / Verified</span>
                <span className="font-semibold text-green-600">{evalStats.approved || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Under Supervisor Review</span>
                <span className="font-semibold text-blue-600">{evalStats.under_review || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Returned for Revision</span>
                <span className="font-semibold text-yellow-600">{evalStats.returned || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Rejected / Cancelled</span>
                <span className="font-semibold text-red-600">{(evalStats.rejected || 0) + (evalStats.cancelled || 0)}</span>
              </div>
            </div>
          </div>

          {/* Logbook Stats Card */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Logbook Procedures</h2>
            <div className="space-y-2 text-sm text-slate-700">
              <div className="flex justify-between">
                <span>Total Logged Cases</span>
                <span className="font-semibold text-slate-900">{logStats.total || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Verified by Supervisor</span>
                <span className="font-semibold text-green-600">{logStats.verified || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Submitted for Review</span>
                <span className="font-semibold text-blue-600">{logStats.submitted || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Returned for Revision</span>
                <span className="font-semibold text-yellow-600">{logStats.returned || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Rejected / Cancelled</span>
                <span className="font-semibold text-red-600">{(logStats.rejected || 0) + (logStats.cancelled || 0)}</span>
              </div>
            </div>
          </div>

          {/* Review Queue Workload Card */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Review Queue Metrics</h2>
            <div className="space-y-2 text-sm text-slate-700">
              <div className="flex justify-between">
                <span>Total Queue Items</span>
                <span className="font-semibold text-slate-900">{reviewStats.total || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Pending Review</span>
                <span className="font-semibold text-blue-600">{reviewStats.pending || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Under Active Review</span>
                <span className="font-semibold text-indigo-600">{reviewStats.in_progress || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Completed Reviews</span>
                <span className="font-semibold text-green-600">{reviewStats.done || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Dismissed Reviews</span>
                <span className="font-semibold text-slate-500">{reviewStats.dismissed || 0}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
