'use client';

import { useCallback, useEffect, useState } from 'react';
import { format } from 'date-fns';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import DataTable, { Column } from '@/components/ui/DataTable';
import EmptyState from '@/components/ui/EmptyState';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import { rotationsApi, RotationSummary } from '@/lib/api';

const normalizeRotations = (data: { results?: RotationSummary[] }) => {
  return data.results ?? [];
};

const statusClassMap: Record<string, string> = {
  ongoing: 'bg-green-100 text-green-800',
  planned: 'bg-blue-100 text-blue-800',
  completed: 'bg-gray-100 text-gray-800',
  cancelled: 'bg-red-100 text-red-800',
};

const columns: Column<RotationSummary>[] = [
  {
    key: 'name',
    label: 'Rotation',
    render: (item) => item.name || item.department || '-'
  },
  {
    key: 'department',
    label: 'Department',
    render: (item) => item.department || '-'
  },
  {
    key: 'hospital',
    label: 'Hospital',
    render: (item) => item.hospital || '-'
  },
  {
    key: 'start_date',
    label: 'Start Date',
    render: (item) => {
      try {
        return format(new Date(item.start_date), 'MMM dd, yyyy');
      } catch {
        return item.start_date || '-';
      }
    }
  },
  {
    key: 'end_date',
    label: 'End Date',
    render: (item) => {
      try {
        return format(new Date(item.end_date), 'MMM dd, yyyy');
      } catch {
        return item.end_date || '-';
      }
    }
  },
  {
    key: 'status',
    label: 'Status',
    render: (item) => {
      const className = statusClassMap[item.status] || 'bg-yellow-100 text-yellow-800';
      return (
        <span className={`px-2 py-1 text-xs rounded-full ${className}`}>
          {item.status}
        </span>
      );
    }
  },
  {
    key: 'supervisor_name',
    label: 'Supervisor',
    render: (item) => item.supervisor_name || '-'
  }
];

export default function PGRotationsPage() {
  const [rotations, setRotations] = useState<RotationSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadRotations = useCallback(async () => {
    try {
      setError(null);
      const data = await rotationsApi.getMyRotations();
      setRotations(normalizeRotations(data));
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load rotations';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRotations();
  }, [loadRotations]);

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Rotations</h1>
            <p className="mt-2 text-gray-600">View your rotation schedule and assignments</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

          <SectionCard title="Rotations">
            {loading ? (
              <TableSkeleton rows={5} cols={6} />
            ) : rotations.length === 0 ? (
              <EmptyState
                title="No rotations yet"
                description="You don't have any rotations assigned yet. Check back later for updates."
              />
            ) : (
              <DataTable columns={columns} data={rotations} emptyMessage="No rotations found" />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
