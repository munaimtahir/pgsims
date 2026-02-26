'use client';

import { useCallback, useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';
import { casesApi, ClinicalCase, ClinicalCasePayload } from '@/lib/api/cases';

const emptyPayload: ClinicalCasePayload = {
  case_title: '',
  date_encountered: '',
  patient_age: 0,
  patient_gender: 'M',
  chief_complaint: '',
  history_of_present_illness: '',
  physical_examination: '',
  management_plan: '',
  clinical_reasoning: '',
  learning_points: '',
};

export default function PGCasesPage() {
  const [items, setItems] = useState<ClinicalCase[]>([]);
  const [form, setForm] = useState<ClinicalCasePayload>(emptyPayload);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const loadCases = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await casesApi.getMyCases();
      setItems(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load cases');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCases();
  }, [loadCases]);

  const onChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: name === 'patient_age' ? Number(value) : value }));
  };

  const onEdit = (item: ClinicalCase) => {
    setEditingId(item.id);
    setForm({
      ...emptyPayload,
      case_title: item.case_title,
      date_encountered: item.date_encountered,
      patient_age: item.patient_age,
      patient_gender: (item.patient_gender as ClinicalCasePayload['patient_gender']) || 'M',
      chief_complaint: item.chief_complaint,
      history_of_present_illness: '',
      physical_examination: '',
      management_plan: '',
      clinical_reasoning: item.clinical_reasoning,
      learning_points: item.learning_points,
    });
  };

  const onSave = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      setSaving(true);
      setError(null);
      if (editingId) {
        await casesApi.updateMyCase(editingId, form);
        setSuccess('Case updated.');
      } else {
        await casesApi.createMyCase(form);
        setSuccess('Case created as draft.');
      }
      setEditingId(null);
      setForm(emptyPayload);
      await loadCases();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to save case');
    } finally {
      setSaving(false);
    }
  };

  const onSubmitCase = async (id: number) => {
    try {
      await casesApi.submitMyCase(id);
      setSuccess('Case submitted for review.');
      await loadCases();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to submit case');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <h1 className="text-3xl font-bold text-gray-900">Cases</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

          <SectionCard title={editingId ? 'Edit Case' : 'Create Case'}>
            <form className="space-y-3" onSubmit={onSave}>
              <input name="case_title" value={form.case_title} onChange={onChange} placeholder="Case title" required className="w-full rounded border p-2" />
              <div className="grid grid-cols-3 gap-3">
                <input type="date" name="date_encountered" value={form.date_encountered} onChange={onChange} required className="rounded border p-2" />
                <input type="number" min={0} max={150} name="patient_age" value={form.patient_age || ''} onChange={onChange} required className="rounded border p-2" />
                <select name="patient_gender" value={form.patient_gender} onChange={onChange} className="rounded border p-2">
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                  <option value="U">Unknown</option>
                </select>
              </div>
              <textarea name="chief_complaint" value={form.chief_complaint} onChange={onChange} placeholder="Chief complaint" required className="w-full rounded border p-2" />
              <textarea name="history_of_present_illness" value={form.history_of_present_illness} onChange={onChange} placeholder="History of present illness" required className="w-full rounded border p-2" />
              <textarea name="physical_examination" value={form.physical_examination} onChange={onChange} placeholder="Physical examination" required className="w-full rounded border p-2" />
              <textarea name="management_plan" value={form.management_plan} onChange={onChange} placeholder="Management plan" required className="w-full rounded border p-2" />
              <textarea name="clinical_reasoning" value={form.clinical_reasoning} onChange={onChange} placeholder="Clinical reasoning" required className="w-full rounded border p-2" />
              <textarea name="learning_points" value={form.learning_points} onChange={onChange} placeholder="Learning points" required className="w-full rounded border p-2" />
              <button disabled={saving} className="rounded bg-indigo-600 px-4 py-2 text-white">{saving ? 'Saving...' : 'Save'}</button>
            </form>
          </SectionCard>

          <SectionCard title="My Cases">
            {loading ? (
              <p>Loading...</p>
            ) : items.length === 0 ? (
              <EmptyState title="No cases yet" description="Create your first clinical case draft." />
            ) : (
              <div className="space-y-2">
                {items.map((item) => (
                  <div key={item.id} className="flex items-center justify-between rounded border bg-white p-3">
                    <div>
                      <p className="font-medium">{item.case_title}</p>
                      <p className="text-sm text-gray-600">{item.date_encountered} • {item.status}</p>
                    </div>
                    <div className="flex gap-2">
                      {(item.status === 'draft' || item.status === 'needs_revision') && (
                        <button className="text-sm text-indigo-700" onClick={() => onEdit(item)}>Edit</button>
                      )}
                      {(item.status === 'draft' || item.status === 'needs_revision') && (
                        <button className="text-sm text-green-700" onClick={() => onSubmitCase(item.id)}>Submit</button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
