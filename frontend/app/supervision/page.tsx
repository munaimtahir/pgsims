'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import supervisionApi, { SupervisionAssignment } from '@/lib/api/supervision';

export default function SupervisionHomePage() {
  const [assignments, setAssignments] = useState<SupervisionAssignment[]>([]);
  const [issues, setIssues] = useState<Record<string, Array<Record<string, unknown>>>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;
    Promise.all([
      supervisionApi.listAssignments(),
      supervisionApi.getSupervisionDataQuality().catch(() => ({} as Record<string, Array<Record<string, unknown>>>)),
    ])
      .then(([nextAssignments, nextIssues]) => {
        if (!mounted) return;
        setAssignments(nextAssignments);
        setIssues(nextIssues || {});
      })
      .catch(() => mounted && setError('Unable to load supervision overview.'))
      .finally(() => mounted && setLoading(false));

    return () => {
      mounted = false;
    };
  }, []);

  const activeAssignments = assignments.filter((assignment) => assignment.status === 'ACTIVE');
  const primaryAssignments = activeAssignments.filter((assignment) => assignment.assignment_type === 'PRIMARY');
  const coAssignments = activeAssignments.filter((assignment) => assignment.assignment_type === 'CO_SUPERVISOR');

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page">
        <PageHeader
          title="Supervision"
          description="Canonical supervision dashboard backed by ResidentSupervisorAssignment."
          badges={[
            { label: 'Canonical Spine', tone: 'info' },
            { label: `${activeAssignments.length} Active`, tone: activeAssignments.length ? 'default' : 'warning' },
          ]}
          actions={(
            <div className="flex flex-wrap gap-2">
              <Link href="/supervision/assignments" className="pg-btn-primary">Assignments</Link>
              <Link href="/supervision/import" className="pg-btn-primary">Import</Link>
              <Link href="/supervision/data-quality" className="pg-btn-primary">Data Quality</Link>
            </div>
          )}
        />

        {loading && <p className="text-sm text-slate-500">Loading supervision overview...</p>}
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        {!loading && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <MetricCard label="Active Assignments" value={activeAssignments.length} />
              <MetricCard label="Primary Assignments" value={primaryAssignments.length} tone="info" />
              <MetricCard label="Co-Supervisors" value={coAssignments.length} tone="warning" />
              <MetricCard label="Data Issues" value={Object.values(issues).reduce((count, rows) => count + rows.length, 0)} tone="warning" />
            </div>

            <section className="pg-card space-y-3">
              <h2 className="pg-section-title">Quick Navigation</h2>
              <div className="flex flex-wrap gap-2">
                <Link href="/supervision/assignments/new" className="pg-btn-primary">Add Assignment</Link>
              </div>
            </section>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
