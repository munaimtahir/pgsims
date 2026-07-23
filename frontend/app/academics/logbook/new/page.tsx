'use client';

import { FormEvent, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, LogbookCategory, AcademicOptionRow } from '@/lib/api/academics';

export default function NewLogbookEntryPage() {
  const router = useRouter();
  const [categories, setCategories] = useState<LogbookCategory[]>([]);
  const [supervisors, setSupervisors] = useState<AcademicOptionRow[]>([]);
  const [periods, setPeriods] = useState<AcademicOptionRow[]>([]);

  const [selectedCategoryId, setSelectedCategoryId] = useState('');
  const [selectedSupervisorId, setSelectedSupervisorId] = useState('');
  const [selectedPeriodId, setSelectedPeriodId] = useState('');
  const [entryDate, setEntryDate] = useState(new Date().toISOString().split('T')[0]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [caseIdentifier, setCaseIdentifier] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [patientGender, setPatientGender] = useState('');
  const [residentReflection, setResidentReflection] = useState('');

  // Procedure Record fields (optional/nested)
  const [procedureName, setProcedureName] = useState('');
  const [procedureCode, setProcedureCode] = useState('');
  const [rolePerformed, setRolePerformed] = useState('PERFORMED_UNDER_SUPERVISION');
  const [complexity, setComplexity] = useState('MODERATE');
  const [outcome, setOutcome] = useState('SUCCESSFUL');
  const [complications, setComplications] = useState('');

  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    academicsApi.listLogbookCategories().then(setCategories).catch(() => setCategories([]));
    academicsApi.getOptions().then((opts) => {
      setSupervisors(opts.supervisors || []);
      setPeriods(opts.periods || []);
    }).catch(() => {});
  }, []);

  const selectedCategory = categories.find((c) => String(c.id) === selectedCategoryId);

  const saveLogbook = async (event: FormEvent, isSubmit: boolean) => {
    event.preventDefault();
    if (!selectedCategoryId) {
      setError('Please select a category.');
      return;
    }
    if (!title.trim()) {
      setError('Please enter a title.');
      return;
    }

    try {
      // Build procedure record payload if category is PROCEDURE and we have details
      let procedurePayload = null;
      if (selectedCategory?.category_type === 'PROCEDURE' || procedureName) {
        procedurePayload = {
          procedure_name: procedureName || title,
          procedure_code: procedureCode,
          role_performed: rolePerformed,
          complexity: complexity,
          outcome: outcome,
          complications: complications,
        };
      }

      const entry = await academicsApi.createLogbookEntry({
        category: Number(selectedCategoryId),
        supervisor: selectedSupervisorId ? Number(selectedSupervisorId) : null,
        academic_period: selectedPeriodId ? Number(selectedPeriodId) : null,
        entry_date: entryDate,
        title,
        description,
        case_identifier: caseIdentifier,
        patient_age: patientAge,
        patient_gender: patientGender,
        resident_reflection: residentReflection,
        procedure_record: procedurePayload,
      });

      if (isSubmit) {
        await academicsApi.submitLogbookEntry(entry.id);
        setMessage('Logbook entry submitted successfully.');
      } else {
        setMessage('Logbook entry draft saved.');
      }
      setTimeout(() => router.push('/academics/logbook'), 1000);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'An error occurred while saving.');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'ADMIN']}>
      <div className="pg-page space-y-6 max-w-3xl">
        <PageHeader
          title="Log Clinical Case / Procedure"
          description="Record patient procedures, observation details, or case presentations."
        />

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        <form className="pg-card space-y-6">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Select Category</label>
              <select
                className="pg-form-input"
                value={selectedCategoryId}
                onChange={(e) => setSelectedCategoryId(e.target.value)}
                required
              >
                <option value="">Choose a Category</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name} ({c.category_type})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Select Supervisor</label>
              <select
                className="pg-form-input"
                value={selectedSupervisorId}
                onChange={(e) => setSelectedSupervisorId(e.target.value)}
              >
                <option value="">Primary Supervisor / Verifier</option>
                {supervisors.map((s) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Select Academic Period</label>
              <select
                className="pg-form-input"
                value={selectedPeriodId}
                onChange={(e) => setSelectedPeriodId(e.target.value)}
              >
                <option value="">Choose Period</option>
                {periods.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Entry Date</label>
              <input
                type="date"
                className="pg-form-input"
                value={entryDate}
                onChange={(e) => setEntryDate(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="border-t border-slate-100 pt-4 space-y-4">
            <h3 className="text-sm font-semibold text-slate-800">Case Core Information</h3>
            
            <div className="grid gap-4 md:grid-cols-3">
              <div className="md:col-span-3">
                <label className="block text-sm font-medium text-slate-700 mb-1">Case Title</label>
                <input
                  type="text"
                  className="pg-form-input"
                  placeholder="e.g. Ultrasound-guided central line"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Case ID / Reference</label>
                <input
                  type="text"
                  className="pg-form-input"
                  placeholder="e.g. MRN-120938"
                  value={caseIdentifier}
                  onChange={(e) => setCaseIdentifier(e.target.value)}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Patient Age</label>
                <input
                  type="text"
                  className="pg-form-input"
                  placeholder="e.g. 45y or 6m"
                  value={patientAge}
                  onChange={(e) => setPatientAge(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Patient Gender</label>
                <select
                  className="pg-form-input"
                  value={patientGender}
                  onChange={(e) => setPatientGender(e.target.value)}
                >
                  <option value="">Select Gender</option>
                  <option value="MALE">Male</option>
                  <option value="FEMALE">Female</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>

              <div className="md:col-span-3">
                <label className="block text-sm font-medium text-slate-700 mb-1">Case / Procedure Description</label>
                <textarea
                  className="pg-form-input min-h-[80px]"
                  placeholder="Clinical presentation, key steps, findings..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Procedure Record Fields */}
          {(selectedCategory?.category_type === 'PROCEDURE') && (
            <div className="border-t border-slate-100 pt-4 space-y-4 bg-slate-50 p-4 rounded-xl">
              <h3 className="text-sm font-semibold text-slate-800">Procedure Details</h3>
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Procedure Name</label>
                  <input
                    type="text"
                    className="pg-form-input"
                    placeholder="e.g. Central Venous Catheterization"
                    value={procedureName}
                    onChange={(e) => setProcedureName(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">CPT / Billing Code</label>
                  <input
                    type="text"
                    className="pg-form-input"
                    placeholder="e.g. CPT-36556"
                    value={procedureCode}
                    onChange={(e) => setProcedureCode(e.target.value)}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Role Performed</label>
                  <select
                    className="pg-form-input"
                    value={rolePerformed}
                    onChange={(e) => setRolePerformed(e.target.value)}
                  >
                    <option value="OBSERVED">Observed Only</option>
                    <option value="PERFORMED_UNDER_SUPERVISION">Performed Under Supervision</option>
                    <option value="PERFORMED_INDEPENDENTLY">Performed Independently</option>
                    <option value="ASSISTED_LEAD_SURGEON">Assisted Lead Surgeon</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Complexity</label>
                  <select
                    className="pg-form-input"
                    value={complexity}
                    onChange={(e) => setComplexity(e.target.value)}
                  >
                    <option value="LOW">Low Complexity</option>
                    <option value="MODERATE">Moderate Complexity</option>
                    <option value="HIGH">High Complexity</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Outcome</label>
                  <select
                    className="pg-form-input"
                    value={outcome}
                    onChange={(e) => setOutcome(e.target.value)}
                  >
                    <option value="SUCCESSFUL">Successful</option>
                    <option value="PARTIALLY_SUCCESSFUL">Partially Successful</option>
                    <option value="UNSUCCESSFUL">Unsuccessful</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Complications (if any)</label>
                  <input
                    type="text"
                    className="pg-form-input"
                    placeholder="None"
                    value={complications}
                    onChange={(e) => setComplications(e.target.value)}
                  />
                </div>
              </div>
            </div>
          )}

          <div className="space-y-2 border-t border-slate-100 pt-4">
            <label className="block text-sm font-medium text-slate-700">Resident Self Reflection</label>
            <textarea
              className="pg-form-input min-h-[100px]"
              placeholder="What went well? Areas for clinical growth or improvements..."
              value={residentReflection}
              onChange={(e) => setResidentReflection(e.target.value)}
            />
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={(e) => saveLogbook(e, false)}
              className="pg-btn-secondary"
            >
              Save Draft
            </button>
            <button
              type="button"
              onClick={(e) => saveLogbook(e, true)}
              className="pg-btn-primary"
            >
              Submit for Verification
            </button>
          </div>
        </form>
      </div>
    </ProtectedRoute>
  );
}
