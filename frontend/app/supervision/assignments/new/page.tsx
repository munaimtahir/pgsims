'use client';

import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import supervisionApi, { SupervisionOptions } from '@/lib/api/supervision';

export default function NewSupervisionAssignmentPage() {
  const [options, setOptions] = useState<SupervisionOptions | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [form, setForm] = useState({ resident_id: '', supervisor_id: '', assignment_type: 'PRIMARY', start_date: '' });

  useEffect(() => {
    supervisionApi.getSupervisionOptions()
      .then(setOptions)
      .catch(() => setError('Unable to load supervision options.'))
      .finally(() => setLoading(false));
  }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError('');
    setMessage('');
    try {
      const created = await supervisionApi.createAssignment({
        resident_id: Number(form.resident_id),
        supervisor_id: Number(form.supervisor_id),
        assignment_type: form.assignment_type as 'PRIMARY' | 'CO_SUPERVISOR',
        start_date: form.start_date,
      });
      setMessage(`Created assignment #${created.id}.`);
      setForm({ resident_id: '', supervisor_id: '', assignment_type: 'PRIMARY', start_date: '' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create assignment.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page max-w-3xl">
        <PageHeader
          title="New Assignment"
          description="Create a supervision assignment using the canonical supervision options endpoint."
          actions={<Link href="/supervision/assignments" className="pg-btn-primary">Back</Link>}
        />

        {loading && <p className="text-sm text-slate-500">Loading options...</p>}
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-700">{message}</div>}

        {!loading && (
          <form onSubmit={submit} className="pg-card space-y-4">
            <div>
              <label className="pg-form-label" htmlFor="resident">Resident</label>
              <select id="resident" className="pg-form-input bg-white" required value={form.resident_id} onChange={(event) => setForm({ ...form, resident_id: event.target.value })}>
                <option value="">Select resident</option>
                {(options?.residents || []).map((resident) => (
                  <option key={resident.id} value={resident.id}>{resident.name} ({resident.username})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="pg-form-label" htmlFor="supervisor">Supervisor</label>
              <select id="supervisor" className="pg-form-input bg-white" required value={form.supervisor_id} onChange={(event) => setForm({ ...form, supervisor_id: event.target.value })}>
                <option value="">Select supervisor</option>
                {(options?.supervisors || []).map((supervisor) => (
                  <option key={supervisor.id} value={supervisor.id}>{supervisor.name} ({supervisor.username})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="pg-form-label" htmlFor="assignment_type">Assignment Type</label>
                <select id="assignment_type" className="pg-form-input bg-white" value={form.assignment_type} onChange={(event) => setForm({ ...form, assignment_type: event.target.value })}>
                  <option value="PRIMARY">PRIMARY</option>
                  <option value="CO_SUPERVISOR">CO_SUPERVISOR</option>
                </select>
              </div>
              <div>
                <label className="pg-form-label" htmlFor="start_date">Start Date</label>
                <input id="start_date" type="date" className="pg-form-input" required value={form.start_date} onChange={(event) => setForm({ ...form, start_date: event.target.value })} />
              </div>
            </div>

            <button type="submit" disabled={saving} className="pg-btn-primary">
              {saving ? 'Saving...' : 'Create Assignment'}
            </button>
          </form>
        )}
      </div>
    </ProtectedRoute>
  );
}
