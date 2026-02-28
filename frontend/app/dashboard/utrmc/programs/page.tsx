'use client';

import { useCallback, useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import apiClient from '@/lib/api';

interface Program {
  id: number;
  name: string;
  code: string;
  duration_months: number;
  active: boolean;
  description: string;
}

const columns: Column<Program>[] = [
  { key: 'name', label: 'Program Name' },
  { key: 'code', label: 'Code' },
  { key: 'duration_months', label: 'Duration (months)' },
  {
    key: 'active',
    label: 'Active',
    render: (r) => (
      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${r.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}>
        {r.active ? 'Active' : 'Inactive'}
      </span>
    ),
  },
];

export default function ProgramsPage() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: '', code: '', duration_months: '', description: '', active: true });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await apiClient.get('/api/programs/');
      setPrograms(res.data.results ?? res.data);
    } catch {
      setError('Failed to load programs.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await apiClient.post('/api/programs/', {
        ...form,
        duration_months: Number(form.duration_months),
      });
      setShowForm(false);
      setForm({ name: '', code: '', duration_months: '', description: '', active: true });
      load();
    } catch {
      setError('Failed to create program.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Training Programs</h1>
              <p className="mt-1 text-gray-500">Manage postgraduate training program definitions.</p>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700"
            >
              + New Program
            </button>
          </div>
          {error && <ErrorBanner message={error} />}
          {showForm && (
            <SectionCard title="Create Program">
              <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name *</label>
                  <input required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Code *</label>
                  <input required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.code} onChange={e => setForm({ ...form, code: e.target.value.toUpperCase() })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Duration (months) *</label>
                  <input required type="number" min={1} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.duration_months} onChange={e => setForm({ ...form, duration_months: e.target.value })} />
                </div>
                <div className="flex items-center mt-6">
                  <input type="checkbox" id="prog-active" checked={form.active} onChange={e => setForm({ ...form, active: e.target.checked })} className="mr-2" />
                  <label htmlFor="prog-active" className="text-sm text-gray-700">Active</label>
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <textarea rows={2} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
                </div>
                <div className="sm:col-span-2 flex gap-3">
                  <button type="submit" disabled={saving} className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Saving…' : 'Save Program'}
                  </button>
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200">
                    Cancel
                  </button>
                </div>
              </form>
            </SectionCard>
          )}
          <SectionCard title="All Programs">
            {loading ? <TableSkeleton /> : <DataTable columns={columns} data={programs} emptyMessage="No programs found." />}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
