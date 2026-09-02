'use client';

import { FormEvent, useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import authApi, {
  CompleteProfileForm,
  IdentityOption,
  IdentityOptions,
  MissingProfileField,
  ResidentOnboardingField,
  ResidentOnboardingState,
} from '@/lib/api/auth';

const RESIDENT_SECTION_ORDER = ['identity', 'enrollment', 'supervisor', 'declaration', 'documents_baseline'];

type PageMode = 'loading' | 'resident' | 'generic' | 'error';
type FieldValue = string | number | null;

function errorMessage(error: unknown, fallback: string): string {
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const response = (error as { response?: { data?: { detail?: string; error?: string } } }).response;
    return response?.data?.detail || response?.data?.error || fallback;
  }
  return fallback;
}

function inputType(field: MissingProfileField): string {
  if (field.input_type === 'phone') return 'tel';
  if (field.input_type === 'email') return 'email';
  return field.input_type || 'text';
}

function residentOptionKey(field: string): keyof IdentityOptions | undefined {
  return ({
    hospital: 'hospitals',
    department_ref: 'departments',
    program_ref: 'programs',
    academic_session_ref: 'academic_sessions',
    specialty_ref: 'specialties',
  } as Record<string, keyof IdentityOptions>)[field];
}

export default function CompleteProfilePage() {
  const router = useRouter();
  const [mode, setMode] = useState<PageMode>('loading');
  const [form, setForm] = useState<CompleteProfileForm | null>(null);
  const [residentState, setResidentState] = useState<ResidentOnboardingState | null>(null);
  const [options, setOptions] = useState<IdentityOptions | null>(null);
  const [values, setValues] = useState<Record<string, FieldValue>>({});
  const [section, setSection] = useState(RESIDENT_SECTION_ORDER[0]);
  const [status, setStatus] = useState('Loading…');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const timers = useRef<Record<string, number>>({});

  const applyResidentState = (nextState: ResidentOnboardingState) => {
    setResidentState(nextState);
    setValues((current) => {
      const nextValues = { ...current };
      nextState.sections.flatMap((item) => item.fields).forEach((field) => {
        nextValues[field.field] = field.value;
      });
      nextValues.supervisor_status = nextState.supervisor_status === 'NOT_STARTED' ? 'NOT_ASSIGNED' : nextState.supervisor_status;
      nextValues.research_title = nextState.baseline.research.title;
      nextValues.research_topic_area = nextState.baseline.research.topic_area;
      nextValues.research_status = nextState.baseline.research.status;
      nextValues.thesis_status = nextState.baseline.thesis.status;
      nextValues.thesis_notes = nextState.baseline.thesis.notes;
      return nextValues;
    });
  };

  useEffect(() => {
    let active = true;
    const activeTimers = timers.current;

    const load = async () => {
      try {
        const me = await authApi.me();
        if (!active) return;
        if (me.must_change_password) {
          router.push('/change-password');
          return;
        }
        if (me.allowed_next_route !== '/complete-profile') {
          router.push(me.allowed_next_route);
          return;
        }

        const nextOptions = await authApi.getIdentityOptions();
        if (!active) return;
        setOptions(nextOptions);

        if (me.role === 'RESIDENT') {
          const nextState = await authApi.onboarding();
          if (!active) return;
          applyResidentState(nextState);
          setMode('resident');
          setStatus('All changes saved');
        } else {
          const nextForm = await authApi.getCompleteProfileForm();
          if (!active) return;
          setForm(nextForm);
          setValues(Object.fromEntries(nextForm.missing_fields.map((field) => [field.field, ''])));
          setMode('generic');
          setStatus('Ready');
        }
      } catch (loadError) {
        if (!active) return;
        setError(errorMessage(loadError, 'Unable to load profile requirements.'));
        setStatus('Load failed');
        setMode('error');
      }
    };

    void load();
    return () => {
      active = false;
      Object.values(activeTimers).forEach((timer) => window.clearTimeout(timer));
    };
  }, [router]);

  const residentFields = useMemo(
    () => residentState?.sections.find((item) => item.key === section)?.fields || [],
    [residentState, section],
  );

  const saveResidentField = (field: string, value: FieldValue) => {
    setValues((current) => ({ ...current, [field]: value }));
    window.clearTimeout(timers.current[field]);
    timers.current[field] = window.setTimeout(async () => {
      setStatus('Saving…');
      setError('');
      try {
        applyResidentState(await authApi.saveOnboardingField(field, value));
        setStatus('Saved');
      } catch (saveError) {
        setStatus('Save failed');
        setError(errorMessage(saveError, `Could not save ${field.replaceAll('_', ' ')}.`));
      }
    }, 600);
  };

  const saveResidentSection = async (): Promise<ResidentOnboardingState | null> => {
    residentFields.forEach((field) => {
      window.clearTimeout(timers.current[field.field]);
      delete timers.current[field.field];
    });
    const sectionFields = residentFields.reduce<Record<string, FieldValue>>(
      (all, field) => ({ ...all, [field.field]: values[field.field] ?? '' }),
      {},
    );
    setSaving(true);
    setStatus('Saving draft…');
    setError('');
    try {
      const nextState = await authApi.saveOnboardingDraft(sectionFields);
      applyResidentState(nextState);
      setStatus('Draft saved');
      return nextState;
    } catch (saveError) {
      setStatus('Draft save failed');
      setError(errorMessage(saveError, 'Draft could not be saved. Please retry.'));
      return null;
    } finally {
      setSaving(false);
    }
  };

  const continueResidentSection = async () => {
    const savedState = await saveResidentSection();
    if (!savedState) return;

    const index = RESIDENT_SECTION_ORDER.indexOf(section);
    if (index < RESIDENT_SECTION_ORDER.length - 1) {
      setSection(RESIDENT_SECTION_ORDER[index + 1]);
      return;
    }

    try {
      const me = await authApi.me();
      if (me.allowed_next_route === '/complete-profile') {
        setError('Complete all required fields and accept the declaration before continuing.');
        return;
      }
      router.push(me.allowed_next_route);
    } catch (routeError) {
      setError(errorMessage(routeError, 'Unable to verify profile completion. Please retry.'));
    }
  };

  const acceptDeclaration = async () => {
    setSaving(true);
    setStatus('Saving…');
    setError('');
    try {
      applyResidentState(await authApi.acceptResidentDeclaration());
      setStatus('Saved');
    } catch (saveError) {
      setStatus('Save failed');
      setError(errorMessage(saveError, 'The declaration could not be saved. Please retry.'));
    } finally {
      setSaving(false);
    }
  };

  const submitGenericProfile = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    setStatus('Saving…');
    setError('');
    try {
      const response = await authApi.completeProfile(
        Object.fromEntries(Object.entries(values).map(([key, value]) => [key, String(value ?? '')])),
      );
      if (response.allowed_next_route === '/complete-profile') {
        setForm(await authApi.getCompleteProfileForm());
        setError('Please complete all remaining required fields.');
        setStatus('More information required');
        return;
      }
      router.push(response.allowed_next_route);
    } catch (saveError) {
      setStatus('Save failed');
      setError(errorMessage(saveError, 'Unable to save profile. Please retry.'));
    } finally {
      setSaving(false);
    }
  };

  if (mode === 'loading') {
    return <main className="min-h-screen bg-slate-50 p-8 text-slate-600">Loading profile requirements…</main>;
  }
  if (mode === 'error') {
    return <main className="min-h-screen bg-slate-50 p-8 text-red-700">{error}</main>;
  }
  if (mode === 'generic' && form) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-900">
        <div className="mx-auto max-w-2xl">
          <h1 className="text-2xl font-semibold">Complete Profile</h1>
          <p className="mt-1 text-sm text-slate-600">Provide the required information for your {form.profile_type.replace('Profile', '').toLowerCase()} profile.</p>
          <form onSubmit={submitGenericProfile} className="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5">
            {form.missing_fields.map((field) => (
              <GenericField
                key={field.field}
                field={field}
                value={values[field.field]}
                options={field.options_key ? options?.[field.options_key as keyof IdentityOptions] || [] : []}
                onChange={(value) => setValues((current) => ({ ...current, [field.field]: value }))}
              />
            ))}
            {error && <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
            <button className="pg-btn-primary" disabled={saving} type="submit">{saving ? 'Saving…' : 'Save Profile'}</button>
          </form>
        </div>
      </main>
    );
  }
  if (!residentState) return null;

  const optionList = (field: ResidentOnboardingField): IdentityOption[] => {
    const key = residentOptionKey(field.field);
    return key ? options?.[key] || [] : [];
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-900">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-start justify-between gap-4">
          <div><h1 className="text-2xl font-semibold">Resident onboarding</h1><p className="mt-1 text-sm text-slate-600">Complete each section. Individual fields autosave; use Save draft before leaving.</p></div>
          <span className="text-sm text-slate-500" data-testid="save-status">{status}</span>
        </div>
        <div className="mt-6 flex flex-wrap gap-2">
          {RESIDENT_SECTION_ORDER.map((key, index) => (
            <button key={key} type="button" onClick={() => setSection(key)} className={`rounded-full px-3 py-1.5 text-sm ${section === key ? 'bg-slate-800 text-white' : 'border bg-white text-slate-600'}`}>
              {index + 1}. {residentState.sections.find((item) => item.key === key)?.title}
            </button>
          ))}
        </div>
        <section className="mt-6 rounded-lg border border-slate-200 bg-white p-5">
          <h2 className="text-lg font-semibold">{residentState.sections.find((item) => item.key === section)?.title}</h2>
          {section === 'supervisor' && <SupervisorSection value={String(values.supervisor_status || '')} onChange={saveResidentField} />}
          {section === 'declaration' && (
            <label className="mt-4 flex gap-3 rounded border p-4 text-sm">
              <input type="checkbox" checked={residentState.declaration_accepted} disabled={saving || residentState.declaration_accepted} onChange={(event) => { if (event.target.checked) void acceptDeclaration(); }} />
              I confirm that the information provided is correct and documents are authentic. Deferred documents remain pending.
            </label>
          )}
          {section === 'documents_baseline' && <ResidentBaseline state={residentState} values={values} onChange={saveResidentField} />}
          {residentFields.map((field) => <ResidentField key={field.field} field={field} value={values[field.field]} options={optionList(field)} onChange={saveResidentField} />)}
          {error && <div className="mt-4 rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
          <div className="mt-6 flex justify-between">
            <button type="button" className="pg-btn-secondary" onClick={() => setSection(RESIDENT_SECTION_ORDER[Math.max(0, RESIDENT_SECTION_ORDER.indexOf(section) - 1)])} disabled={saving || section === RESIDENT_SECTION_ORDER[0]}>Back</button>
            <div className="flex gap-2">
              <button type="button" className="pg-btn-secondary" onClick={() => void saveResidentSection()} disabled={saving}>Save draft</button>
              <button type="button" className="pg-btn-primary" onClick={() => void continueResidentSection()} disabled={saving}>{section === RESIDENT_SECTION_ORDER.at(-1) ? 'Finish onboarding' : 'Continue'}</button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

function GenericField({ field, value, options, onChange }: { field: MissingProfileField; value: FieldValue | undefined; options: IdentityOption[]; onChange: (value: string) => void }) {
  return (
    <div>
      <label className="pg-form-label" htmlFor={field.field}>{field.label}</label>
      {field.input_type === 'select' ? (
        <select id={field.field} className="pg-form-input bg-white" value={String(value ?? '')} onChange={(event) => onChange(event.target.value)} required={field.required}>
          <option value="">Select {field.label}…</option>
          {options.map((option) => <option key={String(option.id)} value={String(option.id)}>{option.name}{option.code ? ` (${option.code})` : ''}</option>)}
        </select>
      ) : (
        <input id={field.field} className="pg-form-input" type={inputType(field)} value={String(value ?? '')} onChange={(event) => onChange(event.target.value)} required={field.required} />
      )}
      {field.help_text && <p className="mt-1 text-xs text-slate-500">{field.help_text}</p>}
    </div>
  );
}

function ResidentField({ field, value, options, onChange }: { field: ResidentOnboardingField; value: FieldValue | undefined; options: IdentityOption[]; onChange: (field: string, value: string) => void }) {
  const type = field.field.includes('date') ? 'date' : field.field === 'email' ? 'email' : field.field === 'phone' ? 'tel' : 'text';
  return (
    <div className="mt-4">
      <label className="pg-form-label" htmlFor={field.field}>{field.label}{field.required ? ' *' : ''}</label>
      {options.length ? (
        <select id={field.field} className="pg-form-input bg-white" value={String(value ?? '')} required={field.required} onChange={(event) => onChange(field.field, event.target.value)}>
          <option value="">Select {field.label}…</option>
          {options.map((option) => <option key={String(option.id)} value={String(option.id)}>{option.name}{option.code ? ` (${option.code})` : ''}</option>)}
        </select>
      ) : field.field === 'notes' ? (
        <textarea id={field.field} className="pg-form-input" value={String(value ?? '')} onChange={(event) => onChange(field.field, event.target.value)} />
      ) : (
        <input id={field.field} className="pg-form-input" type={type} value={String(value ?? '')} required={field.required} onChange={(event) => onChange(field.field, event.target.value)} />
      )}
    </div>
  );
}

function SupervisorSection({ value, onChange }: { value: string; onChange: (field: string, value: string) => void }) {
  return (
    <div className="mt-4">
      <label className="pg-form-label" htmlFor="supervisor_status">Supervisor linkage</label>
      <select id="supervisor_status" className="pg-form-input bg-white" value={value} onChange={(event) => onChange('supervisor_status', event.target.value)}>
        <option value="NOT_ASSIGNED">Not yet assigned — continue with warning</option>
        <option value="PENDING">Supervisor requested / pending</option>
      </select>
      <p className="mt-2 text-sm text-amber-700">An administrator can complete the active supervisor assignment later.</p>
    </div>
  );
}

function ResidentBaseline({ state, values, onChange }: { state: ResidentOnboardingState; values: Record<string, FieldValue>; onChange: (field: string, value: string) => void }) {
  return (
    <div className="mt-4 space-y-6">
      <div>
        <h3 className="font-medium">Documents</h3>
        <p className="text-sm text-slate-600">Upload or explicitly defer each required document; documents do not block dashboard access.</p>
        <ul className="mt-2 space-y-2 text-sm">{state.documents.map((document) => <li key={document.id} className="flex justify-between rounded border p-3"><span>{document.title}</span><span className="text-slate-500">{document.status}</span></li>)}</ul>
      </div>
      <div>
        <h3 className="font-medium">Academic baseline</h3>
        <p className="text-sm text-slate-600">Workshop completions, synopsis and thesis are tracked here. Logbook remains part of normal training workflow.</p>
        <div className="mt-3 space-y-2">
          {state.workshops.map((workshop) => (
            <label key={workshop.id} className="flex items-center gap-3 rounded border p-3 text-sm"><span className="w-48">{workshop.name}</span><input className="pg-form-input" type="date" value={String(values[`workshop_completion:${workshop.id}`] ?? workshop.completed_at ?? '')} onChange={(event) => onChange(`workshop_completion:${workshop.id}`, event.target.value)} /><span className="text-slate-500">{workshop.code}</span></label>
          ))}
        </div>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          <input className="pg-form-input" aria-label="Synopsis title" placeholder="Synopsis title" value={String(values.research_title || '')} onChange={(event) => onChange('research_title', event.target.value)} />
          <input className="pg-form-input" aria-label="Synopsis topic area" placeholder="Synopsis topic area" value={String(values.research_topic_area || '')} onChange={(event) => onChange('research_topic_area', event.target.value)} />
          <select className="pg-form-input bg-white" aria-label="Synopsis status" value={String(values.research_status || '')} onChange={(event) => onChange('research_status', event.target.value)}><option value="DRAFT">Synopsis: Draft</option><option value="SUBMITTED_TO_SUPERVISOR">Submitted to supervisor</option></select>
          <select className="pg-form-input bg-white" aria-label="Thesis status" value={String(values.thesis_status || '')} onChange={(event) => onChange('thesis_status', event.target.value)}><option value="NOT_STARTED">Thesis: Not started</option><option value="IN_PROGRESS">Thesis: In progress</option><option value="SUBMITTED">Thesis: Submitted</option></select>
          <textarea className="pg-form-input md:col-span-2" aria-label="Thesis notes" placeholder="Thesis notes" value={String(values.thesis_notes || '')} onChange={(event) => onChange('thesis_notes', event.target.value)} />
        </div>
      </div>
    </div>
  );
}
