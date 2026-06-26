'use client';

import { useEffect, useMemo, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';
import { trainingApi, ResidentTrainingRecordListItem, TrainingProgram } from '@/lib/api/training';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';

type FormState = {
  resident_user: string;
  program: string;
  start_date: string;
  expected_end_date: string;
  current_level: string;
  active: boolean;
};

const EMPTY_FORM: FormState = {
  resident_user: '',
  program: '',
  start_date: '',
  expected_end_date: '',
  current_level: '',
  active: true,
};

const LEVEL_OPTIONS = ['y1', 'y2', 'y3', 'y4', 'y5'];

function getErrorMessage(error: unknown, fallback = 'Save failed') {
  if (
    typeof error === 'object' &&
    error !== null &&
    'response' in error &&
    typeof (error as { response?: unknown }).response === 'object' &&
    (error as { response?: unknown }).response !== null &&
    'data' in ((error as { response?: { data?: unknown } }).response || {})
  ) {
    const data = (error as { response?: { data?: unknown } }).response?.data;
    if (typeof data === 'string') {
      return data;
    }
    return JSON.stringify(data);
  }
  return fallback;
}

export default function ResidentTrainingPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [records, setRecords] = useState<ResidentTrainingRecordListItem[]>([]);
  const [residents, setResidents] = useState<UserbaseUser[]>([]);
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [editing, setEditing] = useState<ResidentTrainingRecordListItem | null>(null);
  const [form, setForm] = useState<FormState>(EMPTY_FORM);

  const residentsOptions = useMemo(
    () => residents.filter((item) => item.role === 'resident' || item.role === 'pg'),
    [residents]
  );

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [recordRows, userRows, programRows] = await Promise.all([
        trainingApi.listResidentTrainingRecords(),
        userbaseApi.users.list(),
        trainingApi.listPrograms(),
      ]);
      setRecords(recordRows);
      setResidents(userRows);
      setPrograms(programRows);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Failed to load resident programme assignments.'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const openAdd = () => {
    setEditing(null);
    setForm(EMPTY_FORM);
    setMessage('');
  };

  const openEdit = (record: ResidentTrainingRecordListItem) => {
    setEditing(record);
    setForm({
      resident_user: String(record.resident_user),
      program: String(record.program),
      start_date: record.start_date,
      expected_end_date: record.expected_end_date || '',
      current_level: record.current_level || '',
      active: record.active,
    });
    setMessage('');
  };

  const save = async () => {
    setBusy(true);
    setError('');
    try {
      const payload = {
        resident_user: Number(form.resident_user),
        program: Number(form.program),
        start_date: form.start_date,
        expected_end_date: form.expected_end_date || null,
        current_level: form.current_level,
        active: form.active,
      };
      if (editing) {
        await trainingApi.updateResidentTrainingRecord(editing.id, payload);
        setMessage('Resident programme assignment updated.');
      } else {
        await trainingApi.createResidentTrainingRecord(payload);
        setMessage('Resident programme assignment created.');
      }
      setEditing(null);
      setForm(EMPTY_FORM);
      await load();
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Save failed.'));
    } finally {
      setBusy(false);
    }
  };

  const remove = async (id: number) => {
    if (!confirm('Delete this resident programme assignment?')) {
      return;
    }
    setBusy(true);
    setError('');
    try {
      await trainingApi.deleteResidentTrainingRecord(id);
      setMessage('Resident programme assignment deleted.');
      await load();
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Delete failed.'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
      <div className="pg-page">
        <PageHeader
          title="Resident Programme Assignment"
          description="Assign residents to a programme or course and keep their training record active."
          actions={canManage ? (
            <button onClick={openAdd} className="pg-btn-primary">+ Add Assignment</button>
          ) : undefined}
        />
        {isReadonly && <ReadonlyNotice />}
        {(error || message) && (
          <div className={`mb-4 rounded-xl border px-4 py-3 text-sm ${error ? 'border-red-200 bg-red-50 text-red-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
            {error || message}
          </div>
        )}

        <div className="grid gap-6 xl:grid-cols-[1.05fr_1.6fr]">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">{editing ? 'Edit Assignment' : 'New Assignment'}</h2>
            <div className="mt-4 space-y-3">
              <div>
                <label className="pg-form-label" htmlFor="resident-user">Resident</label>
                <select
                  id="resident-user"
                  className="pg-form-input w-full"
                  value={form.resident_user}
                  onChange={(event) => setForm((current) => ({ ...current, resident_user: event.target.value }))}
                  disabled={!canManage || residentsOptions.length === 0}
                >
                  <option value="">Select resident</option>
                  {residentsOptions.map((residentItem) => (
                    <option key={residentItem.id} value={residentItem.id}>
                      {residentItem.full_name || `${residentItem.first_name} ${residentItem.last_name}`.trim() || residentItem.username}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="pg-form-label" htmlFor="resident-program">Programme / Course</label>
                <select
                  id="resident-program"
                  className="pg-form-input w-full"
                  value={form.program}
                  onChange={(event) => setForm((current) => ({ ...current, program: event.target.value }))}
                  disabled={!canManage}
                >
                  <option value="">Select programme</option>
                  {programs.map((program) => (
                    <option key={program.id} value={program.id}>
                      {program.code} - {program.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <div>
                  <label className="pg-form-label" htmlFor="resident-start-date">Start Date</label>
                  <input
                    id="resident-start-date"
                    type="date"
                    className="pg-form-input w-full"
                    value={form.start_date}
                    onChange={(event) => setForm((current) => ({ ...current, start_date: event.target.value }))}
                    disabled={!canManage}
                  />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="resident-expected-end-date">Expected End Date</label>
                  <input
                    id="resident-expected-end-date"
                    type="date"
                    className="pg-form-input w-full"
                    value={form.expected_end_date}
                    onChange={(event) => setForm((current) => ({ ...current, expected_end_date: event.target.value }))}
                    disabled={!canManage}
                  />
                </div>
              </div>
              <div>
                <label className="pg-form-label" htmlFor="resident-current-level">Current Level</label>
                <select
                  id="resident-current-level"
                  className="pg-form-input w-full"
                  value={form.current_level}
                  onChange={(event) => setForm((current) => ({ ...current, current_level: event.target.value }))}
                  disabled={!canManage}
                >
                  <option value="">Select level</option>
                  {LEVEL_OPTIONS.map((level) => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
              </div>
              <label className="flex items-center gap-2 text-sm text-slate-700" htmlFor="resident-active">
                <input
                  id="resident-active"
                  type="checkbox"
                  checked={form.active}
                  onChange={(event) => setForm((current) => ({ ...current, active: event.target.checked }))}
                  disabled={!canManage}
                />
                Active
              </label>
              {canManage && (
                <div className="flex gap-2">
                  <button type="button" onClick={save} disabled={busy} className="pg-btn-primary">
                    {busy ? 'Saving...' : 'Save Assignment'}
                  </button>
                  {editing && (
                    <button type="button" onClick={openAdd} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
                      Cancel Edit
                    </button>
                  )}
                </div>
              )}
              {!canManage && (
                <p className="text-sm text-slate-500">Read-only mode for oversight users.</p>
              )}
            </div>
          </div>

          <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
            <table className="min-w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500">
                <tr>
                  <th className="px-3 py-2">Resident</th>
                  <th className="px-3 py-2">Programme</th>
                  <th className="px-3 py-2">Start</th>
                  <th className="px-3 py-2">Expected End</th>
                  <th className="px-3 py-2">Level</th>
                  <th className="px-3 py-2">Active</th>
                  <th className="px-3 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {records.map((record) => (
                  <tr key={record.id} className="border-t border-slate-100">
                    <td className="px-3 py-2">{record.resident_name}</td>
                    <td className="px-3 py-2">{record.program_code || '—'} {record.program_name ? `- ${record.program_name}` : ''}</td>
                    <td className="px-3 py-2">{record.start_date}</td>
                    <td className="px-3 py-2">{record.expected_end_date || '—'}</td>
                    <td className="px-3 py-2">{record.current_level || '—'}</td>
                    <td className="px-3 py-2">{record.active ? 'Yes' : 'No'}</td>
                    <td className="px-3 py-2">
                      <div className="flex flex-wrap gap-2">
                        {canManage && (
                          <>
                            <button type="button" onClick={() => openEdit(record)} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50">
                              Edit
                            </button>
                            <button type="button" onClick={() => remove(record.id)} className="rounded-md border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-medium text-red-700 hover:bg-red-100" disabled={busy}>
                              Delete
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
                {records.length === 0 && !loading && (
                  <tr>
                    <td colSpan={7} className="px-3 py-8 text-center text-sm text-slate-500">
                      No resident programme assignments found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
