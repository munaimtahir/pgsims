'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';

interface RoleDirectoryPageProps {
  title: string;
  description: string;
  role?: 'ADMIN' | 'RESIDENT' | 'SUPERVISOR' | 'SUPPORT_STAFF';
  detailBasePath?: string;
  createHref?: string;
}

export default function RoleDirectoryPage({
  title,
  description,
  role,
  detailBasePath,
  createHref,
}: RoleDirectoryPageProps) {
  const [rows, setRows] = useState<UserbaseUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    setLoading(true);
    userbaseApi.users
      .list(role ? { role } : undefined)
      .then((data) => {
        if (active) {
          setRows(data);
        }
      })
      .catch(() => {
        if (active) {
          setError('Failed to load directory.');
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [role]);

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title={title}
          description={description}
          actions={
            createHref ? (
              <Link href={createHref} className="pg-btn-primary">
                New User
              </Link>
            ) : undefined
          }
        />

        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Username</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td className="px-4 py-6 text-slate-500" colSpan={4}>
                    Loading directory...
                  </td>
                </tr>
              ) : rows.length === 0 ? (
                <tr>
                  <td className="px-4 py-6 text-slate-500" colSpan={4}>
                    No records found.
                  </td>
                </tr>
              ) : (
                rows.map((row) => {
                  const label = row.full_name || `${row.first_name} ${row.last_name}`.trim() || row.username;
                  const content = detailBasePath ? (
                    <Link href={`${detailBasePath}/${row.id}`} className="font-medium text-indigo-600 hover:underline">
                      {label}
                    </Link>
                  ) : (
                    <span className="font-medium text-slate-900">{label}</span>
                  );
                  return (
                    <tr key={row.id}>
                      <td className="px-4 py-3">{content}</td>
                      <td className="px-4 py-3 text-slate-600">{row.username}</td>
                      <td className="px-4 py-3 text-slate-600">{row.role}</td>
                      <td className="px-4 py-3 text-slate-600">{row.is_active ? 'Active' : 'Inactive'}</td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </ProtectedRoute>
  );
}
