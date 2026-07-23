'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, EvaluationSubmission } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function EvaluationsPage() {
  const { user } = useAuthStore();
  const [submissions, setSubmissions] = useState<EvaluationSubmission[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .listEvaluationSubmissions()
      .then(setSubmissions)
      .catch(() => setSubmissions([]))
      .finally(() => setLoading(false));
  }, []);

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';
  const isAdmin = user?.role === 'ADMIN';

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Evaluations & Supervisor Reviews"
            description="Manage rotation evaluations, case-based discussions, and periodic supervisor reviews."
          />
          {isResident && (
            <Link href="/academics/evaluations/new" className="pg-btn-primary">
              New Evaluation
            </Link>
          )}
        </div>

        {loading ? (
          <div className="text-center py-6 text-sm text-slate-500">Loading evaluations...</div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">ID</th>
                  {!isResident && <th className="px-4 py-3 text-left">Resident</th>}
                  <th className="px-4 py-3 text-left">Template</th>
                  {!isSupervisor && <th className="px-4 py-3 text-left">Supervisor</th>}
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Score</th>
                  <th className="px-4 py-3 text-left">Date</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {submissions.map((sub) => (
                  <tr key={sub.id}>
                    <td className="px-4 py-3 font-medium text-slate-900">#{sub.id}</td>
                    {!isResident && <td className="px-4 py-3">{sub.resident_name}</td>}
                    <td className="px-4 py-3">{sub.template_name}</td>
                    {!isSupervisor && <td className="px-4 py-3">{sub.supervisor_name || '—'}</td>}
                    <td className="px-4 py-3">
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
                    </td>
                    <td className="px-4 py-3">
                      {sub.score !== null ? `${sub.score}/${sub.max_score}` : '—'}
                    </td>
                    <td className="px-4 py-3">
                      {sub.submitted_at ? new Date(sub.submitted_at).toLocaleDateString() : '—'}
                    </td>
                    <td className="px-4 py-3 space-x-2">
                      <Link
                        href={`/academics/evaluations/${sub.id}`}
                        className="text-sm font-medium text-indigo-600 hover:underline"
                      >
                        Open
                      </Link>
                      {(isSupervisor || isAdmin) &&
                        (sub.status === 'SUBMITTED' || sub.status === 'UNDER_REVIEW') && (
                          <Link
                            href={`/academics/evaluations/${sub.id}/review`}
                            className="text-sm font-medium text-green-600 hover:underline"
                          >
                            Review
                          </Link>
                        )}
                    </td>
                  </tr>
                ))}
                {submissions.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={8}>
                      No evaluations found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
