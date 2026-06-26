'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseDepartment, UserbaseUser } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

interface LinkEntry {
  id: number;
  supervisor_user?: { id: number; username: string; full_name?: string };
  resident_user?: { id: number; username: string; full_name?: string };
  department?: { id: number; name: string };
  supervisor_user_id?: number;
  resident_user_id?: number;
  department_id?: number | null;
  start_date: string;
  active: boolean;
}

interface SupervisionForm {
  supervisor: string;
  resident: string;
  department_id: string;
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
    if (typeof data === 'string') return data;
    return JSON.stringify(data);
  }
  return fallback;
}

export default function SupervisionPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [links, setLinks] = useState<LinkEntry[]>([]);
  const [users, setUsers] = useState<UserbaseUser[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState<SupervisionForm>({ supervisor:'', resident:'', department_id:'', start_date:'', active: true });
  const [saving, setSaving] = useState(false);

  const load = () => Promise.all([
    userbaseApi.supervisionLinks.list(),
    userbaseApi.users.list(),
    userbaseApi.departments.list(),
  ]).then(([lData, uData, dData]) => {
    const arr = Array.isArray(lData) ? lData : (lData as PagedResponse<LinkEntry>).results || [];
    setLinks(arr);
    setUsers(uData);
    setDepartments(dData);
  }).catch((err: unknown)=>setError(getErrorMessage(err, 'Failed to load'))).finally(()=>setLoading(false));

  useEffect(() => { load(); }, []);

  const supervisors = users.filter(u=>u.role==='supervisor'||u.role==='faculty');
  const residents = users.filter(u=>u.role==='resident'||u.role==='pg');

  const save = async () => {
    setSaving(true);
    try {
      await userbaseApi.supervisionLinks.create({
        supervisor_user_id: Number(form.supervisor),
        resident_user_id: Number(form.resident),
        department_id: form.department_id ? Number(form.department_id) : null,
        start_date: form.start_date,
        active: form.active,
      });
      setShowModal(false);
      load();
    } catch (err: unknown) { setError(getErrorMessage(err)); }
    finally { setSaving(false); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="pg-page">
      <PageHeader
        title="Supervision Links"
        description="Maintain supervisor-to-resident assignments and effective dates."
        actions={
          canManage ? (
            <button onClick={()=>{setForm({supervisor:'',resident:'',department_id:'',start_date:'',active:true});setShowModal(true);}} className="pg-btn-primary">+ Add Link</button>
          ) : undefined
        }
      />
      {isReadonly && <ReadonlyNotice />}
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="bg-white border border-gray-200 rounded-lg overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Supervisor','Resident','Department','Start Date','Active'].map(h=><th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {links.map((l) => (
              <tr key={l.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{userName(l.supervisor_user) || userName(l.supervisor_user_id) || '—'}</td>
                <td className="px-4 py-2">{userName(l.resident_user) || userName(l.resident_user_id) || '—'}</td>
                <td className="px-4 py-2">{l.department?.name || (l.department_id ? String(l.department_id) : '—')}</td>
                <td className="px-4 py-2 text-gray-500">{l.start_date||'—'}</td>
                <td className="px-4 py-2">{l.active?<span className="text-green-600">Yes</span>:<span className="text-gray-400">No</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">Add Supervision Link</h2>
            <div className="mb-3">
              <label className="pg-form-label" htmlFor="supervision-supervisor">Supervisor</label>
              <select id="supervision-supervisor" className="pg-form-input" value={form.supervisor} onChange={e=>setForm({...form,supervisor:e.target.value})}>
                <option value="">Select supervisor</option>
                {supervisors.map(s=><option key={s.id} value={s.id}>{s.full_name||s.username}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="pg-form-label" htmlFor="supervision-resident">Resident / PG</label>
              <select id="supervision-resident" className="pg-form-input" value={form.resident} onChange={e=>setForm({...form,resident:e.target.value})}>
                <option value="">Select resident</option>
                {residents.map(r=><option key={r.id} value={r.id}>{r.full_name||r.username}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="pg-form-label" htmlFor="supervision-department">Department</label>
              <select id="supervision-department" className="pg-form-input" value={form.department_id} onChange={e=>setForm({...form,department_id:e.target.value})}>
                <option value="">Optional</option>
                {departments.map(d=><option key={d.id} value={d.id}>{d.name}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="pg-form-label" htmlFor="supervision-start-date">Start Date</label>
              <input id="supervision-start-date" type="date" className="pg-form-input" value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})} />
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
