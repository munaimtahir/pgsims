'use client';

import { FormEvent, useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicOptions, AcademicPeriod } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function AcademicPeriodsPage() {
  const { user } = useAuthStore();
  const canManage = user?.role === 'ADMIN';
  const [rows, setRows] = useState<AcademicPeriod[]>([]);
  const [options, setOptions] = useState<AcademicOptions | null>(null);
  const [form, setForm] = useState({ name: '', code: '', academic_session: '', start_date: '', end_date: '', period_type: 'CUSTOM' });

  const load = () => {
    academicsApi.listPeriods().then(setRows).catch(() => setRows([]));
    academicsApi.getOptions().then(setOptions).catch(() => setOptions(null));
  };
  useEffect(() => { load(); }, []);

  const createItem = async (event: FormEvent) => {
    event.preventDefault();
    await academicsApi.createPeriod({
      ...form,
      academic_session: form.academic_session ? Number(form.academic_session) : null,
      sort_order: rows.length + 1,
    });
    setForm({ name: '', code: '', academic_session: '', start_date: '', end_date: '', period_type: 'CUSTOM' });
    load();
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader title="Academic Periods" description="CRUD registry for academic and reporting periods." />
        {canManage && options && (
          <form onSubmit={createItem} className="pg-card grid gap-3 md:grid-cols-3">
            <input className="pg-form-input" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <input className="pg-form-input" placeholder="Code" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} required />
            <select className="pg-form-input" value={form.academic_session} onChange={(e) => setForm({ ...form, academic_session: e.target.value })}>
              <option value="">Academic Session</option>
              {options.academic_sessions.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}
            </select>
            <input className="pg-form-input" type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} required />
            <input className="pg-form-input" type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} required />
            <select className="pg-form-input" value={form.period_type} onChange={(e) => setForm({ ...form, period_type: e.target.value })}>
              {['YEAR', 'TERM', 'QUARTER', 'MONTH', 'CUSTOM'].map((value) => <option key={value} value={value}>{value}</option>)}
            </select>
            <button className="pg-btn-primary md:col-span-3" type="submit">Create Period</button>
          </form>
        )}
        <div className="space-y-3">
          {rows.map((row) => (
            <div key={row.id} className="pg-card">
              <p className="font-semibold text-slate-900">{row.name}</p>
              <p className="text-sm text-slate-600">{row.code} · {row.period_type} · {row.start_date} to {row.end_date}</p>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
