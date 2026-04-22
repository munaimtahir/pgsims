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
          description="Review assigned residents, clear approval queues, and monitor departmental lag."
        />

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}
        {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4">{message}</div>}

        {summary && (
          <div className="space-y-8">
            {/* Pending Inbox */}
            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending Actions</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <MetricCard
                  label="Logbook Reviews"
                  value={opsSummary?.pending_logbook_reviews || 0}
                  tone="info"
                />
                <MetricCard
                  label="Leave Approvals"
                  value={summary.pending.leave_approvals}
                  tone="warning"
                />
              </div>
            </section>

            {opsSummary && (
              <section>
                <h2 className="text-lg font-semibold text-gray-800 mb-3">
                  Operational Snapshot {opsSummary.is_hod ? '(HOD Scope)' : ''}
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {[
                    { label: 'Assigned Residents', value: opsSummary.assigned_residents },
                    { label: 'Pending Logbook', value: opsSummary.pending_logbook_reviews },
                    { label: 'Returned Logbook', value: opsSummary.returned_logbook_queue },
                  ].map((item) => (
                    <MetricCard key={item.label} label={item.label} value={item.value} />
                  ))}
                </div>
              </section>
            )}

            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending Logbook Reviews</h2>
              {pendingLogbook.length === 0 ? (
                <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-gray-200">
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
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending Leave Requests</h2>
              {pendingLeaves.length === 0 ? (
                <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-gray-200">
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

            {/* Residents Table */}
            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">My Residents</h2>
              {summary.residents.length === 0 ? (
                <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-gray-200">
                  No residents assigned to you yet.
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
                      {summary.residents.map(r => (
                        <tr key={r.id} className="hover:bg-gray-50 transition">
                          <td className="px-4 py-3 font-medium text-gray-900">{r.name}</td>
                          <td className="px-4 py-3 text-gray-600">{r.program}</td>
                          <td className="px-4 py-3 text-gray-600 text-xs">{r.current_rotation || <span className="text-gray-400">None</span>}</td>
                          <td className="px-4 py-3"><WorkflowStatusBadge status={r.imm_status} /></td>
                          <td className="px-4 py-3"><WorkflowStatusBadge status={r.final_status} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
