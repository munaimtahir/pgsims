'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi } from '@/lib/api/userbase';

export default function UTRMCUserCreatePage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: 'resident',
    specialty: '',
    year: '1',
    training_start: '',
    training_level: '',
    designation: '',
    phone: '',
  });
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async () => {
    try {
      setError(null);
      const payload: Record<string, unknown> = {
        username: form.username,
        email: form.email,
        password: form.password,
        first_name: form.first_name,
        last_name: form.last_name,
        role: form.role,
        specialty: form.specialty || null,
        year: form.year || null,
      };
      if (form.role === 'resident' || form.role === 'pg') {
        payload.resident_profile = {
          training_start: form.training_start,
          training_level: form.training_level,
        };
      }
      if (form.role === 'supervisor' || form.role === 'faculty') {
        payload.staff_profile = {
          designation: form.designation,
          phone: form.phone,
        };
      }
      const created = await userbaseApi.users.create(payload);
      router.push(`/dashboard/utrmc/users/${created.id}`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Create failed');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">Create User</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
            <input className="rounded border p-2" placeholder="Username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
            <input className="rounded border p-2" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            <input className="rounded border p-2" placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
            <input className="rounded border p-2" placeholder="First name" value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} />
            <input className="rounded border p-2" placeholder="Last name" value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
            <select className="rounded border p-2" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
              <option value="resident">resident</option>
              <option value="faculty">faculty</option>
              <option value="supervisor">supervisor</option>
              <option value="utrmc_user">utrmc_user</option>
              <option value="utrmc_admin">utrmc_admin</option>
              <option value="admin">admin</option>
            </select>
            <input className="rounded border p-2" placeholder="Specialty" value={form.specialty} onChange={(e) => setForm({ ...form, specialty: e.target.value })} />
            <input className="rounded border p-2" placeholder="Year/Level" value={form.year} onChange={(e) => setForm({ ...form, year: e.target.value })} />
            <input className="rounded border p-2" placeholder="Training start (YYYY-MM-DD)" value={form.training_start} onChange={(e) => setForm({ ...form, training_start: e.target.value })} />
            <input className="rounded border p-2" placeholder="Training level text" value={form.training_level} onChange={(e) => setForm({ ...form, training_level: e.target.value })} />
            <input className="rounded border p-2" placeholder="Designation" value={form.designation} onChange={(e) => setForm({ ...form, designation: e.target.value })} />
            <input className="rounded border p-2" placeholder="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          </div>
          <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={onSubmit}>
            Create User
          </button>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
