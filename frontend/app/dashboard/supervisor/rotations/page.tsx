'use client';

import { useCallback, useEffect, useState } from 'react';
import { format } from 'date-fns';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import apiClient from '@/lib/api';

interface RotationAssignment {
  id: number;
  resident_name: string;
  program_name: string;
  hospital_name: string;
  department_name: string;
  start_date: string;
  end_date: string;
  status: string;
}

const STATUS_COLORS: Record<string, string> = {
  SUBMITTED: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  ACTIVE: 'bg-emerald-100 text-emerald-800',
  COMPLETED: 'bg-purple-100 text-purple-800',
  RETURNED: 'bg-yellow-100 text-yellow-800',
  REJECTED: 'bg-red-100 text-red-800',
};

const columns: Column<RotationAssignment>[] = [
  { key: 'resident_name', label: 'Resident' },
  { key: 'program_name', label: 'Program' },
  { key: 'hospital_name', label: 'Hospital' },
  { key: 'department_name', label: 'Department' },
  { key: 'start_date', label: 'Start', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'End', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'status', label: 'Status', render: r => <span className={`text-xs font-medium px-2 py-0.5 rounded ${STATUS_COLORS[r.status] ?? 'bg-gray-100 text-gray-700'}`}>{r.status}</span> },
];

export default function SupervisorRotationsPage() {
  const [items, setItems] = useState<RotationAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const res = await apiClient.get('/api/rotations/');
      setItems(res.data.results ?? res.data);
    } catch { setError('Failed to load rotations.'); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Department Rotations</h1>
            <p className="mt-1 text-gray-500">Rotation assignments in your department(s).</p>
          </div>
          {error && <ErrorBanner message={error} />}
          <SectionCard title="Rotations">
            {loading ? <TableSkeleton /> : <DataTable columns={columns} data={items} emptyMessage="No rotations found." />}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
