'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { trainingApi, TrainingProgram, ProgramPolicy, ProgramMilestone } from '@/lib/api/training';

type Tab = 'overview' | 'policy' | 'milestones';

export default function UTRMCProgramsPage() {
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [selected, setSelected] = useState<TrainingProgram | null>(null);
  const [policy, setPolicy] = useState<ProgramPolicy | null>(null);
  const [milestones, setMilestones] = useState<ProgramMilestone[]>([]);
  const [tab, setTab] = useState<Tab>('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [policyForm, setPolicyForm] = useState<Partial<ProgramPolicy>>({});
  const [savingPolicy, setSavingPolicy] = useState(false);

  useEffect(() => {
    trainingApi.listPrograms()
      .then(setPrograms)
      .catch(() => setError('Failed to load programs.'))
      .finally(() => setLoading(false));
  }, []);

  const selectProgram = async (p: TrainingProgram) => {
    setSelected(p);
    setTab('overview');
    setPolicy(null);
    setMilestones([]);
    const [pol, mils] = await Promise.allSettled([
      trainingApi.getProgramPolicy(p.id),
      trainingApi.listMilestones(p.id),
    ]);
    if (pol.status === 'fulfilled') { setPolicy(pol.value); setPolicyForm(pol.value); }
    if (mils.status === 'fulfilled') setMilestones(mils.value);
  };

  const savePolicy = async () => {
    if (!selected) return;
    setSavingPolicy(true);
    try {
      const updated = await trainingApi.updateProgramPolicy(selected.id, policyForm);
      setPolicy(updated);
      setPolicyForm(updated);
    } catch {
      setError('Failed to save policy.');
    } finally {
      setSavingPolicy(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
      <DashboardLayout>
        <div className="flex gap-6">
          {/* Program list */}
          <div className="w-64 flex-shrink-0">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Programmes</h2>
            {loading && <p className="text-gray-400 text-sm">Loading…</p>}
            <ul className="space-y-1">
              {programs.map((p) => (
                <li key={p.id}>
                  <button
                    onClick={() => selectProgram(p)}
                    className={`w-full text-left px-3 py-2 rounded-md text-sm ${
                      selected?.id === p.id
                        ? 'bg-indigo-50 text-indigo-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <span className="font-mono text-xs text-gray-400 block">{p.code}</span>
                    {p.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Detail pane */}
          <div className="flex-1">
            {!selected && (
              <div className="text-center text-gray-400 mt-20">
                <p>Select a programme to view details.</p>
              </div>
            )}

            {selected && (
              <>
                <h1 className="text-2xl font-bold text-gray-900 mb-1">{selected.name}</h1>
                <p className="text-gray-500 text-sm mb-4">
                  {selected.code} · {selected.degree_type_display} · {selected.duration_months} months
                </p>
                {error && <p className="text-red-600 mb-3">{error}</p>}

                {/* Tabs */}
                <div className="flex gap-1 border-b border-gray-200 mb-6">
                  {(['overview', 'policy', 'milestones'] as Tab[]).map((t) => (
                    <button
                      key={t}
                      onClick={() => setTab(t)}
                      className={`px-4 py-2 text-sm capitalize ${
                        tab === t
                          ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium'
                          : 'text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>

                {/* Overview Tab */}
                {tab === 'overview' && (
                  <div className="space-y-2">
                    <p className="text-sm text-gray-700"><span className="font-medium">Code:</span> {selected.code}</p>
                    <p className="text-sm text-gray-700"><span className="font-medium">Duration:</span> {selected.duration_months} months</p>
                    <p className="text-sm text-gray-700"><span className="font-medium">Active:</span> {selected.is_active ? 'Yes' : 'No'}</p>
                    {selected.notes && <p className="text-sm text-gray-500">{selected.notes}</p>}
                  </div>
                )}

                {/* Policy Tab */}
                {tab === 'policy' && policy && (
                  <div className="bg-white border border-gray-200 rounded-lg p-5 space-y-4">
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={policyForm.allow_program_change ?? false}
                        onChange={(e) => setPolicyForm({ ...policyForm, allow_program_change: e.target.checked })}
                        id="allow_prog"
                      />
                      <label htmlFor="allow_prog" className="text-sm text-gray-700">Allow program change</label>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">iMM allowed from month</label>
                      <input
                        type="number"
                        value={policyForm.imm_allowed_from_month ?? ''}
                        onChange={(e) => setPolicyForm({ ...policyForm, imm_allowed_from_month: e.target.value ? Number(e.target.value) : null })}
                        className="mt-1 w-32 border border-gray-300 rounded-md px-3 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Final allowed from month</label>
                      <input
                        type="number"
                        value={policyForm.final_allowed_from_month ?? ''}
                        onChange={(e) => setPolicyForm({ ...policyForm, final_allowed_from_month: e.target.value ? Number(e.target.value) : null })}
                        className="mt-1 w-32 border border-gray-300 rounded-md px-3 py-1.5 text-sm"
                      />
                    </div>
                    <button
                      disabled={savingPolicy}
                      onClick={savePolicy}
                      className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50"
                    >
                      {savingPolicy ? 'Saving…' : 'Save Policy'}
                    </button>
                  </div>
                )}

                {/* Milestones Tab */}
                {tab === 'milestones' && (
                  <div className="space-y-4">
                    {milestones.length === 0 && (
                      <p className="text-sm text-gray-500">No milestones configured.</p>
                    )}
                    {milestones.map((m) => (
                      <div key={m.id} className="bg-white border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900">{m.name}</h3>
                          <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded font-mono">{m.code}</span>
                        </div>
                        {m.recommended_month && (
                          <p className="text-sm text-gray-500 mt-1">Recommended month: {m.recommended_month}</p>
                        )}
                        {m.research_requirement && (
                          <div className="mt-2 text-xs text-gray-500 space-y-0.5">
                            {m.research_requirement.requires_synopsis_approved && <p>✓ Synopsis approval required</p>}
                            {m.research_requirement.requires_thesis_submitted && <p>✓ Thesis submission required</p>}
                          </div>
                        )}
                        {m.workshop_requirements.length > 0 && (
                          <div className="mt-2 text-xs text-gray-500">
                            Workshops: {m.workshop_requirements.map((w) => w.workshop_name).join(', ')}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
