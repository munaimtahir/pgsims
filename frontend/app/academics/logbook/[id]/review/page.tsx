'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, LogbookEntry } from '@/lib/api/academics';

export default function LogbookReviewPage() {
  const params = useParams();
  const router = useRouter();
  const entryId = Number(params.id);

  const [entry, setEntry] = useState<LogbookEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [supervisorComments, setSupervisorComments] = useState('');
  
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    academicsApi
      .getLogbookEntry(entryId)
      .then((data) => {
        setEntry(data);
        setSupervisorComments(data.supervisor_comments || '');
      })
      .catch(() => setEntry(null))
      .finally(() => setLoading(false));
  }, [entryId]);

  const handleAction = async (actionType: 'verify' | 'return' | 'reject') => {
    setError('');
    setMessage('');
    
    if (actionType === 'return' && !supervisorComments.trim()) {
      setError('Comments are required when returning an entry for revision.');
      return;
    }

    try {
      if (actionType === 'verify') {
        await academicsApi.verifyLogbookEntry(entryId, {
          supervisor_comments: supervisorComments,
        });
        setMessage('Logbook entry verified successfully.');
      } else if (actionType === 'return') {
        await academicsApi.returnLogbookEntry(entryId, {
          supervisor_comments: supervisorComments,
        });
        setMessage('Logbook entry returned to resident for revision.');
      } else if (actionType === 'reject') {
        await academicsApi.rejectLogbookEntry(entryId, {
          supervisor_comments: supervisorComments,
        });
        setMessage('Logbook entry rejected.');
      }
      setTimeout(() => router.push(`/academics/logbook/${entryId}`), 1000);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Action failed.');
    }
  };

  if (loading) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading entry...</div>;
  }

  if (!entry) {
    return <div className="text-center py-6 text-sm text-red-500">Logbook entry not found.</div>;
  }

  return (
    <ProtectedRoute allowedRoles={['SUPERVISOR', 'ADMIN']}>
      <div className="pg-page space-y-6 max-w-3xl">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Verify Logbook Submission"
            description={`Assigned Resident: ${entry.resident_name}`}
          />
          <Link href={`/academics/logbook/${entry.id}`} className="text-sm font-medium text-slate-600 hover:underline">
            View Details
          </Link>
        </div>

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        <div className="pg-card space-y-6">
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-2">
            <h3 className="text-sm font-semibold text-slate-800">Case Description</h3>
            <p className="text-sm text-slate-700">{entry.description || 'No description provided.'}</p>
          </div>

          {entry.procedure_record && (
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-slate-800">Procedure Details</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span className="text-slate-500">Procedure:</span>{' '}
                  <span className="font-semibold text-slate-800">{entry.procedure_record.procedure_name}</span>
                </div>
                <div>
                  <span className="text-slate-500">Code:</span>{' '}
                  <span className="font-semibold text-slate-800">{entry.procedure_record.procedure_code || '—'}</span>
                </div>
                <div>
                  <span className="text-slate-500">Role:</span>{' '}
                  <span className="font-semibold text-slate-800">{entry.procedure_record.role_performed}</span>
                </div>
                <div>
                  <span className="text-slate-500">Complexity:</span>{' '}
                  <span className="font-semibold text-slate-800">{entry.procedure_record.complexity}</span>
                </div>
                <div>
                  <span className="text-slate-500">Outcome:</span>{' '}
                  <span className="font-semibold text-slate-800">{entry.procedure_record.outcome}</span>
                </div>
              </div>
            </div>
          )}

          <div className="border-t border-slate-100 pt-4 space-y-2">
            <h3 className="text-sm font-semibold text-slate-800">Resident Self Reflection</h3>
            <p className="text-sm text-slate-700 italic">{entry.resident_reflection || 'No reflection provided.'}</p>
          </div>

          <div className="border-t border-slate-100 pt-4 space-y-4">
            <h3 className="text-sm font-semibold text-slate-800">Verification Comments</h3>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Supervisor Remarks & Feedback</label>
              <textarea
                className="pg-form-input min-h-[120px]"
                placeholder="Provide feedback on technique, case presentation, or verification details..."
                value={supervisorComments}
                onChange={(e) => setSupervisorComments(e.target.value)}
              />
            </div>
          </div>

          <div className="flex flex-wrap gap-3 border-t border-slate-100 pt-4">
            <button
              onClick={() => handleAction('verify')}
              className="pg-btn-primary bg-green-600 hover:bg-green-700 border-green-600 text-white"
            >
              Verify Entry
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
              Reject Entry
            </button>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
