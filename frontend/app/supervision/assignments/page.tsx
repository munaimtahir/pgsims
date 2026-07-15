'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import supervisionApi, { SupervisionAssignment } from '@/lib/api/supervision';

export default function SupervisionAssignmentsPage() {
  const [assignments, setAssignments] = useState<SupervisionAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    supervisionApi.listAssignments()
      .then(setAssignments)
      .catch(() => setError('Unable to load assignments.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page">
        <PageHeader
          title="Assignments"
          description="All active and historical supervision assignments."
          actions={(
            <div className="flex flex-wrap gap-2">
              <Link href="/supervision" className="pg-btn-primary">Overview</Link>
              <Link href="/supervision/assignments/new" className="pg-btn-primary">New Assignment</Link>
            </div>
          )}
        />
        {loading && <p className="text-sm text-slate-500">Loading assignments...</p>}
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        {!loading && (
          <div className="bg-white border border-slate-200 rounded-xl overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600 text-xs uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3 text-left">Resident</th>
                  <th className="px-4 py-3 text-left">Supervisor</th>
                  <th className="px-4 py-3 text-left">Type</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Start</th>
                  <th className="px-4 py-3 text-left">Detail</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {assignments.map((assignment) => (
                  <tr key={assignment.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3 font-medium text-slate-900">{assignment.resident?.name}</td>
                    <td className="px-4 py-3 text-slate-700">{assignment.supervisor?.name}</td>
                    <td className="px-4 py-3 text-slate-600">{assignment.assignment_type}</td>
                    <td className="px-4 py-3 text-slate-600">{assignment.status}</td>
                    <td className="px-4 py-3 text-slate-600">{assignment.start_date || '—'}</td>
                    <td className="px-4 py-3">
                      <Link href={`/supervision/assignments/${assignment.id}`} className="text-indigo-600 font-semibold hover:underline">
                        Open
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
