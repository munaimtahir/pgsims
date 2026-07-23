'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi } from '@/lib/api/academics';

interface CoSupervisorRow {
  id: number;
  name: string;
}

interface LogbookSummaryRow {
  category_id: number;
  category_name: string;
  category_type: string;
  verified_count: number;
  minimum_required: number | null;
}

interface ProgressData {
  program_name: string | null;
  department_name: string | null;
  training_year: number | null;
  training_record_status: string | null;
  start_date: string | null;
  expected_end_date: string | null;
  primary_supervisor: { name: string; email?: string | null } | null;
  co_supervisors?: CoSupervisorRow[];
  evaluations_approved?: number;
  evaluations_pending?: number;
  evaluations_total?: number;
  logbooks_summary?: LogbookSummaryRow[];
}

export default function MyProgressPage() {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getMyAcademicProgress()
      .then((data) => setProgress(data as unknown as ProgressData))
      .catch(() => setProgress(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading progress...</div>;
  }

  if (!progress) {
    return (
      <div className="text-center py-6 text-sm text-red-500">
        Personal academic progress data is not available. Please verify you have an active training record.
      </div>
    );
  }

  return (
    <ProtectedRoute allowedRoles={['RESIDENT']}>
      <div className="pg-page space-y-6 max-w-4xl">
        <PageHeader
          title="My Academic Progress"
          description="View your training records, supervisor assignments, evaluation submissions, and logbook procedure metrics."
        />

        <div className="grid gap-6 md:grid-cols-2">
          {/* Training Record Card */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Training Spine Record</h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-slate-500 font-medium">Program:</span>{' '}
                <span className="font-semibold text-slate-800">{progress.program_name || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Department:</span>{' '}
                <span className="font-semibold text-slate-800">{progress.department_name || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Training Year:</span>{' '}
                <span className="font-semibold text-slate-800">Year {progress.training_year || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Status:</span>{' '}
                <span className="font-semibold text-indigo-600">{progress.training_record_status}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Start Date:</span>{' '}
                <span className="font-semibold text-slate-800">{progress.start_date || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Expected End:</span>{' '}
                <span className="font-semibold text-slate-800">{progress.expected_end_date || '—'}</span>
              </div>
            </div>
          </div>

          {/* Supervision Assignment Card */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Supervisor Assignment</h2>
            {progress.primary_supervisor ? (
              <div className="space-y-2">
                <div className="text-sm">
                  <div className="text-slate-500 font-medium">Primary Supervisor</div>
                  <div className="font-semibold text-slate-800 text-base">{progress.primary_supervisor.name}</div>
                  <div className="text-xs text-slate-500">{progress.primary_supervisor.email || 'No email registered'}</div>
                </div>
                {progress.co_supervisors && progress.co_supervisors.length > 0 && (
                  <div className="text-sm border-t border-slate-100 pt-2">
                    <div className="text-slate-500 font-medium mb-1">Co-Supervisors</div>
                    <ul className="list-disc pl-4 text-slate-700 space-y-1">
                      {progress.co_supervisors.map((co) => (
                        <li key={co.id}>{co.name}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-sm text-yellow-600 font-medium">
                No primary supervisor assignment found. Please contact administration.
              </div>
            )}
          </div>
        </div>

        {/* Evaluation Summary */}
        <div className="pg-card space-y-4">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Rotation Evaluations & Reviews</h2>
          <div className="grid gap-4 sm:grid-cols-3 text-center">
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div className="text-2xl font-bold text-slate-900">{progress.evaluations_approved || 0}</div>
              <div className="text-xs text-slate-500 font-medium">Approved / Verified</div>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div className="text-2xl font-bold text-slate-900">{progress.evaluations_pending || 0}</div>
              <div className="text-xs text-slate-500 font-medium">Pending Review</div>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div className="text-2xl font-bold text-slate-900">{progress.evaluations_total || 0}</div>
              <div className="text-xs text-slate-500 font-medium">Total Logged</div>
            </div>
          </div>
        </div>

        {/* Logbooks Categories & Progress */}
        <div className="pg-card space-y-4">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Logbook Procedures & Milestones</h2>
          <div className="space-y-4">
            {progress.logbooks_summary?.map((cat) => {
              const count = cat.verified_count;
              const req = cat.minimum_required || 0;
              const percent = req > 0 ? Math.min(Math.round((count / req) * 100), 100) : 100;
              return (
                <div key={cat.category_id} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-semibold text-slate-800">{cat.category_name} ({cat.category_type})</span>
                    <span className="text-slate-600">
                      {count} / {req > 0 ? req : 'No Min'} verified
                    </span>
                  </div>
                  {req > 0 && (
                    <div className="w-full bg-slate-100 rounded-full h-2.5">
                      <div
                        className={`h-2.5 rounded-full ${percent === 100 ? 'bg-green-500' : 'bg-indigo-600'}`}
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                  )}
                </div>
              );
            })}
            {(!progress.logbooks_summary || progress.logbooks_summary.length === 0) && (
              <p className="text-sm text-slate-500">No logbook entries or categories registered.</p>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
