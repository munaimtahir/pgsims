'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { AlertTriangle, ArrowRight, ClipboardCheck, FilePlus2, GraduationCap, Link2, RefreshCw, ShieldAlert, Users, UserRound } from 'lucide-react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import LoadingSkeleton from '@/components/ui/LoadingSkeleton';
import { academicsApi } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

type DashboardData = { total_users?: number; total_residents?: number; active_residents?: number; supervisor_users?: number; support_staff_users?: number; residents_without_training_record?: number; residents_without_primary_supervisor?: number; pending_supervisor_reviews?: number; pending_supervisor_links?: number; overdue_supervisor_reviews?: number; data_quality_issue_count?: number; residents_with_training_record?: number; pending_review_queue_items?: number; active_training_records?: number; };
type Tone = 'blue' | 'amber' | 'red' | 'green';
const metrics = [
  { key: 'active_residents', label: 'Residents', hint: 'Active postgraduate trainees', href: '/residents', icon: GraduationCap, tone: 'blue' as Tone },
  { key: 'supervisor_users', label: 'Supervisors', hint: 'Registered supervisors', href: '/supervisors', icon: UserRound, tone: 'green' as Tone },
  { key: 'pending_supervisor_reviews', label: 'Pending reviews', hint: 'Awaiting supervisor action', href: '/academics/review-queue', icon: ClipboardCheck, tone: 'amber' as Tone },
  { key: 'residents_without_primary_supervisor', label: 'Supervision alerts', hint: 'Residents needing attention', href: '/supervision/data-quality', icon: ShieldAlert, tone: 'red' as Tone },
];

function value(data: DashboardData, key: string) { return Number(data[key as keyof DashboardData] ?? 0); }
function Metric({ item, data }: { item: (typeof metrics)[number]; data: DashboardData }) { const Icon = item.icon; return <Link href={item.href} className="pg-dashboard-card group p-5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"><div className="flex items-start justify-between"><span className={`flex h-11 w-11 items-center justify-center rounded-xl ${item.tone === 'red' ? 'bg-red-50 text-red-600' : item.tone === 'amber' ? 'bg-amber-50 text-amber-600' : item.tone === 'green' ? 'bg-emerald-50 text-emerald-600' : 'bg-blue-50 text-blue-600'}`}><Icon className="h-5 w-5" aria-hidden="true" /></span><ArrowRight className="h-4 w-4 text-slate-300 transition group-hover:translate-x-1 group-hover:text-blue-500" /></div><p className="mt-5 text-3xl font-bold tracking-tight text-slate-900">{value(data, item.key)}</p><p className="mt-1 font-semibold text-slate-800">{item.label}</p><p className="mt-1 text-xs text-slate-500">{item.hint}</p></Link>; }

export default function UTRMCOverviewPage() {
  const { user } = useAuthStore(); const [data, setData] = useState<DashboardData | null>(null); const [error, setError] = useState(false); const [loading, setLoading] = useState(true);
  const load = () => { setLoading(true); setError(false); academicsApi.getAdminDashboardMonitoring().then((result) => setData(result as DashboardData)).catch(() => setError(true)).finally(() => setLoading(false)); };
  useEffect(() => { if (user?.role === 'ADMIN') load(); else setLoading(false); }, [user?.role]);
  if (user?.role === 'SUPPORT_STAFF') return <ProtectedRoute allowedRoles={['ADMIN', 'SUPPORT_STAFF']}><div className="pg-page"><PageHeader title="Support workspace" description="Read-only tools for keeping postgraduate records organised." /><section className="pg-dashboard-card p-6"><h2 className="pg-section-title">Your account</h2><p className="mt-2 text-sm text-slate-600">Use your profile and password controls from the navigation.</p><Link href="/profile" className="pg-btn-primary mt-5 inline-flex">Open profile</Link></section></div></ProtectedRoute>;
  return <ProtectedRoute allowedRoles={['ADMIN', 'SUPPORT_STAFF']}><div className="pg-page space-y-7"><PageHeader title="Admin Dashboard" description="A live view of postgraduate residency operations." badges={[{ label: 'Programme overview', tone: 'info' }]} actions={<span className="hidden text-xs text-slate-500 sm:block">Home / Dashboard / Admin</span>} />
    {loading && <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><div className="pg-dashboard-card p-5 sm:col-span-2 xl:col-span-4"><LoadingSkeleton lines={4} /></div></div>}
    {error && <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-5 text-red-800"><div className="flex items-start gap-3"><AlertTriangle className="mt-0.5 h-5 w-5" /><div><p className="font-semibold">Unable to load the dashboard</p><p className="mt-1 text-sm">The live programme summary could not be retrieved.</p><button type="button" onClick={load} className="mt-3 inline-flex items-center gap-2 rounded-lg bg-red-700 px-3 py-2 text-sm font-semibold text-white hover:bg-red-800"><RefreshCw className="h-4 w-4" /> Try again</button></div></div></div>}
    {!loading && !error && data && <><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{metrics.map((item) => <Metric key={item.key} item={item} data={data} />)}</div>
      <div className="grid gap-6 xl:grid-cols-[1.45fr_1fr]"><section className="pg-dashboard-card p-6"><div className="flex items-center justify-between"><div><h2 className="pg-section-title">Needs attention</h2><p className="pg-section-note">Prioritised work surfaced from programme data.</p></div><AlertTriangle className="h-5 w-5 text-amber-500" aria-hidden="true" /></div><div className="mt-5 divide-y divide-slate-100">{[
        { label: 'Residents without training record', count: value(data, 'residents_without_training_record'), href: '/academics/data-quality', tone: 'amber' },
        { label: 'Pending supervisor links', count: value(data, 'pending_supervisor_links'), href: '/admin/pending-supervisor-links', tone: 'blue' },
        { label: 'Review queue', count: value(data, 'pending_supervisor_reviews'), href: '/academics/review-queue', tone: 'amber' },
        { label: 'Data quality issues', count: value(data, 'data_quality_issue_count'), href: '/academics/data-quality', tone: 'red' },
      ].map((item) => <Link key={item.label} href={item.href} className="flex items-center gap-3 py-4 group"><span className={`h-2.5 w-2.5 rounded-full ${item.tone === 'red' ? 'bg-red-500' : item.tone === 'amber' ? 'bg-amber-500' : 'bg-blue-500'}`} /><span className="flex-1 text-sm font-medium text-slate-700">{item.label}</span><span className="mr-3 rounded-full bg-slate-100 px-2.5 py-1 text-sm font-bold text-slate-800">{item.count}</span><ArrowRight className="h-4 w-4 text-slate-300 group-hover:text-blue-500" /></Link>)}</div></section>
        <section className="pg-dashboard-card p-6"><h2 className="pg-section-title">Quick actions</h2><p className="pg-section-note">Common administration tasks.</p><div className="mt-5 space-y-2">{[
          { label: 'Add resident', href: '/users/new?role=RESIDENT', icon: GraduationCap }, { label: 'Add supervisor', href: '/users/new?role=SUPERVISOR', icon: UserRound }, { label: 'Review documents', href: '/residents/document-requirements', icon: FilePlus2 }, { label: 'Manage users', href: '/users', icon: Users },
        ].map((item) => { const Icon = item.icon; return <Link key={item.label} href={item.href} className="flex items-center gap-3 rounded-xl border border-slate-200 px-3 py-3 text-sm font-semibold text-slate-700 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"><Icon className="h-4 w-4" />{item.label}<ArrowRight className="ml-auto h-4 w-4" /></Link>; })}</div></section></div>
      <section className="pg-dashboard-card p-6"><div className="flex items-center gap-3"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600"><Link2 className="h-5 w-5" /></span><div><h2 className="pg-section-title">Programme health</h2><p className="pg-section-note">Coverage indicators from the academic monitoring service.</p></div></div><div className="mt-5 grid gap-4 sm:grid-cols-3"><div><p className="text-2xl font-bold text-slate-900">{value(data, 'total_users')}</p><p className="text-sm text-slate-500">Active users</p></div><div><p className="text-2xl font-bold text-slate-900">{value(data, 'residents_with_training_record')}</p><p className="text-sm text-slate-500">Residents with training records</p></div><div><p className="text-2xl font-bold text-slate-900">{value(data, 'active_training_records')}</p><p className="text-sm text-slate-500">Active training records</p></div></div></section></>}
  </div></ProtectedRoute>;
}
