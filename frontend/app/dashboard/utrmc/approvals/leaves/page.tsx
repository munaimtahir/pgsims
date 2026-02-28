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

interface LeaveRequest {
  id: number;
  resident_name: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
}

const LEAVE_TYPE_LABELS: Record<string, string> = {
  annual: 'Annual', sick: 'Sick', casual: 'Casual',
  study: 'Study', maternity: 'Maternity', other: 'Other',
};

const columns: Column<LeaveRequest>[] = [
  { key: 'resident_name', label: 'Resident' },
  { key: 'leave_type', label: 'Type', render: r => LEAVE_TYPE_LABELS[r.leave_type] ?? r.leave_type },
  { key: 'start_date', label: 'From', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'To', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'reason', label: 'Reason', render: r => r.reason || '—' },
];

export default function LeaveApprovalsPage() {
  const [items, setItems] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const res = await apiClient.get('/api/utrmc/approvals/leaves/');
      setItems(res.data.results ?? res.data);
    } catch { setError('Failed to load leave approvals.'); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const action = async (id: number, act: string, body: Record<string, string> = {}) => {
    try {
      await apiClient.post(`/api/leaves/${id}/${act}/`, body);
      load();
    } catch { setError(`Action '${act}' failed.`); }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'supervisor', 'faculty']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Leave Approvals</h1>
            <p className="mt-1 text-gray-500">Pending leave requests awaiting approval.</p>
          </div>
          {error && <ErrorBanner message={error} />}
          <SectionCard title={`Pending Leave Requests (${items.length})`}>
            {loading ? <TableSkeleton /> : (
              <DataTable
                columns={[
                  ...columns,
                  {
                    key: 'id',
                    label: 'Actions',
                    render: r => (
                      <div className="flex gap-1">
                        <button onClick={() => action(r.id, 'approve')} className="text-xs px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700">Approve</button>
                        <button onClick={() => { const reason = prompt('Rejection reason?'); if (reason) action(r.id, 'reject', { reason }); }} className="text-xs px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700">Reject</button>
                      </div>
                    ),
                  },
                ]}
                data={items}
                emptyMessage="No pending leave requests."
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
