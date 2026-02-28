'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuthStore } from '@/store/authStore';
import { casesApi } from '@/lib/api/cases';
import { reportsApi } from '@/lib/api/reports';
import SectionCard from '@/components/ui/SectionCard';
import ErrorBanner from '@/components/ui/ErrorBanner';

export default function UTRMCDashboardPage() {
  const { user } = useAuthStore();
  const isReadOnly = user?.role === 'utrmc_user';
  const [kpi, setKpi] = useState({
    totalCases: 0,
    pendingCases: 0,
    pendingLogbook: 0,
    overdueVerification: 0,
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [caseStats, pendingLogbook, overdue] = await Promise.all([
          casesApi.getStatistics(),
          reportsApi.run('pending-logbook-queue'),
          reportsApi.run('overdue-verification'),
        ]);
        setKpi({
          totalCases: caseStats.total_cases,
          pendingCases: caseStats.pending_cases,
          pendingLogbook: pendingLogbook.summary.total as number,
          overdueVerification: overdue.summary.total as number,
        });
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load UTRMC KPIs.');
      }
    };
    load();
  }, []);

  return (
    <ProtectedRoute allowedRoles={['utrmc_user', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 data-testid="utrmc-dashboard-title" className="text-3xl font-bold text-gray-900">UTRMC Dashboard</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          <div data-testid="utrmc-access-panel" className="rounded-md border border-gray-200 bg-white p-4">
            <p data-testid="utrmc-access-mode" className="text-sm font-medium text-gray-900">
              Access Mode: {isReadOnly ? 'Read-only oversight' : 'UTRMC admin'}
            </p>
            <p data-testid="utrmc-readonly-note" className="mt-1 text-sm text-gray-600">
              {isReadOnly
                ? 'Mutation actions are hidden for utrmc_user accounts.'
                : 'Admin approvals are handled in workflow-specific pages or backend/admin tools. This dashboard remains non-mutating.'}
            </p>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
            <SectionCard title="Total Cases">
              <p className="text-2xl font-semibold">{kpi.totalCases}</p>
            </SectionCard>
            <SectionCard title="Pending Cases">
              <p className="text-2xl font-semibold">{kpi.pendingCases}</p>
            </SectionCard>
            <SectionCard title="Pending Logbook Queue">
              <p className="text-2xl font-semibold">{kpi.pendingLogbook}</p>
            </SectionCard>
            <SectionCard title="Overdue Verification">
              <p className="text-2xl font-semibold">{kpi.overdueVerification}</p>
            </SectionCard>
          </div>
          <SectionCard title="Quick Links">
            <div className="space-x-2">
              <a href="/dashboard/utrmc/reports" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                Open Reports
              </a>
              <a href="/dashboard/utrmc/cases" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                View Cases
              </a>
              {!isReadOnly && (
                <>
                  <a href="/dashboard/utrmc/users" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                    Manage Users
                  </a>
                  <a href="/dashboard/utrmc/matrix" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                    Matrix
                  </a>
                </>
              )}
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
