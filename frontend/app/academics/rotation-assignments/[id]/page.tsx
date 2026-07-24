'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import { rotationsApi, RotationAssignment } from '@/lib/api/rotations';
import { useAuthStore } from '@/store/authStore';

export default function RotationAssignmentDetailPage() {
  const params = useParams();
  const id = Number(params.id);
  const { user } = useAuthStore();
  const [rotation, setRotation] = useState<RotationAssignment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [acting, setActing] = useState(false);
  const [reason, setReason] = useState('');

  const load = () => {
    setLoading(true);
    rotationsApi
      .get(Number(id))
      .then(setRotation)
      .catch(() => setError('Unable to load rotation assignment'))
      .finally(() => setLoading(false));
  };

  useEffect(load, [id]);

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';
  const isAdmin = user?.role === 'ADMIN';

  const runAction = async (fn: () => Promise<RotationAssignment>) => {
    setActing(true);
    setError('');
    try {
      const updated = await fn();
      setRotation(updated);
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

  if (!rotation) {
    return (
      <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
        <div className="pg-page">
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error || 'Rotation assignment not found.'}
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  const canSubmit =
    (isAdmin || isResident) &&
    (rotation.status === 'DRAFT' || rotation.status === 'RETURNED');
  const canReview =
    (isSupervisor || isAdmin) &&
    (rotation.status === 'SUBMITTED' || rotation.status === 'APPROVED');
  const canUtrmcApprove =
    isAdmin && (rotation.status === 'SUBMITTED' || rotation.status === 'APPROVED');
  const canActivate = isAdmin && rotation.status === 'APPROVED';
  const canComplete = isAdmin && rotation.status === 'ACTIVE';

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page max-w-3xl space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title={`Rotation Assignment #${rotation.id}`}
            description={`${rotation.resident_name} — ${rotation.hospital_name} / ${rotation.department_name}`}
          />
          <Link href="/academics/rotation-assignments" className="text-sm font-medium text-indigo-600 hover:underline">
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
            <WorkflowStatusBadge status={rotation.status} />
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-slate-500">Resident</div>
              <div className="font-medium text-slate-900">{rotation.resident_name}</div>
            </div>
            <div>
              <div className="text-slate-500">Program</div>
              <div className="font-medium text-slate-900">{rotation.program_name}</div>
            </div>
            <div>
              <div className="text-slate-500">Hospital</div>
              <div className="font-medium text-slate-900">{rotation.hospital_name}</div>
            </div>
            <div>
              <div className="text-slate-500">Department</div>
              <div className="font-medium text-slate-900">{rotation.department_name}</div>
            </div>
            <div>
              <div className="text-slate-500">Start Date</div>
              <div className="font-medium text-slate-900">
                {new Date(rotation.start_date).toLocaleDateString()}
              </div>
            </div>
            <div>
              <div className="text-slate-500">End Date</div>
              <div className="font-medium text-slate-900">
                {new Date(rotation.end_date).toLocaleDateString()}
              </div>
            </div>
          </div>
          {rotation.notes && (
            <div className="text-sm">
              <div className="text-slate-500">Notes</div>
              <div className="whitespace-pre-wrap text-slate-800">{rotation.notes}</div>
            </div>
          )}
          {rotation.return_reason && (
            <div className="text-sm">
              <div className="text-slate-500">Return Reason</div>
              <div className="text-orange-700">{rotation.return_reason}</div>
            </div>
          )}
          {rotation.reject_reason && (
            <div className="text-sm">
              <div className="text-slate-500">Reject Reason</div>
              <div className="text-red-700">{rotation.reject_reason}</div>
            </div>
          )}
        </div>

        {(canSubmit || canReview || canUtrmcApprove || canActivate || canComplete) && (
          <div className="pg-card space-y-4">
            <h3 className="text-sm font-semibold text-slate-700">Actions</h3>

            {canSubmit && (
              <button
                disabled={acting}
                onClick={() => runAction(() => rotationsApi.submit(rotation.id))}
                className="pg-btn-primary"
              >
                Submit for Review
              </button>
            )}

            {canReview && (
              <div className="space-y-2 border-t border-slate-100 pt-4">
                <label className="block text-sm font-medium text-slate-700">
                  Reason (required for reject/defer)
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
                    onClick={() =>
                      runAction(() =>
                        rotationsApi.reviewApplication(rotation.id, { action: 'approve', reason })
                      )
                    }
                    className="pg-btn-success"
                  >
                    Approve
                  </button>
                  <button
                    disabled={acting}
                    onClick={() =>
                      runAction(() =>
                        rotationsApi.reviewApplication(rotation.id, { action: 'defer', reason })
                      )
                    }
                    className="pg-btn-warning"
                  >
                    Return for Revision
                  </button>
                  <button
                    disabled={acting}
                    onClick={() =>
                      runAction(() =>
                        rotationsApi.reviewApplication(rotation.id, { action: 'reject', reason })
                      )
                    }
                    className="pg-btn-danger"
                  >
                    Reject
                  </button>
                </div>
              </div>
            )}

            {canUtrmcApprove && (
              <button
                disabled={acting}
                onClick={() => runAction(() => rotationsApi.utrmcApprove(rotation.id))}
                className="pg-btn-success"
              >
                UTRMC Approve
              </button>
            )}

            {canActivate && (
              <button
                disabled={acting}
                onClick={() => runAction(() => rotationsApi.activate(rotation.id))}
                className="pg-btn-primary"
              >
                Activate Rotation
              </button>
            )}

            {canComplete && (
              <button
                disabled={acting}
                onClick={() => runAction(() => rotationsApi.complete(rotation.id))}
                className="pg-btn-primary"
              >
                Mark Completed
              </button>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
