'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';

import { trainingApi, MilestoneEligibility } from '@/lib/api/training';

export default function UTRMCEligibilityMonitoringPage() {
  const [records, setRecords] = useState<MilestoneEligibility[]>([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({ status: '' });

  const load = (params?: { status?: string }) => {
    setLoading(true);
    trainingApi.getUTRMCEligibility(params)
      .then((data) => {
        setRecords(data.results || []);
        setCount(data.count || 0);
      })
      .catch(() => setError('Failed to load eligibility data.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const applyFilters = () => {
    load({ status: filters.status || undefined });
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
        <div className="pg-page max-w-5xl">
          <PageHeader
            title="Eligibility Monitoring"
            description="Track milestone readiness status across programs and departments."
          />

          {/* Filters */}
          <div className="pg-card mb-6 flex items-center gap-4">
            <div>
              <label className="pg-form-label text-xs">Status</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="pg-form-input"
              >
                <option value="">All</option>
                <option value="ELIGIBLE">Eligible</option>
                <option value="PARTIALLY_READY">Partially Ready</option>
                <option value="NOT_READY">Not Ready</option>
              </select>
            </div>
              <button
                onClick={applyFilters}
                className="mt-4 pg-btn-primary"
              >
                Filter
              </button>
          </div>

          {loading && <p className="text-gray-500">Loading…</p>}
          {error && <p className="text-red-600 mb-4">{error}</p>}

          <p className="text-sm text-gray-500 mb-4">Showing {records.length} of {count} records</p>

          {records.length === 0 && !loading && (
            <div className="pg-empty-state">No eligibility records found.</div>
          )}

          <div className="space-y-3">
            {records.map((e) => (
              <div key={e.id} className="pg-card">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-900">
                    {e.milestone_name}
                    <span className="ml-2 font-mono text-xs text-gray-400">{e.milestone_code}</span>
                  </h3>
                  <WorkflowStatusBadge status={e.status} label={e.status_display} />
                </div>
                {e.reasons.length > 0 && (
                  <ul className="mt-2 space-y-0.5">
                    {e.reasons.map((r, i) => (
                      <li key={i} className="text-xs text-red-600">✗ {r}</li>
                    ))}
                  </ul>
                )}
                <p className="text-xs text-gray-400 mt-2">Computed: {new Date(e.computed_at).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
    </ProtectedRoute>
  );
}
