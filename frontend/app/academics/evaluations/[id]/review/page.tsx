'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, EvaluationSubmission } from '@/lib/api/academics';

export default function EvaluationReviewPage() {
  const params = useParams();
  const router = useRouter();
  const subId = Number(params.id);

  const [sub, setSub] = useState<EvaluationSubmission | null>(null);
  const [loading, setLoading] = useState(true);
  const [score, setScore] = useState('');
  const [maxScore, setMaxScore] = useState('5');
  const [supervisorComments, setSupervisorComments] = useState('');
  
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    academicsApi
      .getEvaluationSubmission(subId)
      .then((data) => {
        setSub(data);
        setScore(data.score !== null ? String(data.score) : '');
        setMaxScore(data.max_score !== null ? String(data.max_score) : '5');
        setSupervisorComments(data.supervisor_comments || '');
        
        // Auto start review state if SUBMITTED
        if (data.status === 'SUBMITTED') {
          academicsApi.startEvaluationReview(subId).catch(() => {});
        }
      })
      .catch(() => setSub(null))
      .finally(() => setLoading(false));
  }, [subId]);

  const handleAction = async (actionType: 'approve' | 'return' | 'reject') => {
    setError('');
    setMessage('');
    
    if (actionType === 'return' && !supervisorComments.trim()) {
      setError('Comments are required when returning an evaluation for revision.');
      return;
    }

    try {
      if (actionType === 'approve') {
        await academicsApi.approveEvaluation(subId, {
          score: score ? Number(score) : null,
          max_score: maxScore ? Number(maxScore) : null,
          supervisor_comments: supervisorComments,
        });
        setMessage('Evaluation approved successfully.');
      } else if (actionType === 'return') {
        await academicsApi.returnEvaluation(subId, {
          supervisor_comments: supervisorComments,
        });
        setMessage('Evaluation returned to resident for revision.');
      } else if (actionType === 'reject') {
        await academicsApi.rejectEvaluation(subId, {
          supervisor_comments: supervisorComments,
        });
        setMessage('Evaluation rejected.');
      }
      setTimeout(() => router.push(`/academics/evaluations/${subId}`), 1000);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Action failed.');
    }
  };

  if (loading) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading evaluation...</div>;
  }

  if (!sub) {
    return <div className="text-center py-6 text-sm text-red-500">Evaluation not found.</div>;
  }

  return (
    <ProtectedRoute allowedRoles={['SUPERVISOR', 'ADMIN']}>
      <div className="pg-page space-y-6 max-w-3xl">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Evaluate Submission"
            description={`Assigned Resident: ${sub.resident_name}`}
          />
          <Link href={`/academics/evaluations/${sub.id}`} className="text-sm font-medium text-slate-600 hover:underline">
            View Details
          </Link>
        </div>

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        <div className="pg-card space-y-6">
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-2">
            <h3 className="text-sm font-semibold text-slate-800">Resident Self Comments</h3>
            <p className="text-sm text-slate-700 italic">{sub.resident_comments || 'No self reflection provided.'}</p>
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-slate-800">Response Verification</h3>
            <div className="grid gap-3">
              {sub.responses?.map((resp) => (
                <div key={resp.id} className="text-sm flex justify-between border-b border-slate-100 pb-2">
                  <span className="text-slate-600 font-medium">{resp.field_label}</span>
                  <span className="text-slate-900 font-semibold">
                    {resp.field_type === 'number' ? `Score: ${resp.value_number}` : resp.value_text || '—'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="border-t border-slate-100 pt-4 space-y-4">
            <h3 className="text-sm font-semibold text-slate-800">Supervisor Decision Inputs</h3>
            
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Final Score</label>
                <input
                  type="number"
                  step="0.1"
                  className="pg-form-input"
                  placeholder="e.g. 4.5"
                  value={score}
                  onChange={(e) => setScore(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Maximum Score</label>
                <input
                  type="number"
                  className="pg-form-input"
                  placeholder="e.g. 5"
                  value={maxScore}
                  onChange={(e) => setMaxScore(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Remarks & Feedback</label>
              <textarea
                className="pg-form-input min-h-[120px]"
                placeholder="Provide evaluation notes, feedback, and guidance details here..."
                value={supervisorComments}
                onChange={(e) => setSupervisorComments(e.target.value)}
              />
            </div>
          </div>

          <div className="flex flex-wrap gap-3 border-t border-slate-100 pt-4">
            <button
              onClick={() => handleAction('approve')}
              className="pg-btn-primary bg-green-600 hover:bg-green-700 border-green-600 text-white"
            >
              Approve Evaluation
            </button>
            <button
              onClick={() => handleAction('return')}
              className="pg-btn-secondary text-yellow-700 border-yellow-300 hover:bg-yellow-50"
            >
              Return for Revision
            </button>
            <button
              onClick={() => handleAction('reject')}
              className="pg-btn-secondary text-red-600 border-red-300 hover:bg-red-50"
            >
              Reject Submission
            </button>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
