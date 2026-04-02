'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { LeaveRequest, RotationAssignment, trainingApi, SupervisorSummary } from '@/lib/api/training';

function CountCard({ label, count, color }: { label: string; count: number; color: string }) {
  return (
    <div className={`rounded-xl border p-4 flex flex-col ${color}`}>
      <span className="text-3xl font-bold">{count}</span>
      <span className="text-sm mt-1 opacity-80">{label}</span>
    </div>
  );
}

function StatusBadge({ status }: { status: string | null }) {
  if (!status) {
    return <span className="px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-500">—</span>;
  }
  const map: Record<string, string> = {
    ELIGIBLE: 'bg-green-100 text-green-800',
    NOT_READY: 'bg-red-100 text-red-700',
    PARTIALLY_READY: 'bg-yellow-100 text-yellow-700',
    APPROVED_BY_SUPERVISOR: 'bg-green-100 text-green-800',
    SUBMITTED_TO_SUPERVISOR: 'bg-yellow-100 text-yellow-700',
    SUBMITTED_TO_UNIVERSITY: 'bg-blue-100 text-blue-700',
    ACCEPTED_BY_UNIVERSITY: 'bg-green-100 text-green-800',
    DRAFT: 'bg-gray-100 text-gray-600',
  };
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${map[status] || 'bg-gray-100 text-gray-600'}`}>{status.replace(/_/g, ' ')}</span>;
}

export default function SupervisorHomePage() {
  const [summary, setSummary] = useState<SupervisorSummary | null>(null);
  const [pendingLeaves, setPendingLeaves] = useState<LeaveRequest[]>([]);
  const [pendingRotations, setPendingRotations] = useState<RotationAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [processingLeaveId, setProcessingLeaveId] = useState<number | null>(null);
  const [processingRotationId, setProcessingRotationId] = useState<number | null>(null);
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
      trainingApi.getSupervisorPendingLeaves(),
      trainingApi.listSupervisorPendingRotations(),
    ])
      .then(([nextSummary, nextPendingLeaves, nextPendingRotations]) => {
        setSummary(nextSummary);
        setPendingLeaves(nextPendingLeaves);
        setPendingRotations(nextPendingRotations.results || []);
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

  const approveRotation = async (rotationId: number) => {
    setProcessingRotationId(rotationId);
    try {
      await trainingApi.rotationAction(rotationId, 'hod-approve');
      flash('Rotation approved.');
      load();
    } catch {
      flash('Failed to approve rotation.', true);
    } finally {
      setProcessingRotationId(null);
    }
  };

  const returnRotation = async (rotationId: number) => {
    const reason = window.prompt('Reason for return:');
    if (reason === null) {
      return;
    }

    setProcessingRotationId(rotationId);
    try {
      await trainingApi.rotationAction(rotationId, 'returned', { reason });
      flash('Rotation returned to resident.');
      load();
    } catch {
      flash('Failed to return rotation.', true);
    } finally {
      setProcessingRotationId(null);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Supervisor Dashboard</h1>

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}
        {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4">{message}</div>}

        {summary && (
          <div className="space-y-8">
            {/* Pending Inbox */}
            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending Actions</h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <Link href="/dashboard/supervisor/research-approvals">
                  <CountCard
                    label="Research Approvals"
                    count={summary.pending.research_approvals}
                    color="bg-yellow-50 border-yellow-200 text-yellow-900 hover:bg-yellow-100 cursor-pointer transition"
                  />
                </Link>
                <CountCard
                  label="Rotation Approvals"
                  count={summary.pending.rotation_approvals}
                  color="bg-blue-50 border-blue-200 text-blue-900"
                />
                <CountCard
                  label="Leave Approvals"
                  count={summary.pending.leave_approvals}
                  color="bg-orange-50 border-orange-200 text-orange-900"
                />
              </div>
            </section>

            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Pending Rotation Requests</h2>
              {pendingRotations.length === 0 ? (
                <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-gray-200">
                  No rotation requests awaiting review.
                </div>
              ) : (
                <div className="space-y-3">
                  {pendingRotations.map((rotation) => (
                    <div key={rotation.id} className="bg-white border border-gray-200 rounded-xl p-5">
                      <div className="flex items-start justify-between gap-4 flex-wrap">
                        <div>
                          <p className="font-semibold text-gray-900">{rotation.resident_name}</p>
                          <p className="text-sm text-gray-500">
                            {rotation.department_name} · {rotation.hospital_name}
                          </p>
                          <p className="text-sm text-gray-500">
                            {rotation.start_date} → {rotation.end_date}
                          </p>
                          {rotation.notes && (
                            <p className="text-sm text-gray-700 mt-2">{rotation.notes}</p>
                          )}
                        </div>
                        <StatusBadge status={rotation.status} />
                      </div>

                      <div className="mt-4 flex gap-2 flex-wrap">
                        <button
                          onClick={() => approveRotation(rotation.id)}
                          disabled={processingRotationId === rotation.id}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
                        >
                          {processingRotationId === rotation.id ? 'Processing…' : 'Approve Rotation'}
                        </button>
                        <button
                          onClick={() => returnRotation(rotation.id)}
                          disabled={processingRotationId === rotation.id}
                          className="px-4 py-2 bg-orange-50 border border-orange-200 text-orange-700 rounded-lg text-sm font-medium hover:bg-orange-100 disabled:opacity-50"
                        >
                          Return to Resident
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
                    <div key={leave.id} className="bg-white border border-gray-200 rounded-xl p-5">
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
                        <StatusBadge status={leave.status} />
                      </div>

                      <div className="mt-4 flex gap-2 flex-wrap">
                        <button
                          onClick={() => approveLeave(leave.id)}
                          disabled={processingLeaveId === leave.id}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
                        >
                          {processingLeaveId === leave.id ? 'Processing…' : 'Approve'}
                        </button>
                        <button
                          onClick={() => rejectLeave(leave.id)}
                          disabled={processingLeaveId === leave.id}
                          className="px-4 py-2 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm font-medium hover:bg-red-100 disabled:opacity-50"
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
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-gray-600 text-xs uppercase tracking-wider">
                      <tr>
                        <th className="px-4 py-3 text-left">Resident</th>
                        <th className="px-4 py-3 text-left">Program</th>
                        <th className="px-4 py-3 text-left">Rotation</th>
                        <th className="px-4 py-3 text-left">IMM</th>
                        <th className="px-4 py-3 text-left">Final</th>
                        <th className="px-4 py-3 text-left">Research</th>
                        <th className="px-4 py-3 text-left"></th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {summary.residents.map(r => (
                        <tr key={r.id} className="hover:bg-gray-50 transition">
                          <td className="px-4 py-3 font-medium text-gray-900">{r.name}</td>
                          <td className="px-4 py-3 text-gray-600">{r.program}</td>
                          <td className="px-4 py-3 text-gray-600 text-xs">{r.current_rotation || <span className="text-gray-400">None</span>}</td>
                          <td className="px-4 py-3"><StatusBadge status={r.imm_status} /></td>
                          <td className="px-4 py-3"><StatusBadge status={r.final_status} /></td>
                          <td className="px-4 py-3"><StatusBadge status={r.research_status} /></td>
                          <td className="px-4 py-3">
                            <Link href={`/dashboard/supervisor/residents/${r.id}/progress`}
                              className="text-indigo-600 hover:underline text-xs font-medium">
                              View Progress →
                            </Link>
                          </td>
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
