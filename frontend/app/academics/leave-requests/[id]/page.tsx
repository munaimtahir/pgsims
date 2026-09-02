'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import { leaveApi, LeaveRequest } from '@/lib/api/leave';
import { useAuthStore } from '@/store/authStore';

export default function LeaveRequestDetailPage() {
  const params = useParams();
  const id = Number(params.id);
  const { user } = useAuthStore();
  const [leave, setLeave] = useState<LeaveRequest | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [acting, setActing] = useState(false);
  const [reason, setReason] = useState('');

  const load = () => {
    setLoading(true);
    leaveApi
      .get(id)
      .then(setLeave)
      .catch(() => setError('Unable to load leave request'))
      .finally(() => setLoading(false));
  };

  useEffect(load, [id]);

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';
  const isAdmin = user?.role === 'ADMIN';

  const runAction = async (fn: () => Promise<LeaveRequest>) => {
    setActing(true);
    setError('');
    try {
      const updated = await fn();
      setLeave(updated);
      setReason('');
    } catch (err: unknown) {
      const message =
        typeof err === 'object' && err !== null && 'response' in err
          ? JSON.stringify((err as { response?: { data?: unknown } }).response?.data)
          : 'Action failed';
      setError(message);
    } finally {
      setActing(false);
    }
  };

  if (loading) {
    return (
      <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
        <div className="pg-page">
          <div className="text-center py-6 text-sm text-slate-500">Loading...</div>
        </div>
      </ProtectedRoute>
    );
  }

  if (!leave) {
    return (
      <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
        <div className="pg-page">
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error || 'Leave request not found.'}
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  const canSubmit = (isAdmin || isResident) && leave.status === 'DRAFT';
  const canReview = (isSupervisor || isAdmin) && leave.status === 'SUBMITTED';

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page max-w-3xl space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title={`Leave Request #${leave.id}`}
            description={`${leave.resident_name} — ${leave.leave_type} leave`}
          />
          <Link href="/academics/leave-requests" className="text-sm font-medium text-indigo-600 hover:underline">
            Back to list
          </Link>
        </div>

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="pg-card space-y-3">
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-slate-500">Status</span>
            <WorkflowStatusBadge status={leave.status} />
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-slate-500">Resident</div>
              <div className="font-medium text-slate-900">{leave.resident_name}</div>
            </div>
            <div>
              <div className="text-slate-500">Leave Type</div>
              <div className="font-medium text-slate-900 capitalize">{leave.leave_type}</div>
            </div>
            <div>
              <div className="text-slate-500">Start Date</div>
              <div className="font-medium text-slate-900">
                {new Date(leave.start_date).toLocaleDateString()}
              </div>
            </div>
            <div>
              <div className="text-slate-500">End Date</div>
              <div className="font-medium text-slate-900">
                {new Date(leave.end_date).toLocaleDateString()}
              </div>
            </div>
          </div>
          {leave.reason && (
            <div className="text-sm">
              <div className="text-slate-500">Reason</div>
              <div className="whitespace-pre-wrap text-slate-800">{leave.reason}</div>
            </div>
          )}
          {leave.reject_reason && (
            <div className="text-sm">
              <div className="text-slate-500">Reject Reason</div>
              <div className="text-red-700">{leave.reject_reason}</div>
            </div>
          )}
        </div>

        {(canSubmit || canReview) && (
          <div className="pg-card space-y-4">
            <h3 className="text-sm font-semibold text-slate-700">Actions</h3>

            {canSubmit && (
              <button
                disabled={acting}
                onClick={() => runAction(() => leaveApi.submit(leave.id))}
                className="pg-btn-primary"
              >
                Submit for Approval
              </button>
            )}

            {canReview && (
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">
                  Reason (required for reject)
                </label>
                <textarea
                  className="pg-form-input w-full"
                  rows={2}
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                />
                <div className="flex gap-2">
                  <button
                    disabled={acting}
                    onClick={() => runAction(() => leaveApi.approve(leave.id))}
                    className="pg-btn-success"
                  >
                    Approve
                  </button>
                  <button
                    disabled={acting}
                    onClick={() => runAction(() => leaveApi.reject(leave.id, reason))}
                    className="pg-btn-danger"
                  >
                    Reject
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
