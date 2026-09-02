'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi } from '@/lib/api/academics';
import apiClient from '@/lib/api/client';

interface CoSupervisor {
  id: number;
  name: string;
}

interface LogbookSummary {
  category_id: number;
  category_name: string;
  category_type: string;
  verified_count: number;
  minimum_required: number | null;
}

interface ProgressReport {
  resident?: {
    id: number;
    name: string;
    username: string;
    email: string;
    hospital_name: string | null;
    program_name: string | null;
    department_name: string | null;
  };
  progress?: {
    training_record_id: number | null;
    program_name: string | null;
    department_name: string | null;
    training_year: number | null;
    training_record_status: string | null;
    start_date: string | null;
    expected_end_date: string | null;
    primary_supervisor: { name: string; email?: string | null } | null;
    co_supervisors?: CoSupervisor[];
    evaluations_total: number;
    evaluations_approved: number;
    evaluations_pending: number;
    logbooks_total: number;
    logbooks_verified: number;
    logbooks_pending: number;
    logbooks_summary?: LogbookSummary[];
  };
}

export default function ResidentProgressReportDetailPage() {
  const params = useParams();
  const residentId = Number(params.id);

  const [report, setReport] = useState<ProgressReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getResidentProgressReportDetail(residentId)
      .then((data) => setReport(data as unknown as ProgressReport))
      .catch(() => setReport(null))
      .finally(() => setLoading(false));
  }, [residentId]);

  if (loading) {
    return <div className="text-center py-8 text-sm text-slate-500">Loading progress report...</div>;
  }

  if (!report || !report.resident || !report.progress) {
    return (
      <div className="text-center py-8 text-sm text-red-500">
        Resident progress report is not available. Please verify active training records exist.
      </div>
    );
  }

  const res = report.resident;
  const prog = report.progress;

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR', 'RESIDENT']}>
      <div className="pg-page space-y-6 max-w-4xl">
        <div className="flex items-center justify-between">
          <PageHeader
            title={`${res.name}'s Academic Progress Report`}
            description="Detail view of the postgraduate training spine, assigned primary supervisor, and procedure requirements."
          />
          <a
            href={`${apiClient.defaults.baseURL || ''}/api/academics/reports/resident-progress/export.csv?resident_id=${res.id}`}
            target="_blank"
            rel="noreferrer"
            className="pg-btn-secondary border-indigo-300 text-indigo-700 hover:bg-indigo-50"
          >
            Export Progress CSV
          </a>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Identity Card */}
          <div className="pg-card space-y-3">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-1.5">Resident Identity</h2>
            <div className="space-y-1.5 text-sm">
              <div>
                <span className="text-slate-500 font-medium">Full Name:</span>{' '}
                <span className="font-semibold text-slate-800">{res.name}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Username:</span>{' '}
                <span className="font-semibold text-slate-850">{res.username}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Email:</span>{' '}
                <span className="font-semibold text-slate-800">{res.email}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Hospital:</span>{' '}
                <span className="font-semibold text-slate-850">{res.hospital_name || '—'}</span>
              </div>
            </div>
          </div>

          {/* Training Spine status */}
          <div className="pg-card space-y-3">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-1.5">Training Spine</h2>
            <div className="space-y-1.5 text-sm">
              <div>
                <span className="text-slate-500 font-medium">Program:</span>{' '}
                <span className="font-semibold text-slate-800">{prog.program_name || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Department:</span>{' '}
                <span className="font-semibold text-slate-800">{prog.department_name || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Training Year:</span>{' '}
                <span className="font-semibold text-slate-800">Year {prog.training_year || '—'}</span>
              </div>
              <div>
                <span className="text-slate-500 font-medium">Record Status:</span>{' '}
                <span className="font-semibold text-indigo-600">{prog.training_record_status}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Supervision assignment */}
        <div className="pg-card space-y-3">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-1.5">Supervisors Assigned</h2>
          {prog.primary_supervisor ? (
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-slate-500 font-medium">Primary Supervisor:</span>{' '}
                <span className="font-semibold text-slate-800">{prog.primary_supervisor.name}</span>{' '}
                <span className="text-slate-500">({prog.primary_supervisor.email || 'No email'})</span>
              </div>
              {prog.co_supervisors && prog.co_supervisors.length > 0 && (
                <div>
                  <span className="text-slate-500 font-medium">Co-Supervisors:</span>{' '}
                  <span className="font-semibold text-slate-700">
                    {prog.co_supervisors.map((c) => c.name).join(', ')}
                  </span>
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-yellow-600 font-medium">No primary supervisor linked to this resident.</p>
          )}
        </div>

        {/* Workflows aggregate totals */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Evaluations */}
          <div className="pg-card space-y-3">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-1.5">Evaluations summary</h2>
            <div className="space-y-1.5 text-sm text-slate-700">
              <div className="flex justify-between">
                <span>Approved evaluations:</span>
                <span className="font-semibold text-green-600">{prog.evaluations_approved || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Pending evaluations:</span>
                <span className="font-semibold text-amber-600">{prog.evaluations_pending || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Total logged:</span>
                <span className="font-semibold text-slate-800">{prog.evaluations_total || 0}</span>
              </div>
            </div>
          </div>

          {/* Logbooks */}
          <div className="pg-card space-y-3">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-1.5">Logbook procedures summary</h2>
            <div className="space-y-1.5 text-sm text-slate-700">
              <div className="flex justify-between">
                <span>Verified procedures:</span>
                <span className="font-semibold text-green-600">{prog.logbooks_verified || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Pending verification:</span>
                <span className="font-semibold text-amber-600">{prog.logbooks_pending || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Total cases logged:</span>
                <span className="font-semibold text-slate-800">{prog.logbooks_total || 0}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Logbooks Categories milestones */}
        <div className="pg-card space-y-4">
          <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Logbook Procedures & Milestones</h2>
          <div className="space-y-4">
            {prog.logbooks_summary?.map((cat) => {
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
            {(!prog.logbooks_summary || prog.logbooks_summary.length === 0) && (
              <p className="text-sm text-slate-500">No logbook entries or categories registered.</p>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
