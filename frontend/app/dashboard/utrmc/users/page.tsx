'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

const ROLES = ['ADMIN', 'RESIDENT', 'SUPERVISOR', 'SUPPORT_STAFF'];

interface UserForm {
  username: string;
  email: string;
  password?: string;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
}

const USER_FIELDS: Array<{ key: keyof Pick<UserForm, 'username' | 'email' | 'first_name' | 'last_name'>; label: string }> = [
  { key: 'username', label: 'Username' },
  { key: 'email', label: 'Email' },
  { key: 'first_name', label: 'First Name' },
  { key: 'last_name', label: 'Last Name' },
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
    return JSON.stringify((error as { response?: { data?: unknown } }).response?.data);
  }
  return fallback;
}

export default function UsersPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [rows, setRows] = useState<UserbaseUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<UserbaseUser | null>(null);
  const [form, setForm] = useState<UserForm>({ username:'',email:'',password:'',first_name:'',last_name:'',role:'RESIDENT',is_active:true });
  const [saving, setSaving] = useState(false);

  const load = () => userbaseApi.users.list().then(setRows).catch(() => setError('Failed to load')).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const openAdd = () => { setForm({username:'',email:'',password:'',first_name:'',last_name:'',role:'RESIDENT',is_active:true}); setEditing(null); setShowModal(true); };
  const openEdit = (u: UserbaseUser) => { setForm({username:u.username,email:u.email,password:'',first_name:u.first_name,last_name:u.last_name,role:u.role,is_active:u.is_active}); setEditing(u); setShowModal(true); };

  const save = async () => {
    setSaving(true);
    try {
      const payload = editing ? { ...form } : form;
      if (editing && !payload.password) delete payload.password;
      if (editing) await userbaseApi.users.update(editing.id, payload);
      else await userbaseApi.users.create(payload);
      setShowModal(false);
      load();
    } catch (error: unknown) {
      setError(getErrorMessage(error));
    }
    finally { setSaving(false); }
  };

  const filtered = rows.filter(u =>
    !search || u.username.toLowerCase().includes(search.toLowerCase()) ||
    u.email.toLowerCase().includes(search.toLowerCase()) ||
    (u.full_name||'').toLowerCase().includes(search.toLowerCase())
  );
  const isEmpty = filtered.length === 0;

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="pg-page">
      <PageHeader
        title="Users"
        description="Manage role assignments and account activation state."
        actions={
          canManage ? (
            <button onClick={openAdd} className="pg-btn-primary">+ Add User</button>
          ) : undefined
        }
      />
      {isReadonly && <ReadonlyNotice />}
      {error && <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">{error}</div>}
      <div className="mb-4">
        <label className="pg-form-label" htmlFor="user-search">Search users</label>
        <input
          id="user-search"
          className="pg-form-input w-full sm:w-96"
          placeholder="Search by username, name, or email"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      {isEmpty ? (
        <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-6 text-sm leading-6 text-slate-600">
          No users match this search, or no user accounts are loaded yet.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                {['Username', 'Name', 'Email', 'Role', 'Active', 'Actions'].map((h) => (
                  <th key={h} className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50">
                  <td className="px-3 py-3 font-medium text-gray-900">{u.username}</td>
                  <td className="px-3 py-3">{u.full_name || `${u.first_name} ${u.last_name}`.trim()}</td>
                  <td className="px-3 py-3 text-gray-500 text-xs">{u.email}</td>
                  <td className="px-3 py-3"><span className="rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-semibold text-indigo-700">{u.role}</span></td>
                  <td className="px-3 py-3">{u.is_active ? <span className="text-green-600 text-xs">Yes</span> : <span className="text-gray-400 text-xs">No</span>}</td>
                  <td className="px-3 py-3">
                    {canManage ? (
                      <button onClick={() => openEdit(u)} className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700">
                        Edit
                      </button>
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
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">{editing?'Edit':'Add'} User</h2>
            {USER_FIELDS.map(({ key, label }) => (
              <div key={key} className="mb-3">
                <label className="pg-form-label" htmlFor={key}>{label}</label>
                <input
                  id={key}
                  className="pg-form-input"
                  value={form[key]}
                  onChange={(event) => setForm({ ...form, [key]: event.target.value })}
                />
              </div>
            ))}
            <div className="mb-3">
              <label className="pg-form-label" htmlFor="user-password">
                {editing ? 'New Password (leave blank to keep current)' : 'Password'}
              </label>
              <input
                id="user-password"
                type="password"
                className="pg-form-input"
                value={form.password||''}
                onChange={e=>setForm({...form,password:e.target.value})}
              />
            </div>
            <div className="mb-3">
              <label className="pg-form-label" htmlFor="role-select">Role</label>
              <select id="role-select" className="pg-form-input" value={form.role} onChange={e=>setForm({...form,role:e.target.value})}>
                {ROLES.map(r=><option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div className="mb-4 flex items-center gap-2">
              <input type="checkbox" id="uactive" checked={!!form.is_active} onChange={e=>setForm({...form,is_active:e.target.checked})} />
              <label htmlFor="uactive" className="text-sm">Active</label>
            </div>
            <div className="flex gap-2 justify-end">
              <button onClick={()=>setShowModal(false)} className="px-4 py-2 text-sm border rounded">Cancel</button>
              <button onClick={save} disabled={saving} className="pg-btn-primary">{saving?'Saving...':'Save'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
