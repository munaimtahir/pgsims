'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { trainingApi, MilestoneEligibility, ResidentResearchProject } from '@/lib/api/training';

const STATUS_COLOR: Record<string, string> = {
  ELIGIBLE: 'bg-green-100 text-green-800',
  PARTIALLY_READY: 'bg-yellow-100 text-yellow-800',
  NOT_READY: 'bg-red-100 text-red-800',
};

export default function ResidentProgressPage() {
  const [eligibility, setEligibility] = useState<MilestoneEligibility[]>([]);
  const [research, setResearch] = useState<ResidentResearchProject | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      trainingApi.getMyEligibility(),
      trainingApi.getMyResearch(),
    ]).then(([eli, res]) => {
      if (eli.status === 'fulfilled') setEligibility(eli.value);
      if (res.status === 'fulfilled') setResearch(res.value);
    }).finally(() => setLoading(false));
  }, []);

  return (
    <ProtectedRoute allowedRoles={['resident', 'pg']}>
      <DashboardLayout>
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Academic Progress</h1>

          {loading && <p className="text-gray-500">Loading…</p>}

          {/* Research Status */}
          <section className="mb-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-3">Research Project</h2>
            {research ? (
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <p className="font-medium text-gray-900">{research.title}</p>
                <p className="text-sm text-gray-500 mt-1">
                  Status: <span className="font-semibold">{research.status_display}</span>
                </p>
                {research.topic_area && (
                  <p className="text-sm text-gray-500">Topic: {research.topic_area}</p>
                )}
              </div>
            ) : (
              !loading && (
                <p className="text-sm text-gray-500">
                  No research project yet.{' '}
                  <a href="/dashboard/resident/research" className="text-indigo-600 hover:underline">
                    Start one →
                  </a>
                </p>
              )
            )}
          </section>

          {/* Eligibility Snapshots */}
          <section>
            <h2 className="text-lg font-semibold text-gray-800 mb-3">Exam Eligibility</h2>
            {eligibility.length === 0 && !loading && (
              <p className="text-sm text-gray-500">No milestones configured for your programme yet.</p>
            )}
            <div className="space-y-4">
              {eligibility.map((e) => (
                <div key={e.id} className="bg-white border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900">{e.milestone_name} ({e.milestone_code})</h3>
                    <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[e.status] || 'bg-gray-100 text-gray-600'}`}>
                      {e.status_display}
                    </span>
                  </div>
                  {e.reasons.length > 0 && (
                    <ul className="mt-2 space-y-1">
                      {e.reasons.map((r, i) => (
                        <li key={i} className="text-sm text-red-600 flex items-start gap-1">
                          <span>✗</span> {r}
                        </li>
                      ))}
                    </ul>
                  )}
                  {e.reasons.length === 0 && e.status === 'ELIGIBLE' && (
                    <p className="text-sm text-green-600 mt-2">All requirements met.</p>
                  )}
                  <p className="text-xs text-gray-400 mt-2">Last computed: {new Date(e.computed_at).toLocaleString()}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
