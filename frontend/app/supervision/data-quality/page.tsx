'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import supervisionApi, { SupervisionDataQuality } from '@/lib/api/supervision';

export default function SupervisionDataQualityPage() {
  const [data, setData] = useState<SupervisionDataQuality>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    supervisionApi.getSupervisionDataQuality()
      .then(setData)
      .catch(() => setError('Unable to load supervision data quality.'))
      .finally(() => setLoading(false));
  }, []);

  const totalIssues = useMemo(() => Object.values(data).reduce((count, rows) => count + rows.length, 0), [data]);

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page">
        <PageHeader
          title="Supervision Data Quality"
          description="Audit categories produced by the supervision spine."
          actions={(
            <div className="flex flex-wrap gap-2">
              <Link href="/supervision" className="pg-btn-primary">Overview</Link>
            </div>
          )}
        />

        {loading && <p className="text-sm text-slate-500">Loading data quality...</p>}
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        {!loading && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <MetricCard label="Issue Categories" value={Object.keys(data).length} />
              <MetricCard label="Total Issues" value={totalIssues} tone="warning" />
              <MetricCard label="Primary Gaps" value={(data.residents_no_primary || []).length} tone="info" />
              <MetricCard label="Mismatches" value={(data.hospital_mismatch || []).length + (data.department_mismatch || []).length} tone="warning" />
            </div>

            <div className="space-y-3">
              {Object.entries(data).map(([key, rows]) => (
                <section key={key} className="pg-card">
                  <h2 className="font-semibold text-slate-900">{key.replace(/_/g, ' ')}</h2>
                  <p className="text-sm text-slate-500">{rows.length} record(s)</p>
                </section>
              ))}
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
