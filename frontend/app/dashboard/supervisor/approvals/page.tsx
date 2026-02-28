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

const columns: Column<RotationAssignment>[] = [
  { key: 'resident_name', label: 'Resident' },
  { key: 'program_name', label: 'Program' },
  { key: 'hospital_name', label: 'Hospital' },
  { key: 'department_name', label: 'Department' },
  { key: 'start_date', label: 'Start', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'End', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'status', label: 'Status', render: r => <span className="text-xs font-medium px-2 py-0.5 rounded bg-blue-100 text-blue-800">{r.status}</span> },
];

export default function SupervisorApprovalsPage() {
  const [items, setItems] = useState<RotationAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const res = await apiClient.get('/api/supervisor/rotations/pending/');
      setItems(res.data.results ?? res.data);
    } catch { setError('Failed to load approvals.'); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const action = async (id: number, act: string, body: Record<string, string> = {}) => {
    try {
      await apiClient.post(`/api/rotations/${id}/${act}/`, body);
      load();
    } catch { setError(`Action '${act}' failed.`); }
  };

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Rotation Approvals</h1>
            <p className="mt-1 text-gray-500">Pending rotation assignments in your departments.</p>
          </div>
          {error && <ErrorBanner message={error} />}
          <SectionCard title={`Pending (${items.length})`}>
            {loading ? <TableSkeleton /> : (
              <DataTable
                columns={[
                  ...columns,
                  {
                    key: 'id',
                    label: 'Actions',
                    render: r => (
                      <div className="flex gap-1">
                        <button onClick={() => action(r.id, 'hod-approve')} className="text-xs px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700">Approve</button>
                        <button onClick={() => { const reason = prompt('Return reason?'); if (reason) action(r.id, 'returned', { reason }); }} className="text-xs px-2 py-1 bg-yellow-600 text-white rounded">Return</button>
                        <button onClick={() => { const reason = prompt('Rejection reason?'); if (reason) action(r.id, 'reject', { reason }); }} className="text-xs px-2 py-1 bg-red-600 text-white rounded">Reject</button>
                      </div>
                    ),
                  },
                ]}
                data={items}
                emptyMessage="No pending rotation approvals."
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
