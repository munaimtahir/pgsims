'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { trainingApi, ResidentResearchProject } from '@/lib/api/training';

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, string> = {
    SUBMITTED_TO_SUPERVISOR: 'bg-yellow-100 text-yellow-800',
    APPROVED_BY_SUPERVISOR: 'bg-green-100 text-green-800',
    SUBMITTED_TO_UNIVERSITY: 'bg-blue-100 text-blue-700',
    DRAFT: 'bg-gray-100 text-gray-600',
  };
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${map[status] || 'bg-gray-100 text-gray-600'}`}>{status.replace(/_/g, ' ')}</span>;
}

export default function ResearchApprovalsPage() {
  const [items, setItems] = useState<ResidentResearchProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [feedback, setFeedback] = useState<Record<number, string>>({});
  const [returnOpen, setReturnOpen] = useState<number | null>(null);
  const [processing, setProcessing] = useState<number | null>(null);
  const [msg, setMsg] = useState('');

  const load = () => {
    trainingApi.getSupervisorResearchApprovals()
      .then(setItems)
      .catch(() => setError('Failed to load research approvals'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const flash = (m: string) => { setMsg(m); setTimeout(() => setMsg(''), 3000); };

  const approve = async (id: number) => {
    setProcessing(id);
    try {
      await trainingApi.supervisorApproveResearch(id);
      flash('Approved ✓');
      load();
    } catch { flash('Error approving'); } finally { setProcessing(null); }
  };

  const returnProject = async (id: number) => {
    const reason = feedback[id];
    if (!reason?.trim()) return;
    setProcessing(id);
    try {
      await trainingApi.supervisorReturnResearch(id, reason);
      flash('Returned with feedback');
      setReturnOpen(null);
      setFeedback(f => { const c = { ...f }; delete c[id]; return c; });
      load();
    } catch { flash('Error returning'); } finally { setProcessing(null); }
  };

  const pending = items.filter(i => i.status === 'SUBMITTED_TO_SUPERVISOR');
  const other = items.filter(i => i.status !== 'SUBMITTED_TO_SUPERVISOR');

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Research Approvals</h1>

        {msg && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-3 text-sm">{msg}</div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">{error}</div>}

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}

        {!loading && (
          <>
            {pending.length === 0 && <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-gray-200">No pending research submissions.</div>}
            {pending.length > 0 && (
              <div className="space-y-4 mb-8">
                <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wider">Pending Review ({pending.length})</h2>
                {pending.map(p => (
                  <div key={p.id} className="bg-white border border-yellow-200 rounded-xl p-5 shadow-sm">
                    <div className="flex items-start justify-between gap-4 flex-wrap">
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-gray-900">{p.title}</p>
                        <p className="text-sm text-gray-500 mt-0.5">Topic: {p.topic_area || '—'}</p>
                        <p className="text-xs text-gray-400 mt-1">Resident ID: {p.resident}</p>
                        {p.synopsis_file && (
                          <a href={p.synopsis_file} target="_blank" rel="noreferrer"
                            className="inline-block mt-2 text-xs text-indigo-600 underline">📄 View Synopsis</a>
                        )}
                      </div>
                      <StatusBadge status={p.status} />
                    </div>

                    <div className="mt-4 flex flex-wrap gap-2 items-center">
                      <button
                        onClick={() => approve(p.id)}
                        disabled={processing === p.id}
                        className="px-4 py-1.5 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50">
                        {processing === p.id ? 'Processing…' : 'Approve'}
                      </button>
                      <button
                        onClick={() => setReturnOpen(returnOpen === p.id ? null : p.id)}
                        className="px-4 py-1.5 bg-orange-50 border border-orange-300 text-orange-700 rounded-lg text-sm font-medium hover:bg-orange-100">
                        Return with Feedback
                      </button>
                    </div>

                    {returnOpen === p.id && (
                      <div className="mt-3 space-y-2">
                        <textarea
                          value={feedback[p.id] || ''}
                          onChange={e => setFeedback(f => ({ ...f, [p.id]: e.target.value }))}
                          rows={3}
                          placeholder="Provide feedback reason (required)…"
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                        />
                        <button
                          onClick={() => returnProject(p.id)}
                          disabled={!feedback[p.id]?.trim() || processing === p.id}
                          className="px-4 py-1.5 bg-orange-600 text-white rounded-lg text-sm font-medium hover:bg-orange-700 disabled:opacity-50">
                          {processing === p.id ? 'Sending…' : 'Send Return'}
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {other.length > 0 && (
              <div>
                <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wider mb-3">Previously Reviewed</h2>
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
                      <tr>
                        <th className="px-4 py-3 text-left">Title</th>
                        <th className="px-4 py-3 text-left">Topic</th>
                        <th className="px-4 py-3 text-left">Status</th>
                        <th className="px-4 py-3 text-left">Synopsis</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {other.map(p => (
                        <tr key={p.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 font-medium text-gray-800">{p.title}</td>
                          <td className="px-4 py-3 text-gray-600">{p.topic_area || '—'}</td>
                          <td className="px-4 py-3"><StatusBadge status={p.status} /></td>
                          <td className="px-4 py-3">
                            {p.synopsis_file ? <a href={p.synopsis_file} target="_blank" rel="noreferrer" className="text-indigo-600 underline text-xs">View</a> : '—'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
