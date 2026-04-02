'use client';
import { useEffect, useState } from 'react';
import { userbaseApi, UserbaseHospital } from '@/lib/api/userbase';

const EMPTY: Partial<UserbaseHospital & { address?: string; phone?: string; email?: string }> = {
  name: '', code: '', active: true,
};

type HospitalForm = Partial<UserbaseHospital & { address?: string; phone?: string; email?: string }>;

const HOSPITAL_FIELDS: Array<{ key: 'name' | 'code'; label: string }> = [
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
];

export default function HospitalsPage() {
  const [rows, setRows] = useState<UserbaseHospital[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<UserbaseHospital | null>(null);
  const [form, setForm] = useState<HospitalForm>({ ...EMPTY });
  const [saving, setSaving] = useState(false);

  const load = () => userbaseApi.hospitals.list().then(setRows).catch(() => setError('Failed to load')).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const openAdd = () => { setForm({ ...EMPTY }); setEditing(null); setShowModal(true); };
  const openEdit = (h: UserbaseHospital) => { setForm({ name: h.name, code: h.code, active: h.active }); setEditing(h); setShowModal(true); };

  const save = async () => {
    setSaving(true);
    try {
      if (editing) await userbaseApi.hospitals.update(editing.id, form);
      else await userbaseApi.hospitals.create(form);
      setShowModal(false);
      load();
    } catch { setError('Save failed'); }
    finally { setSaving(false); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-900">Hospitals</h1>
        <button onClick={openAdd} className="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700">+ Add Hospital</button>
      </div>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Name','Code','Active','Actions'].map(h => <th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {rows.map(h => (
              <tr key={h.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{h.name}</td>
                <td className="px-4 py-2 text-gray-500">{h.code}</td>
                <td className="px-4 py-2">{h.active ? <span className="text-green-600">Yes</span> : <span className="text-gray-400">No</span>}</td>
                <td className="px-4 py-2">
                  <button onClick={() => openEdit(h)} className="text-indigo-600 hover:underline text-xs mr-3">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h2 className="text-lg font-semibold mb-4">{editing ? 'Edit' : 'Add'} Hospital</h2>
            {HOSPITAL_FIELDS.map(({ key, label }) => (
              <div key={key} className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
                <input
                  className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                  value={form[key] || ''}
                  onChange={(event) => setForm({ ...form, [key]: event.target.value })}
                />
              </div>
            ))}
            <div className="mb-4 flex items-center gap-2">
              <input type="checkbox" id="active" checked={!!form.active} onChange={e=>setForm({...form,active:e.target.checked})} />
              <label htmlFor="active" className="text-sm">Active</label>
            </div>
            <div className="flex gap-2 justify-end">
              <button onClick={() => setShowModal(false)} className="px-4 py-2 text-sm border rounded">Cancel</button>
              <button onClick={save} disabled={saving} className="px-4 py-2 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50">{saving ? 'Saving...' : 'Save'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
