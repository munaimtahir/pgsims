'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { casesApi, CaseStatistics, ClinicalCase } from '@/lib/api/cases';

export default function UTRMCCasesPage() {
  const [items, setItems] = useState<ClinicalCase[]>([]);
  const [stats, setStats] = useState<CaseStatistics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [pending, statistics] = await Promise.all([
          casesApi.getPendingCases(),
          casesApi.getStatistics(),
        ]);
        setItems(pending);
        setStats(statistics);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load UTRMC cases.');
      }
    };
    load();
  }, []);

  return (
    <ProtectedRoute allowedRoles={['utrmc_user', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <h1 className="text-3xl font-bold text-gray-900">UTRMC Cases Oversight</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {stats && (
            <SectionCard title="Case KPIs">
              <div className="grid grid-cols-2 gap-3 text-sm">
                <p>Total: {stats.total_cases}</p>
                <p>Pending: {stats.pending_cases}</p>
                <p>Approved: {stats.approved_cases}</p>
                <p>Needs revision: {stats.needs_revision_cases}</p>
              </div>
            </SectionCard>
          )}
          <SectionCard title="Pending Cases (Read-only)">
            <div className="space-y-2">
              {items.map((item) => (
                <div key={item.id} className="rounded border p-3">
                  <p className="font-medium">{item.case_title}</p>
                  <p className="text-sm text-gray-600">{item.pg_name || 'PG'} • {item.status}</p>
                </div>
              ))}
              {!items.length && <p className="text-sm text-gray-600">No pending cases.</p>}
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
