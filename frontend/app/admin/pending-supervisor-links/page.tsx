'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import apiClient from '@/lib/api/client';

type Pending = { id: number; resident: string; program?: string; department?: string; supervisor_name: string; status: string; created_at: string };
type Supervisor = { id: number; user?: { full_name?: string; username: string } };
export default function PendingSupervisorLinksPage() {
  const [rows, setRows] = useState<Pending[]>([]);
  const [supervisors, setSupervisors] = useState<Supervisor[]>([]);
  const [selected, setSelected] = useState<Record<number, string>>({});
  const [creating, setCreating] = useState<number | null>(null);
  const [error, setError] = useState('');
  const load = () => apiClient.get<Pending[]>('/api/pending-supervisor-links/').then((r) => setRows(r.data));
  useEffect(() => { load(); apiClient.get<{ results?: Supervisor[] } | Supervisor[]>('/api/supervisors/').then((r) => setSupervisors(Array.isArray(r.data) ? r.data : r.data.results || [])); }, []);
  const resolve = async (id: number) => { if (!selected[id]) return; setError(''); try { await apiClient.post(`/api/pending-supervisor-links/${id}/resolve/`, { supervisor_id: Number(selected[id]) }); await load(); } catch { setError('Unable to link supervisor.'); } };
  const createSupervisor = async (row: Pending) => { setError(''); try { await apiClient.post(`/api/pending-supervisor-links/${row.id}/create-supervisor/`, { full_name: row.supervisor_name }); await load(); } catch { setError('Unable to create and link supervisor. Complete the supervisor profile from Supervisors if more details are required.'); } finally { setCreating(null); } };
  return <ProtectedRoute allowedRoles={['ADMIN']}><div className="pg-page space-y-6"><PageHeader title="Pending Supervisor Links" description="Resolve names captured during resident creation without creating fake supervisor identities." />{error && <p className="text-sm text-red-600">{error}</p>}<div className="overflow-x-auto pg-card"><table className="min-w-full text-sm"><thead><tr className="text-left"><th className="p-2">Resident</th><th className="p-2">Program</th><th className="p-2">Department</th><th className="p-2">Entered name</th><th className="p-2">Status</th><th className="p-2">Created</th><th className="p-2">Action</th></tr></thead><tbody>{rows.map((row) => <tr key={row.id} className="border-t"><td className="p-2">{row.resident}</td><td className="p-2">{row.program || '—'}</td><td className="p-2">{row.department || '—'}</td><td className="p-2">{row.supervisor_name}</td><td className="p-2">{row.status}</td><td className="p-2">{new Date(row.created_at).toLocaleDateString()}</td><td className="p-2"><div className="flex flex-wrap gap-2"><select className="pg-form-input" value={selected[row.id] || ''} onChange={(e) => setSelected({ ...selected, [row.id]: e.target.value })}><option value="">Link existing…</option>{supervisors.map((s) => <option key={s.id} value={s.id}>{s.user?.full_name || s.user?.username || `Supervisor #${s.id}`}</option>)}</select><button className="pg-button-secondary" onClick={() => resolve(row.id)}>Link</button><button className="pg-button-secondary" disabled={creating === row.id} onClick={() => { setCreating(row.id); void createSupervisor(row); }}>{creating === row.id ? 'Creating…' : 'Create Supervisor'}</button></div></td></tr>)}</tbody></table>{rows.length === 0 && <p className="py-6 text-sm text-slate-500">No pending supervisor links.</p>}</div></div></ProtectedRoute>;
}
