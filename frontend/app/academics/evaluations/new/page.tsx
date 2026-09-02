'use client';

import { FormEvent, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, EvaluationFormTemplate, AcademicOptionRow } from '@/lib/api/academics';

interface SchemaField {
  key: string;
  label: string;
  type: string;
  min?: number;
  max?: number;
}

export default function NewEvaluationPage() {
  const router = useRouter();
  const [templates, setTemplates] = useState<EvaluationFormTemplate[]>([]);
  const [supervisors, setSupervisors] = useState<AcademicOptionRow[]>([]);
  const [periods, setPeriods] = useState<AcademicOptionRow[]>([]);
  
  const [selectedTemplateId, setSelectedTemplateId] = useState('');
  const [selectedSupervisorId, setSelectedSupervisorId] = useState('');
  const [selectedPeriodId, setSelectedPeriodId] = useState('');
  const [residentComments, setResidentComments] = useState('');
  const [responses, setResponses] = useState<Record<string, string>>({});
  
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    academicsApi.listEvaluationTemplates().then(setTemplates).catch(() => setTemplates([]));
    academicsApi.getOptions().then((opts) => {
      setSupervisors(opts.supervisors || []);
      setPeriods(opts.periods || []);
    }).catch(() => {});
  }, []);

  const selectedTemplate = templates.find((t) => String(t.id) === selectedTemplateId);
  const schemaFields: SchemaField[] = ((selectedTemplate?.schema as Record<string, unknown>)?.fields as SchemaField[]) || [];

  const handleFieldChange = (key: string, val: string) => {
    setResponses((prev) => ({ ...prev, [key]: val }));
  };

  const saveEvaluation = async (event: FormEvent, isSubmit: boolean) => {
    event.preventDefault();
    if (!selectedTemplateId) {
      setError('Please select a template.');
      return;
    }

    try {
      // Map responses to standard EvaluationResponse payload structure
      const mappedResponses = schemaFields.map((field) => {
        const value = responses[field.key] || '';
        const isNum = field.type === 'number';
        return {
          field_key: field.key,
          field_label: field.label,
          field_type: field.type,
          value_text: isNum ? '' : value,
          value_number: isNum ? Number(value) : null,
          value_json: {},
        };
      });

      const submission = await academicsApi.createEvaluationSubmission({
        template: Number(selectedTemplateId),
        supervisor: selectedSupervisorId ? Number(selectedSupervisorId) : null,
        academic_period: selectedPeriodId ? Number(selectedPeriodId) : null,
        resident_comments: residentComments,
        responses: mappedResponses,
      });

      if (isSubmit) {
        await academicsApi.submitEvaluation(submission.id);
        setMessage('Evaluation submitted successfully.');
      } else {
        setMessage('Evaluation draft saved.');
      }
      setTimeout(() => router.push('/academics/evaluations'), 1000);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'An error occurred while saving.');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'ADMIN']}>
      <div className="pg-page space-y-6 max-w-3xl">
        <PageHeader
          title="New Evaluation"
          description="Create a draft or submit a new academic evaluation/review form."
        />

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{message}</div>}

        <form className="pg-card space-y-6">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Select Form Template</label>
              <select
                className="pg-form-input"
                value={selectedTemplateId}
                onChange={(e) => {
                  setSelectedTemplateId(e.target.value);
                  setResponses({});
                }}
                required
              >
                <option value="">Choose a Template</option>
                {templates.map((t) => (
                  <option key={t.id} value={t.id}>{t.name} ({t.form_type})</option>
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
                <option value="">Prefill Primary / Select Reviewer</option>
                {supervisors.map((s) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>

            <div className="md:col-span-2">
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
          </div>

          {schemaFields.length > 0 && (
            <div className="space-y-4 border-t border-slate-100 pt-4">
              <h3 className="text-sm font-semibold text-slate-800">Form Content Fields</h3>
              <div className="grid gap-4">
                {schemaFields.map((field) => (
                  <div key={field.key}>
                    <label className="block text-sm font-medium text-slate-700 mb-1">{field.label}</label>
                    {field.type === 'number' ? (
                      <input
                        type="number"
                        min={field.min ?? 1}
                        max={field.max ?? 5}
                        step="1"
                        className="pg-form-input"
                        placeholder={`Score (${field.min ?? 1}-${field.max ?? 5})`}
                        value={responses[field.key] || ''}
                        onChange={(e) => handleFieldChange(field.key, e.target.value)}
                      />
                    ) : (
                      <textarea
                        className="pg-form-input min-h-[80px]"
                        placeholder="Add comments / observation details"
                        value={responses[field.key] || ''}
                        onChange={(e) => handleFieldChange(field.key, e.target.value)}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="space-y-2 border-t border-slate-100 pt-4">
            <label className="block text-sm font-medium text-slate-700">Resident Self Comments / Reflection</label>
            <textarea
              className="pg-form-input min-h-[100px]"
              placeholder="Your reflection on this rotation period..."
              value={residentComments}
              onChange={(e) => setResidentComments(e.target.value)}
            />
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={(e) => saveEvaluation(e, false)}
              className="pg-btn-secondary"
            >
              Save Draft
            </button>
            <button
              type="button"
              onClick={(e) => saveEvaluation(e, true)}
              className="pg-btn-primary"
            >
              Submit to Supervisor
            </button>
          </div>
        </form>
      </div>
    </ProtectedRoute>
  );
}
