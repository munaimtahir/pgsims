'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

import { trainingApi, MilestoneEligibility } from '@/lib/api/training';

const STATUS_COLOR: Record<string, string> = {
  ELIGIBLE: 'bg-green-100 text-green-800',
  PARTIALLY_READY: 'bg-yellow-100 text-yellow-800',
  NOT_READY: 'bg-red-100 text-red-800',
};

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
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Eligibility Monitoring</h1>

          {/* Filters */}
          <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6 flex items-center gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Status</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="border border-gray-300 rounded-md px-3 py-1.5 text-sm"
              >
                <option value="">All</option>
                <option value="ELIGIBLE">Eligible</option>
                <option value="PARTIALLY_READY">Partially Ready</option>
                <option value="NOT_READY">Not Ready</option>
              </select>
            </div>
            <button
              onClick={applyFilters}
              className="mt-4 px-4 py-1.5 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700"
            >
              Filter
            </button>
          </div>

          {loading && <p className="text-gray-500">Loading…</p>}
          {error && <p className="text-red-600 mb-4">{error}</p>}

          <p className="text-sm text-gray-500 mb-4">Showing {records.length} of {count} records</p>

          {records.length === 0 && !loading && (
            <p className="text-sm text-gray-500">No eligibility records found.</p>
          )}

          <div className="space-y-3">
            {records.map((e) => (
              <div key={e.id} className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-900">
                    {e.milestone_name}
                    <span className="ml-2 font-mono text-xs text-gray-400">{e.milestone_code}</span>
                  </h3>
                  <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[e.status] || 'bg-gray-100 text-gray-600'}`}>
                    {e.status_display}
                  </span>
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
