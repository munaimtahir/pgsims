'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, LogbookEntry } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function LogbookDetailPage() {
  const params = useParams();
  const { user } = useAuthStore();
  const entryId = Number(params.id);

  const [entry, setEntry] = useState<LogbookEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const load = () => {
    setLoading(true);
    academicsApi
      .getLogbookEntry(entryId)
      .then(setEntry)
      .catch(() => setEntry(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entryId]);

  const handleSubmit = async () => {
    try {
      await academicsApi.submitLogbookEntry(entryId);
      setMessage('Logbook entry submitted successfully.');
      load();
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to submit logbook entry.');
    }
  };

  const handleCancel = async () => {
    try {
      await academicsApi.cancelLogbookEntry(entryId);
      setMessage('Logbook entry submission cancelled.');
      load();
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to cancel submission.');
    }
  };

  if (loading) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading logbook entry...</div>;
  }

  if (!entry) {
    return <div className="text-center py-6 text-sm text-red-500">Logbook entry not found.</div>;
  }

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';
  const isAdmin = user?.role === 'ADMIN';

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page space-y-6 max-w-3xl">
        <div className="flex items-center justify-between">
          <PageHeader
            title={`Logbook Entry #${entry.id}`}
            description={entry.title}
          />
          <Link href="/academics/logbook" className="text-sm font-medium text-slate-600 hover:underline">
            Back to list
          </Link>
        </div>

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        <div className="pg-card space-y-6">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Resident</div>
              <div className="text-base text-slate-900 font-semibold">{entry.resident_name}</div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Assigned Supervisor / Verifier</div>
              <div className="text-base text-slate-900 font-semibold">{entry.supervisor_name || 'Not assigned'}</div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Category</div>
              <div className="text-base text-slate-900 font-semibold">{entry.category_name}</div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Date Logged</div>
              <div className="text-base text-slate-900 font-semibold">
                {entry.entry_date ? new Date(entry.entry_date).toLocaleDateString() : '—'}
              </div>
            </div>
            <div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Status</div>
              <div className="mt-1">
                <span
                  className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                    entry.status === 'VERIFIED'
                      ? 'bg-green-50 text-green-700'
                      : entry.status === 'SUBMITTED'
                      ? 'bg-blue-50 text-blue-700'
                      : entry.status === 'RETURNED'
                      ? 'bg-yellow-50 text-yellow-700'
                      : entry.status === 'REJECTED'
                      ? 'bg-red-50 text-red-700'
                      : 'bg-gray-50 text-gray-700'
                  }`}
                >
                  {entry.status}
                </span>
              </div>
            </div>
            {entry.case_identifier && (
              <div>
                <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Case Identifier</div>
                <div className="text-base text-slate-900 font-semibold">{entry.case_identifier}</div>
              </div>
            )}
            {(entry.patient_age || entry.patient_gender) && (
              <div>
                <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Patient Demographics</div>
                <div className="text-base text-slate-900 font-semibold">
                  {[entry.patient_age, entry.patient_gender].filter(Boolean).join(', ')}
                </div>
              </div>
            )}
          </div>

          {entry.description && (
            <div className="border-t border-slate-100 pt-4 space-y-2">
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Case Description / Context</div>
              <p className="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100 min-h-[60px] whitespace-pre-line">
                {entry.description}
              </p>
            </div>
          )}

          {entry.procedure_record && (
            <div className="border-t border-slate-100 pt-4 space-y-3">
              <h3 className="text-sm font-semibold text-slate-800">Procedure Details</h3>
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 grid gap-3 md:grid-cols-2">
                <div>
                  <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Procedure Name</div>
                  <div className="text-sm text-slate-800 font-medium">{entry.procedure_record.procedure_name}</div>
                </div>
                {entry.procedure_record.procedure_code && (
                  <div>
                    <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">CPT/Billing Code</div>
                    <div className="text-sm text-slate-800 font-medium">{entry.procedure_record.procedure_code}</div>
                  </div>
                )}
                <div>
                  <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Role Performed</div>
                  <div className="text-sm text-slate-800 font-medium">{entry.procedure_record.role_performed}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Complexity</div>
                  <div className="text-sm text-slate-800 font-medium">{entry.procedure_record.complexity}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Outcome</div>
                  <div className="text-sm text-slate-800 font-medium">{entry.procedure_record.outcome}</div>
                </div>
                {entry.procedure_record.complications && (
                  <div>
                    <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Complications</div>
                    <div className="text-sm text-red-600 font-medium">{entry.procedure_record.complications}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {entry.resident_reflection && (
            <div className="border-t border-slate-100 pt-4 space-y-2">
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Resident Reflection</div>
              <p className="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100 min-h-[60px] whitespace-pre-line">
                {entry.resident_reflection}
              </p>
            </div>
          )}

          {entry.supervisor_comments && (
            <div className="border-t border-slate-100 pt-4 space-y-2">
              <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Supervisor Remarks & Feedback</div>
              <p className="text-sm text-slate-700 bg-green-50 p-3 rounded-lg border border-green-100 min-h-[60px] whitespace-pre-line">
                {entry.supervisor_comments}
              </p>
            </div>
          )}

          <div className="flex gap-3 border-t border-slate-100 pt-4">
            {isResident && (entry.status === 'DRAFT' || entry.status === 'RETURNED') && (
              <button onClick={handleSubmit} className="pg-btn-primary">
                Submit for Verification
              </button>
            )}
            {isResident && entry.status === 'SUBMITTED' && (
              <button onClick={handleCancel} className="pg-btn-secondary text-red-600 border-red-200 hover:bg-red-50">
                Cancel Submission
              </button>
            )}
            {(isSupervisor || isAdmin) && entry.status === 'SUBMITTED' && (
              <Link href={`/academics/logbook/${entry.id}/review`} className="pg-btn-primary">
                Verify / Review
              </Link>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
