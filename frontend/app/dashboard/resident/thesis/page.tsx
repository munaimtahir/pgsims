'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

import { trainingApi, ResidentThesis } from '@/lib/api/training';

function getErrorMessage(error: unknown, fallback = 'Submission failed.'): string {
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

export default function ResidentThesisPage() {
  const [thesis, setThesis] = useState<ResidentThesis | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const load = () => {
    setLoading(true);
    trainingApi.getMyThesis()
      .then(setThesis)
      .catch(() => setThesis(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    setError('');
    try {
      const t = await trainingApi.createThesis();
      setThesis(t);
    } catch {
      setError('Failed to create thesis record.');
    }
  };

  const handleSubmit = async () => {
    setActionLoading(true);
    setError('');
    setSuccess('');
    try {
      const t = await trainingApi.submitThesis();
      setThesis(t);
      setSuccess('Thesis submitted successfully.');
    } catch (error: unknown) {
      setError(getErrorMessage(error));
    } finally {
      setActionLoading(false);
    }
  };

  const STATUS_COLOR: Record<string, string> = {
    not_started: 'bg-gray-100 text-gray-600',
    in_progress: 'bg-yellow-100 text-yellow-800',
    submitted: 'bg-green-100 text-green-800',
  };

  return (
    <ProtectedRoute allowedRoles={['resident', 'pg']}>
        <div className="max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Thesis</h1>

          {loading && <p className="text-gray-500">Loading…</p>}
          {error && <p className="text-red-600 mb-4">{error}</p>}
          {success && <p className="text-green-600 mb-4">{success}</p>}

          {!loading && !thesis && (
            <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
              <p className="text-gray-500 mb-4">No thesis record found.</p>
              <button
                onClick={handleCreate}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Create Thesis Record
              </button>
            </div>
          )}

          {thesis && (
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Thesis Record</h2>
                <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[thesis.status] || 'bg-gray-100 text-gray-600'}`}>
                  {thesis.status_display}
                </span>
              </div>

              {thesis.submitted_at && (
                <p className="text-sm text-gray-600 mb-2">
                  Submitted: {new Date(thesis.submitted_at).toLocaleDateString()}
                </p>
              )}
              {thesis.final_submission_ref && (
                <p className="text-sm text-gray-600 mb-2">
                  Reference: {thesis.final_submission_ref}
                </p>
              )}
              {thesis.notes && (
                <p className="text-sm text-gray-500 mb-4">{thesis.notes}</p>
              )}

              {thesis.status !== 'submitted' && (
                <button
                  disabled={actionLoading}
                  onClick={handleSubmit}
                  className="mt-4 px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 disabled:opacity-50"
                >
                  {actionLoading ? 'Submitting…' : 'Submit Thesis'}
                </button>
              )}
            </div>
          )}
        </div>
    </ProtectedRoute>
  );
}
