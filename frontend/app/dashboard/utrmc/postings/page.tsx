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

interface Posting {
  id: number;
  resident_name: string;
  posting_type: string;
  institution_name: string;
  city: string;
  start_date: string;
  end_date: string;
  status: string;
}

const STATUS_COLORS: Record<string, string> = {
  SUBMITTED: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  REJECTED: 'bg-red-100 text-red-800',
  COMPLETED: 'bg-purple-100 text-purple-800',
};

const TYPE_LABELS: Record<string, string> = { deputation: 'Deputation', off_service: 'Off-service' };

const columns: Column<Posting>[] = [
  { key: 'resident_name', label: 'Resident' },
  { key: 'posting_type', label: 'Type', render: r => TYPE_LABELS[r.posting_type] ?? r.posting_type },
  { key: 'institution_name', label: 'Institution' },
  { key: 'city', label: 'City', render: r => r.city || '—' },
  { key: 'start_date', label: 'From', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'To', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'status', label: 'Status', render: r => <span className={`text-xs font-medium px-2 py-0.5 rounded ${STATUS_COLORS[r.status] ?? 'bg-gray-100'}`}>{r.status}</span> },
];

export default function PostingsAdminPage() {
  const [items, setItems] = useState<Posting[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const params: Record<string, string> = {};
      if (statusFilter) params.status = statusFilter;
      const res = await apiClient.get('/api/postings/', { params });
      setItems(res.data.results ?? res.data);
    } catch { setError('Failed to load postings.'); }
    finally { setLoading(false); }
  }, [statusFilter]);

  useEffect(() => { load(); }, [load]);

  const action = async (id: number, act: string, body: Record<string, string> = {}) => {
    try {
      await apiClient.post(`/api/postings/${id}/${act}/`, body);
      load();
    } catch { setError(`Action '${act}' failed.`); }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Deputation & Off-service Postings</h1>
            <p className="mt-1 text-gray-500">Manage all resident deputation and off-service postings.</p>
          </div>
          {error && <ErrorBanner message={error} />}
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700">Filter:</label>
            <select className="border border-gray-300 rounded-md p-1.5 text-sm" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
              <option value="">All</option>
              {['SUBMITTED','APPROVED','REJECTED','COMPLETED'].map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <SectionCard title="Postings">
            {loading ? <TableSkeleton /> : (
              <DataTable
                columns={[
                  ...columns,
                  {
                    key: 'id',
                    label: 'Actions',
                    render: r => (
                      <div className="flex gap-1">
                        {r.status === 'SUBMITTED' && <button onClick={() => action(r.id, 'approve')} className="text-xs px-2 py-1 bg-green-600 text-white rounded">Approve</button>}
                        {r.status === 'SUBMITTED' && <button onClick={() => { const reason = prompt('Reason?'); if (reason) action(r.id, 'reject', { reason }); }} className="text-xs px-2 py-1 bg-red-600 text-white rounded">Reject</button>}
                        {r.status === 'APPROVED' && <button onClick={() => action(r.id, 'complete')} className="text-xs px-2 py-1 bg-purple-600 text-white rounded">Complete</button>}
                      </div>
                    ),
                  },
                ]}
                data={items}
                emptyMessage="No postings found."
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
