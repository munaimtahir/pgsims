'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import { leaveApi, LeaveRequest } from '@/lib/api/leave';
import { useAuthStore } from '@/store/authStore';

export default function LeaveRequestsPage() {
  const { user } = useAuthStore();
  const [leaves, setLeaves] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';

  useEffect(() => {
    leaveApi
      .list()
      .then(setLeaves)
      .catch(() => setLeaves([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Leave Requests"
            description="Resident leave applications, with supervisor/admin approval."
          />
          {isResident && (
            <Link href="/academics/leave-requests/new" className="pg-btn-primary">
              New Leave Request
            </Link>
          )}
        </div>

        {loading ? (
          <div className="text-center py-6 text-sm text-slate-500">Loading leave requests...</div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">ID</th>
                  {!isResident && <th className="px-4 py-3 text-left">Resident</th>}
                  <th className="px-4 py-3 text-left">Type</th>
                  <th className="px-4 py-3 text-left">Start</th>
                  <th className="px-4 py-3 text-left">End</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {leaves.map((l) => (
                  <tr key={l.id}>
                    <td className="px-4 py-3 font-medium text-slate-900">#{l.id}</td>
                    {!isResident && <td className="px-4 py-3">{l.resident_name}</td>}
                    <td className="px-4 py-3 capitalize">{l.leave_type}</td>
                    <td className="px-4 py-3">{new Date(l.start_date).toLocaleDateString()}</td>
                    <td className="px-4 py-3">{new Date(l.end_date).toLocaleDateString()}</td>
                    <td className="px-4 py-3">
                      <WorkflowStatusBadge status={l.status} />
                    </td>
                    <td className="px-4 py-3">
                      <Link
                        href={`/academics/leave-requests/${l.id}`}
                        className="text-sm font-medium text-indigo-600 hover:underline"
                      >
                        Open
                      </Link>
                    </td>
                  </tr>
                ))}
                {leaves.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={isResident ? 6 : 7}>
                      No leave requests found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
        {isSupervisor && (
          <p className="text-xs text-slate-500">
            Leave requests awaiting your review appear above with status &quot;SUBMITTED&quot; — open one to approve or reject it.
          </p>
        )}
      </div>
    </ProtectedRoute>
  );
}
