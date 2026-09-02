'use client';

import { FormEvent, useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicOptions, RotationTemplate } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function RotationTemplatesPage() {
  const { user } = useAuthStore();
  const canManage = user?.role === 'ADMIN';
  const [rows, setRows] = useState<RotationTemplate[]>([]);
  const [options, setOptions] = useState<AcademicOptions | null>(null);
  const [form, setForm] = useState({ name: '', code: '', program: '', department: '', training_year: '', duration_weeks: '' });
  const load = () => {
    academicsApi.listRotationTemplates().then(setRows).catch(() => setRows([]));
    academicsApi.getOptions().then(setOptions).catch(() => setOptions(null));
  };
  useEffect(() => { load(); }, []);
  const createItem = async (event: FormEvent) => {
    event.preventDefault();
    await academicsApi.createRotationTemplate({
      name: form.name,
      code: form.code,
      program: form.program ? Number(form.program) : null,
      department: form.department ? Number(form.department) : null,
      training_year: form.training_year ? Number(form.training_year) : null,
      duration_weeks: form.duration_weeks ? Number(form.duration_weeks) : null,
      description: 'Scaffold only. Resident rotation scheduling will be added later.',
    });
    setForm({ name: '', code: '', program: '', department: '', training_year: '', duration_weeks: '' });
    load();
  };
  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader title="Rotation Templates" description="Scaffold only. Resident rotation scheduling will be added later." />
        {canManage && options && (
          <form onSubmit={createItem} className="pg-card grid gap-3 md:grid-cols-3">
            <input className="pg-form-input" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <input className="pg-form-input" placeholder="Code" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} required />
            <select className="pg-form-input" value={form.program} onChange={(e) => setForm({ ...form, program: e.target.value })}><option value="">Program</option>{options.programs.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select>
            <select className="pg-form-input" value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })}><option value="">Department</option>{options.departments.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select>
            <input className="pg-form-input" type="number" min="1" placeholder="Training year" value={form.training_year} onChange={(e) => setForm({ ...form, training_year: e.target.value })} />
            <input className="pg-form-input" type="number" min="1" placeholder="Duration weeks" value={form.duration_weeks} onChange={(e) => setForm({ ...form, duration_weeks: e.target.value })} />
            <button className="pg-btn-primary md:col-span-3" type="submit">Create Rotation Template</button>
          </form>
        )}
        <div className="space-y-3">{rows.map((row) => <div key={row.id} className="pg-card"><p className="font-semibold">{row.name}</p><p className="text-sm text-slate-600">{row.program_name || 'All programs'} · {row.department_name || 'All departments'}</p></div>)}</div>
      </div>
    </ProtectedRoute>
  );
}
