'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import { trainingApi, ResidentTrainingRecordListItem, UTRMCOperationalDashboard } from '@/lib/api/training';
import { userbaseApi, UserbaseUser, UserbaseDepartment, UserbaseHospitalDepartment, UserbaseHodAssignment } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

function countUniquePrograms(records: ResidentTrainingRecordListItem[]): number {
  return new Set(records.map((record) => record.program)).size;
}

export default function UTRMCOverviewPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);

  const [users, setUsers] = useState<UserbaseUser[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [matrix, setMatrix] = useState<UserbaseHospitalDepartment[]>([]);
  const [hodAssignments, setHodAssignments] = useState<UserbaseHodAssignment[]>([]);
  const [trainingRecords, setTrainingRecords] = useState<ResidentTrainingRecordListItem[]>([]);
  const [opsDashboard, setOpsDashboard] = useState<UTRMCOperationalDashboard | null>(null);
  const [, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dataQualitySummary, setDataQualitySummary] = useState<{ incomplete_profiles: number } | null>(null);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [usersData, departmentsData, matrixData, hodData, recordsData, dashboardData, qualityData] = await Promise.all([
        userbaseApi.users.list(),
        userbaseApi.departments.list(),
        userbaseApi.matrix.list(),
        userbaseApi.hodAssignments.list(),
        trainingApi.listResidentTrainingRecords(),
        trainingApi.getUTRMCOperationalDashboard().catch(() => null),
        userbaseApi.dataQuality.summary().catch(() => null),
      ]);
      setUsers(usersData);
      setDepartments(departmentsData);
      setMatrix(matrixData);
      setHodAssignments(hodData);
      setTrainingRecords(recordsData);
      setOpsDashboard(dashboardData);
      setDataQualitySummary(qualityData ? { incomplete_profiles: qualityData.incomplete_profiles } : null);
    } catch {
      setError('Failed to load monitoring dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) return;
    void load();
  }, [user]);

  const residentRows = useMemo(
    () => users.filter((item) => item.role === 'resident' || item.role === 'pg'),
    [users]
  );
  const activeResidents = residentRows.filter((item) => item.is_active).length;
  const residentIdsWithProgramme = new Set(trainingRecords.filter((record) => record.active).map((record) => record.resident_user));
  const residentsWithoutProgramme = residentRows.filter((item) => !residentIdsWithProgramme.has(item.id)).length;
  const residentsWithoutSupervisor = residentRows.filter((item) => !item.supervisor).length;
  const activeHodDepartmentIds = new Set(hodAssignments.filter((item) => item.active).map((item) => item.department.id));
  const missingHodAssignments = departments.filter((department) => !activeHodDepartmentIds.has(department.id)).length;
  const pendingReviews = (opsDashboard?.pending_synopsis_reviews || 0)
    + (opsDashboard?.pending_thesis_reviews || 0)
    + (opsDashboard?.pending_rotation_completion_verifications || 0);

  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="UTRMC Dashboard"
          description="Monitoring-only summary for onboarding, coverage, and readiness. Operational work has dedicated pages."
        />
        {isReadonly && <ReadonlyNotice />}
        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard label="Active Residents" value={String(activeResidents)} hint="Resident / PG accounts" />
          <MetricCard label="Residents Without Programme" value={String(residentsWithoutProgramme)} hint="Need assignment" />
          <MetricCard label="Residents Without Supervisor" value={String(residentsWithoutSupervisor)} hint="Need supervision link" />
          <MetricCard label="Missing HOD Assignments" value={String(missingHodAssignments)} hint="Department heads to assign" />
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard label="Pending Reviews" value={String(pendingReviews)} hint="Synopsis + thesis + completion queue" />
          <MetricCard label="Programmes" value={String(countUniquePrograms(trainingRecords))} hint="Active training programmes in use" />
          <MetricCard label="Matrix Links" value={String(matrix.filter((item) => item.active).length)} hint="Hospital-department placements" />
          <MetricCard
            label="Data Quality"
            value={dataQualitySummary ? String(dataQualitySummary.incomplete_profiles) : '—'}
            hint={dataQualitySummary ? 'Incomplete resident profiles' : 'Not loaded'}
          />
        </div>

        <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Quick Links</h2>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <Link href="/dashboard/onboarding/residents" className="rounded-xl border border-slate-200 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
                <div className="font-semibold text-slate-900">Resident Onboarding</div>
                <div className="text-sm text-slate-500">Import residents and generate login IDs.</div>
              </Link>
              <Link href="/dashboard/utrmc/resident-training" className="rounded-xl border border-slate-200 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
                <div className="font-semibold text-slate-900">Resident Programme Assignment</div>
                <div className="text-sm text-slate-500">Assign residents to programmes or courses.</div>
              </Link>
              <Link href="/dashboard/utrmc/supervision" className="rounded-xl border border-slate-200 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
                <div className="font-semibold text-slate-900">Supervision Links</div>
                <div className="text-sm text-slate-500">Maintain supervisor-to-resident coverage.</div>
              </Link>
              <Link href="/dashboard/utrmc/hod" className="rounded-xl border border-slate-200 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
                <div className="font-semibold text-slate-900">HOD Assignments</div>
                <div className="text-sm text-slate-500">Review departmental heads.</div>
              </Link>
              <Link href="/dashboard/utrmc/data-quality" className="rounded-xl border border-slate-200 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
                <div className="font-semibold text-slate-900">Data Quality</div>
                <div className="text-sm text-slate-500">Monitor incomplete profiles and data issues.</div>
              </Link>
              <Link href="/dashboard/utrmc/backup" className="rounded-xl border border-slate-200 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
                <div className="font-semibold text-slate-900">Backup Center</div>
                <div className="text-sm text-slate-500">Check backup health and restore status.</div>
              </Link>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Readiness Snapshot</h2>
            <div className="mt-4 space-y-3 text-sm text-slate-600">
              <p>Active programmes tracked: <span className="font-medium text-slate-900">{countUniquePrograms(trainingRecords)}</span></p>
              <p>Departments loaded: <span className="font-medium text-slate-900">{departments.length}</span>, with <span className="font-medium text-slate-900">{matrix.filter((item) => item.active).length}</span> active hospital links</p>
              <p>Onboarding gaps: <span className="font-medium text-slate-900">{residentsWithoutProgramme}</span> without programme, <span className="font-medium text-slate-900">{residentsWithoutSupervisor}</span> without supervisor</p>
              <p>Oversight gaps: <span className="font-medium text-slate-900">{missingHodAssignments}</span> departments missing HOD coverage</p>
            </div>
          </div>
        </div>

        {canManage && (
          <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
            Monitoring note: operational setup workflows live on their own pages. The dashboard should remain a summary surface only.
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
