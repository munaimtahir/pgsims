'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

import { trainingApi, ResidentResearchProject } from '@/lib/api/training';

const STATUS_LABELS: Record<string, string> = {
  draft: 'Draft',
  submitted_to_supervisor: 'Submitted to Supervisor',
  approved_by_supervisor: 'Approved by Supervisor',
  submitted_to_university: 'Submitted to University',
  accepted_by_university: 'Accepted',
};

export default function ResidentResearchPage() {
  const [project, setProject] = useState<ResidentResearchProject | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({ title: '', topic_area: '' });
  const [actionLoading, setActionLoading] = useState(false);

  const load = () => {
    setLoading(true);
    trainingApi.getMyResearch()
      .then(setProject)
      .catch(() => setProject(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const p = await trainingApi.createResearch(form);
      setProject(p);
      setCreating(false);
    } catch {
      setError('Failed to create research project.');
    }
  };

  const handleAction = async (action: string) => {
    setActionLoading(true);
    setError('');
    try {
      const p = await trainingApi.researchAction(action);
      setProject(p);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Action failed.');
    } finally {
      setActionLoading(false);
    }
  };

  const canSubmitToSupervisor = project?.status === 'draft';
  const canSubmitToUniversity = project?.status === 'approved_by_supervisor';

  return (
    <ProtectedRoute allowedRoles={['resident', 'pg']}>
        <div className="max-w-3xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Research Project</h1>

          {loading && <p className="text-gray-500">Loading…</p>}
          {error && <p className="text-red-600 mb-4">{error}</p>}

          {!loading && !project && !creating && (
            <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
              <p className="text-gray-500 mb-4">You have not started a research project yet.</p>
              <button
                onClick={() => setCreating(true)}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Start Research Project
              </button>
            </div>
          )}

          {creating && (
            <form onSubmit={handleCreate} className="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
              <h2 className="font-semibold text-gray-800">New Research Project</h2>
              <div>
                <label className="block text-sm font-medium text-gray-700">Title *</label>
                <input
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Topic Area</label>
                <input
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  value={form.topic_area}
                  onChange={(e) => setForm({ ...form, topic_area: e.target.value })}
                />
              </div>
              <div className="flex gap-3">
                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm">
                  Create
                </button>
                <button type="button" onClick={() => setCreating(false)} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900">
                  Cancel
                </button>
              </div>
            </form>
          )}

          {project && (
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">{project.title}</h2>
                <span className="text-xs bg-indigo-100 text-indigo-800 font-medium px-2 py-1 rounded-full">
                  {STATUS_LABELS[project.status] || project.status_display}
                </span>
              </div>

              {project.topic_area && (
                <p className="text-sm text-gray-600 mb-2">Topic: {project.topic_area}</p>
              )}
              {project.supervisor_name && (
                <p className="text-sm text-gray-600 mb-2">Supervisor: {project.supervisor_name}</p>
              )}
              {project.supervisor_feedback && (
                <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mb-4">
                  <p className="text-sm font-medium text-yellow-800">Supervisor Feedback</p>
                  <p className="text-sm text-yellow-700 mt-1">{project.supervisor_feedback}</p>
                </div>
              )}

              <div className="flex gap-3 mt-4">
                {canSubmitToSupervisor && (
                  <button
                    disabled={actionLoading}
                    onClick={() => handleAction('submit-to-supervisor')}
                    className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    Submit to Supervisor
                  </button>
                )}
                {canSubmitToUniversity && (
                  <button
                    disabled={actionLoading}
                    onClick={() => handleAction('submit-to-university')}
                    className="px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 disabled:opacity-50"
                  >
                    Submit to University
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
    </ProtectedRoute>
  );
}
