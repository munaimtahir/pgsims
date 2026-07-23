'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi } from '@/lib/api/academics';

interface StatsMap {
  SUBMITTED?: number;
  APPROVED?: number;
  VERIFIED?: number;
}

interface MonitoringDashboardData {
  total_residents?: number;
  residents_without_training_record?: number;
  residents_without_primary_supervisor?: number;
  data_quality_issue_count?: number;
  approved_evaluations?: number;
  verified_logbooks?: number;
  eval_stats?: StatsMap;
  log_stats?: StatsMap;
}

interface BreakdownRow {
  department_id?: number;
  program_id?: number;
  session_id?: number;
  name: string;
  code: string;
  active_residents: number;
  supervisors?: number;
  training_records: number;
  pending_evaluations: number;
  pending_logbooks: number;
}

export default function AdminMonitoringPage() {
  const [dashboard, setDashboard] = useState<MonitoringDashboardData | null>(null);
  const [departments, setDepartments] = useState<BreakdownRow[]>([]);
  const [programs, setPrograms] = useState<BreakdownRow[]>([]);
  const [sessions, setSessions] = useState<BreakdownRow[]>([]);
  
  const [activeTab, setActiveTab] = useState<'departments' | 'programs' | 'sessions'>('departments');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      academicsApi.getAdminDashboardMonitoring(),
      academicsApi.getDepartmentMonitoringSummary(),
      academicsApi.getProgramMonitoringSummary(),
      academicsApi.getSessionMonitoringSummary(),
    ])
      .then(([dash, depts, progs, sess]) => {
        setDashboard(dash as unknown as MonitoringDashboardData);
        setDepartments(depts as unknown as BreakdownRow[]);
        setPrograms(progs as unknown as BreakdownRow[]);
        setSessions(sess as unknown as BreakdownRow[]);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center py-8 text-sm text-slate-500">Loading monitoring data...</div>;
  }

  const evalStats = dashboard?.eval_stats || {};
  const logStats = dashboard?.log_stats || {};

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Academic Operations Monitoring"
          description="Global administrative dashboard tracking postgraduate coverage, review queues, and academic quality warning indicators."
        />

        <div className="pg-kpi-grid md:grid-cols-4">
          <MetricCard label="Total Residents" value={dashboard?.total_residents || 0} />
          <MetricCard
            label="Residents w/o Training Spine"
            value={dashboard?.residents_without_training_record || 0}
            tone={dashboard?.residents_without_training_record && dashboard.residents_without_training_record > 0 ? 'warning' : 'default'}
          />
          <MetricCard
            label="Residents w/o Primary Supervisor"
            value={dashboard?.residents_without_primary_supervisor || 0}
            tone={dashboard?.residents_without_primary_supervisor && dashboard.residents_without_primary_supervisor > 0 ? 'warning' : 'default'}
          />
          <MetricCard
            label="Data Quality Warnings"
            value={dashboard?.data_quality_issue_count || 0}
            tone={dashboard?.data_quality_issue_count && dashboard.data_quality_issue_count > 0 ? 'warning' : 'default'}
          />
        </div>

        {/* Workflow Stats Cards */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Evaluations Status */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Evaluations Status</h2>
            <div className="grid grid-cols-2 gap-4 text-center">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <div className="text-2xl font-bold text-slate-800">{dashboard?.approved_evaluations || 0}</div>
                <div className="text-xs text-slate-500 font-medium">Approved / Verified</div>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <div className="text-2xl font-bold text-slate-800">{evalStats.SUBMITTED || 0}</div>
                <div className="text-xs text-slate-500 font-medium">Pending Review</div>
              </div>
            </div>
          </div>

          {/* Logbooks Status */}
          <div className="pg-card space-y-4">
            <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-2">Logbook Status</h2>
            <div className="grid grid-cols-2 gap-4 text-center">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <div className="text-2xl font-bold text-slate-800">{dashboard?.verified_logbooks || 0}</div>
                <div className="text-xs text-slate-500 font-medium">Verified by Supervisor</div>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <div className="text-2xl font-bold text-slate-800">{logStats.SUBMITTED || 0}</div>
                <div className="text-xs text-slate-500 font-medium">Pending Verification</div>
              </div>
            </div>
          </div>
        </div>

        {/* Aggregated Breakdown Tabs */}
        <div className="pg-card space-y-4">
          <div className="flex border-b border-slate-200">
            <button
              onClick={() => setActiveTab('departments')}
              className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-all ${
                activeTab === 'departments'
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              Departments Breakdown
            </button>
            <button
              onClick={() => setActiveTab('programs')}
              className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-all ${
                activeTab === 'programs'
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              Programs Breakdown
            </button>
            <button
              onClick={() => setActiveTab('sessions')}
              className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-all ${
                activeTab === 'sessions'
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              Sessions Breakdown
            </button>
          </div>

          <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-xs uppercase text-slate-600 font-semibold">
                {activeTab === 'departments' && (
                  <tr>
                    <th className="px-4 py-3 text-left">Department</th>
                    <th className="px-4 py-3 text-left">Active Residents</th>
                    <th className="px-4 py-3 text-left">Supervisors</th>
                    <th className="px-4 py-3 text-left">Spine Records</th>
                    <th className="px-4 py-3 text-left">Pending Evals</th>
                    <th className="px-4 py-3 text-left">Pending Logbooks</th>
                  </tr>
                )}
                {activeTab === 'programs' && (
                  <tr>
                    <th className="px-4 py-3 text-left">Program</th>
                    <th className="px-4 py-3 text-left">Active Residents</th>
                    <th className="px-4 py-3 text-left">Spine Records</th>
                    <th className="px-4 py-3 text-left">Pending Evals</th>
                    <th className="px-4 py-3 text-left">Pending Logbooks</th>
                  </tr>
                )}
                {activeTab === 'sessions' && (
                  <tr>
                    <th className="px-4 py-3 text-left">Academic Session</th>
                    <th className="px-4 py-3 text-left">Active Residents</th>
                    <th className="px-4 py-3 text-left">Spine Records</th>
                    <th className="px-4 py-3 text-left">Pending Evals</th>
                    <th className="px-4 py-3 text-left">Pending Logbooks</th>
                  </tr>
                )}
              </thead>
              <tbody className="divide-y divide-gray-100">
                {activeTab === 'departments' &&
                  departments.map((dept) => (
                    <tr key={dept.department_id}>
                      <td className="px-4 py-3 font-semibold text-slate-800">{dept.name} ({dept.code})</td>
                      <td className="px-4 py-3">{dept.active_residents}</td>
                      <td className="px-4 py-3">{dept.supervisors || 0}</td>
                      <td className="px-4 py-3">{dept.training_records}</td>
                      <td className="px-4 py-3 text-amber-600 font-medium">{dept.pending_evaluations}</td>
                      <td className="px-4 py-3 text-amber-600 font-medium">{dept.pending_logbooks}</td>
                    </tr>
                  ))}
                {activeTab === 'programs' &&
                  programs.map((prog) => (
                    <tr key={prog.program_id}>
                      <td className="px-4 py-3 font-semibold text-slate-800">{prog.name} ({prog.code})</td>
                      <td className="px-4 py-3">{prog.active_residents}</td>
                      <td className="px-4 py-3">{prog.training_records}</td>
                      <td className="px-4 py-3 text-amber-600 font-medium">{prog.pending_evaluations}</td>
                      <td className="px-4 py-3 text-amber-600 font-medium">{prog.pending_logbooks}</td>
                    </tr>
                  ))}
                {activeTab === 'sessions' &&
                  sessions.map((sess) => (
                    <tr key={sess.session_id}>
                      <td className="px-4 py-3 font-semibold text-slate-800">{sess.name} ({sess.code})</td>
                      <td className="px-4 py-3">{sess.active_residents}</td>
                      <td className="px-4 py-3">{sess.training_records}</td>
                      <td className="px-4 py-3 text-amber-600 font-medium">{sess.pending_evaluations}</td>
                      <td className="px-4 py-3 text-amber-600 font-medium">{sess.pending_logbooks}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
