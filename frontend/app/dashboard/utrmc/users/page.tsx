'use client';
import { useEffect, useState } from 'react';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';

const ROLES = ['admin','utrmc_admin','utrmc_user','supervisor','faculty','resident','pg'];

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
  const [rows, setRows] = useState<UserbaseUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<UserbaseUser | null>(null);
  const [form, setForm] = useState<UserForm>({ username:'',email:'',password:'',first_name:'',last_name:'',role:'resident',is_active:true });
  const [saving, setSaving] = useState(false);

  const load = () => userbaseApi.users.list().then(setRows).catch(() => setError('Failed to load')).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const openAdd = () => { setForm({username:'',email:'',password:'',first_name:'',last_name:'',role:'resident',is_active:true}); setEditing(null); setShowModal(true); };
  const openEdit = (u: UserbaseUser) => { setForm({username:u.username,email:u.email,first_name:u.first_name,last_name:u.last_name,role:u.role,is_active:u.is_active}); setEditing(u); setShowModal(true); };

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

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-900">Users</h1>
        <button onClick={openAdd} className="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700">+ Add User</button>
      </div>
      {error && <p className="text-red-600 mb-2 text-sm">{error}</p>}
      <input className="mb-3 border border-gray-300 rounded px-3 py-2 text-sm w-64" placeholder="Search..." value={search} onChange={e=>setSearch(e.target.value)} />
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Username','Name','Email','Role','Active','Actions'].map(h=><th key={h} className="text-left px-3 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.map(u=>(
              <tr key={u.id} className="hover:bg-gray-50">
                <td className="px-3 py-2">{u.username}</td>
                <td className="px-3 py-2">{u.full_name||`${u.first_name} ${u.last_name}`.trim()}</td>
                <td className="px-3 py-2 text-gray-500 text-xs">{u.email}</td>
                <td className="px-3 py-2"><span className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded text-xs">{u.role}</span></td>
                <td className="px-3 py-2">{u.is_active ? <span className="text-green-600 text-xs">Yes</span>:<span className="text-gray-400 text-xs">No</span>}</td>
                <td className="px-3 py-2"><button onClick={()=>openEdit(u)} className="text-indigo-600 hover:underline text-xs">Edit</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h2 className="text-lg font-semibold mb-4">{editing?'Edit':'Add'} User</h2>
            {USER_FIELDS.map(({ key, label }) => (
              <div key={key} className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
                <input
                  className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                  value={form[key]}
                  onChange={(event) => setForm({ ...form, [key]: event.target.value })}
                />
              </div>
            ))}
            {!editing && (
              <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input type="password" className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.password||''} onChange={e=>setForm({...form,password:e.target.value})} />
              </div>
            )}
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.role} onChange={e=>setForm({...form,role:e.target.value})}>
                {ROLES.map(r=><option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div className="mb-4 flex items-center gap-2">
              <input type="checkbox" id="uactive" checked={!!form.is_active} onChange={e=>setForm({...form,is_active:e.target.checked})} />
              <label htmlFor="uactive" className="text-sm">Active</label>
            </div>
            <div className="flex gap-2 justify-end">
              <button onClick={()=>setShowModal(false)} className="px-4 py-2 text-sm border rounded">Cancel</button>
              <button onClick={save} disabled={saving} className="px-4 py-2 text-sm bg-indigo-600 text-white rounded disabled:opacity-50">{saving?'Saving...':'Save'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
