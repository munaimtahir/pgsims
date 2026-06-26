'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import {
  trainingApi,
  MilestoneEligibility,
  ResidentOperationalDashboard,
  LogbookEntry,
  LogbookThresholdSnapshot,
} from '@/lib/api/training';

const STATUS_COLOR: Record<string, string> = {
  ELIGIBLE: 'bg-green-100 text-green-800',
  PARTIALLY_READY: 'bg-yellow-100 text-yellow-800',
  NOT_READY: 'bg-red-100 text-red-800',
};

const UROLOGY_CATEGORIES = [
  {
    name: '1. OPD & Ward Work',
    procedures: [
      'Clinical History & Management Plan Formulation',
      'Ward Presentations & Case Discussions'
    ]
  },
  {
    name: '2. Emergency Urology',
    procedures: [
      'Acute Urinary Retention Management / Catheterization',
      'Urological Trauma Assessment & Shock Management',
      'Acute Scrotum / Testicular Torsion Repairs'
    ]
  },
  {
    name: '3. Diagnostic Skills',
    procedures: [
      'Retrograde/Voiding Cystourethrography Interpretation',
      'Renal & Prostate Ultrasound/Doppler Interpretation',
      'Prostate Biopsy (TRUS-guided)'
    ]
  },
  {
    name: '4. Basic Procedures',
    procedures: [
      'Suprapubic Catheterization (SPC)',
      'Circumcision & Penile/Scrotal Biopsies',
      'Urethral Dilatations / Manipulations'
    ]
  },
  {
    name: '5. Endoscopic Procedures',
    procedures: [
      'Diagnostic Cystoscopy / Urethroscopy',
      'Ureteric Stent Insertion / JJ Stenting',
      'Transurethral Resection of Prostate (TURP)',
      'Transurethral Resection of Bladder Tumor (TURBT)',
      'Ureteroscopy & Laser/Lithoclast Lithotripsy (URS)',
      'Percutaneous Nephrolithotomy (PCNL)'
    ]
  },
  {
    name: '6. Open Surgical',
    procedures: [
      'Hydrocele / Varicocele / Epididymal surgeries',
      'Orchidopexy & Orchidectomy (Simple/Radical)',
      'Retropubic Prostatectomy',
      'Urethroplasty & Reconstructive Surgery'
    ]
  },
  {
    name: '7. Therapeutic Tech',
    procedures: [
      'ESWL (Extracorporeal Shock Wave Lithotripsy)'
    ]
  },
  {
    name: '8. Renal Transplantation',
    procedures: [
      'Recipient & Donor Workup',
      'Vascular Anastomosis / Implantation Exposure'
    ]
  },
  {
    name: '9. Nephrology Rotation',
    procedures: [
      'Pre-op Assessment of Medical Renal Diseases',
      'Hemodialysis / Peritoneal Dialysis Exposure'
    ]
  }
];

const ROLES = [
  'First Surgeon / Performed',
  'Assistant',
  'Observer / Presenter',
  'Evaluator / Evaluated',
  'First Assessor'
];

type LogbookForm = {
  patient_id_number: string;
  patient_name: string;
  age: string;
  gender: string;
  disease_area: string;
  diagnosis: string;
  clinical_presentation: string;
  management_plan: string;
  resident_reflection: string;
  patient_seen_at: string;
  role: string;
};

const EMPTY_LOGBOOK_FORM: LogbookForm = {
  patient_id_number: '',
  patient_name: '',
  age: '',
  gender: '',
  disease_area: '',
  diagnosis: '',
  clinical_presentation: '',
  management_plan: '',
  resident_reflection: '',
  patient_seen_at: '',
  role: '',
};

export default function ResidentProgressPage() {
  const [eligibility, setEligibility] = useState<MilestoneEligibility[]>([]);
  const [ops, setOps] = useState<ResidentOperationalDashboard | null>(null);
  const [logbook, setLogbook] = useState<LogbookEntry[]>([]);
  const [threshold, setThreshold] = useState<{
    overall_met: boolean;
    results: LogbookThresholdSnapshot[];
  }>({ overall_met: false, results: [] });
  const [logbookForm, setLogbookForm] = useState<LogbookForm>(EMPTY_LOGBOOK_FORM);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const flash = (text: string, isError = false) => {
    if (isError) {
      setError(text);
    } else {
      setMessage(text);
    }
    window.setTimeout(() => {
      setError('');
      setMessage('');
    }, 3500);
  };

  const load = () => {
    setLoading(true);
    Promise.allSettled([
      trainingApi.getMyEligibility(),
      trainingApi.getResidentOperationalDashboard(),
      trainingApi.listLogbook(),
      trainingApi.getMyLogbookThreshold(),
    ]).then((results) => {
      const [eliResult, opsResult, logbookResult, thresholdResult] = results;

      if (eliResult.status === 'fulfilled') setEligibility(eliResult.value);
      if (opsResult.status === 'fulfilled') setOps(opsResult.value);
      if (logbookResult.status === 'fulfilled') setLogbook(logbookResult.value.results || []);
      if (thresholdResult.status === 'fulfilled') {
        setThreshold({
          overall_met: thresholdResult.value.overall_met,
          results: thresholdResult.value.results || [],
        });
      }
    }).finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const createLogbookDraft = async () => {
    if (!logbookForm.patient_id_number || !logbookForm.patient_seen_at) {
      flash('Patient ID and seen date/time are required.', true);
      return;
    }

    setBusy(true);
    try {
      await trainingApi.createLogbookEntry({
        patient_id_number: logbookForm.patient_id_number,
        patient_name: logbookForm.patient_name,
        age: logbookForm.age ? Number(logbookForm.age) : null,
        gender: logbookForm.gender,
        disease_area: logbookForm.disease_area,
        diagnosis: logbookForm.diagnosis,
        clinical_presentation: logbookForm.clinical_presentation,
        management_plan: logbookForm.management_plan,
        resident_reflection: logbookForm.resident_reflection,
        patient_seen_at: logbookForm.patient_seen_at,
        demographics: logbookForm.role ? `Role: ${logbookForm.role}` : '',
      });
      setLogbookForm(EMPTY_LOGBOOK_FORM);
      flash('Logbook draft saved.');
      load();
    } catch {
      flash('Failed to save logbook draft.', true);
    } finally {
      setBusy(false);
    }
  };

  const submitLogbook = async (entryId: number) => {
    setBusy(true);
    try {
      await trainingApi.submitLogbookEntry(entryId);
      flash('Logbook entry submitted.');
      load();
    } catch {
      flash('Failed to submit logbook entry.', true);
    } finally {
      setBusy(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['resident', 'pg']}>
      <div className="pg-page">
        <PageHeader
          title="Logbook"
          description="Create logbook drafts, submit them for review, and track the active threshold state."
        />
        {loading && <p className="text-gray-500">Loading...</p>}
        {error && <div className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">{error}</div>}
        {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-3 text-sm">{message}</div>}

        {!loading && (
          <div className="space-y-8">
            <section className="pg-kpi-grid md:grid-cols-5">
              {[
                { label: 'Logbook Total', value: ops?.logbook.total || 0 },
                { label: 'Draft', value: ops?.logbook.draft || 0 },
                { label: 'Submitted', value: ops?.logbook.submitted || 0 },
                { label: 'Returned', value: ops?.logbook.returned || 0 },
                { label: 'Approved', value: ops?.logbook.approved || 0 },
              ].map((item) => (
                <MetricCard
                  key={item.label}
                  label={item.label}
                  value={item.value}
                  tone={item.label === 'Approved' ? 'success' : item.label === 'Returned' ? 'warning' : 'default'}
                />
              ))}
            </section>
            <section className="pg-card">
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Logbook Entry (Draft)</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Patient ID / MRN *</label>
                  <input
                    value={logbookForm.patient_id_number}
                    onChange={(event) => setLogbookForm((current) => ({ ...current, patient_id_number: event.target.value }))}
                    className="pg-form-input w-full"
                    placeholder="Patient ID number"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Patient Seen At *</label>
                  <input
                    type="datetime-local"
                    value={logbookForm.patient_seen_at}
                    onChange={(event) => setLogbookForm((current) => ({ ...current, patient_seen_at: event.target.value }))}
                    className="pg-form-input w-full"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Patient Name (Optional)</label>
                  <input
                    value={logbookForm.patient_name}
                    onChange={(event) => setLogbookForm((current) => ({ ...current, patient_name: event.target.value }))}
                    className="pg-form-input w-full"
                    placeholder="Patient name"
                  />
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Age</label>
                    <input
                      type="number"
                      value={logbookForm.age}
                      onChange={(event) => setLogbookForm((current) => ({ ...current, age: event.target.value }))}
                      className="pg-form-input w-full"
                      placeholder="Age"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Gender</label>
                    <select
                      value={logbookForm.gender}
                      onChange={(event) => setLogbookForm((current) => ({ ...current, gender: event.target.value }))}
                      className="pg-form-input w-full"
                    >
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Logbook Category *</label>
                  <select
                    value={logbookForm.disease_area.split(';')[0] || ''}
                    onChange={(event) => {
                      const catName = event.target.value;
                      setLogbookForm((current) => ({
                        ...current,
                        disease_area: catName ? `${catName};` : '',
                      }));
                    }}
                    className="pg-form-input w-full"
                  >
                    <option value="">Select Category</option>
                    {UROLOGY_CATEGORIES.map((c) => (
                      <option key={c.name} value={c.name}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Procedure / Activity *</label>
                  <select
                    value={logbookForm.disease_area.split(';')[1] || ''}
                    disabled={!logbookForm.disease_area.split(';')[0]}
                    onChange={(event) => {
                      const procName = event.target.value;
                      const catName = logbookForm.disease_area.split(';')[0] || '';
                      setLogbookForm((current) => ({
                        ...current,
                        disease_area: `${catName};${procName}`,
                      }));
                    }}
                    className="pg-form-input w-full"
                  >
                    <option value="">Select Procedure</option>
                    {UROLOGY_CATEGORIES.find(c => c.name === (logbookForm.disease_area.split(';')[0]))?.procedures.map((p) => (
                      <option key={p} value={p}>{p}</option>
                    )) || null}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Resident Role *</label>
                  <select
                    value={logbookForm.role}
                    onChange={(event) => setLogbookForm((current) => ({ ...current, role: event.target.value }))}
                    className="pg-form-input w-full"
                  >
                    <option value="">Select Role</option>
                    {ROLES.map((r) => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="mt-3">
                <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Clinical Presentation</label>
                <textarea
                  value={logbookForm.clinical_presentation}
                  onChange={(event) => setLogbookForm((current) => ({ ...current, clinical_presentation: event.target.value }))}
                  className="pg-form-input w-full"
                  rows={2}
                  placeholder="Describe the clinical presentation"
                />
              </div>

              <div className="mt-3">
                <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Diagnosis</label>
                <input
                  value={logbookForm.diagnosis}
                  onChange={(event) => setLogbookForm((current) => ({ ...current, diagnosis: event.target.value }))}
                  className="pg-form-input w-full"
                  placeholder="Diagnosis"
                />
              </div>

              <div className="mt-3">
                <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Management Plan</label>
                <textarea
                  value={logbookForm.management_plan}
                  onChange={(event) => setLogbookForm((current) => ({ ...current, management_plan: event.target.value }))}
                  className="pg-form-input w-full"
                  rows={2}
                  placeholder="Management plan"
                />
              </div>

              <div className="mt-3">
                <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Resident Reflection & Learning Points</label>
                <textarea
                  value={logbookForm.resident_reflection}
                  onChange={(event) => setLogbookForm((current) => ({ ...current, resident_reflection: event.target.value }))}
                  className="pg-form-input w-full"
                  rows={2}
                  placeholder="Reflect on key learning points from this case"
                />
              </div>

              <button onClick={createLogbookDraft} disabled={busy} className="mt-4 pg-btn-primary">
                Save Urology Logbook Draft
              </button>
            </section>

            <section className="pg-card">
              <h2 className="text-lg font-semibold text-gray-800 mb-3">My Logbook Entries</h2>
              {logbook.length === 0 ? (
                <p className="text-sm text-gray-500">No logbook entries yet.</p>
              ) : (
                <div className="space-y-3">
                  {logbook.slice(0, 12).map((entry) => {
                    const parts = entry.disease_area ? entry.disease_area.split(';') : [];
                    const category = parts[0] || 'Uncategorized';
                    const procedure = parts[1] || '';
                    const role = entry.demographics && entry.demographics.startsWith('Role: ') ? entry.demographics.replace('Role: ', '') : '';

                    return (
                      <div key={entry.id} className="pg-card-muted">
                        <div className="flex items-start justify-between gap-4 flex-wrap border-b border-slate-100 pb-2 mb-2">
                          <div>
                            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded mr-2">
                              {category}
                            </span>
                            {procedure && (
                              <span className="text-xs font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                                {procedure}
                              </span>
                            )}
                            <p className="font-medium text-gray-900 mt-1">Patient ID: {entry.patient_id_number} ({entry.age || '?'}y, {entry.gender || 'Unknown'})</p>
                          </div>
                          <WorkflowStatusBadge status={entry.status} />
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-600 mt-2">
                          {role && <p><span className="font-semibold text-slate-700">Role:</span> {role}</p>}
                          <p><span className="font-semibold text-slate-700">Seen:</span> {entry.patient_seen_at.slice(0, 16).replace('T', ' ')}</p>
                          {entry.diagnosis && <p className="md:col-span-2"><span className="font-semibold text-slate-700">Diagnosis:</span> {entry.diagnosis}</p>}
                          {entry.clinical_presentation && <p className="md:col-span-2"><span className="font-semibold text-slate-700">Presentation:</span> {entry.clinical_presentation}</p>}
                          {entry.management_plan && <p className="md:col-span-2"><span className="font-semibold text-slate-700">Management:</span> {entry.management_plan}</p>}
                          {entry.resident_reflection && <p className="md:col-span-2"><span className="font-semibold text-slate-700">Reflection:</span> {entry.resident_reflection}</p>}
                          {entry.feedback && <p className="md:col-span-2 text-orange-700 font-semibold"><span className="font-semibold">Feedback:</span> {entry.feedback}</p>}
                        </div>
                        {['DRAFT', 'RETURNED'].includes(entry.status) && (
                          <button onClick={() => submitLogbook(entry.id)} disabled={busy} className="mt-3 pg-btn-success px-3 py-1.5 text-xs">
                            Submit for Approval
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            <section className="pg-card">
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Logbook Threshold Progress</h2>
              <p className="text-sm text-gray-600 mb-2">
                Overall status: {threshold.overall_met ? 'Met' : 'Not met'}
              </p>
              <div className="space-y-2">
                {threshold.results.map((row) => (
                  <div key={row.id} className="text-sm text-gray-700 border border-gray-200 rounded-lg p-2.5 bg-slate-50">
                    <span className="font-medium">{row.threshold_name}</span> - {row.approved_entries}/{row.required_entries}
                  </div>
                ))}
              </div>
            </section>

            <section>
              <h2 className="text-lg font-semibold text-gray-800 mb-3">Exam Eligibility</h2>
              {eligibility.length === 0 && (
                <p className="text-sm text-gray-500">No milestones configured for your programme yet.</p>
              )}
              <div className="space-y-4">
                {eligibility.map((entry) => (
                  <div key={entry.id} className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-gray-900">{entry.milestone_name} ({entry.milestone_code})</h3>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[entry.status] || 'bg-slate-100 text-slate-600'}`}>
                        {entry.status_display}
                      </span>
                    </div>
                    {entry.reasons.length > 0 && (
                      <ul className="mt-2 space-y-1">
                        {entry.reasons.map((reason, index) => (
                          <li key={`${reason}-${index}`} className="text-sm text-red-600 flex items-start gap-1">
                            <span>x</span> {reason}
                          </li>
                        ))}
                      </ul>
                    )}
                    {entry.reasons.length === 0 && entry.status === 'ELIGIBLE' && (
                      <p className="text-sm text-green-600 mt-2">All requirements met.</p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
