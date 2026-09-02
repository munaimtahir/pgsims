'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, LogbookEntry } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function LogbookPage() {
  const { user } = useAuthStore();
  const [entries, setEntries] = useState<LogbookEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .listLogbookEntries()
      .then(setEntries)
      .catch(() => setEntries([]))
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
            title="Logbooks & Procedure Records"
            description="Log and verify clinical procedures, case submissions, and academic milestones."
          />
          {isResident && (
            <Link href="/academics/logbook/new" className="pg-btn-primary">
              Log Procedure
            </Link>
          )}
        </div>

        {loading ? (
          <div className="text-center py-6 text-sm text-slate-500">Loading logbook entries...</div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">ID</th>
                  {!isResident && <th className="px-4 py-3 text-left">Resident</th>}
                  <th className="px-4 py-3 text-left">Date</th>
                  <th className="px-4 py-3 text-left">Title/Case</th>
                  <th className="px-4 py-3 text-left">Category</th>
                  <th className="px-4 py-3 text-left">Complexity</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {entries.map((entry) => (
                  <tr key={entry.id}>
                    <td className="px-4 py-3 font-medium text-slate-900">#{entry.id}</td>
                    {!isResident && <td className="px-4 py-3">{entry.resident_name}</td>}
                    <td className="px-4 py-3">
                      {entry.entry_date ? new Date(entry.entry_date).toLocaleDateString() : '—'}
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-medium text-slate-900">{entry.title}</div>
                      {entry.case_identifier && (
                        <div className="text-xs text-slate-500">Case ID: {entry.case_identifier}</div>
                      )}
                    </td>
                    <td className="px-4 py-3">{entry.category_name}</td>
                    <td className="px-4 py-3">
                      {entry.procedure_record?.complexity ? (
                        <span className="inline-flex items-center rounded bg-slate-100 px-1.5 py-0.5 text-xs font-medium text-slate-800">
                          {entry.procedure_record.complexity}
                        </span>
                      ) : (
                        '—'
                      )}
                    </td>
                    <td className="px-4 py-3">
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
                    </td>
                    <td className="px-4 py-3 space-x-2">
                      <Link
                        href={`/academics/logbook/${entry.id}`}
                        className="text-sm font-medium text-indigo-600 hover:underline"
                      >
                        Open
                      </Link>
                      {(isSupervisor || isAdmin) && entry.status === 'SUBMITTED' && (
                        <Link
                          href={`/academics/logbook/${entry.id}/review`}
                          className="text-sm font-medium text-green-600 hover:underline"
                        >
                          Verify
                        </Link>
                      )}
                    </td>
                  </tr>
                ))}
                {entries.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={8}>
                      No logbook entries found.
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
