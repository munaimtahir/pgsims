'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';

export default function UTRMCUsersPage() {
  const [items, setItems] = useState<UserbaseUser[]>([]);
  const [role, setRole] = useState('');
  const [search, setSearch] = useState('');
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setError(null);
      const list = await userbaseApi.users.list({
        role: role || undefined,
        search: search || undefined,
      });
      setItems(list);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load users');
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ProtectedRoute allowedRoles={['utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">UTRMC Users</h1>
            <Link href="/dashboard/utrmc/users/new" className="rounded bg-indigo-600 px-3 py-2 text-white">
              Create User
            </Link>
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
            <select className="rounded border p-2" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="">All roles</option>
              <option value="admin">admin</option>
              <option value="utrmc_admin">utrmc_admin</option>
              <option value="utrmc_user">utrmc_user</option>
              <option value="supervisor">supervisor</option>
              <option value="faculty">faculty</option>
              <option value="resident">resident</option>
              <option value="pg">pg</option>
            </select>
            <input className="rounded border p-2" placeholder="Search users" value={search} onChange={(e) => setSearch(e.target.value)} />
            <button className="rounded bg-gray-800 px-3 py-2 text-white" onClick={load}>
              Apply Filters
            </button>
          </div>
          <div className="rounded border bg-white p-3 text-sm">
            <p className="font-medium">Quick actions</p>
            <div className="mt-2 space-x-4">
              <Link className="text-indigo-600" href="/dashboard/utrmc/linking/supervision">
                Link Supervisor ↔ Resident
              </Link>
              <Link className="text-indigo-600" href="/dashboard/utrmc/linking/hod">
                Assign HOD
              </Link>
            </div>
          </div>
          <table className="min-w-full border bg-white text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1 text-left">Name</th>
                <th className="border px-2 py-1 text-left">Username</th>
                <th className="border px-2 py-1 text-left">Role</th>
                <th className="border px-2 py-1 text-left">Active</th>
                <th className="border px-2 py-1 text-left">Open</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="border px-2 py-1">{item.full_name || `${item.first_name} ${item.last_name}`}</td>
                  <td className="border px-2 py-1">{item.username}</td>
                  <td className="border px-2 py-1">{item.role}</td>
                  <td className="border px-2 py-1">{item.is_active ? 'Yes' : 'No'}</td>
                  <td className="border px-2 py-1">
                    <Link className="text-indigo-600" href={`/dashboard/utrmc/users/${item.id}`}>
                      Details
                    </Link>
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
