'use client';

import { FormEvent, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import authApi, { CompleteProfileForm, MissingProfileField } from '@/lib/api/auth';

function inputType(field: MissingProfileField): string {
  if (field.input_type === 'phone') return 'tel';
  if (field.input_type === 'email') return 'email';
  return field.input_type || 'text';
}

export default function CompleteProfilePage() {
  const router = useRouter();
  const [form, setForm] = useState<CompleteProfileForm | null>(null);
  const [values, setValues] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    authApi
      .getCompleteProfileForm()
      .then((data) => {
        setForm(data);
        setValues(Object.fromEntries(data.missing_fields.map((field) => [field.field, ''])));
      })
      .catch(() => setError('Unable to load profile requirements'))
      .finally(() => setLoading(false));
  }, []);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    setError('');
    try {
      const response = await authApi.completeProfile(values);
      router.push(response.allowed_next_route || '/dashboard');
    } catch (err: unknown) {
      const message =
        typeof err === 'object' && err !== null && 'response' in err
          ? JSON.stringify((err as { response?: { data?: unknown } }).response?.data)
          : 'Unable to complete profile';
      setError(message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <main className="min-h-screen bg-slate-50 p-8 text-slate-600">Loading...</main>;
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-900">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-2xl font-semibold">Complete Profile</h1>
        <form onSubmit={submit} className="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5">
          {form?.missing_fields.length ? (
            form.missing_fields.map((field) => (
              <div key={field.field}>
                <label className="pg-form-label" htmlFor={field.field}>{field.label}</label>
                <input
                  id={field.field}
                  className="pg-form-input"
                  type={inputType(field)}
                  value={values[field.field] || ''}
                  onChange={(event) => setValues({ ...values, [field.field]: event.target.value })}
                  required={field.required}
                />
                {field.help_text && <p className="mt-1 text-xs text-slate-500">{field.help_text}</p>}
              </div>
            ))
          ) : (
            <div className="rounded border border-green-200 bg-green-50 p-3 text-sm text-green-700">
              Profile requirements are complete.
            </div>
          )}
          {error && <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
          <button className="pg-btn-primary" disabled={saving || !form?.missing_fields.length} type="submit">
            {saving ? 'Saving...' : 'Save Profile'}
          </button>
        </form>
      </div>
    </main>
  );
}
