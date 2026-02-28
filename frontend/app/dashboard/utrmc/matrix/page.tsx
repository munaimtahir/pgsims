'use client';

import { useEffect, useMemo, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi, UserbaseDepartment, UserbaseHospital, UserbaseHospitalDepartment } from '@/lib/api/userbase';

export default function UTRMCMatrixPage() {
  const [matrix, setMatrix] = useState<UserbaseHospitalDepartment[]>([]);
  const [hospitals, setHospitals] = useState<UserbaseHospital[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [hospitalId, setHospitalId] = useState<number | null>(null);
  const [departmentId, setDepartmentId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const [m, h, d] = await Promise.all([
        userbaseApi.matrix.list(),
        userbaseApi.hospitals.list(),
        userbaseApi.departments.list(),
      ]);
      setMatrix(m);
      setHospitals(h);
      setDepartments(d);
      if (!hospitalId && h[0]) setHospitalId(h[0].id);
      if (!departmentId && d[0]) setDepartmentId(d[0].id);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load matrix');
    }
  };

  useEffect(() => {
    load();
  }, []);

  const createMatrix = async () => {
    if (!hospitalId || !departmentId) return;
    try {
      setError(null);
      await userbaseApi.matrix.create({ hospital_id: hospitalId, department_id: departmentId, active: true });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Create failed');
    }
  };

  const toggle = async (item: UserbaseHospitalDepartment) => {
    try {
      await userbaseApi.matrix.update(item.id, { active: !item.active });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Update failed');
    }
  };

  const options = useMemo(() => ({ hospitals, departments }), [hospitals, departments]);

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">Hospital-Department Matrix</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            <select className="rounded border p-2" value={hospitalId ?? ''} onChange={(e) => setHospitalId(Number(e.target.value))}>
              {options.hospitals.map((h) => (
                <option key={h.id} value={h.id}>
                  {h.name}
                </option>
              ))}
            </select>
            <select className="rounded border p-2" value={departmentId ?? ''} onChange={(e) => setDepartmentId(Number(e.target.value))}>
              {options.departments.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
            <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={createMatrix}>
              Add Mapping
            </button>
          </div>
          <table className="min-w-full border bg-white text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1 text-left">Hospital</th>
                <th className="border px-2 py-1 text-left">Department</th>
                <th className="border px-2 py-1 text-left">Active</th>
                <th className="border px-2 py-1 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {matrix.map((item) => (
                <tr key={item.id}>
                  <td className="border px-2 py-1">{item.hospital?.name}</td>
                  <td className="border px-2 py-1">{item.department?.name}</td>
                  <td className="border px-2 py-1">{item.active ? 'Yes' : 'No'}</td>
                  <td className="border px-2 py-1">
                    <button className="text-indigo-600" onClick={() => toggle(item)}>
                      {item.active ? 'Deactivate' : 'Activate'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
