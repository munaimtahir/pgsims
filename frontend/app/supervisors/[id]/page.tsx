'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicSummary } from '@/lib/api/academics';
import { userbaseApi } from '@/lib/api/userbase';

export default function SupervisorDetailPage() {
  const params = useParams();
  const [profile, setProfile] = useState<Record<string, unknown> | null>(null);
  const [summary, setSummary] = useState<AcademicSummary | null>(null);

  useEffect(() => {
    const id = Number(params.id);
    if (!id) return;
    userbaseApi.supervisors.get(id).then(setProfile).catch(() => setProfile(null));
    academicsApi.getSupervisorSummary(id).then(setSummary).catch(() => setSummary(null));
  }, [params.id]);

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR', 'RESIDENT', 'SUPPORT_STAFF']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Supervisor Detail"
          description="Assigned resident training records, readiness status, and pending review queue."
          actions={<Link href="/academics/review-queue" className="text-sm font-medium text-indigo-600 hover:underline">Review Queue</Link>}
        />
        <div className="grid gap-4 md:grid-cols-2">
          <div className="pg-card">
            <h2 className="pg-section-title">Supervisor Profile</h2>
            <p className="mt-3 font-semibold text-slate-900">{String((profile as { user?: { full_name?: string; username?: string } } | null)?.user?.full_name || (profile as { user?: { full_name?: string; username?: string } } | null)?.user?.username || 'Supervisor')}</p>
            <p className="text-sm text-slate-600">Academic supervisor profile</p>
          </div>
          <div className="pg-card">
            <h2 className="pg-section-title">Academic Summary</h2>
            <p className="mt-3 text-sm text-slate-600">Assigned residents: {summary?.summary?.assigned_residents || 0}</p>
            <p className="text-sm text-slate-600">Active training records: {summary?.summary?.active_training_records || 0}</p>
            <p className="text-sm text-slate-600">Pending queue items: {summary?.summary?.pending_review_queue_items || 0}</p>
          </div>
        </div>
        <div className="pg-card">
          <h2 className="pg-section-title">Assigned Residents Training Records</h2>
          <div className="mt-3 space-y-2">
            {(summary?.assigned_residents || []).map((row) => (
              <div key={row.resident_id} className="rounded-lg border border-slate-200 p-3">
                <p className="font-medium text-slate-900">{row.name}</p>
                <p className="text-sm text-slate-600">{row.program || 'Program not set'} · {row.status}</p>
              </div>
            ))}
            {(summary?.assigned_residents || []).length === 0 && (
              <p className="text-sm text-slate-500">No assigned residents yet.</p>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
