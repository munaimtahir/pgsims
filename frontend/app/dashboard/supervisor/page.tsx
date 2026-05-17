'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import {
  LeaveRequest,
  trainingApi,
  SupervisorSummary,
  SupervisorOperationalDashboard,
  LogbookEntry,
} from '@/lib/api/training';

function EmptyStateCard({ lines }: { lines: string[] }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-5 text-sm leading-6 text-slate-600">
      <div className="space-y-2">
        {lines.map((line) => (
          <p key={line}>{line}</p>
        ))}
      </div>
    </div>
  );
}

export default function SupervisorHomePage() {
  const [summary, setSummary] = useState<SupervisorSummary | null>(null);
  const [opsSummary, setOpsSummary] = useState<SupervisorOperationalDashboard | null>(null);
  const [pendingLeaves, setPendingLeaves] = useState<LeaveRequest[]>([]);
  const [pendingLogbook, setPendingLogbook] = useState<LogbookEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [processingLeaveId, setProcessingLeaveId] = useState<number | null>(null);
  const [processingLogbookId, setProcessingLogbookId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const flash = (nextMessage: string, isError = false) => {
    if (isError) {
      setError(nextMessage);
    } else {
      setMessage(nextMessage);
    }

    window.setTimeout(() => {
      setError('');
      setMessage('');
    }, 4000);
  };

  const load = () => {
    setLoading(true);
    Promise.all([
      trainingApi.getSupervisorSummary(),
      trainingApi.getSupervisorOperationalDashboard().catch(() => null),
      trainingApi.getSupervisorPendingLeaves(),
      trainingApi.getLogbookReviewQueue().catch(() => ({ count: 0, results: [] })),
    ])
      .then(([
        nextSummary,
        nextOpsSummary,
        nextPendingLeaves,
        logbookQueue,
      ]) => {
        setSummary(nextSummary);
        setOpsSummary(nextOpsSummary);
        setPendingLeaves(nextPendingLeaves);
        setPendingLogbook(logbookQueue.results || []);
      })
      .catch(() => setError('Failed to load supervisor summary'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const approveLeave = async (leaveId: number) => {
    setProcessingLeaveId(leaveId);
    try {
      await trainingApi.approveLeave(leaveId);
      flash('Leave request approved.');
      load();
    } catch {
      flash('Failed to approve leave request.', true);
    } finally {
      setProcessingLeaveId(null);
    }
  };

  const laggingResidents = opsSummary?.lagging_residents || [];

  const rejectLeave = async (leaveId: number) => {
    const reason = window.prompt('Reason for rejection:');
    if (reason === null) {
      return;
    }

    setProcessingLeaveId(leaveId);
    try {
      await trainingApi.rejectLeave(leaveId, reason);
      flash('Leave request rejected.');
      load();
    } catch {
      flash('Failed to reject leave request.', true);
    } finally {
      setProcessingLeaveId(null);
    }
  };

  const reviewLogbook = async (entryId: number, action: 'approved' | 'returned') => {
    const feedback = action === 'returned'
      ? (window.prompt('Feedback for return:') || '').trim()
      : (window.prompt('Optional approval feedback:') || '').trim();
    if (action === 'returned' && !feedback) {
      return;
    }

    setProcessingLogbookId(entryId);
    try {
      await trainingApi.reviewLogbookEntry(entryId, action, feedback || undefined);
      flash(action === 'approved' ? 'Logbook entry approved.' : 'Logbook entry returned.');
      load();
    } catch {
      flash('Failed to review logbook entry.', true);
    } finally {
      setProcessingLogbookId(null);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <div className="pg-page">
        <PageHeader
          title="Supervisor Dashboard"
          description="Focus on assigned residents, pending reviews, and approvals that need attention now."
        />

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}
        {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4">{message}</div>}

        {summary && (
          <div className="space-y-8">
            <section className="pg-card space-y-4">
              <div>
                <h2 className="pg-section-title">Today’s attention</h2>
                <p className="pg-section-note">A quick summary of items that need your review.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                <MetricCard label="Assigned Residents" value={opsSummary?.assigned_residents || summary.residents.length} />
                <MetricCard label="Pending Logbook Reviews" value={opsSummary?.pending_logbook_reviews || 0} tone="info" />
                <MetricCard label="Leave Approvals" value={summary.pending.leave_approvals} tone="warning" />
                <MetricCard label="Rotation Requests" value={opsSummary?.pending_rotation_applications || 0} tone="warning" />
              </div>
            </section>

            {summary.residents.length === 0 && (
              <EmptyStateCard
                lines={[
                  'No residents are assigned to you yet.',
                  'Once UTRMC assigns residents, pending reviews and submissions will appear here.',
                ]}
              />
            )}

            <section className="space-y-3">
              <h2 className="text-lg font-semibold text-gray-800">My Residents</h2>
              {summary.residents.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 bg-white px-4 py-6 text-sm text-slate-500">
                  No resident roster is available yet.
                </div>
              ) : (
                <div className="bg-white border border-gray-200 rounded-xl overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-gray-600 text-xs uppercase tracking-wider">
                      <tr>
                        <th className="px-4 py-3 text-left">Resident</th>
                        <th className="px-4 py-3 text-left">Program</th>
                        <th className="px-4 py-3 text-left">Rotation</th>
                        <th className="px-4 py-3 text-left">IMM</th>
                        <th className="px-4 py-3 text-left">Final</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {summary.residents.map((r) => (
                        <tr key={r.id} className="hover:bg-gray-50 transition">
                          <td className="px-4 py-3 font-medium text-gray-900">{r.name}</td>
                          <td className="px-4 py-3 text-gray-600">{r.program}</td>
                          <td className="px-4 py-3 text-gray-600 text-xs">
                            {r.current_rotation || <span className="text-gray-400">None</span>}
                          </td>
                          <td className="px-4 py-3"><WorkflowStatusBadge status={r.imm_status} /></td>
                          <td className="px-4 py-3"><WorkflowStatusBadge status={r.final_status} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>

            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending logbook reviews</h2>
              {pendingLogbook.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 bg-white px-4 py-6 text-sm text-slate-500">
                  No submitted logbook entries in your queue.
                </div>
              ) : (
                <div className="space-y-3">
                  {pendingLogbook.map((entry) => (
                    <div key={entry.id} className="pg-card">
                      <div className="flex items-start justify-between gap-4 flex-wrap">
                        <div>
                          <p className="font-semibold text-gray-900">{entry.resident_name}</p>
                          <p className="text-sm text-gray-500">
                            Patient ID: {entry.patient_id_number} · Seen: {entry.patient_seen_at.slice(0, 10)}
                          </p>
                          {entry.diagnosis && <p className="text-sm text-gray-700 mt-2">{entry.diagnosis}</p>}
                        </div>
                        <WorkflowStatusBadge status={entry.status} />
                      </div>
                      <div className="mt-4 flex gap-2 flex-wrap">
                        <button
                          onClick={() => reviewLogbook(entry.id, 'approved')}
                          disabled={processingLogbookId === entry.id}
                          className="pg-btn-success"
                        >
                          {processingLogbookId === entry.id ? 'Processing…' : 'Approve'}
                        </button>
                        <button
                          onClick={() => reviewLogbook(entry.id, 'returned')}
                          disabled={processingLogbookId === entry.id}
                          className="pg-btn-warning"
                        >
                          Return with Feedback
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending approvals</h2>
              {pendingLeaves.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 bg-white px-4 py-6 text-sm text-slate-500">
                  No leave requests awaiting review.
                </div>
              ) : (
                <div className="space-y-3">
                  {pendingLeaves.map((leave) => (
                    <div key={leave.id} className="pg-card">
                      <div className="flex items-start justify-between gap-4 flex-wrap">
                        <div>
                          <p className="font-semibold text-gray-900">{leave.resident_name}</p>
                          <p className="text-sm text-gray-500">
                            {leave.leave_type} · {leave.start_date} → {leave.end_date}
                          </p>
                          {leave.reason && (
                            <p className="text-sm text-gray-700 mt-2">{leave.reason}</p>
                          )}
                        </div>
                        <WorkflowStatusBadge status={leave.status} />
                      </div>

                      <div className="mt-4 flex gap-2 flex-wrap">
                        <button
                          onClick={() => approveLeave(leave.id)}
                          disabled={processingLeaveId === leave.id}
                          className="pg-btn-success"
                        >
                          {processingLeaveId === leave.id ? 'Processing…' : 'Approve'}
                        </button>
                        <button
                          onClick={() => rejectLeave(leave.id)}
                          disabled={processingLeaveId === leave.id}
                          className="pg-btn-danger"
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Recent submissions</h2>
              {pendingLogbook.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 bg-white px-4 py-6 text-sm text-slate-500">
                  No new submissions are waiting in the queue.
                </div>
              ) : (
                <div className="space-y-3">
                  {pendingLogbook.slice(0, 3).map((entry) => (
                    <div key={`recent-${entry.id}`} className="rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-700">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="font-medium text-slate-900">{entry.resident_name}</p>
                          <p className="text-slate-500">
                            {entry.patient_id_number} · {entry.patient_seen_at.slice(0, 10)}
                          </p>
                        </div>
                        <WorkflowStatusBadge status={entry.status} />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {opsSummary && (
              <section>
                <h2 className="text-lg font-semibold text-gray-800 mb-3">Alerts / needs attention</h2>
                {laggingResidents.length === 0 ? (
                  <div className="rounded-xl border border-dashed border-slate-200 bg-white px-4 py-6 text-sm text-slate-500">
                    No lagging residents were flagged.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {laggingResidents.slice(0, 5).map((resident) => (
                      <div key={resident.resident_id} className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                        <p className="font-medium text-amber-900">{resident.resident_name}</p>
                        <p className="text-sm text-amber-800">
                          {resident.pending_reviews} pending review(s) · {resident.logbook_approved} approved entries
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
