'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';
import { trainingApi, TrainingProgram } from '@/lib/api/training';
import {
  userbaseApi,
  UserbaseDepartment,
  UserbaseUserUpsert,
  UserbaseUser,
} from '@/lib/api/userbase';

type UserFilters = {
  role: string;
  department: string;
  active: string;
  supervisor: string;
  program: string;
  search: string;
};

type UserForm = {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: string;
  specialty: string;
  year: string;
  supervisor: string;
  home_department: string;
  is_active: boolean;
};

const DEFAULT_FILTERS: UserFilters = {
  role: '',
  department: '',
  active: '',
  supervisor: '',
  program: '',
  search: '',
};

const EMPTY_FORM: UserForm = {
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  role: 'resident',
  specialty: '',
  year: '',
  supervisor: '',
  home_department: '',
  is_active: true,
};

const ACTIVE_OPTIONS = [
  { value: '', label: 'All statuses' },
  { value: 'true', label: 'Active' },
  { value: 'false', label: 'Inactive' },
];

const ROLE_OPTIONS = ['admin', 'utrmc_admin', 'utrmc_user', 'supervisor', 'faculty', 'resident', 'pg'];

const YEAR_OPTIONS = ['1', '2', '3', '4', '5'];
const SPECIALTY_OPTIONS = [
  { value: 'medicine', label: 'Internal Medicine' },
  { value: 'surgery', label: 'Surgery' },
  { value: 'pediatrics', label: 'Pediatrics' },
  { value: 'gynecology', label: 'Gynecology & Obstetrics' },
  { value: 'orthopedics', label: 'Orthopedics' },
  { value: 'cardiology', label: 'Cardiology' },
  { value: 'neurology', label: 'Neurology' },
  { value: 'urology', label: 'Urology' },
  { value: 'psychiatry', label: 'Psychiatry' },
  { value: 'dermatology', label: 'Dermatology' },
  { value: 'radiology', label: 'Radiology' },
  { value: 'anesthesia', label: 'Anesthesia' },
  { value: 'pathology', label: 'Pathology' },
  { value: 'microbiology', label: 'Microbiology' },
  { value: 'pharmacology', label: 'Pharmacology' },
  { value: 'community_medicine', label: 'Community Medicine' },
  { value: 'forensic_medicine', label: 'Forensic Medicine' },
  { value: 'other', label: 'Other' },
];

function getErrorMessage(error: unknown, fallback = 'Save failed'): string {
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

function buildUserQuery(filters: UserFilters) {
  const params: {
    role?: string;
    department?: number;
    supervisor?: number;
    program?: number;
    active?: boolean;
    search?: string;
    is_complete_profile?: boolean;
  } = {};

  if (filters.role) params.role = filters.role;
  if (filters.department) params.department = Number(filters.department);
  if (filters.supervisor) params.supervisor = Number(filters.supervisor);
  if (filters.program) params.program = Number(filters.program);
  if (filters.active === 'true') params.active = true;
  if (filters.active === 'false') params.active = false;
  if (filters.search.trim()) params.search = filters.search.trim();

  return params;
}

function formatDepartments(user: UserbaseUser): string {
  if (!user.departments || user.departments.length === 0) return '—';
  return user.departments.map((department) => department.code || department.name).join(', ');
}

export default function UsersPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);

  const [rows, setRows] = useState<UserbaseUser[]>([]);
  const [allUsers, setAllUsers] = useState<UserbaseUser[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [programRows, setProgramRows] = useState<Array<{ resident_user: number; program_name: string }>>([]);
  const [loading, setLoading] = useState(true);
  const [loadingLookups, setLoadingLookups] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState<UserFilters>(DEFAULT_FILTERS);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<UserbaseUser | null>(null);
  const [form, setForm] = useState<UserForm>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [actionBusyId, setActionBusyId] = useState<number | null>(null);

  const residentProgramMap = useMemo(() => {
    const map = new Map<number, string>();
    programRows.forEach((row) => {
      if (!map.has(row.resident_user)) {
        map.set(row.resident_user, row.program_name);
      }
    });
    return map;
  }, [programRows]);

  const supervisorOptions = useMemo(
    () => allUsers.filter((item) => item.role === 'supervisor' || item.role === 'faculty'),
    [allUsers]
  );

  const loadLookups = async () => {
    setLoadingLookups(true);
    try {
      const [departmentRows, userRows, trainingRows, programList] = await Promise.all([
        userbaseApi.departments.list(),
        userbaseApi.users.list(),
        trainingApi.listResidentTrainingRecords(),
        trainingApi.listPrograms(),
      ]);
      setDepartments(departmentRows);
      setAllUsers(userRows);
      setProgramRows(trainingRows.map((row) => ({ resident_user: row.resident_user, program_name: row.program_name })));
      setPrograms(programList);
    } catch {
      setDepartments([]);
      setAllUsers([]);
      setProgramRows([]);
      setPrograms([]);
    } finally {
      setLoadingLookups(false);
    }
  };

  const loadUsers = async (nextFilters: UserFilters) => {
    setLoading(true);
    setError('');
    try {
      const rowsData = await userbaseApi.users.list(buildUserQuery(nextFilters));
      setRows(rowsData);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Failed to load users.'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadLookups();
  }, []);

  useEffect(() => {
    void loadUsers(filters);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.role, filters.department, filters.active, filters.supervisor, filters.program, filters.search]);

  const openAdd = () => {
    setEditing(null);
    setForm(EMPTY_FORM);
    setShowModal(true);
  };

  const openEdit = (userRow: UserbaseUser) => {
    setEditing(userRow);
    setForm({
      username: userRow.username,
      email: userRow.email,
      password: '',
      first_name: userRow.first_name,
      last_name: userRow.last_name,
      role: userRow.role,
      specialty: userRow.specialty || '',
      year: userRow.year || '',
      supervisor: userRow.supervisor ? String(userRow.supervisor) : '',
      home_department: userRow.home_department ? String(userRow.home_department) : '',
      is_active: userRow.is_active,
    });
    setShowModal(true);
  };

  const save = async () => {
    setSaving(true);
    setError('');
    try {
      const payload: UserbaseUserUpsert = {
        username: form.username,
        email: form.email,
        first_name: form.first_name,
        last_name: form.last_name,
        role: form.role,
        specialty: form.specialty || undefined,
        year: form.year || undefined,
        supervisor: form.supervisor ? Number(form.supervisor) : null,
        home_department: form.home_department ? Number(form.home_department) : null,
        is_active: form.is_active,
      };
      if (form.password) {
        payload.password = form.password;
      }
      if (editing) {
        await userbaseApi.users.update(editing.id, payload);
      } else {
        await userbaseApi.users.create(payload);
      }
      setShowModal(false);
      await Promise.all([loadUsers(filters), loadLookups()]);
    } catch (err: unknown) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const resetPassword = async (userId: number) => {
    setActionBusyId(userId);
    setError('');
    try {
      await userbaseApi.users.resetPassword(userId, 'pgfmu123');
      setError('');
      await loadUsers(filters);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Password reset failed.'));
    } finally {
      setActionBusyId(null);
    }
  };

  const deactivateUser = async (userId: number) => {
    setActionBusyId(userId);
    setError('');
    try {
      await userbaseApi.users.deactivate(userId);
      await loadUsers(filters);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Deactivate failed.'));
    } finally {
      setActionBusyId(null);
    }
  };

  const deleteUser = async (userId: number) => {
    if (!confirm('Delete this user? This will archive the account.')) {
      return;
    }
    setActionBusyId(userId);
    setError('');
    try {
      await userbaseApi.users.delete(userId);
      await loadUsers(filters);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Delete failed.'));
    } finally {
      setActionBusyId(null);
    }
  };

  const selectedDepartment = departments.find((item) => String(item.id) === filters.department);
  const selectedSupervisor = supervisorOptions.find((item) => String(item.id) === filters.supervisor);
  const selectedProgram = programs.find((item) => String(item.id) === filters.program);

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
      <div className="pg-page">
        <PageHeader
          title="Users"
          description="Manage user accounts, filters, activation state, and first-line workflow actions."
          actions={canManage ? (
            <div className="flex gap-2">
              <Link href="/dashboard/utrmc/resident-training" className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
                Resident Programme Assignment
              </Link>
              <button onClick={openAdd} className="pg-btn-primary">+ Add User</button>
            </div>
          ) : undefined}
        />
        {isReadonly && <ReadonlyNotice />}
        {error && <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">{error}</div>}

        <div className="mb-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-600">Filters</h2>
              <p className="text-xs text-slate-500">Search by role, department, supervisor, programme, or account state.</p>
            </div>
            <div className="flex items-center gap-3 text-xs text-slate-500">
              {loading && <span>Refreshing...</span>}
              <span>{rows.length} user{rows.length === 1 ? '' : 's'}</span>
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-6">
            <div>
              <label className="pg-form-label" htmlFor="user-search">Search users</label>
              <input
                id="user-search"
                className="pg-form-input w-full"
                placeholder="Search by username, name, email"
                value={filters.search}
                onChange={(event) => setFilters((current) => ({ ...current, search: event.target.value }))}
              />
            </div>
            <div>
              <label className="pg-form-label" htmlFor="role-filter">Role</label>
              <select
                id="role-filter"
                className="pg-form-input w-full"
                value={filters.role}
                onChange={(event) => setFilters((current) => ({ ...current, role: event.target.value }))}
              >
                <option value="">All roles</option>
                {ROLE_OPTIONS.map((role) => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="pg-form-label" htmlFor="department-filter">Department</label>
              <select
                id="department-filter"
                className="pg-form-input w-full"
                value={filters.department}
                onChange={(event) => setFilters((current) => ({ ...current, department: event.target.value }))}
                disabled={loadingLookups}
              >
                <option value="">All departments</option>
                {departments.map((department) => (
                  <option key={department.id} value={department.id}>{department.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="pg-form-label" htmlFor="supervisor-filter">Supervisor</label>
              <select
                id="supervisor-filter"
                className="pg-form-input w-full"
                value={filters.supervisor}
                onChange={(event) => setFilters((current) => ({ ...current, supervisor: event.target.value }))}
                disabled={loadingLookups}
              >
                <option value="">All supervisors</option>
                {supervisorOptions.map((item) => (
                  <option key={item.id} value={item.id}>{item.full_name || `${item.first_name} ${item.last_name}`.trim() || item.username}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="pg-form-label" htmlFor="program-filter">Programme / Course</label>
              <select
                id="program-filter"
                className="pg-form-input w-full"
                value={filters.program}
                onChange={(event) => setFilters((current) => ({ ...current, program: event.target.value }))}
                disabled={loadingLookups}
              >
                <option value="">All programmes</option>
                {programs.map((program) => (
                  <option key={program.id} value={program.id}>{program.code} - {program.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="pg-form-label" htmlFor="active-filter">Account status</label>
              <select
                id="active-filter"
                className="pg-form-input w-full"
                value={filters.active}
                onChange={(event) => setFilters((current) => ({ ...current, active: event.target.value }))}
              >
                {ACTIVE_OPTIONS.map((option) => (
                  <option key={option.value || 'all-active'} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-4 flex flex-wrap items-center gap-3">
            <button type="button" className="rounded-full border border-slate-300 bg-white px-4 py-2 text-xs font-semibold text-slate-700" onClick={() => setFilters(DEFAULT_FILTERS)}>
              Reset filters
            </button>
            <button type="button" className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-xs font-semibold text-slate-600" onClick={() => void loadUsers(filters)}>
              Refresh results
            </button>
            {selectedDepartment && <span className="text-xs text-slate-500">Department: {selectedDepartment.name}</span>}
            {selectedSupervisor && <span className="text-xs text-slate-500">Supervisor: {selectedSupervisor.full_name || selectedSupervisor.username}</span>}
            {selectedProgram && <span className="text-xs text-slate-500">Programme: {selectedProgram.code}</span>}
          </div>
        </div>

        {loading ? (
          <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-6 text-sm leading-6 text-slate-600">
            Loading users...
          </div>
        ) : rows.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-6 text-sm leading-6 text-slate-600">
            No users match the selected filters, or no user accounts are loaded yet.
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  {['Username', 'Name', 'Email', 'Role', 'Departments', 'Supervisor', 'Programme', 'Active', 'Actions'].map((heading) => (
                    <th key={heading} className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
                      {heading}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {rows.map((row) => (
                  <tr key={row.id} className="hover:bg-gray-50">
                    <td className="px-3 py-3 font-medium text-gray-900">{row.username}</td>
                    <td className="px-3 py-3">{row.full_name || `${row.first_name} ${row.last_name}`.trim()}</td>
                    <td className="px-3 py-3 text-xs text-gray-500">{row.email}</td>
                    <td className="px-3 py-3">
                      <span className="rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-semibold text-indigo-700">{row.role}</span>
                    </td>
                    <td className="px-3 py-3 text-xs text-gray-600">{formatDepartments(row)}</td>
                    <td className="px-3 py-3 text-xs text-gray-600">
                      {row.supervisor ? (
                        allUsers.find((candidate) => candidate.id === row.supervisor)?.full_name
                        || allUsers.find((candidate) => candidate.id === row.supervisor)?.username
                        || row.supervisor
                      ) : '—'}
                    </td>
                    <td className="px-3 py-3 text-xs text-gray-600">{residentProgramMap.get(row.id) || '—'}</td>
                    <td className="px-3 py-3">
                      {row.is_active ? (
                        <span className="text-xs font-semibold text-green-600">Active</span>
                      ) : (
                        <span className="text-xs font-semibold text-gray-400">Inactive</span>
                      )}
                    </td>
                    <td className="px-3 py-3">
                      {canManage ? (
                        <div className="flex flex-wrap gap-2">
                          <button onClick={() => openEdit(row)} className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700">
                            Edit
                          </button>
                          <button onClick={() => resetPassword(row.id)} className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700" disabled={actionBusyId === row.id}>
                            Reset Password
                          </button>
                          <button onClick={() => deactivateUser(row.id)} className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-700" disabled={actionBusyId === row.id}>
                            Deactivate
                          </button>
                          <button onClick={() => deleteUser(row.id)} className="rounded-full border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-semibold text-red-700" disabled={actionBusyId === row.id}>
                            Delete
                          </button>
                        </div>
                      ) : (
                        <span className="text-xs text-gray-400">View only</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {showModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 px-4">
            <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg bg-white p-6 shadow-xl">
              <h2 className="mb-4 text-lg font-semibold">{editing ? 'Edit User' : 'Add User'}</h2>
              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <label className="pg-form-label" htmlFor="username">Username</label>
                  <input id="username" className="pg-form-input w-full" value={form.username} onChange={(event) => setForm((current) => ({ ...current, username: event.target.value }))} />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="email">Email</label>
                  <input id="email" type="email" className="pg-form-input w-full" value={form.email} onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))} />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="first_name">First Name</label>
                  <input id="first_name" className="pg-form-input w-full" value={form.first_name} onChange={(event) => setForm((current) => ({ ...current, first_name: event.target.value }))} />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="last_name">Last Name</label>
                  <input id="last_name" className="pg-form-input w-full" value={form.last_name} onChange={(event) => setForm((current) => ({ ...current, last_name: event.target.value }))} />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="password">Password</label>
                  <input id="password" type="password" className="pg-form-input w-full" value={form.password} onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))} placeholder={editing ? 'Leave blank to keep current' : 'Set initial password'} />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="role">Role</label>
                  <select id="role" className="pg-form-input w-full" value={form.role} onChange={(event) => setForm((current) => ({ ...current, role: event.target.value }))}>
                    {ROLE_OPTIONS.map((role) => <option key={role} value={role}>{role}</option>)}
                  </select>
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="specialty">Specialty</label>
                  <select id="specialty" className="pg-form-input w-full" value={form.specialty} onChange={(event) => setForm((current) => ({ ...current, specialty: event.target.value }))}>
                    <option value="">Select specialty</option>
                    {SPECIALTY_OPTIONS.map((option) => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="year">Year</label>
                  <select id="year" className="pg-form-input w-full" value={form.year} onChange={(event) => setForm((current) => ({ ...current, year: event.target.value }))}>
                    <option value="">Select year</option>
                    {YEAR_OPTIONS.map((year) => <option key={year} value={year}>{year}</option>)}
                  </select>
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="supervisor">Supervisor</label>
                  <select id="supervisor" className="pg-form-input w-full" value={form.supervisor} onChange={(event) => setForm((current) => ({ ...current, supervisor: event.target.value }))}>
                    <option value="">Unassigned</option>
                    {supervisorOptions.map((item) => (
                      <option key={item.id} value={item.id}>{item.full_name || `${item.first_name} ${item.last_name}`.trim() || item.username}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="home_department">Home Department</label>
                  <select id="home_department" className="pg-form-input w-full" value={form.home_department} onChange={(event) => setForm((current) => ({ ...current, home_department: event.target.value }))}>
                    <option value="">Select department</option>
                    {departments.map((department) => (
                      <option key={department.id} value={department.id}>{department.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="mt-4 flex items-center gap-2">
                <input id="is_active" type="checkbox" checked={form.is_active} onChange={(event) => setForm((current) => ({ ...current, is_active: event.target.checked }))} />
                <label htmlFor="is_active" className="text-sm">Active</label>
              </div>

              <div className="mt-5 flex justify-end gap-2">
                <button onClick={() => setShowModal(false)} className="rounded border px-4 py-2 text-sm">Cancel</button>
                <button onClick={save} disabled={saving} className="pg-btn-primary">{saving ? 'Saving...' : 'Save'}</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
