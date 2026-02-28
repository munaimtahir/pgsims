'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi, UserbaseDepartment, UserbaseHospitalDepartment, UserbaseUser } from '@/lib/api/userbase';

interface PageProps {
  params: { id: string };
}

export default function UTRMCUserDetailPage({ params }: PageProps) {
  const userId = Number(params.id);
  const [user, setUser] = useState<UserbaseUser | null>(null);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [matrix, setMatrix] = useState<UserbaseHospitalDepartment[]>([]);
  const [role, setRole] = useState('resident');
  const [active, setActive] = useState(true);
  const [departmentId, setDepartmentId] = useState<number | null>(null);
  const [memberType, setMemberType] = useState('resident');
  const [hospitalDepartmentId, setHospitalDepartmentId] = useState<number | null>(null);
  const [assignmentType, setAssignmentType] = useState('primary_training');
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const [u, d, m] = await Promise.all([
        userbaseApi.users.get(userId),
        userbaseApi.departments.list(),
        userbaseApi.matrix.list(),
      ]);
      setUser(u);
      setRole(u.role);
      setActive(u.is_active);
      setDepartments(d);
      setMatrix(m);
      if (!departmentId && d[0]) setDepartmentId(d[0].id);
      if (!hospitalDepartmentId && m[0]) setHospitalDepartmentId(m[0].id);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Load failed');
    }
  };

  useEffect(() => {
    load();
  }, [params.id]);

  const updateUser = async () => {
    try {
      await userbaseApi.users.update(userId, { role, is_active: active });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Update failed');
    }
  };

  const assignDepartment = async () => {
    if (!departmentId) return;
    try {
      await userbaseApi.memberships.create({
        user_id: userId,
        department_id: departmentId,
        member_type: memberType,
        is_primary: true,
        start_date: new Date().toISOString().slice(0, 10),
        active: true,
      });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Department assignment failed');
    }
  };

  const assignHospital = async () => {
    if (!hospitalDepartmentId) return;
    try {
      await userbaseApi.hospitalAssignments.create({
        user_id: userId,
        hospital_department_id: hospitalDepartmentId,
        assignment_type: assignmentType,
        start_date: new Date().toISOString().slice(0, 10),
        active: true,
      });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Hospital assignment failed');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">User Detail</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          {user && (
            <div className="rounded border bg-white p-3 text-sm">
              <p>
                <span className="font-medium">Name:</span> {user.full_name || `${user.first_name} ${user.last_name}`}
              </p>
              <p>
                <span className="font-medium">Username:</span> {user.username}
              </p>
              <p>
                <span className="font-medium">Email:</span> {user.email}
              </p>
            </div>
          )}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            <select className="rounded border p-2" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="resident">resident</option>
              <option value="faculty">faculty</option>
              <option value="supervisor">supervisor</option>
              <option value="utrmc_user">utrmc_user</option>
              <option value="utrmc_admin">utrmc_admin</option>
              <option value="admin">admin</option>
            </select>
            <select className="rounded border p-2" value={active ? 'true' : 'false'} onChange={(e) => setActive(e.target.value === 'true')}>
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </select>
            <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={updateUser}>
              Save User
            </button>
          </div>
          <div className="rounded border bg-white p-3">
            <h2 className="mb-2 font-semibold">Quick Action: Assign Department</h2>
            <div className="grid grid-cols-1 gap-2 md:grid-cols-4">
              <select className="rounded border p-2" value={departmentId ?? ''} onChange={(e) => setDepartmentId(Number(e.target.value))}>
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </select>
              <select className="rounded border p-2" value={memberType} onChange={(e) => setMemberType(e.target.value)}>
                <option value="resident">resident</option>
                <option value="supervisor">supervisor</option>
                <option value="faculty">faculty</option>
              </select>
              <button className="rounded bg-gray-800 px-3 py-2 text-white" onClick={assignDepartment}>
                Assign Department
              </button>
            </div>
          </div>
          <div className="rounded border bg-white p-3">
            <h2 className="mb-2 font-semibold">Quick Action: Assign Hospital-Department</h2>
            <div className="grid grid-cols-1 gap-2 md:grid-cols-4">
              <select className="rounded border p-2" value={hospitalDepartmentId ?? ''} onChange={(e) => setHospitalDepartmentId(Number(e.target.value))}>
                {matrix.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.hospital?.name} / {m.department?.name}
                  </option>
                ))}
              </select>
              <select className="rounded border p-2" value={assignmentType} onChange={(e) => setAssignmentType(e.target.value)}>
                <option value="primary_training">primary_training</option>
                <option value="posting">posting</option>
                <option value="faculty_site">faculty_site</option>
              </select>
              <button className="rounded bg-gray-800 px-3 py-2 text-white" onClick={assignHospital}>
                Assign Site
              </button>
            </div>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
