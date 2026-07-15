'use client';

import { useEffect, useState } from 'react';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi, AcademicSummary } from '@/lib/api/academics';

export default function ResidentHomePage() {
  const [summary, setSummary] = useState<AcademicSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    academicsApi
      .getMyResidentSummary()
      .then((data) => {
        if (active) {
          setSummary(data);
        }
      })
      .catch(() => {
        if (active) {
          setSummary(null);
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  const trainingRecord = summary?.training_record;
  const primarySupervisor = summary?.supervision?.primary_supervisor?.supervisor;
  const coSupervisors = summary?.supervision?.co_supervisors || [];
  const readiness = summary?.readiness;

  return (
    <ProtectedRoute allowedRoles={['RESIDENT']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Resident Dashboard"
          description="Canonical resident shell for training, supervision, and academic readiness."
        />

        {loading ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-500">
            Loading resident summary...
          </div>
        ) : (
          <>
            <div className="grid gap-4 md:grid-cols-3">
              <MetricCard label="Active Training Record" value={trainingRecord ? 'Yes' : 'No'} tone={trainingRecord ? 'success' : 'warning'} />
              <MetricCard label="Primary Supervisor" value={primarySupervisor ? 'Assigned' : 'Missing'} tone={primarySupervisor ? 'success' : 'warning'} />
              <MetricCard label="Pending Review Items" value={summary?.review_queue?.pending_count || 0} />
            </div>

            <section className="grid gap-4 md:grid-cols-2">
              <div className="pg-card">
                <h2 className="pg-section-title">My Training</h2>
                <div className="mt-3 space-y-2 text-sm text-slate-600">
                  <p>Program: {trainingRecord?.program.name || 'Not linked yet'}</p>
                  <p>Academic session: {trainingRecord?.academic_session.name || 'Not set'}</p>
                  <p>Training year: {trainingRecord?.training_year || 'Not set'}</p>
                  <p>Department: {trainingRecord?.department.name || 'Not set'}</p>
                  <p>Training site: {trainingRecord?.training_site.name || 'Not set'}</p>
                  <p>Start date: {trainingRecord?.start_date || 'Not set'}</p>
                  <p>Expected end date: {trainingRecord?.expected_end_date || 'Not set'}</p>
                </div>
              </div>

              <div className="pg-card">
                <h2 className="pg-section-title">My Supervisor</h2>
                <div className="mt-3 space-y-2 text-sm text-slate-600">
                  <p>Primary supervisor: {primarySupervisor?.name || 'Not assigned'}</p>
                  <p>Designation: {primarySupervisor?.designation || 'Not set'}</p>
                  <p>Department: {primarySupervisor?.department || 'Not set'}</p>
                  <p>Contact email: {primarySupervisor?.email || 'Not available'}</p>
                  <p>Contact phone: {primarySupervisor?.phone || 'Not available'}</p>
                  <p>Co-supervisors: {coSupervisors.length}</p>
                </div>
              </div>
            </section>

            <section className="pg-card">
              <h2 className="pg-section-title">My Academic Summary</h2>
              <div className="mt-3 space-y-2 text-sm text-slate-600">
                <p>Has active training record: {readiness?.has_active_training_record ? 'Yes' : 'No'}</p>
                <p>Has primary supervisor: {readiness?.has_primary_supervisor ? 'Yes' : 'No'}</p>
                <p>
                  Missing items:{' '}
                  {readiness?.missing_items && readiness.missing_items.length > 0
                    ? readiness.missing_items.join(', ')
                    : 'None'}
                </p>
                <p className="pt-2 text-xs text-slate-500">
                  Evaluations, logbooks, and other academic workflows will attach to this training container in later bricks.
                </p>
              </div>
            </section>
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
