'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { trainingApi, ResidentSummary } from '@/lib/api/training';

const STATUS_COLORS: Record<string, string> = {
  ACTIVE: 'bg-blue-100 text-blue-800',
  APPROVED: 'bg-green-100 text-green-800',
  SUBMITTED: 'bg-yellow-100 text-yellow-800',
  DRAFT: 'bg-gray-100 text-gray-600',
  COMPLETED: 'bg-slate-100 text-slate-600',
  RETURNED: 'bg-orange-100 text-orange-700',
  REJECTED: 'bg-red-100 text-red-700',
};

function StatusBadge({ status }: { status: string }) {
  const cls = STATUS_COLORS[status] || 'bg-gray-100 text-gray-600';
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{status}</span>;
}

const LEAVE_STATUS_COLORS: Record<string, string> = {
  APPROVED: 'bg-green-50 text-green-700',
  SUBMITTED: 'bg-yellow-50 text-yellow-700',
  DRAFT: 'bg-gray-50 text-gray-600',
  REJECTED: 'bg-red-50 text-red-700',
};

export default function ResidentSchedulePage() {
  const [summary, setSummary] = useState<ResidentSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    trainingApi.getResidentSummary()
      .then(setSummary)
      .catch(() => setError('Failed to load schedule'))
      .finally(() => setLoading(false));
  }, []);

  const allEvents = summary ? [
    ...summary.schedule.map(r => ({ ...r, kind: 'rotation' as const })),
    ...summary.leaves.list.map(l => ({ ...l, department: `Leave: ${l.leave_type}`, hospital: '', kind: 'leave' as const })),
  ].sort((a, b) => a.start_date.localeCompare(b.start_date)) : [];

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">My Schedule</h1>

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}

        {summary && (
          <>
            {/* Program info bar */}
            <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 mb-6 flex items-center gap-6 flex-wrap">
              <div>
                <span className="text-xs text-indigo-500 font-semibold uppercase tracking-wider">Program</span>
                <p className="font-semibold text-gray-900">{summary.training_record.program_name}</p>
              </div>
              <div>
                <span className="text-xs text-indigo-500 font-semibold uppercase tracking-wider">Started</span>
                <p className="font-semibold text-gray-900">{summary.training_record.start_date}</p>
              </div>
              <div>
                <span className="text-xs text-indigo-500 font-semibold uppercase tracking-wider">Month</span>
                <p className="font-semibold text-gray-900">{summary.training_record.current_month_index}</p>
              </div>
            </div>

            {allEvents.length === 0 ? (
              <div className="text-center py-16 text-gray-400">
                <p className="text-lg">No schedule entries yet.</p>
                <p className="text-sm mt-1">Rotations and leaves will appear here once assigned.</p>
              </div>
            ) : (
              <div className="relative pl-8">
                {/* Vertical timeline line */}
                <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-200" />

                <div className="space-y-3">
                  {allEvents.map((ev, idx) => (
                    <div key={`${ev.kind}-${ev.id}-${idx}`} className="relative">
                      {/* Timeline dot */}
                      <div className={`absolute -left-5 top-4 w-3 h-3 rounded-full border-2 border-white ${
                        ev.kind === 'rotation' ? 'bg-indigo-500' : 'bg-yellow-400'
                      }`} />

                      <div className={`rounded-xl border p-4 ${
                        ev.kind === 'rotation'
                          ? 'bg-white border-gray-200'
                          : 'bg-yellow-50 border-yellow-100'
                      }`}>
                        <div className="flex items-start justify-between gap-4 flex-wrap">
                          <div>
                            {ev.kind === 'rotation' ? (
                              <>
                                <p className="font-semibold text-gray-900">{(ev as any).department}</p>
                                <p className="text-sm text-gray-500">{(ev as any).hospital}</p>
                              </>
                            ) : (
                              <p className="font-semibold text-gray-700">{(ev as any).department}</p>
                            )}
                            <p className="text-xs text-gray-400 mt-1">
                              {ev.start_date} → {ev.end_date}
                            </p>
                          </div>
                          <div className="flex flex-col items-end gap-1.5">
                            <StatusBadge status={ev.status} />
                            <span className={`text-xs px-2 py-0.5 rounded ${
                              ev.kind === 'rotation' ? 'bg-indigo-50 text-indigo-600' : 'bg-yellow-100 text-yellow-700'
                            }`}>
                              {ev.kind === 'rotation' ? 'Rotation' : 'Leave'}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
