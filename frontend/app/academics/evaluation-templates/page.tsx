'use client';

import { FormEvent, useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicOptions, EvaluationFormTemplate } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function EvaluationTemplatesPage() {
  const { user } = useAuthStore();
  const canManage = user?.role === 'ADMIN';
  const [rows, setRows] = useState<EvaluationFormTemplate[]>([]);
  const [options, setOptions] = useState<AcademicOptions | null>(null);
  const [form, setForm] = useState({ name: '', code: '', program: '', department: '', form_type: 'SUPERVISOR_REVIEW' });
  const load = () => {
    academicsApi.listEvaluationTemplates().then(setRows).catch(() => setRows([]));
    academicsApi.getOptions().then(setOptions).catch(() => setOptions(null));
  };
  useEffect(() => { load(); }, []);
  const createItem = async (event: FormEvent) => {
    event.preventDefault();
    await academicsApi.createEvaluationTemplate({
      ...form,
      program: form.program ? Number(form.program) : null,
      department: form.department ? Number(form.department) : null,
      schema: {},
      description: 'Template registry only. Evaluation submissions will be added later.',
    });
    setForm({ name: '', code: '', program: '', department: '', form_type: 'SUPERVISOR_REVIEW' });
    load();
  };
  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader title="Evaluation Templates" description="Template registry only. Evaluation submissions will be added later." />
        {canManage && options && (
          <form onSubmit={createItem} className="pg-card grid gap-3 md:grid-cols-3">
            <input className="pg-form-input" placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <input className="pg-form-input" placeholder="Code" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} required />
            <select className="pg-form-input" value={form.form_type} onChange={(e) => setForm({ ...form, form_type: e.target.value })}>{['SUPERVISOR_REVIEW', 'ROTATION_EVALUATION', 'CASE_BASED_DISCUSSION', 'MINI_CEX', 'DOPS', 'PROGRESS_REVIEW'].map((value) => <option key={value} value={value}>{value}</option>)}</select>
            <select className="pg-form-input" value={form.program} onChange={(e) => setForm({ ...form, program: e.target.value })}><option value="">Program</option>{options.programs.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select>
            <select className="pg-form-input" value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })}><option value="">Department</option>{options.departments.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select>
            <button className="pg-btn-primary md:col-span-3" type="submit">Create Evaluation Template</button>
          </form>
        )}
        <div className="space-y-3">{rows.map((row) => <div key={row.id} className="pg-card"><p className="font-semibold">{row.name}</p><p className="text-sm text-slate-600">{row.form_type} · {row.program_name || 'All programs'}</p></div>)}</div>
      </div>
    </ProtectedRoute>
  );
}
