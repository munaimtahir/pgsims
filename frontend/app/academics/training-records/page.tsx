'use client';

import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicOptions, AcademicTrainingRecord } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

const EMPTY_FORM = {
  resident: '',
  program: '',
  academic_session: '',
  training_site: '',
  department: '',
  start_date: '',
  expected_end_date: '',
  training_year: '',
  notes: '',
};

export default function TrainingRecordsPage() {
  const { user } = useAuthStore();
  const canManage = user?.role === 'ADMIN';
  const [records, setRecords] = useState<AcademicTrainingRecord[]>([]);
  const [options, setOptions] = useState<AcademicOptions | null>(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [message, setMessage] = useState('');

  const load = () => {
    academicsApi.listTrainingRecords().then(setRecords).catch(() => setRecords([]));
    academicsApi.getOptions().then(setOptions).catch(() => setOptions(null));
  };

  useEffect(() => {
    load();
  }, []);

  const createRecord = async (event: FormEvent) => {
    event.preventDefault();
    await academicsApi.createTrainingRecord({
      resident: Number(form.resident),
      program: form.program ? Number(form.program) : null,
      academic_session: form.academic_session ? Number(form.academic_session) : null,
      training_site: form.training_site ? Number(form.training_site) : null,
      department: form.department ? Number(form.department) : null,
      start_date: form.start_date || null,
      expected_end_date: form.expected_end_date || null,
      training_year: form.training_year ? Number(form.training_year) : null,
      notes: form.notes,
    });
    setForm(EMPTY_FORM);
    setMessage('Training record created.');
    load();
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Training Records"
          description="One active academic training record per resident."
        />
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        {canManage && options && (
          <form onSubmit={createRecord} className="pg-card space-y-4">
            <div>
              <h2 className="pg-section-title">Create Training Record</h2>
              <p className="pg-section-note">Prefill from resident profile where possible.</p>
            </div>
            <div className="grid gap-3 md:grid-cols-3">
              <select className="pg-form-input" value={form.resident} onChange={(event) => setForm({ ...form, resident: event.target.value })} required>
                <option value="">Resident</option>
                {options.residents.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}
              </select>
              <select className="pg-form-input" value={form.program} onChange={(event) => setForm({ ...form, program: event.target.value })}>
                <option value="">Program</option>
                {options.programs.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}
              </select>
              <select className="pg-form-input" value={form.academic_session} onChange={(event) => setForm({ ...form, academic_session: event.target.value })}>
                <option value="">Academic Session</option>
                {options.academic_sessions.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}
              </select>
              <select className="pg-form-input" value={form.training_site} onChange={(event) => setForm({ ...form, training_site: event.target.value })}>
                <option value="">Training Site</option>
                {options.training_sites.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}
              </select>
              <select className="pg-form-input" value={form.department} onChange={(event) => setForm({ ...form, department: event.target.value })}>
                <option value="">Department</option>
                {options.departments.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}
              </select>
              <input className="pg-form-input" type="number" min="1" placeholder="Training year" value={form.training_year} onChange={(event) => setForm({ ...form, training_year: event.target.value })} />
              <input className="pg-form-input" type="date" value={form.start_date} onChange={(event) => setForm({ ...form, start_date: event.target.value })} />
              <input className="pg-form-input" type="date" value={form.expected_end_date} onChange={(event) => setForm({ ...form, expected_end_date: event.target.value })} />
              <input className="pg-form-input md:col-span-3" placeholder="Notes" value={form.notes} onChange={(event) => setForm({ ...form, notes: event.target.value })} />
            </div>
            <button className="pg-btn-primary" type="submit">Create Record</button>
          </form>
        )}

        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
              <tr>
                {['Resident', 'Program', 'Session', 'Year', 'Status', 'Actions'].map((header) => (
                  <th key={header} className="px-4 py-3 text-left">{header}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {records.map((record) => (
                <tr key={record.id}>
                  <td className="px-4 py-3 font-medium text-slate-900">{record.resident_name}</td>
                  <td className="px-4 py-3">{record.program_name || '—'}</td>
                  <td className="px-4 py-3">{record.academic_session_name || '—'}</td>
                  <td className="px-4 py-3">{record.training_year || '—'}</td>
                  <td className="px-4 py-3">{record.status}</td>
                  <td className="px-4 py-3">
                    <Link href={`/academics/training-records/${record.id}`} className="text-sm font-medium text-indigo-600 hover:underline">
                      Open
                    </Link>
                  </td>
                </tr>
              ))}
              {records.length === 0 && (
                <tr>
                  <td className="px-4 py-6 text-sm text-slate-500" colSpan={6}>No training records found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </ProtectedRoute>
  );
}
