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

type ActiveFilter = 'all' | 'active' | 'inactive';

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
  const [searchInput, setSearchInput] = useState('');
  const [search, setSearch] = useState('');
  const [activeFilter, setActiveFilter] = useState<ActiveFilter>('all');

  // Debounce the search box so it doesn't fire a request on every keystroke.
  useEffect(() => {
    const timer = setTimeout(() => setSearch(searchInput.trim()), 300);
    return () => clearTimeout(timer);
  }, [searchInput]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    const params: { role?: string; search?: string; active?: boolean } = role ? { role } : {};
    if (search) {
      params.search = search;
    }
    if (activeFilter !== 'all') {
      params.active = activeFilter === 'active';
    }
    userbaseApi.users
      .list(params)
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
  }, [role, search, activeFilter]);

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

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <input
            type="search"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search by name, username, or email..."
            aria-label="Search directory"
            className="w-full max-w-sm rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <select
            value={activeFilter}
            onChange={(e) => setActiveFilter(e.target.value as ActiveFilter)}
            aria-label="Filter by status"
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="all">All statuses</option>
            <option value="active">Active only</option>
            <option value="inactive">Inactive only</option>
          </select>
          {(search || activeFilter !== 'all') && (
            <span className="text-xs text-slate-500">
              {loading ? 'Searching…' : `${rows.length} result${rows.length === 1 ? '' : 's'}`}
            </span>
          )}
        </div>

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
