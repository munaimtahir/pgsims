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

interface TrainingRecord {
  id: number;
  resident_user: number;
  resident_name: string;
  program: number;
  program_name: string;
  program_code: string;
  start_date: string;
  expected_end_date: string | null;
  current_level: string;
  active: boolean;
}

interface Program { id: number; name: string; code: string; }
interface ResidentUser { id: number; username: string; first_name: string; last_name: string; }

const LEVEL_LABELS: Record<string, string> = {
  y1: 'Year 1', y2: 'Year 2', y3: 'Year 3', y4: 'Year 4', y5: 'Year 5',
};

const columns: Column<TrainingRecord>[] = [
  { key: 'resident_name', label: 'Resident' },
  { key: 'program_name', label: 'Program' },
  { key: 'start_date', label: 'Start', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'expected_end_date', label: 'Expected End', render: r => r.expected_end_date ? (() => { try { return format(new Date(r.expected_end_date!), 'MMM dd, yyyy'); } catch { return r.expected_end_date!; } })() : '—' },
  { key: 'current_level', label: 'Level', render: r => LEVEL_LABELS[r.current_level] ?? r.current_level ?? '—' },
  {
    key: 'active', label: 'Active',
    render: r => <span className={`text-xs font-medium px-2 py-0.5 rounded ${r.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}>{r.active ? 'Yes' : 'No'}</span>,
  },
];

export default function ResidentTrainingPage() {
  const [records, setRecords] = useState<TrainingRecord[]>([]);
  const [programs, setPrograms] = useState<Program[]>([]);
  const [residents, setResidents] = useState<ResidentUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ resident_user: '', program: '', start_date: '', expected_end_date: '', current_level: '', active: true });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const [rRes, pRes, uRes] = await Promise.all([
        apiClient.get('/api/resident-training/'),
        apiClient.get('/api/programs/'),
        apiClient.get('/api/users/?role=resident&role=pg&page_size=200'),
      ]);
      setRecords(rRes.data.results ?? rRes.data);
      setPrograms(pRes.data.results ?? pRes.data);
      setResidents(uRes.data.results ?? uRes.data);
    } catch { setError('Failed to load data.'); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true);
    try {
      await apiClient.post('/api/resident-training/', {
        ...form,
        resident_user: Number(form.resident_user),
        program: Number(form.program),
        expected_end_date: form.expected_end_date || null,
        current_level: form.current_level || '',
      });
      setShowForm(false); load();
    } catch { setError('Failed to save record.'); }
    finally { setSaving(false); }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Resident Training Records</h1>
              <p className="mt-1 text-gray-500">Enroll residents in training programs.</p>
            </div>
            <button onClick={() => setShowForm(!showForm)} className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
              + Enroll Resident
            </button>
          </div>
          {error && <ErrorBanner message={error} />}
          {showForm && (
            <SectionCard title="Enroll Resident">
              <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Resident *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.resident_user} onChange={e => setForm({ ...form, resident_user: e.target.value })}>
                    <option value="">-- Select Resident --</option>
                    {residents.map(u => <option key={u.id} value={u.id}>{u.first_name} {u.last_name} ({u.username})</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Program *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.program} onChange={e => setForm({ ...form, program: e.target.value })}>
                    <option value="">-- Select Program --</option>
                    {programs.map(p => <option key={p.id} value={p.id}>{p.name} ({p.code})</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Start Date *</label>
                  <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Expected End Date</label>
                  <input type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.expected_end_date} onChange={e => setForm({ ...form, expected_end_date: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Current Level</label>
                  <select className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.current_level} onChange={e => setForm({ ...form, current_level: e.target.value })}>
                    <option value="">-- None --</option>
                    {Object.entries(LEVEL_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                  </select>
                </div>
                <div className="flex items-center mt-6">
                  <input type="checkbox" id="rec-active" checked={form.active} onChange={e => setForm({ ...form, active: e.target.checked })} className="mr-2" />
                  <label htmlFor="rec-active" className="text-sm text-gray-700">Active</label>
                </div>
                <div className="sm:col-span-2 flex gap-3">
                  <button type="submit" disabled={saving} className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Saving…' : 'Save Record'}
                  </button>
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md">Cancel</button>
                </div>
              </form>
            </SectionCard>
          )}
          <SectionCard title="All Training Records">
            {loading ? <TableSkeleton /> : <DataTable columns={columns} data={records} emptyMessage="No training records." />}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
