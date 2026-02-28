'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi, UserbaseHospital } from '@/lib/api/userbase';

export default function UTRMCHospitalsPage() {
  const [items, setItems] = useState<UserbaseHospital[]>([]);
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setItems(await userbaseApi.hospitals.list());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load hospitals');
    }
  };

  useEffect(() => {
    load();
  }, []);

  const createHospital = async () => {
    try {
      setError(null);
      await userbaseApi.hospitals.create({ name, code, active: true });
      setName('');
      setCode('');
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Create failed');
    }
  };

  const toggle = async (item: UserbaseHospital) => {
    try {
      await userbaseApi.hospitals.update(item.id, { active: !item.active });
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Update failed');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">UTRMC Hospitals</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            <input className="rounded border p-2" placeholder="Hospital name" value={name} onChange={(e) => setName(e.target.value)} />
            <input className="rounded border p-2" placeholder="Code" value={code} onChange={(e) => setCode(e.target.value)} />
            <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={createHospital}>Create</button>
          </div>
          <table className="min-w-full border bg-white text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1 text-left">Name</th>
                <th className="border px-2 py-1 text-left">Code</th>
                <th className="border px-2 py-1 text-left">Active</th>
                <th className="border px-2 py-1 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="border px-2 py-1">{item.name}</td>
                  <td className="border px-2 py-1">{item.code}</td>
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
