'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicSummary } from '@/lib/api/academics';
import { userbaseApi } from '@/lib/api/userbase';

export default function ResidentDetailPage() {
  const params = useParams();
  const [profile, setProfile] = useState<Record<string, unknown> | null>(null);
  const [summary, setSummary] = useState<AcademicSummary | null>(null);

  useEffect(() => {
    const id = Number(params.id);
    if (!id) return;
    userbaseApi.residents.get(id).then(setProfile).catch(() => setProfile(null));
    academicsApi.getResidentSummary(id).then(setSummary).catch(() => setSummary(null));
  }, [params.id]);

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR', 'RESIDENT', 'SUPPORT_STAFF']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Resident Detail"
          description="Profile, training history, supervision summary, and academic readiness."
          actions={<Link href="/academics/training-records" className="text-sm font-medium text-indigo-600 hover:underline">Training Records</Link>}
        />
        <div className="grid gap-4 md:grid-cols-2">
          <div className="pg-card">
            <h2 className="pg-section-title">Resident Profile</h2>
            <p className="mt-3 font-semibold text-slate-900">{String((profile as { user?: { full_name?: string; username?: string } } | null)?.user?.full_name || (profile as { user?: { full_name?: string; username?: string } } | null)?.user?.username || 'Resident')}</p>
            <p className="text-sm text-slate-600">{summary?.resident?.program || 'Program not set'}</p>
            <p className="text-sm text-slate-600">{summary?.resident?.department || 'Department not set'}</p>
          </div>
          <div className="pg-card">
            <h2 className="pg-section-title">Active Training Record</h2>
            <p className="mt-3 text-sm text-slate-600">Status: {summary?.training_record?.status || 'Missing'}</p>
            <p className="text-sm text-slate-600">Training year: {summary?.training_record?.training_year || '—'}</p>
            <p className="text-sm text-slate-600">Session: {summary?.training_record?.academic_session.name || '—'}</p>
          </div>
        </div>
        <div className="pg-card">
          <h2 className="pg-section-title">Academic Section</h2>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            <div>
              <p className="font-medium text-slate-900">Supervisor Summary</p>
              <p className="text-sm text-slate-600">Primary supervisor: {summary?.supervision?.primary_supervisor?.supervisor.name || 'Not assigned'}</p>
              <p className="text-sm text-slate-600">Co-supervisors: {summary?.supervision?.co_supervisors.length || 0}</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Review Queue</p>
              <p className="text-sm text-slate-600">Pending items: {summary?.review_queue?.pending_count || 0}</p>
              <p className="text-sm text-slate-600">Warnings: {(summary?.readiness?.missing_items || []).join(', ') || 'None'}</p>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
