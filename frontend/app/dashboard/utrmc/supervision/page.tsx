'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

interface LinkEntry {
  id: number;
  supervisor: number | { id: number; username: string; full_name?: string };
  resident: number | { id: number; username: string; full_name?: string };
  start_date: string;
  active: boolean;
}

interface SupervisionForm {
  supervisor: string;
  resident: string;
  start_date: string;
  active: boolean;
}

interface PagedResponse<T> {
  results?: T[];
}

function userName(u: number | { id?: number; username?: string; full_name?: string } | undefined): string {
  if (!u) return '';
  if (typeof u === 'object') return u.full_name || u.username || String(u.id || '');
  return String(u);
}

export default function SupervisionPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [links, setLinks] = useState<LinkEntry[]>([]);
  const [users, setUsers] = useState<UserbaseUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState<SupervisionForm>({ supervisor:'', resident:'', start_date:'', active: true });
  const [saving, setSaving] = useState(false);

  const load = () => Promise.all([
    userbaseApi.supervisionLinks.list(),
    userbaseApi.users.list(),
  ]).then(([lData, uData]) => {
    const arr = Array.isArray(lData) ? lData : (lData as PagedResponse<LinkEntry>).results || [];
    setLinks(arr);
    setUsers(uData);
  }).catch(()=>setError('Failed to load')).finally(()=>setLoading(false));

  useEffect(() => { load(); }, []);

  const supervisors = users.filter(u=>u.role==='supervisor'||u.role==='faculty');
  const residents = users.filter(u=>u.role==='resident'||u.role==='pg');

  const save = async () => {
    setSaving(true);
    try {
      await userbaseApi.supervisionLinks.create({ ...form, supervisor: Number(form.supervisor), resident: Number(form.resident) });
      setShowModal(false);
      load();
    } catch { setError('Save failed'); }
    finally { setSaving(false); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-900">Supervision Links</h1>
        {canManage && (
          <button onClick={()=>{setForm({supervisor:'',resident:'',start_date:'',active:true});setShowModal(true);}} className="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700">+ Add Link</button>
        )}
      </div>
      {isReadonly && <ReadonlyNotice />}
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Supervisor','Resident','Start Date','Active'].map(h=><th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {links.map((l) => (
              <tr key={l.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{userName(l.supervisor)}</td>
                <td className="px-4 py-2">{userName(l.resident)}</td>
                <td className="px-4 py-2 text-gray-500">{l.start_date||'—'}</td>
                <td className="px-4 py-2">{l.active?<span className="text-green-600">Yes</span>:<span className="text-gray-400">No</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h2 className="text-lg font-semibold mb-4">Add Supervision Link</h2>
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-1">Supervisor</label>
              <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.supervisor} onChange={e=>setForm({...form,supervisor:e.target.value})}>
                <option value="">Select supervisor</option>
                {supervisors.map(s=><option key={s.id} value={s.id}>{s.full_name||s.username}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-1">Resident / PG</label>
              <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.resident} onChange={e=>setForm({...form,resident:e.target.value})}>
                <option value="">Select resident</option>
                {residents.map(r=><option key={r.id} value={r.id}>{r.full_name||r.username}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input type="date" className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})} />
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
