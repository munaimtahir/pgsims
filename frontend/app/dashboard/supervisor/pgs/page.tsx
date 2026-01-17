'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';
import ErrorBanner from '@/components/ui/ErrorBanner';
import DataTable, { Column } from '@/components/ui/DataTable';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import { AssignedPG, usersApi } from '@/lib/api';

const formatValue = (
  value?: string | number | { name?: string; label?: string; value?: string | number },
) => {
  if (typeof value === 'string' || typeof value === 'number') {
    return String(value);
  }
  if (value && typeof value === 'object') {
    return value.label || value.name || value.value?.toString() || '-';
  }
  return '-';
};

export default function SupervisorPGsPage() {
  const [pgs, setPgs] = useState<AssignedPG[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPGs = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await usersApi.getAssignedPGs();
        setPgs(data || []);
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Failed to load assigned PGs';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    fetchPGs();
  }, []);

  const columns: Column<AssignedPG>[] = [
    {
      key: 'name',
      label: 'Name',
      render: (pg) => pg.full_name || pg.username || '-',
    },
    {
      key: 'specialty',
      label: 'Specialty',
      render: (pg) => formatValue(pg.specialty),
    },
    {
      key: 'year',
      label: 'Year',
      render: (pg) => formatValue(pg.year),
    },
    {
      key: 'email',
      label: 'Email',
      render: (pg) => pg.email || '-',
    },
    {
      key: 'status',
      label: 'Status',
      render: (pg) => (
        <span
          className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
            pg.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-700'
          }`}
        >
          {pg.is_active ? 'Active' : 'Inactive'}
        </span>
      ),
    },
  ];

  return (
    <ProtectedRoute allowedRoles={['supervisor']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My PGs</h1>
            <p className="mt-2 text-gray-600">View assigned postgraduate trainees</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

          <SectionCard title="Assigned PGs">
            {loading ? (
              <TableSkeleton rows={6} cols={5} />
            ) : pgs.length === 0 ? (
              <EmptyState
                title="No assigned PGs"
                description="You currently do not have any PGs assigned."
              />
            ) : (
              <DataTable columns={columns} data={pgs} />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
