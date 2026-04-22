'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import { trainingApi, ResidentProgressSnapshot } from '@/lib/api/training';

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="pg-card">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3">{title}</h3>
      {children}
    </div>
  );
}

export default function ResidentProgressPage() {
  const params = useParams();
  const residentId = Number(params.id);
  const [snap, setSnap] = useState<ResidentProgressSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!residentId) return;
    trainingApi.getResidentProgress(residentId)
      .then(setSnap)
      .catch(() => setError('Failed to load resident progress'))
      .finally(() => setLoading(false));
  }, [residentId]);

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <div className="pg-page max-w-4xl">
        <PageHeader
          title="Resident Progress"
          description="Supervisor snapshot of resident workflow and eligibility readiness."
          actions={(
            <Link href="/dashboard/supervisor" className="text-sm font-medium text-indigo-600 hover:underline">
              ← Back
            </Link>
          )}
        />

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}

        {snap && (
          <div className="space-y-4">
            {/* Header */}
            <div className="pg-kpi-grid">
              <MetricCard label="Resident" value={snap.resident_name || snap.resident.name} />
              <MetricCard label="Program" value={snap.program_name || snap.training_record.program_name} />
              <MetricCard label="Month" value={snap.current_month_index ?? snap.training_record.current_month_index} />
              <MetricCard
                label="Current Rotation"
                value={snap.current_rotation ? `${snap.current_rotation.department} @ ${snap.current_rotation.hospital}` : 'No active rotation'}
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Research */}
              <Section title="Research">
                {snap.research ? (
                  <div className="space-y-2">
                    <p className="font-medium text-gray-800 text-sm">{snap.research.title}</p>
                    <WorkflowStatusBadge status={snap.research.status} />
                    {snap.research.synopsis_file && (
                      <a href={snap.research.synopsis_file} target="_blank" rel="noreferrer"
                        className="block text-xs text-indigo-600 underline mt-1">View Synopsis</a>
                    )}
                  </div>
                ) : <p className="text-sm text-gray-400">No research project yet</p>}
              </Section>

              {/* Thesis */}
              <Section title="Thesis">
                {snap.thesis ? (
                  <div className="space-y-2">
                    <WorkflowStatusBadge status={snap.thesis.status} />
                    {snap.thesis.submitted_at && <p className="text-xs text-gray-500">Submitted: {snap.thesis.submitted_at.slice(0, 10)}</p>}
                  </div>
                ) : <p className="text-sm text-gray-400">No thesis record</p>}
              </Section>
            </div>

            {/* Workshops */}
            <Section title="Workshops">
              <div className="flex gap-6 flex-wrap">
                <div className="text-center">
                  <span className="text-2xl font-bold text-indigo-700">{snap.workshops.total_completed}</span>
                  <p className="text-xs text-gray-500 mt-0.5">Completed</p>
                </div>
                <div className="text-center">
                  <span className="text-lg font-semibold text-gray-700">{snap.workshops.required_for_imm}</span>
                  <p className="text-xs text-gray-500 mt-0.5">Req. IMM</p>
                </div>
                <div className="text-center">
                  <span className="text-lg font-semibold text-gray-700">{snap.workshops.required_for_final}</span>
                  <p className="text-xs text-gray-500 mt-0.5">Req. Final</p>
                </div>
              </div>
              {(snap.workshops.completed_list ?? []).length > 0 && (
                <ul className="mt-3 space-y-1">
                  {(snap.workshops.completed_list ?? []).map((w, i) => (
                    <li key={i} className="text-xs text-gray-600 flex items-center gap-1.5">
                      <span className="text-green-500">✓</span>{w}
                    </li>
                  ))}
                </ul>
              )}
            </Section>

            {/* Eligibility */}
            <Section title="Eligibility">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {(['IMM', 'FINAL'] as const).map(code => {
                  const elig = snap.eligibility[code];
                  if (!elig) return null;
                  return (
                    <div key={code} className="border rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-gray-800 text-sm">{code === 'IMM' ? 'Intermediate' : 'Final'}</span>
                        <WorkflowStatusBadge status={elig.status} />
                      </div>
                      {elig.reasons.length > 0 ? (
                        <ul className="space-y-1">
                          {elig.reasons.map((r, i) => (
                            <li key={i} className="text-xs text-gray-600 flex gap-1.5">
                              <span className="text-red-400 mt-0.5">•</span>{r}
                            </li>
                          ))}
                        </ul>
                      ) : <p className="text-xs text-green-600">All criteria met</p>}
                    </div>
                  );
                })}
              </div>
            </Section>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
