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
  return_reason: string;
  reject_reason: string;
}

const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'bg-gray-100 text-gray-700',
  SUBMITTED: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  ACTIVE: 'bg-emerald-100 text-emerald-800',
  COMPLETED: 'bg-purple-100 text-purple-800',
  RETURNED: 'bg-yellow-100 text-yellow-800',
  REJECTED: 'bg-red-100 text-red-800',
  CANCELLED: 'bg-gray-100 text-gray-500',
};

function StatusBadge({ status }: { status: string }) {
  return (
    <span className={`text-xs font-medium px-2 py-0.5 rounded ${STATUS_COLORS[status] ?? 'bg-gray-100 text-gray-700'}`}>
      {status}
    </span>
  );
}

const columns: Column<RotationAssignment>[] = [
  { key: 'resident_name', label: 'Resident' },
  { key: 'program_name', label: 'Program' },
  { key: 'hospital_name', label: 'Hospital' },
  { key: 'department_name', label: 'Department' },
  { key: 'start_date', label: 'Start', render: r => { try { return format(new Date(r.start_date), 'MMM dd, yyyy'); } catch { return r.start_date; } } },
  { key: 'end_date', label: 'End', render: r => { try { return format(new Date(r.end_date), 'MMM dd, yyyy'); } catch { return r.end_date; } } },
  { key: 'status', label: 'Status', render: r => <StatusBadge status={r.status} /> },
];

interface HospitalDept { id: number; hospital: { id: number; name: string }; department: { id: number; name: string }; }
interface TrainingRecord { id: number; resident_name: string; program_name: string; }

export default function RotationsPage() {
  const [rotations, setRotations] = useState<RotationAssignment[]>([]);
  const [trainingRecords, setTrainingRecords] = useState<TrainingRecord[]>([]);
  const [hospitalDepts, setHospitalDepts] = useState<HospitalDept[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ resident_training: '', hospital_department: '', start_date: '', end_date: '', notes: '' });
  const [saving, setSaving] = useState(false);
  const [statusFilter, setStatusFilter] = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const params: Record<string, string> = {};
      if (statusFilter) params.status = statusFilter;
      const [rRes, trRes, hdRes] = await Promise.all([
        apiClient.get('/api/rotations/', { params }),
        apiClient.get('/api/resident-training/'),
        apiClient.get('/api/hospital-departments/'),
      ]);
      setRotations(rRes.data.results ?? rRes.data);
      setTrainingRecords(trRes.data.results ?? trRes.data);
      setHospitalDepts(hdRes.data.results ?? hdRes.data);
    } catch { setError('Failed to load data.'); }
    finally { setLoading(false); }
  }, [statusFilter]);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true);
    try {
      await apiClient.post('/api/rotations/', {
        ...form,
        resident_training: Number(form.resident_training),
        hospital_department: Number(form.hospital_department),
      });
      setShowForm(false); load();
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string; non_field_errors?: string[] } } })?.response?.data;
      setError(msg?.detail ?? msg?.non_field_errors?.[0] ?? 'Failed to create rotation.');
    } finally { setSaving(false); }
  };

  const action = async (id: number, act: string, body: Record<string, string> = {}) => {
    try {
      await apiClient.post(`/api/rotations/${id}/${act}/`, body);
      load();
    } catch { setError(`Action '${act}' failed.`); }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Rotation Assignments</h1>
              <p className="mt-1 text-gray-500">Manage and track resident rotation assignments.</p>
            </div>
            <button onClick={() => setShowForm(!showForm)} className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700">
              + New Rotation
            </button>
          </div>
          {error && <ErrorBanner message={error} />}

          {/* Filters */}
          <div className="flex items-center gap-4">
            <label className="text-sm text-gray-700 font-medium">Filter by status:</label>
            <select className="border border-gray-300 rounded-md p-1.5 text-sm" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
              <option value="">All</option>
              {['DRAFT','SUBMITTED','APPROVED','ACTIVE','COMPLETED','RETURNED','REJECTED','CANCELLED'].map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {showForm && (
            <SectionCard title="Create Rotation Assignment">
              <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Training Record *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.resident_training} onChange={e => setForm({ ...form, resident_training: e.target.value })}>
                    <option value="">-- Select --</option>
                    {trainingRecords.map(r => <option key={r.id} value={r.id}>{r.resident_name} – {r.program_name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Hospital / Department *</label>
                  <select required className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.hospital_department} onChange={e => setForm({ ...form, hospital_department: e.target.value })}>
                    <option value="">-- Select --</option>
                    {hospitalDepts.map(hd => <option key={hd.id} value={hd.id}>{hd.hospital?.name ?? '?'} / {hd.department?.name ?? '?'}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Start Date *</label>
                  <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">End Date *</label>
                  <input required type="date" className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })} />
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Notes</label>
                  <textarea rows={2} className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-sm" value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} />
                </div>
                <div className="sm:col-span-2 flex gap-3">
                  <button type="submit" disabled={saving} className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Creating…' : 'Create'}
                  </button>
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-md">Cancel</button>
                </div>
              </form>
            </SectionCard>
          )}

          <SectionCard title="All Rotations">
            {loading ? <TableSkeleton /> : (
              <DataTable
                columns={[
                  ...columns,
                  {
                    key: 'id',
                    label: 'Actions',
                    render: r => (
                      <div className="flex gap-1 flex-wrap">
                        {r.status === 'DRAFT' && <button onClick={() => action(r.id, 'submit')} className="text-xs px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">Submit</button>}
                        {r.status === 'SUBMITTED' && <button onClick={() => action(r.id, 'hod-approve')} className="text-xs px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700">HOD Approve</button>}
                        {['SUBMITTED','APPROVED'].includes(r.status) && <button onClick={() => action(r.id, 'utrmc-approve')} className="text-xs px-2 py-1 bg-emerald-600 text-white rounded hover:bg-emerald-700">UTRMC Approve</button>}
                        {r.status === 'APPROVED' && <button onClick={() => action(r.id, 'activate')} className="text-xs px-2 py-1 bg-purple-600 text-white rounded hover:bg-purple-700">Activate</button>}
                        {r.status === 'ACTIVE' && <button onClick={() => action(r.id, 'complete')} className="text-xs px-2 py-1 bg-gray-600 text-white rounded hover:bg-gray-700">Complete</button>}
                        {['SUBMITTED','APPROVED'].includes(r.status) && <button onClick={() => { const reason = prompt('Return reason?'); if (reason) action(r.id, 'returned', { reason }); }} className="text-xs px-2 py-1 bg-yellow-600 text-white rounded hover:bg-yellow-700">Return</button>}
                        {['SUBMITTED','APPROVED'].includes(r.status) && <button onClick={() => { const reason = prompt('Rejection reason?'); if (reason) action(r.id, 'reject', { reason }); }} className="text-xs px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700">Reject</button>}
                      </div>
                    ),
                  },
                ]}
                data={rotations}
                emptyMessage="No rotation assignments found."
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
