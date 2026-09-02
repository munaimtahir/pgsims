'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, EvaluationSubmission } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function EvaluationDetailPage() {
  const params = useParams();
  const { user } = useAuthStore();
  const subId = Number(params.id);

  const [sub, setSub] = useState<EvaluationSubmission | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const load = () => {
    setLoading(true);
    academicsApi
      .getEvaluationSubmission(subId)
      .then(setSub)
      .catch(() => setSub(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [subId]);

  const handleSubmit = async () => {
    try {
      await academicsApi.submitEvaluation(subId);
      setMessage('Evaluation submitted successfully.');
      load();
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to submit.');
    }
  };

  const handleCancel = async () => {
    try {
      await academicsApi.cancelEvaluation(subId);
      setMessage('Evaluation submission cancelled.');
      load();
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to cancel.');
    }
  };

  if (loading) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading evaluation details...</div>;
  }

  if (!sub) {
    return <div className="text-center py-6 text-sm text-red-500">Evaluation not found.</div>;
  }

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';
  const isAdmin = user?.role === 'ADMIN';

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page space-y-6 max-w-3xl">
        <div className="flex items-center justify-between">
          <PageHeader
            title={`Evaluation Submission #${sub.id}`}
            description={`${sub.template_name}`}
          />
          <Link href="/academics/evaluations" className="text-sm font-medium text-slate-600 hover:underline">
            Back to list
          </Link>
        </div>

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        <div className="pg-card space-y-6">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Resident</div>
              <div className="text-base text-slate-900 font-semibold">{sub.resident_name} ({sub.resident_username})</div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Supervisor / Reviewer</div>
              <div className="text-base text-slate-900 font-semibold">{sub.supervisor_name || 'Not assigned'}</div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Status</div>
              <div className="mt-1">
                <span
                  className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                    sub.status === 'APPROVED'
                      ? 'bg-green-50 text-green-700'
                      : sub.status === 'SUBMITTED' || sub.status === 'UNDER_REVIEW'
                      ? 'bg-blue-50 text-blue-700'
                      : sub.status === 'RETURNED'
                      ? 'bg-yellow-50 text-yellow-700'
                      : sub.status === 'REJECTED'
                      ? 'bg-red-50 text-red-700'
                      : 'bg-gray-50 text-gray-700'
                  }`}
                >
                  {sub.status}
                </span>
              </div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Score</div>
              <div className="text-base text-slate-900 font-semibold">
                {sub.score !== null ? `${sub.score}/${sub.max_score}` : 'Pending supervisor evaluation'}
              </div>
            </div>
          </div>

          <div className="border-t border-slate-100 pt-4 space-y-3">
            <h3 className="text-sm font-semibold text-slate-800">Form Fields responses</h3>
            <div className="grid gap-4">
              {sub.responses?.map((resp) => (
                <div key={resp.id} className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                  <div className="text-xs text-slate-600 font-semibold">{resp.field_label}</div>
                  <div className="text-sm text-slate-800 mt-1">
                    {resp.field_type === 'number' ? `Score: ${resp.value_number}` : resp.value_text || '—'}
                  </div>
                </div>
              ))}
              {(!sub.responses || sub.responses.length === 0) && (
                <div className="text-sm text-slate-500">No response data fields.</div>
              )}
            </div>
          </div>

          <div className="border-t border-slate-100 pt-4 space-y-2">
            <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Resident reflection / comments</div>
            <div className="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100 min-h-[60px]">
              {sub.resident_comments || 'No comment provided.'}
            </div>
          </div>

          {sub.supervisor_comments && (
            <div className="border-t border-slate-100 pt-4 space-y-2">
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Supervisor Evaluation Remarks</div>
              <div className="text-sm text-slate-700 bg-green-50 p-3 rounded-lg border border-green-100 min-h-[60px]">
                {sub.supervisor_comments}
              </div>
            </div>
          )}

          <div className="flex gap-3 border-t border-slate-100 pt-4">
            {isResident && (sub.status === 'DRAFT' || sub.status === 'RETURNED') && (
              <button onClick={handleSubmit} className="pg-btn-primary">
                Submit for Verification
              </button>
            )}
            {isResident && (sub.status === 'SUBMITTED' || sub.status === 'UNDER_REVIEW') && (
              <button onClick={handleCancel} className="pg-btn-secondary text-red-600 border-red-200 hover:bg-red-50">
                Cancel Submission
              </button>
            )}
            {(isSupervisor || isAdmin) && (sub.status === 'SUBMITTED' || sub.status === 'UNDER_REVIEW') && (
              <Link href={`/academics/evaluations/${sub.id}/review`} className="pg-btn-primary">
                Evaluate / Review
              </Link>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
