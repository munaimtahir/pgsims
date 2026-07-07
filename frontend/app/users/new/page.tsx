'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { userbaseApi } from '@/lib/api/userbase';

const ROLE_OPTIONS = ['ADMIN', 'RESIDENT', 'SUPERVISOR', 'SUPPORT_STAFF'] as const;

type Role = (typeof ROLE_OPTIONS)[number];

interface IdentityForm {
  full_name: string;
  email: string;
  phone: string;
  username: string;
  password: string;
  role: Role;
}

function readInitialRole(): Role {
  if (typeof window === 'undefined') return 'RESIDENT';
  const role = new URLSearchParams(window.location.search).get('role');
  return ROLE_OPTIONS.includes(role as Role) ? (role as Role) : 'RESIDENT';
}

export default function NewUserPage() {
  const router = useRouter();
  const [form, setForm] = useState<IdentityForm>({
    full_name: '',
    email: '',
    phone: '',
    username: '',
    password: '',
    role: 'RESIDENT',
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [created, setCreated] = useState('');

  useEffect(() => {
    setForm((current) => ({ ...current, role: readInitialRole() }));
  }, []);

  const canSave = useMemo(() => form.full_name.trim().length > 0, [form.full_name]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    setError('');
    setCreated('');
    try {
      const [first_name, ...rest] = form.full_name.trim().split(/\s+/);
      const payload = {
        username: form.username.trim() || undefined,
        password: form.password || undefined,
        first_name,
        last_name: rest.join(' '),
        full_name: form.full_name.trim(),
        email: form.email.trim(),
        phone: form.phone.trim(),
        phone_number: form.phone.trim(),
        role: form.role,
        is_active: true,
      };
      const user = await userbaseApi.users.create(payload);
      setCreated(`${user.username} (${user.role})`);
      router.refresh();
    } catch (err: unknown) {
      const message =
        typeof err === 'object' && err !== null && 'response' in err
          ? JSON.stringify((err as { response?: { data?: unknown } }).response?.data)
          : 'Unable to create user';
      setError(message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-900">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-2xl font-semibold">New User</h1>
        <form onSubmit={submit} className="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5">
          <div>
            <label className="pg-form-label" htmlFor="role">Role</label>
            <select
              id="role"
              className="pg-form-input"
              value={form.role}
              onChange={(event) => setForm({ ...form, role: event.target.value as Role })}
            >
              {ROLE_OPTIONS.map((role) => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="pg-form-label" htmlFor="full_name">Full Name</label>
            <input
              id="full_name"
              className="pg-form-input"
              value={form.full_name}
              onChange={(event) => setForm({ ...form, full_name: event.target.value })}
              required
            />
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="pg-form-label" htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                className="pg-form-input"
                value={form.email}
                onChange={(event) => setForm({ ...form, email: event.target.value })}
              />
            </div>
            <div>
              <label className="pg-form-label" htmlFor="phone">Phone</label>
              <input
                id="phone"
                className="pg-form-input"
                value={form.phone}
                onChange={(event) => setForm({ ...form, phone: event.target.value })}
              />
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="pg-form-label" htmlFor="username">Username</label>
              <input
                id="username"
                className="pg-form-input"
                value={form.username}
                onChange={(event) => setForm({ ...form, username: event.target.value })}
              />
            </div>
            <div>
              <label className="pg-form-label" htmlFor="password">Temporary Password</label>
              <input
                id="password"
                type="password"
                className="pg-form-input"
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
              />
            </div>
          </div>
          {error && <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
          {created && <div className="rounded border border-green-200 bg-green-50 p-3 text-sm text-green-700">Created {created}</div>}
          <button className="pg-btn-primary" disabled={saving || !canSave} type="submit">
            {saving ? 'Creating...' : 'Create User'}
          </button>
        </form>
      </div>
    </main>
  );
}
