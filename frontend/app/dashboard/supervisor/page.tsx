'use client';

import { useEffect, useState } from 'react';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi, AcademicSummary } from '@/lib/api/academics';

export default function SupervisorHomePage() {
  const [summary, setSummary] = useState<AcademicSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    academicsApi
      .getMySupervisorSummary()
      .then((data) => {
        if (active) {
          setSummary(data);
        }
      })
      .catch(() => {
        if (active) {
          setSummary(null);
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  return (
    <ProtectedRoute allowedRoles={['SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Supervisor Dashboard"
          description="Canonical supervisor shell for assigned residents and academic review work."
        />

        {loading ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-500">
            Loading supervisor summary...
          </div>
        ) : (
          <>
            <div className="grid gap-4 md:grid-cols-3">
              <MetricCard label="Assigned Residents" value={summary?.summary?.assigned_residents || 0} />
              <MetricCard label="Missing Training Records" value={summary?.summary?.residents_missing_training_records || 0} tone="warning" />
              <MetricCard label="Pending Review Queue Items" value={summary?.summary?.pending_review_queue_items || 0} tone="info" />
            </div>

            <section className="pg-card">
              <h2 className="pg-section-title">My Residents</h2>
              <div className="mt-3 space-y-3">
                {(summary?.assigned_residents || []).map((resident) => (
                  <div key={resident.resident_id} className="rounded-xl border border-slate-200 bg-white p-4">
                    <p className="font-semibold text-slate-900">{resident.name}</p>
                    <p className="text-sm text-slate-600">Program: {resident.program || 'Not set'}</p>
                    <p className="text-sm text-slate-600">Training year: {resident.training_year || 'Not set'}</p>
                    <p className="text-sm text-slate-600">Status: {resident.status}</p>
                  </div>
                ))}
                {(summary?.assigned_residents || []).length === 0 && (
                  <p className="text-sm text-slate-500">No residents are assigned yet.</p>
                )}
              </div>
            </section>

            <section className="pg-card">
              <h2 className="pg-section-title">Academic Review Queue</h2>
              <p className="mt-3 text-sm text-slate-600">
                Pending queue items: {summary?.review_queue?.pending_count || 0}
              </p>
              <p className="mt-2 text-xs text-slate-500">
                Full evaluation and logbook review forms remain deferred. This queue is the canonical scaffold for future academic review work.
              </p>
            </section>
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
