'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { trainingApi, ResidentSummary, ResidentOperationalDashboard } from '@/lib/api/training';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';

function EmptyStateCard({
  title,
  body,
}: {
  title: string;
  body: string[];
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-slate-700">
      <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
      <div className="mt-2 space-y-2 text-sm leading-6 text-slate-600">
        {body.map((line) => (
          <p key={line}>{line}</p>
        ))}
      </div>
    </div>
  );
}

function EligibilityCard({ label, eli }: { label: string; eli: { status: string | null; reasons: string[] } }) {
  return (
    <div className="pg-card">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-slate-900">{label}</h3>
        <WorkflowStatusBadge status={eli.status} />
      </div>
      {eli.reasons.length > 0 && (
        <ul className="space-y-1.5">
          {eli.reasons.slice(0, 4).map((reason, index) => (
            <li key={`${reason}-${index}`} className="flex items-start gap-2 text-sm text-red-700">
              <span className="mt-0.5 text-red-400">x</span>
              <span>{reason}</span>
            </li>
          ))}
        </ul>
      )}
      {eli.status === 'ELIGIBLE' && (
        <p className="text-sm text-green-700 flex items-center gap-1.5 mt-1">
          <span>OK</span> All requirements met
        </p>
      )}
    </div>
  );
}

export default function ResidentHomePage() {
  const [summary, setSummary] = useState<ResidentSummary | null>(null);
  const [ops, setOps] = useState<ResidentOperationalDashboard | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const loadData = async () => {
      try {
        // Small delay to ensure localStorage from addInitScript is available
        await new Promise(resolve => setTimeout(resolve, 100));

        const [nextSummary, nextOps] = await Promise.all([
          trainingApi.getResidentSummary(),
          trainingApi.getResidentOperationalDashboard().catch(() => null),
        ]);

        if (mounted) {
          setSummary(nextSummary);
          setOps(nextOps);
        }
      } catch (err) {
        console.error('Failed to load resident dashboard:', err);
        if (mounted) {
          setSummary(null);
          setOps(null);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadData();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'RESIDENT']}>
      <div className="pg-page">
        <PageHeader
          title="My Training Dashboard"
          description="Track resident training progress, leave status, schedule, and logbook readiness."
          badges={[
            {
              label: summary?.training_record?.program_name || 'Setup pending',
              tone: summary?.training_record ? 'info' : 'warning',
            },
            {
              label: summary?.training_record ? `Month ${summary.training_record.current_month_index}` : 'No active record',
              tone: summary?.training_record ? 'default' : 'warning',
            },
          ]}
          actions={(
            <Link href="/dashboard/resident/progress" className="pg-btn-primary inline-flex items-center">
              Open Logbook
            </Link>
          )}
        />

        {loading && (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
          </div>
        )}

        {!loading && !summary?.training_record && (
          <div className="space-y-4">
            <EmptyStateCard
              title="No active resident training record is linked yet."
              body={[
                'This page will show your training progress once FMU-UTRMC admin completes your setup.',
                'Please contact the FMU-UTRMC postgraduate office if this is unexpected.',
              ]}
            />
            <div className="pg-card">
              <h2 className="pg-section-title">Quick Actions</h2>
              <p className="pg-section-note">These links stay available while your resident record is being prepared.</p>
              <div className="mt-4 flex flex-wrap gap-3">
                {[
                  { label: 'View Schedule', href: '/dashboard/resident/schedule' },
                  { label: 'Logbook & Readiness', href: '/dashboard/resident/progress' },
                ].map((action) => (
                  <Link key={action.label} href={action.href} className="pg-btn-primary transition-colors">
                    {action.label}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        )}

        {!loading && summary?.training_record && (
          <div className="space-y-6">
            {ops && (
              <section className="pg-card space-y-4">
                <div>
                  <h2 className="pg-section-title">Needs Attention Now</h2>
                  <p className="pg-section-note">Current logbook readiness and pending actions.</p>
                </div>
                <div className="pg-kpi-grid md:grid-cols-5">
                  <MetricCard label="Logbook Total" value={ops.logbook.total} />
                  <MetricCard label="Draft" value={ops.logbook.draft} tone="warning" />
                  <MetricCard label="Submitted" value={ops.logbook.submitted} tone="info" />
                  <MetricCard label="Returned" value={ops.logbook.returned} tone="warning" />
                  <MetricCard label="Approved" value={ops.logbook.approved} tone="success" />
                </div>
                <div className="grid grid-cols-1 gap-2 text-sm md:grid-cols-2">
                  <p>
                    Logbook threshold:{' '}
                    <WorkflowStatusBadge
                      status={ops.readiness.logbook_threshold_met ? 'ELIGIBLE' : 'NOT_READY'}
                      label={ops.readiness.logbook_threshold_met ? 'Met' : 'Not met'}
                    />
                  </p>
                  <p>
                    Approved logbook entries: <span className="font-medium text-slate-700">{ops.logbook.approved}</span>
                  </p>
                </div>
                {ops.pending_actions.length > 0 && (
                  <ul className="space-y-1">
                    {ops.pending_actions.map((item) => (
                      <li key={item} className="text-sm text-orange-700">
                        - {item}
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="pg-card">
                <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Current Program</h2>
                <p className="text-lg font-bold text-gray-900">{summary.training_record.program_name}</p>
                <p className="text-sm text-gray-500">
                  {summary.training_record.degree_type.toUpperCase()} / Started {summary.training_record.start_date}
                </p>
                <div className="mt-3 bg-indigo-50 rounded-lg px-3 py-2 flex items-center gap-2">
                  <span className="text-indigo-600 font-bold text-lg">{summary.training_record.current_month_index}</span>
                  <span className="text-indigo-600 text-sm">months completed</span>
                </div>
              </div>

              <div className="pg-card">
                <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Current Rotation</h2>
                {summary.rotation.current ? (
                  <>
                    <p className="font-semibold text-gray-900">{summary.rotation.current.department}</p>
                    <p className="text-sm text-gray-500">{summary.rotation.current.hospital}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      {summary.rotation.current.start_date} to {summary.rotation.current.end_date}
                    </p>
                    <WorkflowStatusBadge status={summary.rotation.current.status} />
                  </>
                ) : (
                  <p className="text-gray-500 text-sm">No active rotation is linked yet.</p>
                )}
              </div>
            </div>

            <div>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Exam Eligibility</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <EligibilityCard label="IMM (Intermediate)" eli={summary.eligibility.IMM} />
                <EligibilityCard label="FINAL" eli={summary.eligibility.FINAL} />
              </div>
            </div>

            <div>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Quick Actions</h2>
              <div className="flex flex-wrap gap-3">
                {[
                  { label: 'View Schedule', href: '/dashboard/resident/schedule' },
                  { label: 'Logbook & Readiness', href: '/dashboard/resident/progress' },
                ].map((action) => (
                  <Link key={action.label} href={action.href} className="pg-btn-primary transition-colors">
                    {action.label}
                  </Link>
                ))}
              </div>
            </div>

            {summary.leaves.pending_count > 0 && (
              <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                <p className="text-sm font-medium text-amber-800">
                  Pending approvals: {summary.leaves.pending_count} leave request(s)
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
