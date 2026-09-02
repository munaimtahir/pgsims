'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import authApi, { IdentityOptions, ResidentOnboardingField, ResidentOnboardingState } from '@/lib/api/auth';

const ORDER = ['identity', 'enrollment', 'supervisor', 'declaration', 'documents_baseline'];

export default function CompleteProfilePage() {
  const router = useRouter();
  const [state, setState] = useState<ResidentOnboardingState | null>(null);
  const [options, setOptions] = useState<IdentityOptions | null>(null);
  const [values, setValues] = useState<Record<string, string | number | null>>({});
  const [section, setSection] = useState('identity');
  const [status, setStatus] = useState('Loading…');
  const [error, setError] = useState('');
  const timers = useRef<Record<string, number>>({});

  const load = async () => {
    const [nextState, nextOptions] = await Promise.all([authApi.onboarding(), authApi.getIdentityOptions()]);
    setState(nextState); setOptions(nextOptions);
    const nextValues: Record<string, string | number | null> = {};
    nextState.sections.flatMap((item) => item.fields).forEach((field) => { nextValues[field.field] = field.value; });
    nextValues.supervisor_status = nextState.supervisor_status === 'NOT_STARTED' ? 'NOT_ASSIGNED' : nextState.supervisor_status;
    nextValues.research_title = nextState.baseline.research.title; nextValues.research_topic_area = nextState.baseline.research.topic_area;
    nextValues.research_status = nextState.baseline.research.status; nextValues.thesis_status = nextState.baseline.thesis.status; nextValues.thesis_notes = nextState.baseline.thesis.notes;
    setValues(nextValues); setStatus('All changes saved');
  };

  useEffect(() => { load().catch(() => { setError('Unable to load onboarding requirements.'); setStatus('Load failed'); }); }, []);
  const fields = useMemo(() => state?.sections.find((item) => item.key === section)?.fields || [], [state, section]);
  const save = (field: string, value: string | number | null) => {
    setValues((old) => ({ ...old, [field]: value })); window.clearTimeout(timers.current[field]);
    timers.current[field] = window.setTimeout(async () => { setStatus('Saving…'); setError(''); try { setState(await authApi.saveOnboardingField(field, value)); setStatus('Saved'); } catch { setStatus('Save failed'); setError(`Could not save ${field.replaceAll('_', ' ')}. Your input is still on this page.`); } }, 600);
  };
  const saveSection = async () => {
    const sectionFields = fields.reduce<Record<string, string | number | null>>((all, field) => ({ ...all, [field.field]: values[field.field] ?? '' }), {});
    setStatus('Saving draft…'); setError(''); try { setState(await authApi.saveOnboardingDraft(sectionFields)); setStatus('Draft saved'); } catch { setStatus('Draft save failed'); setError('Draft could not be saved. Please retry.'); }
  };
  const continueSection = async () => { await saveSection(); const index = ORDER.indexOf(section); if (index < ORDER.length - 1) setSection(ORDER[index + 1]); else router.push('/dashboard'); };
  const optionList = (field: ResidentOnboardingField) => { const key = ({ hospital: 'hospitals', department_ref: 'departments', program_ref: 'programs', academic_session_ref: 'academic_sessions', specialty_ref: 'specialties' } as Record<string, keyof IdentityOptions>)[field.field]; return key ? options?.[key] || [] : []; };

  if (!state) return <main className="min-h-screen bg-slate-50 p-8 text-slate-600">Loading onboarding…</main>;
  return <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-900"><div className="mx-auto max-w-4xl"><div className="flex items-start justify-between gap-4"><div><h1 className="text-2xl font-semibold">Resident onboarding</h1><p className="mt-1 text-sm text-slate-600">Complete each section. Individual fields autosave; use Save draft before leaving.</p></div><span className="text-sm text-slate-500" data-testid="save-status">{status}</span></div><div className="mt-6 flex flex-wrap gap-2">{ORDER.map((key, index) => <button key={key} type="button" onClick={() => setSection(key)} className={`rounded-full px-3 py-1.5 text-sm ${section === key ? 'bg-slate-800 text-white' : 'bg-white text-slate-600 border'}`}>{index + 1}. {state.sections.find((item) => item.key === key)?.title}</button>)}</div><section className="mt-6 rounded-lg border border-slate-200 bg-white p-5"><h2 className="text-lg font-semibold">{state.sections.find((item) => item.key === section)?.title}</h2>
    {section === 'supervisor' && <div className="mt-4"><label className="pg-form-label" htmlFor="supervisor_status">Supervisor linkage</label><select id="supervisor_status" className="pg-form-input bg-white" value={String(values.supervisor_status || '')} onChange={(event) => save('supervisor_status', event.target.value)}><option value="NOT_ASSIGNED">Not yet assigned — continue with warning</option><option value="PENDING">Supervisor requested / pending</option></select><p className="mt-2 text-sm text-amber-700">An administrator can complete the active supervisor assignment later.</p></div>}
    {section === 'declaration' && <label className="mt-4 flex gap-3 rounded border p-4 text-sm"><input type="checkbox" checked={state.declaration_accepted} onChange={async (event) => { if (event.target.checked) { setStatus('Saving…'); await authApi.acceptResidentDeclaration(); await load(); } }} />I confirm that the information provided is correct and documents are authentic. Deferred documents remain pending.</label>}
    {section === 'documents_baseline' && <div className="mt-4 space-y-6"><div><h3 className="font-medium">Documents</h3><p className="text-sm text-slate-600">Upload or explicitly defer each required document; documents do not block dashboard access.</p><ul className="mt-2 space-y-2 text-sm">{state.documents.map((doc) => <li key={doc.id} className="flex justify-between rounded border p-3"><span>{doc.title}</span><span className="text-slate-500">{doc.status}</span></li>)}</ul></div><div><h3 className="font-medium">Academic baseline</h3><p className="text-sm text-slate-600">Workshop completions, synopsis and thesis are tracked here. Logbook remains part of normal training workflow.</p><div className="mt-3 space-y-2">{state.workshops.map((workshop) => <label key={workshop.id} className="flex items-center gap-3 rounded border p-3 text-sm"><span className="w-48">{workshop.name}</span><input className="pg-form-input" type="date" value={String(values[`workshop_completion:${workshop.id}`] ?? workshop.completed_at ?? '')} onChange={(e) => save(`workshop_completion:${workshop.id}`, e.target.value)} /><span className="text-slate-500">{workshop.code}</span></label>)}</div><div className="mt-3 grid gap-3 md:grid-cols-2"><input className="pg-form-input" placeholder="Synopsis title" value={String(values.research_title || '')} onChange={(e) => save('research_title', e.target.value)} /><input className="pg-form-input" placeholder="Synopsis topic area" value={String(values.research_topic_area || '')} onChange={(e) => save('research_topic_area', e.target.value)} /><select className="pg-form-input bg-white" value={String(values.research_status || '')} onChange={(e) => save('research_status', e.target.value)}><option value="DRAFT">Synopsis: Draft</option><option value="SUBMITTED_TO_SUPERVISOR">Submitted to supervisor</option></select><select className="pg-form-input bg-white" value={String(values.thesis_status || '')} onChange={(e) => save('thesis_status', e.target.value)}><option value="NOT_STARTED">Thesis: Not started</option><option value="IN_PROGRESS">Thesis: In progress</option><option value="SUBMITTED">Thesis: Submitted</option></select><textarea className="pg-form-input md:col-span-2" placeholder="Thesis notes" value={String(values.thesis_notes || '')} onChange={(e) => save('thesis_notes', e.target.value)} /></div></div></div>}
    {fields.map((field) => <Field key={field.field} field={field} value={values[field.field]} options={optionList(field)} onChange={save} />)}
    {error && <div className="mt-4 rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}<div className="mt-6 flex justify-between"><button type="button" className="pg-btn-secondary" onClick={() => setSection(ORDER[Math.max(0, ORDER.indexOf(section) - 1)])} disabled={section === ORDER[0]}>Back</button><div className="flex gap-2"><button type="button" className="pg-btn-secondary" onClick={saveSection}>Save draft</button><button type="button" className="pg-btn-primary" onClick={continueSection}>{section === ORDER.at(-1) ? 'Finish onboarding' : 'Continue'}</button></div></div></section></div></main>;
}

function Field({ field, value, options, onChange }: { field: ResidentOnboardingField; value: string | number | null | undefined; options: Array<{ id: string | number; name: string; code?: string }>; onChange: (field: string, value: string) => void }) {
  const type = field.field.includes('date') ? 'date' : field.field === 'email' ? 'email' : field.field === 'phone' ? 'tel' : 'text';
  return <div className="mt-4"><label className="pg-form-label" htmlFor={field.field}>{field.label}{field.required ? ' *' : ''}</label>{options.length ? <select id={field.field} className="pg-form-input bg-white" value={String(value ?? '')} required={field.required} onChange={(e) => onChange(field.field, e.target.value)}><option value="">Select {field.label}…</option>{options.map((option) => <option key={option.id} value={option.id}>{option.name}{option.code ? ` (${option.code})` : ''}</option>)}</select> : field.field === 'notes' ? <textarea id={field.field} className="pg-form-input" value={String(value ?? '')} onChange={(e) => onChange(field.field, e.target.value)} /> : <input id={field.field} className="pg-form-input" type={type} value={String(value ?? '')} required={field.required} onChange={(e) => onChange(field.field, e.target.value)} />}</div>;
}
