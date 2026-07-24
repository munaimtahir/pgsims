'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import { rotationsApi, RotationAssignment } from '@/lib/api/rotations';
import { useAuthStore } from '@/store/authStore';

export default function RotationAssignmentsPage() {
  const { user } = useAuthStore();
  const [rotations, setRotations] = useState<RotationAssignment[]>([]);
  const [loading, setLoading] = useState(true);

  const isResident = user?.role === 'RESIDENT';
  const isSupervisor = user?.role === 'SUPERVISOR';
  const isAdmin = user?.role === 'ADMIN';

  useEffect(() => {
    rotationsApi
      .list()
      .then(setRotations)
      .catch(() => setRotations([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'RESIDENT', 'SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <div className="flex items-center justify-between">
          <PageHeader
            title="Rotation Assignments"
            description="Placements into a hospital/department rotation, with HOD and UTRMC approval."
          />
          {isAdmin && (
            <Link href="/academics/rotation-assignments/new" className="pg-btn-primary">
              New Assignment
            </Link>
          )}
        </div>

        {loading ? (
          <div className="text-center py-6 text-sm text-slate-500">Loading rotation assignments...</div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
                <tr>
                  <th className="px-4 py-3 text-left">ID</th>
                  {!isResident && <th className="px-4 py-3 text-left">Resident</th>}
                  <th className="px-4 py-3 text-left">Hospital / Department</th>
                  <th className="px-4 py-3 text-left">Start</th>
                  <th className="px-4 py-3 text-left">End</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {rotations.map((r) => (
                  <tr key={r.id}>
                    <td className="px-4 py-3 font-medium text-slate-900">#{r.id}</td>
                    {!isResident && <td className="px-4 py-3">{r.resident_name}</td>}
                    <td className="px-4 py-3">
                      <div className="font-medium text-slate-900">{r.hospital_name}</div>
                      <div className="text-xs text-slate-500">{r.department_name}</div>
                    </td>
                    <td className="px-4 py-3">{new Date(r.start_date).toLocaleDateString()}</td>
                    <td className="px-4 py-3">{new Date(r.end_date).toLocaleDateString()}</td>
                    <td className="px-4 py-3">
                      <WorkflowStatusBadge status={r.status} />
                    </td>
                    <td className="px-4 py-3">
                      <Link
                        href={`/academics/rotation-assignments/${r.id}`}
                        className="text-sm font-medium text-indigo-600 hover:underline"
                      >
                        Open
                      </Link>
                    </td>
                  </tr>
                ))}
                {rotations.length === 0 && (
                  <tr>
                    <td className="px-4 py-6 text-sm text-slate-500 text-center" colSpan={isResident ? 6 : 7}>
                      No rotation assignments found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
        {isSupervisor && (
          <p className="text-xs text-slate-500">
            Rotations awaiting your review appear above with status &quot;SUBMITTED&quot; — open one to approve or reject it.
          </p>
        )}
      </div>
    </ProtectedRoute>
  );
}
