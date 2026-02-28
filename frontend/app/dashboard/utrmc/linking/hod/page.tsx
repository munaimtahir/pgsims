'use client';

import { useEffect, useMemo, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi, UserbaseDepartment, UserbaseUser } from '@/lib/api/userbase';

interface HODAssignmentRow {
  id: number;
  department?: { name?: string };
  hod_user?: { full_name?: string; username?: string };
  active?: boolean;
}

export default function HODLinkingPage() {
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [users, setUsers] = useState<UserbaseUser[]>([]);
  const [assignments, setAssignments] = useState<HODAssignmentRow[]>([]);
  const [departmentId, setDepartmentId] = useState<number | null>(null);
  const [hodUserId, setHodUserId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const [d, u, a] = await Promise.all([
        userbaseApi.departments.list(),
        userbaseApi.users.list({ active: true }),
        userbaseApi.hodAssignments.list(),
      ]);
      setDepartments(d);
      setUsers(u);
      setAssignments(Array.isArray(a) ? a : a.results || []);
      if (!departmentId && d[0]) setDepartmentId(d[0].id);
      if (!hodUserId) setHodUserId(u.find((item) => ['faculty', 'supervisor'].includes(item.role))?.id ?? null);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load data');
    }
  };

  useEffect(() => {
    load();
  }, []);

  const candidates = useMemo(() => users.filter((u) => ['faculty', 'supervisor'].includes(u.role)), [users]);

  const assign = async () => {
    if (!departmentId || !hodUserId) return;
    try {
      await userbaseApi.hodAssignments.create({
        department_id: departmentId,
        hod_user_id: hodUserId,
        start_date: new Date().toISOString().slice(0, 10),
        active: true,
      });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Assign HOD failed');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">HOD Assignment</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            <select className="rounded border p-2" value={departmentId ?? ''} onChange={(e) => setDepartmentId(Number(e.target.value))}>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
            <select className="rounded border p-2" value={hodUserId ?? ''} onChange={(e) => setHodUserId(Number(e.target.value))}>
              {candidates.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.full_name || u.username}
                </option>
              ))}
            </select>
            <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={assign}>
              Assign HOD
            </button>
          </div>
          <table className="min-w-full border bg-white text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1 text-left">Department</th>
                <th className="border px-2 py-1 text-left">HOD</th>
                <th className="border px-2 py-1 text-left">Active</th>
              </tr>
            </thead>
            <tbody>
              {assignments.map((item) => (
                <tr key={item.id}>
                  <td className="border px-2 py-1">{item.department?.name}</td>
                  <td className="border px-2 py-1">{item.hod_user?.full_name || item.hod_user?.username}</td>
                  <td className="border px-2 py-1">{item.active ? 'Yes' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
