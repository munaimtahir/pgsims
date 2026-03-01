'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { trainingApi, ResidentSummary } from '@/lib/api/training';

const STATUS_COLORS: Record<string, string> = {
  ELIGIBLE: 'bg-green-100 text-green-800',
  PARTIALLY_READY: 'bg-yellow-100 text-yellow-800',
  NOT_READY: 'bg-red-100 text-red-800',
  ACTIVE: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  SUBMITTED: 'bg-yellow-100 text-yellow-800',
  DRAFT: 'bg-gray-100 text-gray-700',
  SUBMITTED_TO_SUPERVISOR: 'bg-yellow-100 text-yellow-800',
  APPROVED_BY_SUPERVISOR: 'bg-green-100 text-green-800',
  SUBMITTED_TO_UNIVERSITY: 'bg-blue-100 text-blue-800',
  ACCEPTED_BY_UNIVERSITY: 'bg-green-100 text-green-800',
  NOT_STARTED: 'bg-gray-100 text-gray-600',
  IN_PROGRESS: 'bg-blue-100 text-blue-800',
  SUBMITTED_THESIS: 'bg-green-100 text-green-800',
};

function StatusBadge({ status, label }: { status: string | null; label?: string }) {
  if (!status) return <span className="px-2 py-0.5 rounded text-xs bg-gray-100 text-gray-500">—</span>;
  const cls = STATUS_COLORS[status] || 'bg-gray-100 text-gray-700';
  const text = label || status.replace(/_/g, ' ').replace('SUBMITTED THESIS', 'SUBMITTED');
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{text}</span>;
}

const ELIGIBILITY_ROUTE: Record<string, string> = {
  'Research synopsis not approved': '/dashboard/resident/research',
  'Thesis not submitted': '/dashboard/resident/thesis',
  'Workshop requirement not met': '/dashboard/resident/workshops',
};

function EligibilityCard({ label, eli }: { label: string; eli: { status: string | null; reasons: string[] } }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-800">{label}</h3>
        <StatusBadge status={eli.status} />
      </div>
      {eli.reasons.length > 0 && (
        <ul className="space-y-1.5">
          {eli.reasons.slice(0, 4).map((r, i) => {
            const route = Object.entries(ELIGIBILITY_ROUTE).find(([k]) => r.toLowerCase().includes(k.toLowerCase()))?.[1];
            return (
              <li key={i} className="flex items-start gap-2 text-sm text-red-700">
                <span className="mt-0.5 text-red-400">✗</span>
                {route ? <Link href={route} className="underline hover:text-red-900">{r}</Link> : <span>{r}</span>}
              </li>
            );
          })}
        </ul>
      )}
      {eli.status === 'ELIGIBLE' && (
        <p className="text-sm text-green-700 flex items-center gap-1.5 mt-1">
          <span>✓</span> All requirements met
        </p>
      )}
    </div>
  );
}

export default function ResidentHomePage() {
  const [summary, setSummary] = useState<ResidentSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    trainingApi.getResidentSummary()
      .then(setSummary)
      .catch(() => setError('Failed to load dashboard. Please refresh.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      {loading && (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
        </div>
      )}
      {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}

      {summary && (
        <div className="space-y-6 max-w-5xl mx-auto">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">My Training Dashboard</h1>
            <p className="text-gray-500 text-sm mt-1">
              {summary.training_record.program_name} · Month {summary.training_record.current_month_index}
            </p>
          </div>

          {/* Program + Rotation Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white border border-gray-200 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Current Program</h2>
              <p className="text-lg font-bold text-gray-900">{summary.training_record.program_name}</p>
              <p className="text-sm text-gray-500">{summary.training_record.degree_type.toUpperCase()} · Started {summary.training_record.start_date}</p>
              <div className="mt-3 bg-indigo-50 rounded-lg px-3 py-2 flex items-center gap-2">
                <span className="text-indigo-600 font-bold text-lg">{summary.training_record.current_month_index}</span>
                <span className="text-indigo-600 text-sm">months completed</span>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Current Rotation</h2>
              {summary.rotation.current ? (
                <>
                  <p className="font-semibold text-gray-900">{summary.rotation.current.department}</p>
                  <p className="text-sm text-gray-500">{summary.rotation.current.hospital}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {summary.rotation.current.start_date} → {summary.rotation.current.end_date}
                  </p>
                  <StatusBadge status={summary.rotation.current.status} />
                </>
              ) : (
                <p className="text-gray-400 text-sm">No active rotation</p>
              )}
              {summary.rotation.next && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <p className="text-xs text-gray-500">Next: <span className="font-medium text-gray-700">{summary.rotation.next.department}</span> from {summary.rotation.next.start_date}</p>
                </div>
              )}
            </div>
          </div>

          {/* Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white border border-gray-200 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-gray-500 mb-2">Research</h3>
              <StatusBadge status={summary.research.status || 'NOT_STARTED'} />
              {summary.research.supervisor_name && (
                <p className="text-xs text-gray-500 mt-2">Supervisor: {summary.research.supervisor_name}</p>
              )}
              <Link href="/dashboard/resident/research" className="mt-3 block text-xs text-indigo-600 hover:underline">
                Manage →
              </Link>
            </div>
            <div className="bg-white border border-gray-200 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-gray-500 mb-2">Thesis</h3>
              <StatusBadge status={summary.thesis.status} />
              {summary.thesis.submitted_at && (
                <p className="text-xs text-gray-500 mt-2">Submitted: {summary.thesis.submitted_at.slice(0, 10)}</p>
              )}
              <Link href="/dashboard/resident/thesis" className="mt-3 block text-xs text-indigo-600 hover:underline">
                Manage →
              </Link>
            </div>
            <div className="bg-white border border-gray-200 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-gray-500 mb-2">Workshops</h3>
              <p className="text-2xl font-bold text-gray-900">{summary.workshops.total_completed}</p>
              <p className="text-xs text-gray-500">completed · IMM needs {summary.workshops.required_for_imm} · FINAL needs {summary.workshops.required_for_final}</p>
              <Link href="/dashboard/resident/workshops" className="mt-3 block text-xs text-indigo-600 hover:underline">
                Manage →
              </Link>
            </div>
          </div>

          {/* Eligibility */}
          <div>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Exam Eligibility</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <EligibilityCard label="IMM (Intermediate)" eli={summary.eligibility.IMM} />
              <EligibilityCard label="FINAL" eli={summary.eligibility.FINAL} />
            </div>
          </div>

          {/* Quick Actions */}
          <div>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Quick Actions</h2>
            <div className="flex flex-wrap gap-3">
              {[
                { label: 'View Schedule', href: '/dashboard/resident/schedule' },
                { label: 'Update Research', href: '/dashboard/resident/research' },
                { label: 'Upload Workshop', href: '/dashboard/resident/workshops' },
                { label: 'Apply for Leave', href: '/dashboard/resident/progress' },
              ].map((a) => (
                <Link
                  key={a.href}
                  href={a.href}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
                >
                  {a.label}
                </Link>
              ))}
            </div>
          </div>

          {/* Pending alerts */}
          {(summary.leaves.pending_count > 0 || summary.postings.pending_count > 0) && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
              <p className="text-sm font-medium text-yellow-800">
                Pending approvals: {summary.leaves.pending_count > 0 ? `${summary.leaves.pending_count} leave request(s)` : ''}{' '}
                {summary.postings.pending_count > 0 ? `${summary.postings.pending_count} deputation(s)` : ''}
              </p>
            </div>
          )}
        </div>
      )}
    </ProtectedRoute>
  );
}
