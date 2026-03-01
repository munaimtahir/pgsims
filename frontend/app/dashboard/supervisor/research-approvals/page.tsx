'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { trainingApi, ResidentResearchProject } from '@/lib/api/training';

export default function SupervisorResearchApprovalsPage() {
  const [projects, setProjects] = useState<ResidentResearchProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [feedback, setFeedback] = useState<Record<number, string>>({});
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const load = () => {
    setLoading(true);
    trainingApi.getSupervisorResearchApprovals()
      .then((data) => setProjects(Array.isArray(data) ? data : []))
      .catch(() => setError('Failed to load research approvals.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleApprove = async (project: ResidentResearchProject) => {
    setActionLoading(project.id);
    setError('');
    try {
      await trainingApi.supervisorApproveResearch(project.id, feedback[project.id]);
      load();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Approval failed.');
    } finally {
      setActionLoading(null);
    }
  };

  const pending = projects.filter((p) => p.status === 'submitted_to_supervisor');
  const others = projects.filter((p) => p.status !== 'submitted_to_supervisor');

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty']}>
      <DashboardLayout>
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Research Approvals</h1>

          {loading && <p className="text-gray-500">Loading…</p>}
          {error && <p className="text-red-600 mb-4">{error}</p>}

          {/* Pending section */}
          <section className="mb-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-3">
              Awaiting Approval <span className="ml-2 text-sm font-normal text-gray-500">({pending.length})</span>
            </h2>
            {!loading && pending.length === 0 && (
              <p className="text-sm text-gray-500">No submissions awaiting review.</p>
            )}
            <div className="space-y-4">
              {pending.map((p) => (
                <div key={p.id} className="bg-white border border-indigo-200 rounded-lg p-5">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">{p.title}</h3>
                    <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                      Awaiting Review
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-1">Resident: {p.resident_name}</p>
                  {p.topic_area && <p className="text-sm text-gray-500 mb-3">Topic: {p.topic_area}</p>}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Feedback (optional)
                    </label>
                    <textarea
                      rows={2}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      placeholder="Provide feedback to the resident…"
                      value={feedback[p.id] || ''}
                      onChange={(e) => setFeedback({ ...feedback, [p.id]: e.target.value })}
                    />
                  </div>

                  <button
                    disabled={actionLoading === p.id}
                    onClick={() => handleApprove(p)}
                    className="mt-3 px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 disabled:opacity-50"
                  >
                    {actionLoading === p.id ? 'Approving…' : 'Approve Synopsis'}
                  </button>
                </div>
              ))}
            </div>
          </section>

          {/* Historical section */}
          {others.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Other Projects</h2>
              <div className="space-y-3">
                {others.map((p) => (
                  <div key={p.id} className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{p.title}</p>
                      <p className="text-sm text-gray-500">{p.resident_name} — {p.status_display}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
