'use client';

import { FormEvent, useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import supervisionApi, { SupervisionAssignment } from '@/lib/api/supervision';

export default function SupervisionAssignmentDetailPage() {
  const params = useParams();
  const id = Number(params.id);
  const [assignment, setAssignment] = useState<SupervisionAssignment | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [form, setForm] = useState({ end_date: '', reason_for_change: '' });

  useEffect(() => {
    if (!id) return;
    supervisionApi.getAssignment(id)
      .then(setAssignment)
      .catch(() => setError('Unable to load assignment.'))
      .finally(() => setLoading(false));
  }, [id]);

  const endAssignment = async (event: FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError('');
    setMessage('');
    try {
      const next = await supervisionApi.endAssignment(id, form);
      setAssignment(next);
      setMessage('Assignment ended.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to end assignment.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page max-w-4xl">
        <PageHeader
          title={`Assignment ${id}`}
          description="Assignment detail and closure controls."
          actions={<Link href="/supervision/assignments" className="pg-btn-primary">Back</Link>}
        />
        {loading && <p className="text-sm text-slate-500">Loading assignment...</p>}
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-700">{message}</div>}

        {assignment && (
          <div className="space-y-4">
            <section className="pg-card">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">{assignment.resident?.name}</h2>
                  <p className="text-sm text-slate-600">Supervisor: {assignment.supervisor?.name}</p>
                  <p className="text-sm text-slate-600">Type: {assignment.assignment_type}</p>
                  <p className="text-sm text-slate-600">Start: {assignment.start_date || '—'}</p>
                </div>
                <WorkflowStatusBadge status={assignment.status} />
              </div>
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-slate-600">
                <p>Email: {assignment.supervisor?.email || '—'}</p>
                <p>Phone: {assignment.supervisor?.phone || '—'}</p>
                <p>Department: {assignment.supervisor?.department || '—'}</p>
                <p>Training site: {assignment.supervisor?.training_site || '—'}</p>
              </div>
            </section>

            {assignment.status === 'ACTIVE' && (
              <form onSubmit={endAssignment} className="pg-card space-y-4">
                <h3 className="text-base font-semibold text-slate-900">End Assignment</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="pg-form-label" htmlFor="end_date">End Date</label>
                    <input id="end_date" type="date" className="pg-form-input" value={form.end_date} onChange={(event) => setForm({ ...form, end_date: event.target.value })} required />
                  </div>
                  <div>
                    <label className="pg-form-label" htmlFor="reason_for_change">Reason</label>
                    <input id="reason_for_change" className="pg-form-input" value={form.reason_for_change} onChange={(event) => setForm({ ...form, reason_for_change: event.target.value })} />
                  </div>
                </div>
                <button type="submit" disabled={saving} className="pg-btn-primary">
                  {saving ? 'Ending...' : 'End Assignment'}
                </button>
              </form>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
