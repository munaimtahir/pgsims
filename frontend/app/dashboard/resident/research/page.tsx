'use client';
import { useEffect, useState, useRef } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { trainingApi, ResidentResearchProject } from '@/lib/api/training';
import { usersApi } from '@/lib/api/users';

const STEPS = [
  { key: 'topic', label: 'Topic & Supervisor' },
  { key: 'synopsis', label: 'Upload Synopsis' },
  { key: 'supervisor', label: 'Submit to Supervisor' },
  { key: 'approval', label: 'Supervisor Approval' },
  { key: 'university', label: 'University Submission' },
];

function stepIndex(project: ResidentResearchProject | null): number {
  if (!project) return 0;
  switch (project.status) {
    case 'DRAFT': return project.synopsis_file ? 2 : (project.title ? 1 : 0);
    case 'SUBMITTED_TO_SUPERVISOR': return 3;
    case 'APPROVED_BY_SUPERVISOR': return 3;
    case 'SUBMITTED_TO_UNIVERSITY': return 4;
    case 'ACCEPTED_BY_UNIVERSITY': return 4;
    default: return 0;
  }
}

const STATUS_LABELS: Record<string, string> = {
  DRAFT: 'Draft',
  SUBMITTED_TO_SUPERVISOR: 'Awaiting Supervisor',
  APPROVED_BY_SUPERVISOR: 'Approved by Supervisor',
  SUBMITTED_TO_UNIVERSITY: 'Submitted to University',
  ACCEPTED_BY_UNIVERSITY: 'Accepted ✓',
};

function getErrorMessage(error: unknown, fallback = 'Failed'): string {
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

export default function ResidentResearchPage() {
  const [project, setProject] = useState<ResidentResearchProject | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [supervisors, setSupervisors] = useState<Array<{ id: number; full_name?: string; username: string }>>([]);
  const [form, setForm] = useState({ title: '', topic_area: '', supervisor: '' });
  const fileRef = useRef<HTMLInputElement>(null);

  const loadProject = () => {
    trainingApi.getMyResearch()
      .then((p) => { setProject(p); setForm({ title: p.title, topic_area: p.topic_area, supervisor: String(p.supervisor || '') }); })
      .catch(() => setProject(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadProject();
    usersApi.getSupervisors().then(data => setSupervisors(data)).catch(() => {});
  }, []);

  const msg = (s: string, isErr = false) => {
    if (isErr) {
      setError(s);
    } else {
      setSuccess(s);
    }
    setTimeout(() => {
      setError('');
      setSuccess('');
    }, 4000);
  };

  const saveTopicSupervisor = async () => {
    setSaving(true);
    try {
      if (!project) {
        const p = await trainingApi.createResearch({ title: form.title, topic_area: form.topic_area, supervisor: form.supervisor ? Number(form.supervisor) : undefined });
        setProject(p);
      } else {
        const p = await trainingApi.patchResearch({ title: form.title, topic_area: form.topic_area, supervisor: form.supervisor ? Number(form.supervisor) : undefined });
        setProject(p);
      }
      msg('Saved');
    } catch { msg('Save failed', true); } finally { setSaving(false); }
  };

  const uploadSynopsis = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file || !project) return;
    setSaving(true);
    try {
      const p = await trainingApi.patchResearchFile(file);
      setProject(p);
      msg('Synopsis uploaded');
    } catch { msg('Upload failed', true); } finally { setSaving(false); }
  };

  const submitToSupervisor = async () => {
    setSaving(true);
    try {
      const p = await trainingApi.researchAction('submit-to-supervisor');
      setProject(p);
      msg('Submitted to supervisor');
    } catch (error: unknown) { msg(getErrorMessage(error), true); } finally { setSaving(false); }
  };

  const submitToUniversity = async () => {
    setSaving(true);
    try {
      const p = await trainingApi.researchAction('submit-to-university');
      setProject(p);
      msg('Submitted to university');
    } catch (error: unknown) { msg(getErrorMessage(error), true); } finally { setSaving(false); }
  };

  const curStep = stepIndex(project);

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Research Project</h1>
          {project && (
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              project.status === 'ACCEPTED_BY_UNIVERSITY' ? 'bg-green-100 text-green-800' :
              project.status === 'APPROVED_BY_SUPERVISOR' ? 'bg-green-100 text-green-800' :
              project.status === 'SUBMITTED_TO_SUPERVISOR' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-700'
            }`}>{STATUS_LABELS[project.status] || project.status}</span>
          )}
        </div>

        {error && <div className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">{error}</div>}
        {success && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-3 text-sm">{success}</div>}

        {/* Stepper */}
        <div className="flex items-center gap-0 mb-8 overflow-x-auto pb-2">
          {STEPS.map((s, i) => (
            <div key={s.key} className="flex items-center flex-shrink-0">
              <div className="flex flex-col items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 ${
                  i < curStep ? 'bg-indigo-600 border-indigo-600 text-white' :
                  i === curStep ? 'border-indigo-600 text-indigo-600 bg-white' :
                  'border-gray-300 text-gray-400 bg-white'
                }`}>{i < curStep ? '✓' : i + 1}</div>
                <span className={`text-xs mt-1 whitespace-nowrap ${i === curStep ? 'text-indigo-600 font-semibold' : 'text-gray-500'}`}>{s.label}</span>
              </div>
              {i < STEPS.length - 1 && <div className={`h-0.5 w-8 mx-1 mb-4 ${i < curStep ? 'bg-indigo-600' : 'bg-gray-200'}`} />}
            </div>
          ))}
        </div>

        {loading && <div className="flex justify-center py-16"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}

        {!loading && (
          <div className="space-y-6">
            {/* Step 1: Topic + Supervisor */}
            <div className={`bg-white border rounded-xl p-5 ${curStep === 0 || (project && project.status === 'DRAFT') ? 'border-indigo-200 shadow-sm' : 'border-gray-200'}`}>
              <h2 className="font-semibold text-gray-800 mb-4">Step 1: Research Topic & Supervisor</h2>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
                  <input value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
                    disabled={project?.status !== 'DRAFT' && !!project}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm disabled:bg-gray-50" placeholder="Research title" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Topic Area</label>
                  <input value={form.topic_area} onChange={e => setForm(f => ({ ...f, topic_area: e.target.value }))}
                    disabled={project?.status !== 'DRAFT' && !!project}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm disabled:bg-gray-50" placeholder="e.g., Cardiology, Oncology" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Supervisor</label>
                  <select value={form.supervisor} onChange={e => setForm(f => ({ ...f, supervisor: e.target.value }))}
                    disabled={project?.status !== 'DRAFT' && !!project}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm disabled:bg-gray-50">
                    <option value="">— Select supervisor —</option>
                    {supervisors.map(s => <option key={s.id} value={s.id}>{s.full_name || s.username}</option>)}
                  </select>
                </div>
                {(!project || project.status === 'DRAFT') && (
                  <button onClick={saveTopicSupervisor} disabled={saving || !form.title}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Saving…' : 'Save'}
                  </button>
                )}
              </div>
            </div>

            {/* Step 2: Upload Synopsis */}
            <div className={`bg-white border rounded-xl p-5 ${!project ? 'opacity-50 pointer-events-none' : 'border-gray-200'}`}>
              <h2 className="font-semibold text-gray-800 mb-4">Step 2: Upload Synopsis</h2>
              {project?.synopsis_file && (
                <p className="text-sm text-green-700 mb-3">✓ Synopsis uploaded. <a href={project.synopsis_file} target="_blank" rel="noreferrer" className="underline">View</a></p>
              )}
              {project?.status === 'DRAFT' && (
                <div className="flex items-center gap-3">
                  <input ref={fileRef} type="file" accept=".pdf,.doc,.docx" className="text-sm" />
                  <button onClick={uploadSynopsis} disabled={saving}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Uploading…' : 'Upload'}
                  </button>
                </div>
              )}
            </div>

            {/* Step 3: Submit to Supervisor */}
            <div className={`bg-white border rounded-xl p-5 ${project?.status === 'DRAFT' && project?.synopsis_file ? 'border-indigo-200' : 'border-gray-200'} ${!project?.synopsis_file ? 'opacity-50 pointer-events-none' : ''}`}>
              <h2 className="font-semibold text-gray-800 mb-2">Step 3: Submit to Supervisor</h2>
              {project?.status === 'DRAFT' && project?.synopsis_file && (
                <button onClick={submitToSupervisor} disabled={saving}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? 'Submitting…' : 'Submit to Supervisor'}
                </button>
              )}
              {project?.status === 'SUBMITTED_TO_SUPERVISOR' && <p className="text-sm text-yellow-700">⏳ Awaiting supervisor review…</p>}
            </div>

            {/* Step 4: Supervisor Approval */}
            <div className="bg-white border border-gray-200 rounded-xl p-5">
              <h2 className="font-semibold text-gray-800 mb-2">Step 4: Supervisor Approval</h2>
              {project?.status === 'APPROVED_BY_SUPERVISOR' && (
                <p className="text-sm text-green-700">✓ Approved on {project.synopsis_approved_at?.slice(0, 10)}</p>
              )}
              {project?.supervisor_feedback && (
                <div className="mt-2 bg-gray-50 rounded-lg p-3 text-sm text-gray-700">
                  <span className="font-medium">Feedback:</span> {project.supervisor_feedback}
                </div>
              )}
              {!project || !['APPROVED_BY_SUPERVISOR', 'SUBMITTED_TO_UNIVERSITY', 'ACCEPTED_BY_UNIVERSITY'].includes(project.status) && !project?.supervisor_feedback && (
                <p className="text-sm text-gray-400">Pending supervisor review</p>
              )}
            </div>

            {/* Step 5: University Submission */}
            <div className={`bg-white border rounded-xl p-5 ${project?.status === 'APPROVED_BY_SUPERVISOR' ? 'border-indigo-200' : 'border-gray-200'} ${project?.status !== 'APPROVED_BY_SUPERVISOR' && project?.status !== 'SUBMITTED_TO_UNIVERSITY' && project?.status !== 'ACCEPTED_BY_UNIVERSITY' ? 'opacity-50 pointer-events-none' : ''}`}>
              <h2 className="font-semibold text-gray-800 mb-2">Step 5: University Submission</h2>
              {project?.status === 'APPROVED_BY_SUPERVISOR' && (
                <button onClick={submitToUniversity} disabled={saving}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50">
                  {saving ? 'Submitting…' : 'Submit to University'}
                </button>
              )}
              {project?.status === 'SUBMITTED_TO_UNIVERSITY' && <p className="text-sm text-yellow-700">⏳ Awaiting university acceptance</p>}
              {project?.status === 'ACCEPTED_BY_UNIVERSITY' && <p className="text-sm text-green-700">✓ Accepted by university on {project.accepted_at?.slice(0, 10)}</p>}
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
