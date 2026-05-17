'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { LeaveRequest, RotationAssignment, trainingApi, ResidentSummary } from '@/lib/api/training';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';

function EmptyStateCard({ lines }: { lines: string[] }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-slate-700">
      <div className="space-y-2 text-sm leading-6 text-slate-600">
        {lines.map((line) => (
          <p key={line}>{line}</p>
        ))}
      </div>
    </div>
  );
}

type RotationEvent = RotationAssignment & { kind: 'rotation' };
type LeaveEvent = LeaveRequest & {
  department: string;
  hospital: string;
  kind: 'leave';
};
type ScheduleEvent = RotationEvent | LeaveEvent;

const LEAVE_OPTIONS = [
  { value: 'annual', label: 'Annual Leave' },
  { value: 'sick', label: 'Sick Leave' },
  { value: 'casual', label: 'Casual Leave' },
  { value: 'study', label: 'Study Leave' },
  { value: 'maternity', label: 'Maternity Leave' },
  { value: 'other', label: 'Other' },
];

export default function ResidentSchedulePage() {
  const [summary, setSummary] = useState<ResidentSummary | null>(null);
  const [leaves, setLeaves] = useState<LeaveRequest[]>([]);
  const [rotations, setRotations] = useState<RotationAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [submittingLeaveId, setSubmittingLeaveId] = useState<number | null>(null);
  const [notice, setNotice] = useState('');
  const [message, setMessage] = useState('');
  const [leaveForm, setLeaveForm] = useState({
    leave_type: 'annual',
    start_date: '',
    end_date: '',
    reason: '',
  });

  const flash = (nextMessage: string, isError = false) => {
    if (isError) {
      setNotice(nextMessage);
    } else {
      setMessage(nextMessage);
    }

    window.setTimeout(() => {
      setNotice('');
      setMessage('');
    }, 4000);
  };

  const load = () => {
    setLoading(true);
    setNotice('');
    Promise.all([
      trainingApi.getResidentSummary(),
      trainingApi.listMyLeaves(),
      trainingApi.listMyRotations(),
    ])
      .then(([nextSummary, leaveResponse, rotationResponse]) => {
        setSummary(nextSummary);
        setLeaves(leaveResponse.results || []);
        setRotations(rotationResponse.results || []);
      })
      .catch(() => {
        setSummary(null);
        setLeaves([]);
        setRotations([]);
        setNotice('No active resident training record is linked yet.');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const createLeaveDraft = async () => {
    if (!summary?.training_record?.id) {
      flash('Training record is not available for leave requests yet.', true);
      return;
    }

    setSaving(true);
    setNotice('');
    try {
      await trainingApi.createLeave({
        resident_training: summary.training_record.id,
        leave_type: leaveForm.leave_type,
        start_date: leaveForm.start_date,
        end_date: leaveForm.end_date,
        reason: leaveForm.reason || undefined,
      });
      setLeaveForm({ leave_type: 'annual', start_date: '', end_date: '', reason: '' });
      flash('Leave request saved as draft.');
      load();
    } catch {
      flash('Failed to save leave request.', true);
    } finally {
      setSaving(false);
    }
  };

  const submitLeave = async (leaveId: number) => {
    setSubmittingLeaveId(leaveId);
    setNotice('');
    try {
      await trainingApi.submitLeave(leaveId);
      flash('Leave request submitted for review.');
      load();
    } catch {
      flash('Failed to submit leave request.', true);
    } finally {
      setSubmittingLeaveId(null);
    }
  };

  const allEvents: ScheduleEvent[] = summary ? [
    ...rotations.map((rotation) => ({ ...rotation, kind: 'rotation' as const })),
    ...leaves.map(l => ({ ...l, department: `Leave: ${l.leave_type}`, hospital: '', kind: 'leave' as const })),
  ].sort((a, b) => a.start_date.localeCompare(b.start_date)) : [];
  const hasTrainingRecord = Boolean(summary?.training_record);

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <div className="pg-page">
        <PageHeader
          title="My Schedule"
          description="Track rotation lifecycle and manage leave requests in one place."
        />

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}
        {!loading && notice && <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">{notice}</div>}
        {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4">{message}</div>}

        {!loading && !hasTrainingRecord && (
          <div className="space-y-4">
            <EmptyStateCard
              lines={[
                'No active resident training record is linked yet.',
                'This page will show your training progress once UTRMC/admin completes your setup.',
                'Please contact the UTRMC office if this is unexpected.',
              ]}
            />
            <div className="pg-card">
              <h2 className="text-lg font-semibold text-gray-800 mb-1">What you can do now</h2>
              <p className="text-sm text-gray-500 mb-4">
                Your schedule, leave requests, and rotation timeline will appear here once onboarding is complete.
              </p>
              <div className="flex flex-wrap gap-3">
                <a href="/dashboard/resident/progress" className="pg-btn-primary">
                  Open Logbook & Readiness
                </a>
                <a
                  href="/dashboard/resident"
                  className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                >
                  Back to Dashboard
                </a>
              </div>
            </div>
          </div>
        )}

        {!loading && hasTrainingRecord && summary && (
          <>
            {/* Program info bar */}
            <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 mb-6 flex items-center gap-6 flex-wrap">
              <div>
                <span className="text-xs text-indigo-500 font-semibold uppercase tracking-wider">Program</span>
                <p className="font-semibold text-gray-900">{summary.training_record.program_name}</p>
              </div>
              <div>
                <span className="text-xs text-indigo-500 font-semibold uppercase tracking-wider">Started</span>
                <p className="font-semibold text-gray-900">{summary.training_record.start_date}</p>
              </div>
              <div>
                <span className="text-xs text-indigo-500 font-semibold uppercase tracking-wider">Month</span>
                <p className="font-semibold text-gray-900">{summary.training_record.current_month_index}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)] gap-6 mb-6">
              <section className="pg-card">
                <h2 className="text-lg font-semibold text-gray-800 mb-1">Request Leave</h2>
                <p className="text-sm text-gray-500 mb-4">
                  Save a draft here, then submit it for supervisor review from your leave list.
                </p>

                <div className="space-y-3">
                  <div>
                    <label htmlFor="leave_type" className="pg-form-label">Leave Type</label>
                    <select
                      id="leave_type"
                      value={leaveForm.leave_type}
                      onChange={(event) => setLeaveForm((current) => ({ ...current, leave_type: event.target.value }))}
                      className="pg-form-input"
                      >
                      {LEAVE_OPTIONS.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label htmlFor="leave_start_date" className="pg-form-label">Start Date</label>
                      <input
                        id="leave_start_date"
                        type="date"
                        value={leaveForm.start_date}
                        onChange={(event) => setLeaveForm((current) => ({ ...current, start_date: event.target.value }))}
                        className="pg-form-input"
                      />
                    </div>
                    <div>
                      <label htmlFor="leave_end_date" className="pg-form-label">End Date</label>
                      <input
                        id="leave_end_date"
                        type="date"
                        value={leaveForm.end_date}
                        onChange={(event) => setLeaveForm((current) => ({ ...current, end_date: event.target.value }))}
                        className="pg-form-input"
                      />
                    </div>
                  </div>

                  <div>
                    <label htmlFor="leave_reason" className="pg-form-label">Reason</label>
                    <textarea
                      id="leave_reason"
                      rows={3}
                      value={leaveForm.reason}
                      onChange={(event) => setLeaveForm((current) => ({ ...current, reason: event.target.value }))}
                      className="pg-form-input"
                      placeholder="Reason for leave"
                    />
                  </div>

                  <button
                    onClick={createLeaveDraft}
                    disabled={saving || !leaveForm.start_date || !leaveForm.end_date}
                    className="pg-btn-primary"
                  >
                    {saving ? 'Saving…' : 'Save Draft'}
                  </button>
                </div>
              </section>

              <section className="pg-card">
                <h2 className="text-lg font-semibold text-gray-800 mb-1">My Leave Requests</h2>
                <p className="text-sm text-gray-500 mb-4">
                  Draft requests stay editable in principle; submitted requests wait for supervisor review.
                </p>

                {leaves.length === 0 ? (
                  <div className="text-sm text-gray-400 py-8 text-center border border-dashed border-gray-200 rounded-lg">
                    No leave requests yet.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {leaves.map((leave) => (
                      <div key={leave.id} className="pg-card-muted">
                        <div className="flex items-start justify-between gap-4 flex-wrap">
                          <div>
                            <p className="font-medium text-gray-900">
                              {LEAVE_OPTIONS.find((option) => option.value === leave.leave_type)?.label || leave.leave_type}
                            </p>
                            <p className="text-sm text-gray-500">
                              {leave.start_date} → {leave.end_date}
                            </p>
                          </div>
                          <WorkflowStatusBadge status={leave.status} />
                        </div>

                        {leave.reason && (
                          <p className="text-sm text-gray-700 mt-3">{leave.reason}</p>
                        )}

                        {leave.reject_reason && (
                          <div className="mt-3 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
                            <span className="font-medium">Rejected:</span> {leave.reject_reason}
                          </div>
                        )}

                        {leave.status === 'DRAFT' && (
                          <div className="mt-3">
                            <button
                              onClick={() => submitLeave(leave.id)}
                              disabled={submittingLeaveId === leave.id}
                              className="pg-btn-success"
                            >
                              {submittingLeaveId === leave.id ? 'Submitting…' : 'Submit for Review'}
                            </button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </div>

            {allEvents.length === 0 ? (
              <div className="text-center py-16 text-gray-400">
                <p className="text-lg">No schedule entries yet.</p>
                <p className="text-sm mt-1">Rotations and leaves will appear here once assigned.</p>
              </div>
            ) : (
              <div className="relative pl-8">
                {/* Vertical timeline line */}
                <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-200" />

                <div className="space-y-3">
                  {allEvents.map((ev, idx) => (
                    <div key={`${ev.kind}-${ev.id}-${idx}`} className="relative">
                      {/* Timeline dot */}
                      <div className={`absolute -left-5 top-4 w-3 h-3 rounded-full border-2 border-white ${
                        ev.kind === 'rotation' ? 'bg-indigo-500' : 'bg-yellow-400'
                      }`} />

                      <div className={`rounded-xl border p-4 ${
                        ev.kind === 'rotation'
                          ? 'bg-white border-gray-200'
                          : 'bg-yellow-50 border-yellow-100'
                      }`}>
                        <div className="flex items-start justify-between gap-4 flex-wrap">
                          <div>
                            {ev.kind === 'rotation' ? (
                              <>
                                <p className="font-semibold text-gray-900">{ev.department_name}</p>
                                <p className="text-sm text-gray-500">{ev.hospital_name}</p>
                                {ev.notes && (
                                  <p className="text-sm text-gray-600 mt-2 italic">{ev.notes}</p>
                                )}
                              </>
                            ) : (
                              <p className="font-semibold text-gray-700">{ev.department}</p>
                            )}
                            <p className="text-xs text-gray-400 mt-1">
                              {ev.start_date} → {ev.end_date}
                            </p>
                          </div>
                          <div className="flex flex-col items-end gap-1.5">
                            <WorkflowStatusBadge status={ev.status} />
                            <span className={`text-xs px-2 py-0.5 rounded ${
                              ev.kind === 'rotation' ? 'bg-indigo-50 text-indigo-600' : 'bg-yellow-100 text-yellow-700'
                            }`}>
                              {ev.kind === 'rotation' ? 'Rotation' : 'Leave'}
                            </span>
                          </div>
                        </div>

                        {ev.kind === 'rotation' && ev.return_reason && (
                          <div className="mt-3 bg-orange-50 border border-orange-200 text-orange-700 rounded-lg p-3 text-sm">
                            <span className="font-medium">Returned:</span> {ev.return_reason}
                          </div>
                        )}

                        {ev.kind === 'rotation' && ev.reject_reason && (
                          <div className="mt-3 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
                            <span className="font-medium">Rejected:</span> {ev.reject_reason}
                          </div>
                        )}

                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
