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
  posting_type: string;
  institution_name: string;
  city: string;
  start_date: string;
  end_date: string;
  status: string;
  notes: string;
}

const STATUS_COLORS: Record<string, string> = {
  SUBMITTED: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  REJECTED: 'bg-red-100 text-red-800',
  COMPLETED: 'bg-purple-100 text-purple-800',
};

const TYPE_LABELS: Record<string, string> = { deputation: 'Deputation', off_service: 'Off-service' };

const columns: Column<Posting>[] = [
  { key: 'posting_type', label: 'Type', render: r => TYPE_LABELS[r.posting_type] ?? r.posting_type },
  { key: 'institution_name', label: 'Institution' },
  { key: 'city', label: 'City', render: r => r.city || '—' },
  { key: 'start_date', label: 'From', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'To', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'status', label: 'Status', render: r => <span className={`text-xs font-medium px-2 py-0.5 rounded ${STATUS_COLORS[r.status] ?? 'bg-gray-100'}`}>{r.status}</span> },
];

export default function MyPostingsPage() {
  const [postings, setPostings] = useState<Posting[]>([]);
  const [trainingId, setTrainingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ posting_type: 'deputation', institution_name: '', city: '', start_date: '', end_date: '', notes: '' });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const [pRes, trRes] = await Promise.all([
        apiClient.get('/api/postings/'),
        apiClient.get('/api/resident-training/'),
      ]);
      setPostings(pRes.data.results ?? pRes.data);
      const records = trRes.data.results ?? trRes.data;
      if (records.length > 0) setTrainingId(records[0].id);
    } catch { setError('Failed to load.'); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); if (!trainingId) return; setSaving(true);
    try {
      await apiClient.post('/api/postings/', { ...form, resident_training: trainingId });
      setShowForm(false); load();
    } catch { setError('Failed to submit posting.'); }
    finally { setSaving(false); }
  };

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Deputation & Postings</h1>
              <p className="mt-1 text-gray-500">Track your deputation and off-service postings.</p>
            </div>
            {trainingId && (
              <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
                + New Posting
              </button>
            )}
          </div>
          {error && <ErrorBanner message={error} />}
          {showForm && (
            <SectionCard title="New Posting">
              <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Type *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.posting_type} onChange={e => setForm({ ...form, posting_type: e.target.value })}>
                    {Object.entries(TYPE_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Institution *</label>
                  <input required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.institution_name} onChange={e => setForm({ ...form, institution_name: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">City</label>
                  <input className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.city} onChange={e => setForm({ ...form, city: e.target.value })} />
                </div>
                <div className="sm:col-span-2 grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Start Date *</label>
                    <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">End Date *</label>
                    <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })} />
                  </div>
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Notes</label>
                  <textarea rows={2} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} />
                </div>
                <div className="sm:col-span-2 flex gap-3">
                  <button type="submit" disabled={saving} className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Submitting…' : 'Submit'}
                  </button>
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md">Cancel</button>
                </div>
              </form>
            </SectionCard>
          )}
          <SectionCard title="Posting History">
            {loading ? <TableSkeleton /> : <DataTable columns={columns} data={postings} emptyMessage="No postings." />}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
