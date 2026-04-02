'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

import { trainingApi, WorkshopCompletion, Workshop } from '@/lib/api/training';

function getErrorMessage(error: unknown, fallback = 'Failed to save.'): string {
  if (
    typeof error === 'object' &&
    error !== null &&
    'response' in error &&
    typeof (error as { response?: unknown }).response === 'object' &&
    (error as { response?: unknown }).response !== null &&
    'data' in ((error as { response?: { data?: unknown } }).response || {}) &&
    typeof ((error as { response?: { data?: { detail?: unknown } } }).response?.data?.detail) === 'string'
  ) {
    return (error as { response?: { data?: { detail?: string } } }).response?.data?.detail || fallback;
  }
  return fallback;
}

export default function ResidentWorkshopsPage() {
  const [completions, setCompletions] = useState<WorkshopCompletion[]>([]);
  const [workshops, setWorkshops] = useState<Workshop[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ workshop: '', completed_at: '' });
  const [saving, setSaving] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.allSettled([
      trainingApi.listMyWorkshopCompletions(),
      trainingApi.listWorkshops(),
    ]).then(([comp, ws]) => {
      if (comp.status === 'fulfilled') setCompletions(comp.value.results);
      if (ws.status === 'fulfilled') setWorkshops(ws.value);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.workshop || !form.completed_at) return;
    setSaving(true);
    setError('');
    try {
      await trainingApi.createWorkshopCompletion({
        workshop: Number(form.workshop),
        completed_at: form.completed_at,
      });
      setShowForm(false);
      setForm({ workshop: '', completed_at: '' });
      load();
    } catch (error: unknown) {
      setError(getErrorMessage(error));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Remove this completion record?')) return;
    try {
      await trainingApi.deleteWorkshopCompletion(id);
      setCompletions((prev) => prev.filter((c) => c.id !== id));
    } catch {
      setError('Failed to delete.');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['resident', 'pg']}>
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Workshops</h1>
            <button
              onClick={() => setShowForm(true)}
              className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700"
            >
              + Record Completion
            </button>
          </div>

          {loading && <p className="text-gray-500">Loading…</p>}
          {error && <p className="text-red-600 mb-4">{error}</p>}

          {showForm && (
            <form onSubmit={handleAdd} className="bg-white border border-gray-200 rounded-lg p-4 mb-6 space-y-3">
              <h2 className="font-semibold text-gray-800">Record Workshop Completion</h2>
              <div>
                <label className="block text-sm font-medium text-gray-700">Workshop *</label>
                <select
                  required
                  value={form.workshop}
                  onChange={(e) => setForm({ ...form, workshop: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                >
                  <option value="">Select workshop…</option>
                  {workshops.map((w) => (
                    <option key={w.id} value={w.id}>{w.name} ({w.code})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Completion Date *</label>
                <input
                  required
                  type="date"
                  value={form.completed_at}
                  onChange={(e) => setForm({ ...form, completed_at: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                />
              </div>
              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {saving ? 'Saving…' : 'Save'}
                </button>
                <button type="button" onClick={() => setShowForm(false)} className="text-sm text-gray-600 hover:text-gray-900">
                  Cancel
                </button>
              </div>
            </form>
          )}

          {!loading && completions.length === 0 && (
            <p className="text-gray-500 text-sm">No workshop completions recorded yet.</p>
          )}

          <div className="space-y-3">
            {completions.map((c) => (
              <div key={c.id} className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{c.workshop_name}</p>
                  <p className="text-sm text-gray-500">
                    Completed: {new Date(c.completed_at).toLocaleDateString()}
                    {c.source === 'manual_upload' && (
                      <span className="ml-2 text-xs bg-gray-100 text-gray-500 px-1 py-0.5 rounded">Manual</span>
                    )}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(c.id)}
                  className="text-red-400 hover:text-red-600 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
    </ProtectedRoute>
  );
}
