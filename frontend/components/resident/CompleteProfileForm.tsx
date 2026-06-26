'use client';

import { useEffect, useState, type FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api/auth';
import { useAuthStore } from '@/store/authStore';

export default function CompleteProfileForm() {
  const router = useRouter();
  const { user, setUser, hasHydrated, isAuthenticated } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [form, setForm] = useState({
    new_password: '',
    confirm_new_password: '',
    mobile_number: '',
    email: '',
    cnic: '',
    program: '',
    training_year: '',
    joining_date: '',
  });

  useEffect(() => {
    if (!hasHydrated) {
      return;
    }
    if (!isAuthenticated || !user) {
      router.push('/login');
      return;
    }
    if (user.role !== 'pg' && user.role !== 'resident') {
      router.push('/dashboard');
      return;
    }

    authApi.getProfileCompletionStatus()
      .then((status) => {
        if (!status.needs_completion) {
          router.push('/dashboard/resident');
          return;
        }
        setForm((current) => ({
          ...current,
          email: user.email || '',
          mobile_number: user.phone_number || '',
          cnic: user.cnic || '',
          program: status.program || '',
          training_year: status.training_year || '',
          joining_date: status.joining_date || '',
        }));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [hasHydrated, isAuthenticated, user, router]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const response = await authApi.completeProfile({
        ...form,
        joining_date: form.joining_date || null,
      });
      if (user) {
        setUser({
          ...user,
          email: form.email,
          phone_number: form.mobile_number,
          cnic: form.cnic,
          profile_completed: true,
          force_password_change: false,
        });
      }
      setMessage(response.detail);
      router.push(response.redirect_to || '/dashboard/resident');
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string; error?: string } } };
      setError(apiErr.response?.data?.detail || apiErr.response?.data?.error || 'Unable to complete profile.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!hasHydrated || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="rounded-2xl border border-slate-200 bg-white px-6 py-4 text-sm text-slate-600 shadow-sm">Loading profile form…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-slate-900">Complete Profile</h1>
          <p className="mt-1 text-sm text-slate-500">Change the temporary password and fill the missing resident profile details before accessing the dashboard.</p>
        </div>

        {(error || message) && (
          <div className={`mb-4 rounded-xl border px-4 py-3 text-sm ${error ? 'border-red-200 bg-red-50 text-red-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
            {error || message}
          </div>
        )}

        <form className="space-y-4" onSubmit={submit}>
          <div className="grid gap-4 md:grid-cols-2">
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="password" placeholder="New Password" value={form.new_password} onChange={(e) => setForm((current) => ({ ...current, new_password: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="password" placeholder="Confirm New Password" value={form.confirm_new_password} onChange={(e) => setForm((current) => ({ ...current, confirm_new_password: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="text" placeholder="Mobile Number" value={form.mobile_number} onChange={(e) => setForm((current) => ({ ...current, mobile_number: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="email" placeholder="Email" value={form.email} onChange={(e) => setForm((current) => ({ ...current, email: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="text" placeholder="CNIC" value={form.cnic} onChange={(e) => setForm((current) => ({ ...current, cnic: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="text" placeholder="Program" value={form.program} onChange={(e) => setForm((current) => ({ ...current, program: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="text" placeholder="Training Year" value={form.training_year} onChange={(e) => setForm((current) => ({ ...current, training_year: e.target.value }))} required />
            <input className="rounded-xl border border-slate-200 px-4 py-3 text-sm" type="date" placeholder="Joining Date" value={form.joining_date} onChange={(e) => setForm((current) => ({ ...current, joining_date: e.target.value }))} />
          </div>

          <button type="submit" disabled={submitting} className="pg-btn-primary disabled:opacity-60">
            {submitting ? 'Saving…' : 'Complete Profile'}
          </button>
        </form>
      </div>
    </div>
  );
}
