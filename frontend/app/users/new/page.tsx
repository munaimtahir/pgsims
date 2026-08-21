'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { userbaseApi, UserbaseUserUpsert } from '@/lib/api/userbase';
import authApi, { IdentityOptions } from '@/lib/api/auth';

const ROLE_OPTIONS = ['ADMIN', 'RESIDENT', 'SUPERVISOR', 'SUPPORT_STAFF'] as const;

type Role = (typeof ROLE_OPTIONS)[number];

interface IdentityForm {
  full_name: string;
  email: string;
  phone: string;
  username: string;
  password: string;
  role: Role;
  hospital: string;
  department_ref: string;
  program_ref: string;
  academic_session_ref: string;
  designation_ref: string;
  supervisor_id: string;
  supervisor_name: string;
  training_start_date: string;
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
    hospital: '',
    department_ref: '',
    program_ref: '',
    academic_session_ref: '',
    designation_ref: '',
    supervisor_id: '',
    supervisor_name: '',
    training_start_date: '',
  });
  const [options, setOptions] = useState<IdentityOptions | null>(null);
  const [supervisors, setSupervisors] = useState<Array<{ id: number; full_name?: string; username: string }>>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [created, setCreated] = useState<{ name: string; username: string } | null>(null);

  useEffect(() => {
    setForm((current) => ({ ...current, role: readInitialRole() }));
    authApi.getIdentityOptions()
      .then(setOptions)
      .catch(() => setError('Failed to load master dropdown data'));
    userbaseApi.users.list({ role: 'SUPERVISOR' }).then(setSupervisors).catch(() => undefined);
  }, []);

  const canSave = useMemo(() => form.full_name.trim().length > 0, [form.full_name]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    setError('');
    setCreated(null);
    try {
      const [first_name, ...rest] = form.full_name.trim().split(/\s+/);
      const payload: UserbaseUserUpsert = {
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
        profile: {
          hospital: form.hospital ? Number(form.hospital) : undefined,
          department_ref: form.department_ref ? Number(form.department_ref) : undefined,
          program_ref: form.program_ref ? Number(form.program_ref) : undefined,
          academic_session_ref: form.academic_session_ref || undefined,
          designation_ref: form.designation_ref || undefined,
          supervisor_profile_id: form.supervisor_id ? Number(form.supervisor_id) : undefined,
          supervisor_name: form.supervisor_name.trim() || undefined,
          training_start_date: form.training_start_date || undefined,
        },
      };

      const user = await userbaseApi.users.create(payload);
      setCreated({ name: form.full_name.trim(), username: user.username });
      setForm({
        full_name: '',
        email: '',
        phone: '',
        username: '',
        password: '',
        role: form.role,
        hospital: '',
        department_ref: '',
        program_ref: '',
        academic_session_ref: '',
        designation_ref: '',
        supervisor_id: '',
        supervisor_name: '',
        training_start_date: '',
      });
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
              className="pg-form-input bg-white"
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
                placeholder="Optional (auto-generated if empty)"
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
                placeholder="Optional (default: pgfmu123)"
              />
            </div>
          </div>

          {(form.role === 'RESIDENT' || form.role === 'SUPERVISOR') && (
            <div className="border-t border-slate-200 pt-4 space-y-4">
              <h2 className="text-sm font-medium text-slate-700">Optional Profile Settings</h2>
              
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="pg-form-label" htmlFor="hospital">Hospital / Training Site</label>
                  <select
                    id="hospital"
                    className="pg-form-input bg-white"
                    value={form.hospital}
                    onChange={(event) => setForm({ ...form, hospital: event.target.value })}
                  >
                    <option value="">Select Hospital...</option>
                    {(options?.hospitals || []).map((h) => (
                      <option key={h.id} value={h.id}>{h.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="department_ref">Department</label>
                  <select
                    id="department_ref"
                    className="pg-form-input bg-white"
                    value={form.department_ref}
                    onChange={(event) => setForm({ ...form, department_ref: event.target.value })}
                  >
                    <option value="">Select Department...</option>
                    {(options?.departments || []).map((d) => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              {form.role === 'RESIDENT' && (
                <div className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="pg-form-label" htmlFor="program_ref">Training Program</label>
                    <select
                      id="program_ref"
                      className="pg-form-input bg-white"
                      value={form.program_ref}
                      onChange={(event) => setForm({ ...form, program_ref: event.target.value })}
                    >
                      <option value="">Select Program...</option>
                      {(options?.programs || []).map((p) => (
                        <option key={p.id} value={p.id}>{p.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="pg-form-label" htmlFor="academic_session_ref">Academic Session</label>
                    <select
                      id="academic_session_ref"
                      className="pg-form-input bg-white"
                      value={form.academic_session_ref}
                      onChange={(event) => setForm({ ...form, academic_session_ref: event.target.value })}
                    >
                      <option value="">Select Session...</option>
                      {(options?.academic_sessions || []).map((s) => (
                        <option key={String(s.id)} value={String(s.id)}>{s.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div><label className="pg-form-label" htmlFor="training_start_date">Training Start Date</label><input id="training_start_date" type="date" className="pg-form-input" value={form.training_start_date} onChange={(event) => setForm({ ...form, training_start_date: event.target.value })} /></div>
                  <div><label className="pg-form-label" htmlFor="supervisor_id">Supervisor</label><select id="supervisor_id" className="pg-form-input bg-white" value={form.supervisor_id} onChange={(event) => setForm({ ...form, supervisor_id: event.target.value, supervisor_name: '' })}><option value="">Supervisor not yet available</option>{supervisors.map((s) => <option key={s.id} value={s.id}>{s.full_name || s.username}</option>)}</select></div>
                </div>
                {!form.supervisor_id && <div><label className="pg-form-label" htmlFor="supervisor_name">Unavailable Supervisor Name</label><input id="supervisor_name" className="pg-form-input" value={form.supervisor_name} onChange={(event) => setForm({ ...form, supervisor_name: event.target.value })} placeholder="Optional — can be resolved later" /></div>}
                </div>
              )}

              {form.role === 'SUPERVISOR' && (
                <div>
                  <label className="pg-form-label" htmlFor="designation_ref">Supervisor Designation</label>
                  <select
                    id="designation_ref"
                    className="pg-form-input bg-white"
                    value={form.designation_ref}
                    onChange={(event) => setForm({ ...form, designation_ref: event.target.value })}
                  >
                    <option value="">Select Designation...</option>
                    {(options?.designations || []).map((d) => (
                      <option key={String(d.id)} value={String(d.id)}>{d.name}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>
          )}

          {error && <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
          {created && <div className="rounded border border-green-200 bg-green-50 p-4 text-sm text-green-700"><p className="font-semibold">Resident created successfully</p><p>Name: {created.name}</p><p>Username: {created.username}</p><p>Temporary Password: pgfmu123</p><p>Portal: /login</p><div className="mt-3 flex gap-2"><button type="button" className="pg-btn-primary" onClick={() => navigator.clipboard?.writeText(`${created.username}\npgfmu123`)}>Copy Credentials</button><button type="button" className="pg-button-secondary" onClick={() => window.print()}>Print Credentials</button></div></div>}
          <button className="pg-btn-primary" disabled={saving || !canSave} type="submit">
            {saving ? 'Creating...' : 'Create User'}
          </button>
        </form>
      </div>
    </main>
  );
}
