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
  resident_training: number;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
}

const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'bg-gray-100 text-gray-700',
  SUBMITTED: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  REJECTED: 'bg-red-100 text-red-800',
};

const LEAVE_TYPE_LABELS: Record<string, string> = {
  annual: 'Annual', sick: 'Sick', casual: 'Casual',
  study: 'Study', maternity: 'Maternity', other: 'Other',
};

const columns: Column<LeaveRequest>[] = [
  { key: 'leave_type', label: 'Type', render: r => LEAVE_TYPE_LABELS[r.leave_type] ?? r.leave_type },
  { key: 'start_date', label: 'From', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'To', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'reason', label: 'Reason', render: r => r.reason || '—' },
  { key: 'status', label: 'Status', render: r => <span className={`text-xs font-medium px-2 py-0.5 rounded ${STATUS_COLORS[r.status] ?? 'bg-gray-100'}`}>{r.status}</span> },
];

export default function MyLeavesPage() {
  const [leaves, setLeaves] = useState<LeaveRequest[]>([]);
  const [trainingId, setTrainingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ leave_type: 'annual', start_date: '', end_date: '', reason: '' });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const [lRes, trRes] = await Promise.all([
        apiClient.get('/api/my/leaves/'),
        apiClient.get('/api/resident-training/'),
      ]);
      setLeaves(lRes.data.results ?? lRes.data);
      const records = trRes.data.results ?? trRes.data;
      if (records.length > 0) setTrainingId(records[0].id);
    } catch { setError('Failed to load.'); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); if (!trainingId) return; setSaving(true);
    try {
      const res = await apiClient.post('/api/leaves/', { ...form, resident_training: trainingId });
      await apiClient.post(`/api/leaves/${res.data.id}/submit/`);
      setShowForm(false); load();
    } catch { setError('Failed to submit leave.'); }
    finally { setSaving(false); }
  };

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Leave Requests</h1>
              <p className="mt-1 text-gray-500">Submit and track your leave applications.</p>
            </div>
            {trainingId && (
              <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
                + Request Leave
              </button>
            )}
          </div>
          {error && <ErrorBanner message={error} />}
          {showForm && (
            <SectionCard title="New Leave Request">
              <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Leave Type *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.leave_type} onChange={e => setForm({ ...form, leave_type: e.target.value })}>
                    {Object.entries(LEAVE_TYPE_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                  </select>
                </div>
                <div className="sm:col-span-2 grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">From *</label>
                    <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">To *</label>
                    <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })} />
                  </div>
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Reason</label>
                  <textarea rows={2} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.reason} onChange={e => setForm({ ...form, reason: e.target.value })} />
                </div>
                <div className="sm:col-span-2 flex gap-3">
                  <button type="submit" disabled={saving} className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Submitting…' : 'Submit Request'}
                  </button>
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md">Cancel</button>
                </div>
              </form>
            </SectionCard>
          )}
          <SectionCard title="Leave History">
            {loading ? <TableSkeleton /> : <DataTable columns={columns} data={leaves} emptyMessage="No leave requests." />}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
