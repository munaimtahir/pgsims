'use client';

import { useEffect, useMemo, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi, UserbaseDepartment, UserbaseUser } from '@/lib/api/userbase';

interface SupervisionLinkRow {
  id: number;
  supervisor_user?: { full_name?: string; username?: string };
  resident_user?: { full_name?: string; username?: string };
  department?: { name?: string };
  active?: boolean;
}

export default function SupervisionLinkingPage() {
  const [users, setUsers] = useState<UserbaseUser[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [links, setLinks] = useState<SupervisionLinkRow[]>([]);
  const [supervisorId, setSupervisorId] = useState<number | null>(null);
  const [residentId, setResidentId] = useState<number | null>(null);
  const [departmentId, setDepartmentId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const [u, d, l] = await Promise.all([
        userbaseApi.users.list({ active: true }),
        userbaseApi.departments.list(),
        userbaseApi.supervisionLinks.list(),
      ]);
      setUsers(u);
      setDepartments(d);
      setLinks(Array.isArray(l) ? l : l.results || []);
      if (!supervisorId) setSupervisorId(u.find((item) => ['supervisor', 'faculty'].includes(item.role))?.id ?? null);
      if (!residentId) setResidentId(u.find((item) => ['resident', 'pg'].includes(item.role))?.id ?? null);
      if (!departmentId && d[0]) setDepartmentId(d[0].id);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load data');
    }
  };

  useEffect(() => {
    load();
  }, []);

  const supervisors = useMemo(() => users.filter((u) => ['supervisor', 'faculty'].includes(u.role)), [users]);
  const residents = useMemo(() => users.filter((u) => ['resident', 'pg'].includes(u.role)), [users]);

  const createLink = async () => {
    if (!supervisorId || !residentId) return;
    try {
      await userbaseApi.supervisionLinks.create({
        supervisor_user_id: supervisorId,
        resident_user_id: residentId,
        department_id: departmentId,
        start_date: new Date().toISOString().slice(0, 10),
        active: true,
      });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Create link failed');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">Supervisor ↔ Resident Linking</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-4">
            <select className="rounded border p-2" value={supervisorId ?? ''} onChange={(e) => setSupervisorId(Number(e.target.value))}>
              {supervisors.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.full_name || u.username} ({u.role})
                </option>
              ))}
            </select>
            <select className="rounded border p-2" value={residentId ?? ''} onChange={(e) => setResidentId(Number(e.target.value))}>
              {residents.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.full_name || u.username} ({u.role})
                </option>
              ))}
            </select>
            <select className="rounded border p-2" value={departmentId ?? ''} onChange={(e) => setDepartmentId(Number(e.target.value))}>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
            <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={createLink}>
              Create Link
            </button>
          </div>
          <table className="min-w-full border bg-white text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1 text-left">Supervisor</th>
                <th className="border px-2 py-1 text-left">Resident</th>
                <th className="border px-2 py-1 text-left">Department</th>
                <th className="border px-2 py-1 text-left">Active</th>
              </tr>
            </thead>
            <tbody>
              {links.map((link) => (
                <tr key={link.id}>
                  <td className="border px-2 py-1">{link.supervisor_user?.full_name || link.supervisor_user?.username}</td>
                  <td className="border px-2 py-1">{link.resident_user?.full_name || link.resident_user?.username}</td>
                  <td className="border px-2 py-1">{link.department?.name || '-'}</td>
                  <td className="border px-2 py-1">{link.active ? 'Yes' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
