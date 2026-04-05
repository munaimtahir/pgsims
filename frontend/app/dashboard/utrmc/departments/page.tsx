'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseDepartment } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

interface DepartmentForm {
  name: string;
  code: string;
  description: string;
  active: boolean;
}

const DEPARTMENT_FIELDS: Array<{ key: keyof Pick<DepartmentForm, 'name' | 'code' | 'description'>; label: string }> = [
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
  { key: 'description', label: 'Description' },
];

export default function DepartmentsPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [rows, setRows] = useState<UserbaseDepartment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<UserbaseDepartment | null>(null);
  const [form, setForm] = useState<DepartmentForm>({ name: '', code: '', description: '', active: true });
  const [saving, setSaving] = useState(false);

  const load = () => userbaseApi.departments.list().then(setRows).catch(() => setError('Failed to load')).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const openAdd = () => { setForm({ name:'',code:'',description:'',active:true }); setEditing(null); setShowModal(true); };
  const openEdit = (d: UserbaseDepartment) => { setForm({ name:d.name,code:d.code,description:d.description||'',active:d.active }); setEditing(d); setShowModal(true); };

  const save = async () => {
    setSaving(true);
    try {
      if (editing) await userbaseApi.departments.update(editing.id, form);
      else await userbaseApi.departments.create(form);
      setShowModal(false);
      load();
    } catch { setError('Save failed'); }
    finally { setSaving(false); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-900">Departments</h1>
        {canManage && (
          <button onClick={openAdd} className="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700">+ Add Department</button>
        )}
      </div>
      {isReadonly && <ReadonlyNotice />}
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Name','Code','Active','Actions'].map(h => <th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {rows.map(d => (
              <tr key={d.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{d.name}</td>
                <td className="px-4 py-2 text-gray-500">{d.code}</td>
                <td className="px-4 py-2">{d.active ? <span className="text-green-600">Yes</span> : <span className="text-gray-400">No</span>}</td>
                <td className="px-4 py-2">
                  {canManage ? (
                    <button onClick={() => openEdit(d)} className="text-indigo-600 hover:underline text-xs">Edit</button>
                  ) : (
                    <span className="text-xs text-gray-400">View only</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h2 className="text-lg font-semibold mb-4">{editing ? 'Edit' : 'Add'} Department</h2>
            {DEPARTMENT_FIELDS.map(({ key, label }) => (
              <div key={key} className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
                <input
                  className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                  value={form[key]}
                  onChange={(event) => setForm({ ...form, [key]: event.target.value })}
                />
              </div>
            ))}
            <div className="mb-4 flex items-center gap-2">
              <input type="checkbox" id="dactive" checked={!!form.active} onChange={e=>setForm({...form,active:e.target.checked})} />
              <label htmlFor="dactive" className="text-sm">Active</label>
            </div>
            <div className="flex gap-2 justify-end">
              <button onClick={() => setShowModal(false)} className="px-4 py-2 text-sm border rounded">Cancel</button>
              <button onClick={save} disabled={saving} className="px-4 py-2 text-sm bg-indigo-600 text-white rounded disabled:opacity-50">{saving ? 'Saving...' : 'Save'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
