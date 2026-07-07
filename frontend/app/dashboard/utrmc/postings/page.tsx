'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuthStore } from '@/store/authStore';
import { trainingApi, DeputationPosting } from '@/lib/api/training';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';

const STATUS_LABELS: Record<string, string> = {
  SUBMITTED: 'Pending Approval',
  APPROVED: 'Approved',
  REJECTED: 'Rejected',
  COMPLETED: 'Completed',
};

export default function UTRMCPostingsPage() {
  const { user } = useAuthStore();
  const canManagePostings = user?.role === 'ADMIN';
  const [postings, setPostings] = useState<DeputationPosting[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [filter, setFilter] = useState('');
  const [rejectId, setRejectId] = useState<number | null>(null);
  const [rejectReason, setRejectReason] = useState('');
  const [acting, setActing] = useState<number | null>(null);

  useEffect(() => {
    setLoading(true);
    trainingApi.listPostings(filter ? { status: filter } : undefined)
      .then(setPostings)
      .catch(() => setError('Failed to load postings.'))
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  const flash = (msg: string, isErr = false) => {
    if (isErr) { setError(msg); } else { setSuccess(msg); }
    setTimeout(() => { setError(''); setSuccess(''); }, 4000);
  };

  const doAction = async (id: number, action: 'approve' | 'complete', data?: object) => {
    setActing(id);
    try {
      const updated = await trainingApi.postingAction(id, action, data);
      setPostings((prev) => prev.map((p) => (p.id === id ? updated : p)));
      flash(`Posting ${action}d successfully.`);
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      flash(msg || `Failed to ${action}.`, true);
    } finally {
      setActing(null);
    }
  };

  const doReject = async () => {
    if (!rejectId) return;
    setActing(rejectId);
    try {
      const updated = await trainingApi.postingAction(rejectId, 'reject', { reason: rejectReason });
      setPostings((prev) => prev.map((p) => (p.id === rejectId ? updated : p)));
      setRejectId(null);
      setRejectReason('');
      flash('Posting rejected.');
    } catch {
      flash('Failed to reject.', true);
    } finally {
      setActing(null);
    }
  };

  const visible = postings;

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'ADMIN', 'SUPPORT_STAFF']}>
      <div className="pg-page max-w-5xl">
        <PageHeader
          title="Deputation Postings"
          description="Review, approve, reject, and complete resident external posting requests."
        />

        {/* Status filter */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {['', 'SUBMITTED', 'APPROVED', 'REJECTED', 'COMPLETED'].map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                filter === s
                  ? 'bg-indigo-600 text-white border-indigo-600'
                  : 'bg-white text-gray-600 border-gray-200 hover:border-indigo-300 hover:text-indigo-600'
              }`}
            >
              {s ? STATUS_LABELS[s] : 'All'}
            </button>
          ))}
        </div>

        {error && <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{error}</div>}
        {success && <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700">{success}</div>}
        {!canManagePostings && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
            Deputation postings are read-only for FMU-UTRMC support staff. Approval and completion actions require an admin account.
          </div>
        )}

        {loading && <p className="text-gray-400 text-sm">Loading…</p>}

        {!loading && visible.length === 0 && (
          <div className="pg-empty-state">
            <p className="text-lg font-medium">No postings found</p>
            <p className="text-sm mt-1">Residents submit deputation requests from their portal.</p>
          </div>
        )}

        <div className="space-y-4">
          {visible.map((posting) => (
            <div key={posting.id} className="pg-card">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <WorkflowStatusBadge status={posting.status} label={STATUS_LABELS[posting.status] ?? posting.status} />
                    <span className="text-xs text-gray-400 uppercase tracking-wide">{posting.posting_type || 'Deputation'}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900">{posting.institution_name}</h3>
                  {posting.city && <p className="text-sm text-gray-500">{posting.city}</p>}
                  <p className="text-sm text-gray-600 mt-1">
                    <span className="font-medium">Resident:</span> {posting.resident_name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {posting.start_date} → {posting.end_date}
                  </p>
                  {posting.notes && (
                    <p className="text-sm text-gray-500 mt-2 italic">{posting.notes}</p>
                  )}
                  {posting.reject_reason && (
                    <p className="text-sm text-red-600 mt-2">
                      <span className="font-medium">Rejection reason:</span> {posting.reject_reason}
                    </p>
                  )}
                  {posting.approved_at && (
                    <p className="text-xs text-gray-400 mt-1">
                      Approved {new Date(posting.approved_at).toLocaleDateString()}
                    </p>
                  )}
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2 flex-shrink-0">
                  {canManagePostings && posting.status === 'SUBMITTED' && (
                    <>
                        <button
                          disabled={acting === posting.id}
                          onClick={() => doAction(posting.id, 'approve')}
                          className="pg-btn-success px-3 py-1.5 text-xs"
                        >
                          {acting === posting.id ? '…' : 'Approve'}
                        </button>
                      <button
                          disabled={acting === posting.id}
                          onClick={() => { setRejectId(posting.id); setRejectReason(''); }}
                          className="pg-btn-danger px-3 py-1.5 text-xs"
                        >
                          Reject
                        </button>
                    </>
                  )}
                  {canManagePostings && posting.status === 'APPROVED' && (
                      <button
                        disabled={acting === posting.id}
                        onClick={() => doAction(posting.id, 'complete')}
                        className="pg-btn-primary px-3 py-1.5 text-xs"
                      >
                        {acting === posting.id ? '…' : 'Mark Complete'}
                      </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Reject modal */}
        {rejectId !== null && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
            <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Reject Posting</h2>
              <label className="block text-sm font-medium text-gray-700 mb-1">Reason (optional)</label>
                <textarea
                rows={3}
                value={rejectReason}
                onChange={(e) => setRejectReason(e.target.value)}
                placeholder="Explain the reason for rejection…"
                  className="pg-form-input"
                />
                <div className="flex gap-3 mt-4">
                  <button
                    onClick={doReject}
                    disabled={acting !== null}
                    className="flex-1 pg-btn-danger"
                  >
                    {acting !== null ? 'Rejecting…' : 'Confirm Reject'}
                  </button>
                <button
                  onClick={() => setRejectId(null)}
                  className="flex-1 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
