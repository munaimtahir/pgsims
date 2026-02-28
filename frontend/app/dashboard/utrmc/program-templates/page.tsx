'use client';

import { useCallback, useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import apiClient from '@/lib/api';

interface Template {
  id: number;
  program: number;
  program_name: string;
  name: string;
  department: number;
  department_name: string;
  duration_weeks: number;
  required: boolean;
  sequence_order: number;
  active: boolean;
}

interface Program { id: number; name: string; code: string; }
interface Department { id: number; name: string; code: string; }

const columns: Column<Template>[] = [
  { key: 'program_name', label: 'Program' },
  { key: 'name', label: 'Template Name' },
  { key: 'department_name', label: 'Department' },
  { key: 'duration_weeks', label: 'Duration (wks)' },
  {
    key: 'required',
    label: 'Required',
    render: (r) => (
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${r.required ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'}`}>
        {r.required ? 'Required' : 'Optional'}
      </span>
    ),
  },
  { key: 'sequence_order', label: 'Order' },
  {
    key: 'active',
    label: 'Active',
    render: (r) => (
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${r.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}>
        {r.active ? 'Yes' : 'No'}
      </span>
    ),
  },
];

export default function ProgramTemplatesPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [programs, setPrograms] = useState<Program[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ program: '', name: '', department: '', duration_weeks: '', required: true, sequence_order: '0', active: true });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const [tRes, pRes, dRes] = await Promise.all([
        apiClient.get('/api/program-templates/'),
        apiClient.get('/api/programs/'),
        apiClient.get('/api/departments/'),
      ]);
      setTemplates(tRes.data.results ?? tRes.data);
      setPrograms(pRes.data.results ?? pRes.data);
      setDepartments(dRes.data.results ?? dRes.data);
    } catch {
      setError('Failed to load data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await apiClient.post('/api/program-templates/', {
        ...form,
        program: Number(form.program),
        department: Number(form.department),
        duration_weeks: Number(form.duration_weeks),
        sequence_order: Number(form.sequence_order),
      });
      setShowForm(false);
      load();
    } catch {
      setError('Failed to save template.');
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
              <h1 className="text-2xl font-bold text-gray-900">Rotation Templates</h1>
              <p className="mt-1 text-gray-500">Define standard rotation blocks per training program.</p>
            </div>
            <button onClick={() => setShowForm(!showForm)} className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
              + New Template
            </button>
          </div>
          {error && <ErrorBanner message={error} />}
          {showForm && (
            <SectionCard title="Create Template">
              <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Program *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.program} onChange={e => setForm({ ...form, program: e.target.value })}>
                    <option value="">-- Select Program --</option>
                    {programs.map(p => <option key={p.id} value={p.id}>{p.name} ({p.code})</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Template Name *</label>
                  <input required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Department *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.department} onChange={e => setForm({ ...form, department: e.target.value })}>
                    <option value="">-- Select Department --</option>
                    {departments.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Duration (weeks) *</label>
                  <input required type="number" min={1} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.duration_weeks} onChange={e => setForm({ ...form, duration_weeks: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Sequence Order</label>
                  <input type="number" min={0} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.sequence_order} onChange={e => setForm({ ...form, sequence_order: e.target.value })} />
                </div>
                <div className="flex items-center mt-6 gap-4">
                  <label className="flex items-center gap-2 text-sm text-gray-700">
                    <input type="checkbox" checked={form.required} onChange={e => setForm({ ...form, required: e.target.checked })} /> Required
                  </label>
                  <label className="flex items-center gap-2 text-sm text-gray-700">
                    <input type="checkbox" checked={form.active} onChange={e => setForm({ ...form, active: e.target.checked })} /> Active
                  </label>
                </div>
                <div className="sm:col-span-2 flex gap-3">
                  <button type="submit" disabled={saving} className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Saving…' : 'Save Template'}
                  </button>
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md">Cancel</button>
                </div>
              </form>
            </SectionCard>
          )}
          <SectionCard title="All Templates">
            {loading ? <TableSkeleton /> : <DataTable columns={columns} data={templates} emptyMessage="No templates found." />}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
