'use client';

import { useEffect, useState } from 'react';
import { downloadFile } from '@/lib/utils';
import { onboardingApi, IncompleteProfileRow } from '@/lib/api/onboarding';

type EditForm = {
  first_name: string;
  last_name: string;
  email: string;
  mobile_number: string;
  cnic: string;
  program: string;
  training_year: string;
  joining_date: string;
  department_id: string;
};

export default function IncompleteProfilesPanel() {
  const [rows, setRows] = useState<IncompleteProfileRow[]>([]);
  const [selected, setSelected] = useState<IncompleteProfileRow | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [form, setForm] = useState<EditForm>({
    first_name: '',
    last_name: '',
    email: '',
    mobile_number: '',
    cnic: '',
    program: '',
    training_year: '',
    joining_date: '',
    department_id: '',
  });

  const load = async () => {
    setLoading(true);
    try {
      const data = await onboardingApi.listIncompleteProfiles();
      setRows(data);
      setSelected((current) => current ? data.find((row) => row.resident_id === current.resident_id) || data[0] || null : data[0] || null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load incomplete profiles.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  useEffect(() => {
    if (selected) {
      setForm({
        first_name: selected.first_name || '',
        last_name: selected.last_name || '',
        email: selected.email || '',
        mobile_number: selected.mobile_number || '',
        cnic: selected.cnic || '',
        program: selected.program || '',
        training_year: selected.training_year || '',
        joining_date: selected.joining_date || '',
        department_id: selected.department_id ? String(selected.department_id) : '',
      });
    }
  }, [selected]);

  const resetPassword = async (residentId: number) => {
    setBusy(true);
    setError('');
    try {
      await onboardingApi.resetPassword(residentId);
      setMessage('Password reset to pgfmu123.');
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Password reset failed.');
    } finally {
      setBusy(false);
    }
  };

  const markComplete = async (residentId: number) => {
    setBusy(true);
    setError('');
    try {
      await onboardingApi.markProfileComplete(residentId);
      setMessage('Profile marked complete.');
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Unable to mark complete.');
    } finally {
      setBusy(false);
    }
  };

  const saveEdit = async () => {
    if (!selected) return;
    setBusy(true);
    setError('');
    try {
      await onboardingApi.updateResident(selected.resident_id, {
        first_name: form.first_name,
        last_name: form.last_name,
        email: form.email,
        mobile_number: form.mobile_number,
        cnic: form.cnic,
        program: form.program,
        training_year: form.training_year,
        joining_date: form.joining_date || null,
        department_id: form.department_id ? Number(form.department_id) : null,
      });
      setMessage('Resident profile updated.');
      setEditMode(false);
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Update failed.');
    } finally {
      setBusy(false);
    }
  };

  const exportList = async () => {
    const blob = await onboardingApi.exportIncompleteProfiles();
    downloadFile(blob, 'incomplete_resident_profiles.xlsx');
  };

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Incomplete Profiles</h2>
        <p className="mt-1 text-sm text-slate-500">Review residents who still need their first-login profile completed.</p>
      </div>

      {(message || error) && (
        <div className={`rounded-xl border px-4 py-3 text-sm ${error ? 'border-red-200 bg-red-50 text-red-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
          {error || message}
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        <button onClick={exportList} className="pg-btn-primary" disabled={busy || loading}>Export Incomplete List</button>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
          <table className="min-w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-3 py-2">Resident Name</th>
                <th className="px-3 py-2">Username</th>
                <th className="px-3 py-2">Department</th>
                <th className="px-3 py-2">Program</th>
                <th className="px-3 py-2">Mobile</th>
                <th className="px-3 py-2">Email</th>
                <th className="px-3 py-2">CNIC</th>
                <th className="px-3 py-2">Profile Completed</th>
                <th className="px-3 py-2">Force Password Change</th>
                <th className="px-3 py-2">Last Login</th>
                <th className="px-3 py-2">Login Issued</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.resident_id} className="border-t border-slate-100">
                  <td className="px-3 py-2">{row.resident_name}</td>
                  <td className="px-3 py-2">{row.username}</td>
                  <td className="px-3 py-2">{row.department || '—'}</td>
                  <td className="px-3 py-2">{row.program || '—'}</td>
                  <td className="px-3 py-2">{row.mobile_number || '—'}</td>
                  <td className="px-3 py-2">{row.email || '—'}</td>
                  <td className="px-3 py-2">{row.cnic || '—'}</td>
                  <td className="px-3 py-2">{row.profile_completed ? 'Yes' : 'No'}</td>
                  <td className="px-3 py-2">{row.force_password_change ? 'Yes' : 'No'}</td>
                  <td className="px-3 py-2">{row.last_login || '—'}</td>
                  <td className="px-3 py-2">{row.login_issued ? 'Yes' : 'No'}</td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap gap-2">
                      <button onClick={() => { setSelected(row); setEditMode(false); }} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50">View Profile</button>
                      <button onClick={() => { setSelected(row); setEditMode(true); }} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50">Edit Profile</button>
                      <button onClick={() => resetPassword(row.resident_id)} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50" disabled={busy}>Reset Password to pgfmu123</button>
                      <button onClick={() => markComplete(row.resident_id)} className="rounded-md border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 hover:bg-emerald-100" disabled={busy}>Mark Profile Complete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          {selected ? (
            <>
              <div>
                <h3 className="text-lg font-semibold text-slate-900">{selected.resident_name}</h3>
                <p className="text-sm text-slate-500">{selected.username} · {selected.department || 'No department'}</p>
              </div>

              <div className="grid gap-3 text-sm">
                <div><span className="font-medium text-slate-700">Email:</span> {selected.email || '—'}</div>
                <div><span className="font-medium text-slate-700">Mobile:</span> {selected.mobile_number || '—'}</div>
                <div><span className="font-medium text-slate-700">CNIC:</span> {selected.cnic || '—'}</div>
                <div><span className="font-medium text-slate-700">Program:</span> {selected.program || '—'}</div>
              </div>

              {editMode && (
                <div className="space-y-3 border-t border-slate-200 pt-4">
                  <h4 className="text-sm font-semibold text-slate-900">Edit Resident Profile</h4>
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="First Name" value={form.first_name} onChange={(e) => setForm((current) => ({ ...current, first_name: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Last Name" value={form.last_name} onChange={(e) => setForm((current) => ({ ...current, last_name: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Email" value={form.email} onChange={(e) => setForm((current) => ({ ...current, email: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Mobile Number" value={form.mobile_number} onChange={(e) => setForm((current) => ({ ...current, mobile_number: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="CNIC" value={form.cnic} onChange={(e) => setForm((current) => ({ ...current, cnic: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Program" value={form.program} onChange={(e) => setForm((current) => ({ ...current, program: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Training Year" value={form.training_year} onChange={(e) => setForm((current) => ({ ...current, training_year: e.target.value }))} />
                  <input className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Joining Date (YYYY-MM-DD)" value={form.joining_date} onChange={(e) => setForm((current) => ({ ...current, joining_date: e.target.value }))} />
                  <button onClick={saveEdit} className="pg-btn-primary" disabled={busy}>Save Changes</button>
                </div>
              )}
            </>
          ) : (
            <div className="rounded-xl border border-dashed border-slate-200 p-8 text-sm text-slate-500">Select a resident to view or edit their profile.</div>
          )}
        </div>
      </div>
    </div>
  );
}
