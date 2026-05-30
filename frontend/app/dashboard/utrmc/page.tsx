'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';

import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import WorkflowStatusBadge from '@/components/ui/WorkflowStatusBadge';
import { useAuthStore } from '@/store/authStore';
import {
  trainingApi,
  ResidentTrainingRecordListItem,
  RotationAssignment,
  UTRMCOperationalDashboard,
  ResidentSubmissionRecord,
  RotationCompletionRecord,
} from '@/lib/api/training';
import { userbaseApi, UserbaseHospitalDepartment, UserbaseUser } from '@/lib/api/userbase';

type RotationFormState = {
  resident_training: string;
  hospital_department: string;
  start_date: string;
  end_date: string;
  notes: string;
};

const EMPTY_ROTATION_FORM: RotationFormState = {
  resident_training: '',
  hospital_department: '',
  start_date: '',
  end_date: '',
  notes: '',
};

function RotationCard({
  rotation,
  actionLabel,
  actionTone = 'primary',
  actionBusy,
  onAction,
  helperText,
}: {
  rotation: RotationAssignment;
  actionLabel?: string;
  actionTone?: 'primary' | 'success';
  actionBusy?: boolean;
  onAction?: () => void;
  helperText?: string;
}) {
  const actionClassName = actionTone === 'success'
    ? 'pg-btn-success'
    : 'pg-btn-primary';

  return (
    <div className="pg-card">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <p className="font-semibold text-gray-900">{rotation.resident_name}</p>
          <p className="text-sm text-gray-500">
            {rotation.department_name} · {rotation.hospital_name}
          </p>
          <p className="text-sm text-gray-500">
            {rotation.start_date} → {rotation.end_date}
          </p>
          <p className="text-xs text-gray-400 mt-1">{rotation.program_name}</p>
        </div>
        <WorkflowStatusBadge status={rotation.status} />
      </div>

      {rotation.notes && (
        <p className="mt-3 text-sm text-gray-700">{rotation.notes}</p>
      )}

      {rotation.return_reason && (
        <div className="mt-3 bg-orange-50 border border-orange-200 text-orange-700 rounded-lg p-3 text-sm">
          <span className="font-medium">Returned:</span> {rotation.return_reason}
        </div>
      )}

      {rotation.reject_reason && (
        <div className="mt-3 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
          <span className="font-medium">Rejected:</span> {rotation.reject_reason}
        </div>
      )}

      {helperText && (
        <p className="mt-3 text-sm text-gray-500">{helperText}</p>
      )}

      {actionLabel && onAction && (
        <div className="mt-4">
          <button
            onClick={onAction}
            disabled={actionBusy}
            className={`disabled:opacity-50 ${actionClassName}`}
          >
            {actionBusy ? 'Processing…' : actionLabel}
          </button>
        </div>
      )}
    </div>
  );
}

function RotationSection({
  title,
  emptyText,
  children,
}: {
  title: string;
  emptyText: string;
  children: React.ReactNode;
}) {
  const items = Array.isArray(children) ? children : [children];

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold text-gray-800">{title}</h2>
      {items.filter(Boolean).length === 0 ? (
        <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-gray-200">
          {emptyText}
        </div>
      ) : (
        <div className="space-y-3">{children}</div>
      )}
    </section>
  );
}

export default function UTRMCOverviewPage() {
  const { user } = useAuthStore();
  const canManageRotations = user?.role === 'admin' || user?.role === 'utrmc_admin';

  const [stats, setStats] = useState({
    hospitals: 0,
    departments: 0,
    users: 0,
    supervisors: 0,
    residents: 0,
  });
  const [dqIncomplete, setDqIncomplete] = useState<number | null>(null);
  const [trainingRecords, setTrainingRecords] = useState<ResidentTrainingRecordListItem[]>([]);
  const [placements, setPlacements] = useState<UserbaseHospitalDepartment[]>([]);
  const [rotations, setRotations] = useState<RotationAssignment[]>([]);
  const [opsDashboard, setOpsDashboard] = useState<UTRMCOperationalDashboard | null>(null);
  const [pendingSynopsis, setPendingSynopsis] = useState<ResidentSubmissionRecord[]>([]);
  const [pendingThesis, setPendingThesis] = useState<ResidentSubmissionRecord[]>([]);
  const [pendingCompletions, setPendingCompletions] = useState<RotationCompletionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [savingRotation, setSavingRotation] = useState(false);
  const [actingRotationId, setActingRotationId] = useState<number | null>(null);
  const [processingSubmissionId, setProcessingSubmissionId] = useState<number | null>(null);
  const [processingCompletionId, setProcessingCompletionId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [rotationForm, setRotationForm] = useState<RotationFormState>(EMPTY_ROTATION_FORM);

  const flash = (nextMessage: string, isError = false) => {
    if (isError) {
      setError(nextMessage);
    } else {
      setMessage(nextMessage);
    }

    window.setTimeout(() => {
      setError('');
      setMessage('');
    }, 4000);
  };

  const load = async () => {
    setLoading(true);
    setError('');

    try {
      const hospitalsPromise = userbaseApi.hospitals.list();
      const departmentsPromise = userbaseApi.departments.list();
      const usersPromise = userbaseApi.users.list();
      const managePromises = canManageRotations
        ? Promise.all([
          trainingApi.listResidentTrainingRecords(),
          userbaseApi.matrix.list(),
          trainingApi.listRotations(),
          trainingApi.getUTRMCOperationalDashboard().catch(() => null),
          trainingApi.getSynopsisReviewQueue().catch(() => ({ count: 0, results: [] })),
          trainingApi.getThesisReviewQueue().catch(() => ({ count: 0, results: [] })),
          trainingApi.listRotationCompletions({ status: 'PENDING_UTRMC_VERIFICATION' }).catch(() => ({ count: 0, results: [] })),
        ])
        : Promise.resolve<
            [
              ResidentTrainingRecordListItem[],
              UserbaseHospitalDepartment[],
              RotationAssignment[],
              UTRMCOperationalDashboard | null,
              { count: number; results: ResidentSubmissionRecord[] },
              { count: number; results: ResidentSubmissionRecord[] },
              { count: number; results: RotationCompletionRecord[] },
            ]
          >([
          [],
          [],
          [],
          null,
          { count: 0, results: [] },
          { count: 0, results: [] },
          { count: 0, results: [] },
        ]);

      const [
        hospitals,
        departments,
        users,
        [records, matrix, rotationRows, nextOpsDashboard, nextSynopsis, nextThesis, nextCompletions],
      ] = await Promise.all([
        hospitalsPromise,
        departmentsPromise,
        usersPromise,
        managePromises,
      ]);

      const userRows = users as UserbaseUser[];
      setStats({
        hospitals: hospitals.length,
        departments: departments.length,
        users: userRows.length,
        supervisors: userRows.filter((item) => item.role === 'supervisor').length,
        residents: userRows.filter((item) => item.role === 'resident' || item.role === 'pg').length,
      });

      setTrainingRecords(records.filter((item) => item.active));
      setPlacements(matrix.filter((item) => item.active));
      setRotations(rotationRows);
      setOpsDashboard(nextOpsDashboard);
      setPendingSynopsis(nextSynopsis.results || []);
      setPendingThesis(nextThesis.results || []);
      setPendingCompletions(nextCompletions.results || []);
      if (canManageRotations) {
        userbaseApi.dataQuality
          .summary()
          .then((dq) => setDqIncomplete(dq.incomplete_profiles))
          .catch(() => setDqIncomplete(null));
      }
    } catch {
      setError('Failed to load UTRMC overview.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) {
      return;
    }

    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const createRotation = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!canManageRotations) {
      return;
    }

    setSavingRotation(true);
    setError('');

    try {
      await trainingApi.createRotation({
        resident_training: Number(rotationForm.resident_training),
        hospital_department: Number(rotationForm.hospital_department),
        start_date: rotationForm.start_date,
        end_date: rotationForm.end_date,
        notes: rotationForm.notes || undefined,
      });
      setRotationForm(EMPTY_ROTATION_FORM);
      flash('Rotation draft created.');
      await load();
    } catch {
      flash('Failed to create rotation draft.', true);
    } finally {
      setSavingRotation(false);
    }
  };

  const runRotationAction = async (
    rotationId: number,
    action: 'activate' | 'complete',
    successMessage: string
  ) => {
    setActingRotationId(rotationId);
    setError('');

    try {
      await trainingApi.rotationAction(rotationId, action);
      flash(successMessage);
      await load();
    } catch {
      flash(`Failed to ${action} rotation.`, true);
    } finally {
      setActingRotationId(null);
    }
  };

  const verifySubmission = async (
    submissionType: 'SYNOPSIS' | 'THESIS',
    submissionId: number
  ) => {
    setProcessingSubmissionId(submissionId);
    try {
      if (submissionType === 'SYNOPSIS') {
        await trainingApi.reviewSynopsisSubmission(submissionId, 'verify');
      } else {
        await trainingApi.reviewThesisSubmission(submissionId, 'verify');
      }
      flash(`${submissionType.toLowerCase()} submission verified.`);
      await load();
    } catch {
      flash(`Failed to verify ${submissionType.toLowerCase()} submission.`, true);
    } finally {
      setProcessingSubmissionId(null);
    }
  };

  const verifyCompletion = async (completionId: number) => {
    setProcessingCompletionId(completionId);
    try {
      await trainingApi.verifyRotationCompletion(completionId);
      flash('Rotation completion verified.');
      await load();
    } catch {
      flash('Failed to verify rotation completion.', true);
    } finally {
      setProcessingCompletionId(null);
    }
  };

  const draftRotations = rotations.filter((item) => item.status === 'DRAFT');
  const submittedRotations = rotations.filter((item) => item.status === 'SUBMITTED');
  const approvedRotations = rotations.filter((item) => item.status === 'APPROVED');
  const activeRotations = rotations.filter((item) => item.status === 'ACTIVE');
  const returnedRotations = rotations.filter((item) => item.status === 'RETURNED');
  const rejectedRotations = rotations.filter((item) => item.status === 'REJECTED');
  const completedRotations = rotations.filter((item) => item.status === 'COMPLETED').slice(0, 5);

  const cards = [
    { label: 'Residents', value: stats.residents },
    { label: 'Supervisors', value: stats.supervisors },
    { label: 'Departments', value: stats.departments },
    { label: 'Programs', value: opsDashboard?.cross_department_overview.program_count ?? 0 },
    {
      label: 'Pending setup issues',
      value: dqIncomplete ?? 0,
      tone: dqIncomplete === null ? 'default' : dqIncomplete > 0 ? 'warning' : 'success',
    },
  ];

  const dashboardStatus = (() => {
    if (stats.hospitals === 0 && stats.departments === 0 && stats.users === 0) {
      return { label: 'Clean baseline', tone: 'success' as const };
    }
    if ((dqIncomplete ?? 0) > 0 || pendingSynopsis.length + pendingThesis.length + pendingCompletions.length > 0) {
      return { label: 'Needs attention', tone: 'warning' as const };
    }
    return { label: 'Active setup', tone: 'info' as const };
  })();

  if (loading) {
    return <p className="text-gray-500">Loading...</p>;
  }

  return (
    <div className="pg-page">
      <PageHeader
        title="UTRMC Dashboard"
        description="Simple overview of postgraduate training system setup and activity."
        badges={[
          {
            label: dashboardStatus.label,
            tone: dashboardStatus.tone,
          },
        ]}
        actions={(
          <Link href="/dashboard/utrmc/onboarding" className="pg-btn-primary inline-flex items-center">
            Open onboarding tools
          </Link>
        )}
      />
      {error && <div className="mb-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">{error}</div>}
      {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4">{message}</div>}
      <section className="space-y-6">
        <div className="pg-kpi-grid md:grid-cols-5">
          {cards.map((card) => (
            <MetricCard
              key={card.label}
              label={card.label}
              value={card.value}
              tone={card.tone as 'default' | 'warning' | 'success' | 'info' | undefined}
            />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] gap-4">
          <div className="pg-card">
            <h2 className="pg-section-title">Today’s attention</h2>
            <p className="pg-section-note">What needs review right now.</p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              <MetricCard
                label="Logbook reviews"
                value={opsDashboard?.cross_department_overview.pending_logbook_reviews ?? 0}
                tone="info"
              />
              <MetricCard label="Thesis reviews" value={opsDashboard?.pending_thesis_reviews ?? 0} tone="warning" />
              <MetricCard label="Synopsis reviews" value={opsDashboard?.pending_synopsis_reviews ?? 0} tone="warning" />
              <MetricCard
                label="Rotation verifications"
                value={opsDashboard?.pending_rotation_completion_verifications ?? 0}
                tone="info"
              />
            </div>
          </div>

          <div className="pg-card">
            <h2 className="pg-section-title">Setup completeness</h2>
            <p className="pg-section-note">Status of the core university data needed for pilot use.</p>
            <div className="mt-4 space-y-3 text-sm text-slate-700">
              <p>Hospitals: <span className="font-medium text-slate-900">{stats.hospitals}</span></p>
              <p>Departments: <span className="font-medium text-slate-900">{stats.departments}</span></p>
              <p>Hospital-department links: <span className="font-medium text-slate-900">{placements.length}</span></p>
              <p>Data quality issues: <span className="font-medium text-slate-900">{dqIncomplete ?? 0}</span></p>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link href="/dashboard/utrmc/hospitals" className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700">
                Hospitals
              </Link>
              <Link href="/dashboard/utrmc/departments" className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700">
                Departments
              </Link>
              <Link href="/dashboard/utrmc/matrix" className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700">
                Matrix
              </Link>
            </div>
          </div>
        </div>

        <div className="pg-card flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="pg-section-title">Onboarding & import tools</h2>
              <p className="pg-section-note">Upload residents, supervisors, departments, and program data.</p>
            </div>
            <Link href="/dashboard/utrmc/onboarding" className="pg-btn-primary">
              Open onboarding tools
            </Link>
        </div>

        <div className="pg-card flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="pg-section-title">Backup & Restore</h2>
              <p className="pg-section-note">Manage system backups and critical restore operations.</p>
            </div>
            <Link href="/dashboard/utrmc/backup" className="pg-btn-primary">
              Open backup center
            </Link>
        </div>
      </section>

      {opsDashboard && (
        <section className="space-y-4 mt-8">
          <h2 className="text-xl font-semibold text-gray-900">Recent activity</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <MetricCard label="Active Residents" value={opsDashboard.cross_department_overview.active_residents} />
            <MetricCard label="Pending Synopsis Reviews" value={opsDashboard.pending_synopsis_reviews} tone="warning" />
            <MetricCard label="Pending Thesis Reviews" value={opsDashboard.pending_thesis_reviews} tone="warning" />
            <MetricCard
              label="Pending Rotation Verifications"
              value={opsDashboard.pending_rotation_completion_verifications}
              tone="info"
            />
          </div>
        </section>
      )}

      <section className="mt-8 space-y-4">
        <div className="pg-card flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm text-gray-600">Data quality</p>
            <p className="text-lg font-semibold text-gray-900">
              {dqIncomplete === null ? 'No onboarding data yet' : `${dqIncomplete} incomplete profile(s)`}
            </p>
          </div>
          <Link href="/dashboard/utrmc/data-quality" className="pg-btn-primary">
            Open data quality
          </Link>
        </div>
      </section>

      {canManageRotations && (
        <section className="space-y-4 mt-8">
          <h2 className="text-xl font-semibold text-gray-900">Certificate Verification Queues</h2>
          {pendingSynopsis.length + pendingThesis.length === 0 ? (
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 text-sm text-gray-500">
              No synopsis/thesis submissions are awaiting UTRMC verification.
            </div>
          ) : (
            <div className="space-y-3">
              {[...pendingSynopsis, ...pendingThesis].map((submission) => (
                <div key={`${submission.submission_type}-${submission.id}`} className="pg-card">
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div>
                      <p className="font-semibold text-gray-900">{submission.resident_name}</p>
                      <p className="text-sm text-gray-500">
                        {submission.submission_type} · Required {submission.uploaded_required_count}/{submission.required_documents_count}
                      </p>
                    </div>
                    <button
                      onClick={() => verifySubmission(submission.submission_type, submission.id)}
                      disabled={processingSubmissionId === submission.id}
                      className="pg-btn-success px-3 py-1.5"
                    >
                      {processingSubmissionId === submission.id ? 'Processing…' : 'Verify & Issue'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {pendingCompletions.length === 0 ? (
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 text-sm text-gray-500">
              No rotation completion verifications pending.
            </div>
          ) : (
            <div className="space-y-3">
              {pendingCompletions.map((completion) => (
                <div key={completion.id} className="pg-card">
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div>
                      <p className="font-semibold text-gray-900">{completion.resident_name}</p>
                      <p className="text-sm text-gray-500">
                        <WorkflowStatusBadge status={completion.status} />
                      </p>
                    </div>
                    <button
                      onClick={() => verifyCompletion(completion.id)}
                      disabled={processingCompletionId === completion.id}
                      className="pg-btn-success px-3 py-1.5"
                    >
                      {processingCompletionId === completion.id ? 'Processing…' : 'Verify Completion'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      <section className="space-y-6 mt-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Rotation Operations</h2>
          <p className="text-sm text-gray-500 mt-1">
            Active-scope lifecycle: create draft, resident submits, supervisor approves, UTRMC activates and completes.
          </p>
        </div>

        {!canManageRotations ? (
          <div className="rounded-xl border border-blue-200 bg-blue-50 p-4 text-sm text-blue-800">
            Rotation operations are read-only for UTRMC users. Use an admin or UTRMC admin account to create or transition rotations.
          </div>
        ) : (
          <>
            <form onSubmit={createRotation} className="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-800">Create Rotation Draft</h3>
                <p className="text-sm text-gray-500 mt-1">
                  Drafts become visible to the resident on My Schedule and can be submitted from there.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="rotation_resident_training" className="block text-sm font-medium text-gray-700 mb-1">
                    Resident
                  </label>
                  <select
                    id="rotation_resident_training"
                    value={rotationForm.resident_training}
                    onChange={(event) => setRotationForm((current) => ({
                      ...current,
                      resident_training: event.target.value,
                    }))}
                    className="pg-form-input"
                    required
                  >
                    <option value="">Select resident training record</option>
                    {trainingRecords.map((record) => (
                      <option key={record.id} value={record.id}>
                        {record.resident_name} · {record.program_name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="rotation_hospital_department" className="block text-sm font-medium text-gray-700 mb-1">
                    Placement
                  </label>
                  <select
                    id="rotation_hospital_department"
                    value={rotationForm.hospital_department}
                    onChange={(event) => setRotationForm((current) => ({
                      ...current,
                      hospital_department: event.target.value,
                    }))}
                    className="pg-form-input"
                    required
                  >
                    <option value="">Select hospital and department</option>
                    {placements.map((placement) => (
                      <option key={placement.id} value={placement.id}>
                        {placement.department.name} · {placement.hospital.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="rotation_start_date" className="block text-sm font-medium text-gray-700 mb-1">
                    Start Date
                  </label>
                  <input
                    id="rotation_start_date"
                    type="date"
                    value={rotationForm.start_date}
                    onChange={(event) => setRotationForm((current) => ({
                      ...current,
                      start_date: event.target.value,
                    }))}
                    className="pg-form-input"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="rotation_end_date" className="block text-sm font-medium text-gray-700 mb-1">
                    End Date
                  </label>
                  <input
                    id="rotation_end_date"
                    type="date"
                    value={rotationForm.end_date}
                    onChange={(event) => setRotationForm((current) => ({
                      ...current,
                      end_date: event.target.value,
                    }))}
                    className="pg-form-input"
                    required
                  />
                </div>
              </div>

              <div>
                  <label htmlFor="rotation_notes" className="block text-sm font-medium text-gray-700 mb-1">
                    Notes
                  </label>
                <textarea
                  id="rotation_notes"
                  rows={3}
                  value={rotationForm.notes}
                  onChange={(event) => setRotationForm((current) => ({
                    ...current,
                    notes: event.target.value,
                  }))}
                  className="pg-form-input"
                  placeholder="Optional scheduling notes or handoff context"
                />
              </div>

              <button
                type="submit"
                disabled={savingRotation}
                className="pg-btn-primary"
              >
                {savingRotation ? 'Saving…' : 'Create Rotation Draft'}
              </button>
            </form>

            <RotationSection title="Draft Rotations" emptyText="No draft rotations currently waiting for resident submission.">
              {draftRotations.map((rotation) => (
                <RotationCard
                  key={rotation.id}
                  rotation={rotation}
                  helperText="Waiting for the resident to submit from My Schedule."
                />
              ))}
            </RotationSection>

            <RotationSection title="Submitted Rotations" emptyText="No rotations are currently awaiting supervisor approval.">
              {submittedRotations.map((rotation) => (
                <RotationCard
                  key={rotation.id}
                  rotation={rotation}
                  helperText="Waiting for supervisor review on the supervisor dashboard."
                />
              ))}
            </RotationSection>

            <RotationSection title="Approved Rotations" emptyText="No approved rotations are waiting for activation.">
              {approvedRotations.map((rotation) => (
                <RotationCard
                  key={rotation.id}
                  rotation={rotation}
                  actionLabel="Activate Rotation"
                  actionBusy={actingRotationId === rotation.id}
                  onAction={() => runRotationAction(rotation.id, 'activate', 'Rotation activated.')}
                />
              ))}
            </RotationSection>

            <RotationSection title="Active Rotations" emptyText="No rotations are currently active.">
              {activeRotations.map((rotation) => (
                <RotationCard
                  key={rotation.id}
                  rotation={rotation}
                  actionLabel="Mark Complete"
                  actionTone="success"
                  actionBusy={actingRotationId === rotation.id}
                  onAction={() => runRotationAction(rotation.id, 'complete', 'Rotation completed.')}
                />
              ))}
            </RotationSection>

            <RotationSection title="Returned Rotations" emptyText="No rotations have been returned to residents.">
              {returnedRotations.map((rotation) => (
                <RotationCard
                  key={rotation.id}
                  rotation={rotation}
                  helperText="Resident must adjust and resubmit from My Schedule."
                />
              ))}
            </RotationSection>

            <RotationSection title="Rejected Rotations" emptyText="No rejected rotations recorded on the active surface.">
              {rejectedRotations.map((rotation) => (
                <RotationCard key={rotation.id} rotation={rotation} />
              ))}
            </RotationSection>

            <RotationSection title="Recently Completed Rotations" emptyText="No completed rotations yet.">
              {completedRotations.map((rotation) => (
                <RotationCard key={rotation.id} rotation={rotation} />
              ))}
            </RotationSection>
          </>
        )}
      </section>
    </div>
  );
}
