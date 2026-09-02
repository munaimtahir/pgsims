'use client';

import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicOptions, ReviewQueueItem } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function ReviewQueuePage() {
  const { user } = useAuthStore();
  const canManage = user?.role === 'ADMIN';
  const [rows, setRows] = useState<ReviewQueueItem[]>([]);
  const [options, setOptions] = useState<AcademicOptions | null>(null);
  const [records, setRecords] = useState<Array<{ id: number; resident_name: string }>>([]);
  const [form, setForm] = useState({ resident: '', supervisor: '', training_record: '', queue_type: 'TRAINING_RECORD_REVIEW', due_date: '', notes: '' });
  const load = () => {
    academicsApi.listReviewQueue().then(setRows).catch(() => setRows([]));
    academicsApi.getOptions().then(setOptions).catch(() => setOptions(null));
    academicsApi.listTrainingRecords().then((items) => setRecords(items.map((item) => ({ id: item.id, resident_name: item.resident_name })))).catch(() => setRecords([]));
  };
  useEffect(() => { load(); }, []);
  const createItem = async (event: FormEvent) => {
    event.preventDefault();
    await academicsApi.createReviewQueueItem({
      resident: Number(form.resident),
      supervisor: Number(form.supervisor),
      training_record: form.training_record ? Number(form.training_record) : null,
      queue_type: form.queue_type,
      due_date: form.due_date || null,
      notes: form.notes,
    });
    setForm({ resident: '', supervisor: '', training_record: '', queue_type: 'TRAINING_RECORD_REVIEW', due_date: '', notes: '' });
    load();
  };
  const mark = async (id: number, statusValue: 'DONE' | 'DISMISSED') => {
    await academicsApi.updateReviewQueueItem(id, { status: statusValue });
    load();
  };
  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR']}>
      <div className="pg-page space-y-6">
        <PageHeader title="Academic Review Queue" description="Future-ready queue for supervisor review work." />
        {canManage && options && (
          <form onSubmit={createItem} className="pg-card grid gap-3 md:grid-cols-3">
            <select className="pg-form-input" value={form.resident} onChange={(e) => setForm({ ...form, resident: e.target.value })} required><option value="">Resident</option>{options.residents.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select>
            <select className="pg-form-input" value={form.supervisor} onChange={(e) => setForm({ ...form, supervisor: e.target.value })} required><option value="">Supervisor</option>{options.supervisors.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select>
            <select className="pg-form-input" value={form.training_record} onChange={(e) => setForm({ ...form, training_record: e.target.value })}><option value="">Training Record</option>{records.map((row) => <option key={row.id} value={row.id}>#{row.id} · {row.resident_name}</option>)}</select>
            <select className="pg-form-input" value={form.queue_type} onChange={(e) => setForm({ ...form, queue_type: e.target.value })}>{['PROFILE_REVIEW', 'TRAINING_RECORD_REVIEW', 'PROGRESS_REVIEW', 'FUTURE_EVALUATION'].map((value) => <option key={value} value={value}>{value}</option>)}</select>
            <input className="pg-form-input" type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} />
            <input className="pg-form-input" placeholder="Notes" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
            <button className="pg-btn-primary md:col-span-3" type="submit">Create Review Item</button>
          </form>
        )}
        <div className="space-y-3">
          {rows.map((row) => (
            <div key={row.id} className="pg-card">
              <div className="flex items-start justify-between gap-3 flex-wrap">
                <div>
                  <p className="font-semibold text-slate-900">{row.resident_name}</p>
                  <p className="text-sm text-slate-600">{row.queue_type} · Supervisor: {row.supervisor_name}</p>
                  {row.training_record && <p className="text-xs text-slate-500">Training record #{row.training_record}</p>}
                </div>
                <div className="text-sm text-slate-600">{row.status}</div>
              </div>
              <div className="mt-3 flex gap-3 flex-wrap">
                <Link href={`/residents/${row.resident}`} className="text-sm font-medium text-indigo-600 hover:underline">View Resident</Link>
                <Link href={`/supervisors/${row.supervisor}`} className="text-sm font-medium text-indigo-600 hover:underline">View Supervisor</Link>
                {(user?.role === 'ADMIN' || user?.role === 'SUPERVISOR') && row.status === 'PENDING' && (
                  <>
                    <button onClick={() => mark(row.id, 'DONE')} className="pg-btn-success">Mark Done</button>
                    <button onClick={() => mark(row.id, 'DISMISSED')} className="pg-btn-warning">Dismiss</button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
