'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseUser, UserbaseDepartment } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

interface HodEntry {
  id: number;
  department: number | { id: number; name: string };
  hod_user?: { id: number; username: string; full_name?: string };
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
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
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
      await userbaseApi.hodAssignments.create({
        department_id: Number(form.department),
        hod_user_id: Number(form.hod),
        start_date: form.start_date,
        active: true,
      });
      setShowModal(false);
      load();
    } catch { setError('Save failed'); }
    finally { setSaving(false); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="pg-page">
      <PageHeader
        title="HOD Assignments"
        description="Assign and review departmental head oversight relationships."
        actions={
          canManage ? (
            <button onClick={()=>{setForm({department:'',hod:'',start_date:''});setShowModal(true);}} className="pg-btn-primary">+ Add HOD</button>
          ) : undefined
        }
      />
      {isReadonly && <ReadonlyNotice />}
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="bg-white border border-gray-200 rounded-lg overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50"><tr>{['Department','HOD','Start Date','Active'].map(h=><th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr></thead>
          <tbody className="divide-y divide-gray-100">
            {assignments.map((a) => (
              <tr key={a.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{getName(a.department)}</td>
                <td className="px-4 py-2">{getName(a.hod_user)}</td>
                <td className="px-4 py-2 text-gray-500">{a.start_date||'—'}</td>
                <td className="px-4 py-2">{a.active?<span className="text-green-600">Yes</span>:<span className="text-gray-400">No</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">Add HOD Assignment</h2>
            <div className="mb-3">
              <label className="pg-form-label">Department</label>
              <select className="pg-form-input" value={form.department} onChange={e=>setForm({...form,department:e.target.value})}>
                <option value="">Select department</option>
                {departments.map(d=><option key={d.id} value={d.id}>{d.name}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="pg-form-label">HOD User</label>
              <select className="pg-form-input" value={form.hod} onChange={e=>setForm({...form,hod:e.target.value})}>
                <option value="">Select HOD</option>
                {faculty.map(u=><option key={u.id} value={u.id}>{u.full_name||u.username}</option>)}
              </select>
            </div>
            <div className="mb-3">
              <label className="pg-form-label">Start Date</label>
              <input type="date" className="pg-form-input" value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})} />
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
