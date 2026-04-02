'use client';
import { useEffect, useState } from 'react';
import { userbaseApi, UserbaseUser, UserbaseDepartment } from '@/lib/api/userbase';

interface HodEntry {
  id: number;
  department: number | { id: number; name: string };
  hod: number | { id: number; username: string; full_name?: string };
  start_date: string;
  active: boolean;
}

interface NamedEntity {
  id?: number;
  username?: string;
  full_name?: string;
  name?: string;
}

interface HodForm {
  department: string;
  hod: string;
  start_date: string;
}

interface PagedResponse<T> {
  results?: T[];
}

function getName(u: number | NamedEntity | undefined): string {
  if (!u) return '';
  if (typeof u === 'object') return u.full_name || u.name || u.username || String(u.id || '');
  return String(u);
}

export default function HodPage() {
  const [assignments, setAssignments] = useState<HodEntry[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [users, setUsers] = useState<UserbaseUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState<HodForm>({ department:'', hod:'', start_date:'' });
  const [saving, setSaving] = useState(false);

  const load = () => Promise.all([
    userbaseApi.hodAssignments.list(),
    userbaseApi.departments.list(),
    userbaseApi.users.list(),
  ]).then(([aData, dData, uData]) => {
    const arr = Array.isArray(aData) ? aData : (aData as PagedResponse<HodEntry>).results || [];
    setAssignments(arr);
    setDepartments(dData);
    setUsers(uData);
  }).catch(()=>setError('Failed to load')).finally(()=>setLoading(false));

  useEffect(() => { load(); }, []);

  const faculty = users.filter(u=>u.role==='faculty'||u.role==='supervisor'||u.role==='admin');

  const save = async () => {
    setSaving(true);
    try {
      await userbaseApi.hodAssignments.create({ ...form, department: Number(form.department), hod: Number(form.hod) });
      setShowModal(false);
      load();
    } catch { setError('Save failed'); }
    finally { setSaving(false); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-900">HOD Assignments</h1>
        <button onClick={()=>{setForm({department:'',hod:'',start_date:''});setShowModal(true);}} className="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700">+ Add HOD</button>
      </div>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Department','HOD','Start Date','Active'].map(h=><th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {assignments.map((a) => (
              <tr key={a.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{getName(a.department)}</td>
                <td className="px-4 py-2">{getName(a.hod)}</td>
                <td className="px-4 py-2 text-gray-500">{a.start_date||'—'}</td>
                <td className="px-4 py-2">{a.active?<span className="text-green-600">Yes</span>:<span className="text-gray-400">No</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h2 className="text-lg font-semibold mb-4">Add HOD Assignment</h2>
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
              <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.department} onChange={e=>setForm({...form,department:e.target.value})}>
                <option value="">Select department</option>
                {departments.map(d=><option key={d.id} value={d.id}>{d.name}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-1">HOD User</label>
              <select className="w-full border border-gray-300 rounded px-3 py-2 text-sm" value={form.hod} onChange={e=>setForm({...form,hod:e.target.value})}>
                <option value="">Select HOD</option>
                {faculty.map(u=><option key={u.id} value={u.id}>{u.full_name||u.username}</option>)}
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
