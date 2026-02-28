'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { DepartmentRosterResponse, userbaseApi } from '@/lib/api/userbase';

interface PageProps {
  params: { id: string };
}

export default function DepartmentRosterPage({ params }: PageProps) {
  const departmentId = Number(params.id);
  const [roster, setRoster] = useState<DepartmentRosterResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setRoster(await userbaseApi.departments.roster(departmentId));
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Failed to load roster');
      }
    };
    load();
  }, [params.id]);

  return (
    <ProtectedRoute allowedRoles={['utrmc_user', 'utrmc_admin', 'admin']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">Department Roster</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          {roster && (
            <>
              <div className="rounded border bg-white p-3 text-sm">
                <p>
                  <span className="font-semibold">Department:</span> {roster.department.name} ({roster.department.code})
                </p>
                <p>
                  <span className="font-semibold">HOD:</span>{' '}
                  {roster.hod ? roster.hod.full_name || roster.hod.username : 'Not assigned'}
                </p>
              </div>
              <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
                <RosterCard title="Faculty" rows={roster.faculty} />
                <RosterCard title="Supervisors" rows={roster.supervisors} />
                <RosterCard title="Residents" rows={roster.residents} />
              </div>
            </>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}

function RosterCard({ title, rows }: { title: string; rows: Array<{ id: number; username: string; full_name?: string }> }) {
  return (
    <div className="rounded border bg-white p-3">
      <h2 className="mb-2 font-semibold">{title}</h2>
      <ul className="space-y-1 text-sm">
        {rows.length === 0 && <li className="text-gray-500">No records</li>}
        {rows.map((row) => (
          <li key={row.id}>{row.full_name || row.username}</li>
        ))}
      </ul>
    </div>
  );
}
