'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

import { trainingApi, TrainingProgram, ProgramPolicy, ProgramMilestone, ProgramRotationTemplate } from '@/lib/api/training';

type Tab = 'overview' | 'policy' | 'milestones' | 'templates';

export default function UTRMCProgramsPage() {
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [selected, setSelected] = useState<TrainingProgram | null>(null);
  const [policy, setPolicy] = useState<ProgramPolicy | null>(null);
  const [milestones, setMilestones] = useState<ProgramMilestone[]>([]);
  const [templates, setTemplates] = useState<ProgramRotationTemplate[]>([]);
  const [tab, setTab] = useState<Tab>('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [policyForm, setPolicyForm] = useState<Partial<ProgramPolicy>>({});
  const [savingPolicy, setSavingPolicy] = useState(false);
  const [showTemplateForm, setShowTemplateForm] = useState(false);
  const [templateForm, setTemplateForm] = useState({ name: '', department: '', duration_weeks: '4', required: true, sequence_order: '1' });
  const [savingTemplate, setSavingTemplate] = useState(false);

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
    setTemplates([]);
    const [pol, mils, tmpl] = await Promise.allSettled([
      trainingApi.getProgramPolicy(p.id),
      trainingApi.listMilestones(p.id),
      trainingApi.listProgramTemplates(p.id),
    ]);
    if (pol.status === 'fulfilled') { setPolicy(pol.value); setPolicyForm(pol.value); }
    if (mils.status === 'fulfilled') setMilestones(mils.value);
    if (tmpl.status === 'fulfilled') setTemplates(tmpl.value);
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

  const addTemplate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selected) return;
    setSavingTemplate(true);
    try {
      const created = await trainingApi.createProgramTemplate({
        program: selected.id,
        name: templateForm.name,
        department: templateForm.department ? Number(templateForm.department) : undefined,
        duration_weeks: Number(templateForm.duration_weeks),
        required: templateForm.required,
        sequence_order: Number(templateForm.sequence_order),
      });
      setTemplates((prev) => [...prev, created]);
      setShowTemplateForm(false);
      setTemplateForm({ name: '', department: '', duration_weeks: '4', required: true, sequence_order: String(templates.length + 2) });
    } catch {
      setError('Failed to add template.');
    } finally {
      setSavingTemplate(false);
    }
  };

  const deleteTemplate = async (id: number) => {
    if (!confirm('Delete this rotation template?')) return;
    try {
      await trainingApi.deleteProgramTemplate(id);
      setTemplates((prev) => prev.filter((t) => t.id !== id));
    } catch {
      setError('Failed to delete template.');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
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
                  {(['overview', 'policy', 'milestones', 'templates'] as Tab[]).map((t) => (
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
                {/* Templates Tab */}
                {tab === 'templates' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <p className="text-sm text-gray-500">Rotation schedule templates define the sequence of rotations for this programme.</p>
                      <button
                        onClick={() => { setShowTemplateForm(true); setTemplateForm({ name: '', department: '', duration_weeks: '4', required: true, sequence_order: String(templates.length + 1) }); }}
                        className="px-3 py-1.5 bg-indigo-600 text-white text-xs font-medium rounded-lg hover:bg-indigo-700"
                      >
                        + Add Template
                      </button>
                    </div>

                    {showTemplateForm && (
                      <form onSubmit={addTemplate} className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 space-y-3">
                        <h3 className="text-sm font-semibold text-indigo-800">New Rotation Template</h3>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Template Name *</label>
                            <input
                              required
                              type="text"
                              value={templateForm.name}
                              onChange={(e) => setTemplateForm({ ...templateForm, name: e.target.value })}
                              placeholder="e.g. Internal Medicine Block"
                              className="w-full border border-gray-300 rounded-md px-2.5 py-1.5 text-sm"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Department ID</label>
                            <input
                              type="number"
                              value={templateForm.department}
                              onChange={(e) => setTemplateForm({ ...templateForm, department: e.target.value })}
                              placeholder="Department ID"
                              className="w-full border border-gray-300 rounded-md px-2.5 py-1.5 text-sm"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Duration (weeks) *</label>
                            <input
                              required
                              type="number"
                              min={1}
                              value={templateForm.duration_weeks}
                              onChange={(e) => setTemplateForm({ ...templateForm, duration_weeks: e.target.value })}
                              className="w-full border border-gray-300 rounded-md px-2.5 py-1.5 text-sm"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Sequence Order *</label>
                            <input
                              required
                              type="number"
                              min={1}
                              value={templateForm.sequence_order}
                              onChange={(e) => setTemplateForm({ ...templateForm, sequence_order: e.target.value })}
                              className="w-full border border-gray-300 rounded-md px-2.5 py-1.5 text-sm"
                            />
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            id="tmpl_required"
                            checked={templateForm.required}
                            onChange={(e) => setTemplateForm({ ...templateForm, required: e.target.checked })}
                          />
                          <label htmlFor="tmpl_required" className="text-xs text-gray-700">Required rotation</label>
                        </div>
                        <div className="flex gap-2">
                          <button type="submit" disabled={savingTemplate} className="px-3 py-1.5 bg-indigo-600 text-white text-xs rounded-md hover:bg-indigo-700 disabled:opacity-50">
                            {savingTemplate ? 'Saving…' : 'Add'}
                          </button>
                          <button type="button" onClick={() => setShowTemplateForm(false)} className="text-xs text-gray-500 hover:text-gray-700">Cancel</button>
                        </div>
                      </form>
                    )}

                    {templates.length === 0 && !showTemplateForm && (
                      <p className="text-sm text-gray-400 text-center py-8">No rotation templates yet.</p>
                    )}

                    <div className="space-y-2">
                      {[...templates].sort((a, b) => a.sequence_order - b.sequence_order).map((t) => (
                        <div key={t.id} className="bg-white border border-gray-200 rounded-lg px-4 py-3 flex items-center justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="w-6 h-6 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold flex items-center justify-center">
                                {t.sequence_order}
                              </span>
                              <span className="font-medium text-gray-900 text-sm">{t.name}</span>
                              {t.required && (
                                <span className="text-xs bg-red-50 text-red-600 px-1.5 py-0.5 rounded">Required</span>
                              )}
                              {!t.active && (
                                <span className="text-xs bg-gray-100 text-gray-400 px-1.5 py-0.5 rounded">Inactive</span>
                              )}
                            </div>
                            <p className="text-xs text-gray-500 mt-0.5 ml-8">
                              {t.department_name || `Dept ${t.department}`} · {t.duration_weeks} weeks
                              {t.allowed_hospital_names.length > 0 && ` · Allowed: ${t.allowed_hospital_names.join(', ')}`}
                            </p>
                          </div>
                          <button
                            onClick={() => deleteTemplate(t.id)}
                            className="text-red-400 hover:text-red-600 text-xs ml-4"
                          >
                            Remove
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
    </ProtectedRoute>
  );
}
