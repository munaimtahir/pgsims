'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseHospital } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

const EMPTY: Partial<UserbaseHospital & { address?: string; phone?: string; email?: string }> = {
  name: '', code: '', active: true,
};

type HospitalForm = Partial<UserbaseHospital & { address?: string; phone?: string; email?: string }>;

const HOSPITAL_FIELDS: Array<{ key: 'name' | 'code'; label: string }> = [
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
];

function getErrorMessage(error: unknown, fallback = 'Action failed'): string {
  if (
    typeof error === 'object' &&
    error !== null &&
    'response' in error &&
    typeof (error as { response?: unknown }).response === 'object' &&
    (error as { response?: unknown }).response !== null &&
    'data' in ((error as { response?: { data?: unknown } }).response || {})
  ) {
    const data = (error as { response?: { data?: unknown } }).response?.data;
    if (typeof data === 'object' && data !== null) {
      return JSON.stringify(data);
    }
    return String(data);
  }
  return fallback;
}

export default function HospitalsPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [rows, setRows] = useState<UserbaseHospital[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<UserbaseHospital | null>(null);
  const [form, setForm] = useState<HospitalForm>({ ...EMPTY });
  const [saving, setSaving] = useState(false);
  const isEmpty = rows.length === 0;

  const load = () => userbaseApi.hospitals.list().then(setRows).catch(() => setError('Failed to load')).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const openAdd = () => { setForm({ ...EMPTY }); setEditing(null); setShowModal(true); };
  const openEdit = (h: UserbaseHospital) => { setForm({ name: h.name, code: h.code, active: h.active }); setEditing(h); setShowModal(true); };

  const deleteHospital = async (id: number, name: string) => {
    if (!window.confirm(`Are you sure you want to delete the hospital "${name}"? This operation is destructive.`)) {
      return;
    }
    setError('');
    try {
      await userbaseApi.hospitals.delete(id);
      load();
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Failed to delete hospital. It may have dependent data (e.g. matrix assignments).'));
    }
  };

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
    <div className="pg-page">
      <PageHeader
        title="Hospitals"
        description="Manage canonical hospital records used across resident operations."
        actions={
          canManage ? (
            <button onClick={openAdd} className="pg-btn-primary">+ Add Hospital</button>
          ) : undefined
        }
      />
      {isReadonly && <ReadonlyNotice />}
      {error && <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">{error}</div>}
      {isEmpty ? (
        <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-6 text-sm leading-6 text-slate-600">
          No hospitals are loaded yet. Add the first canonical hospital to begin onboarding.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                {['Name', 'Code', 'Active', 'Actions'].map((h) => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {rows.map((h) => (
                <tr key={h.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-900">{h.name}</td>
                  <td className="px-4 py-3 text-gray-500">{h.code}</td>
                  <td className="px-4 py-3">{h.active ? <span className="text-green-600">Yes</span> : <span className="text-gray-400">No</span>}</td>
                  <td className="px-4 py-3">
                    {canManage ? (
                      <div className="flex gap-2">
                        <button onClick={() => openEdit(h)} className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700">
                          Edit
                        </button>
                        <button onClick={() => deleteHospital(h.id, h.name)} className="rounded-full border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-semibold text-red-600 hover:bg-red-100">
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
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">{editing ? 'Edit' : 'Add'} Hospital</h2>
            {HOSPITAL_FIELDS.map(({ key, label }) => (
              <div key={key} className="mb-3">
                <label className="pg-form-label">{label}</label>
                <input
                  className="pg-form-input"
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
              <button onClick={save} disabled={saving} className="pg-btn-primary">{saving ? 'Saving...' : 'Save'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
