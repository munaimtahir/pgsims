'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { DepartmentRosterResponse, userbaseApi } from '@/lib/api/userbase';

interface PageProps {
  params: { id: string };
}

export default function PGDepartmentRosterPage({ params }: PageProps) {
  const [roster, setRoster] = useState<DepartmentRosterResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setRoster(await userbaseApi.departments.roster(Number(params.id)));
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Failed to load roster');
      }
    };
    load();
  }, [params.id]);

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <DashboardLayout>
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">Department Roster</h1>
          {error && <p className="text-sm text-red-600">{error}</p>}
          {roster && (
            <div className="rounded border bg-white p-3 text-sm">
              <p>
                <span className="font-semibold">Department:</span> {roster.department.name}
              </p>
              <p>
                <span className="font-semibold">HOD:</span>{' '}
                {roster.hod ? roster.hod.full_name || roster.hod.username : 'Not assigned'}
              </p>
              <p className="mt-2">
                <span className="font-semibold">Residents:</span> {roster.residents.length}
              </p>
            </div>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
