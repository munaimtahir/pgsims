'use client';
import { useEffect, useState } from 'react';

import { useAuthStore } from '@/store/authStore';
import { trainingApi, ResidentTrainingRecordListItem, RotationAssignment } from '@/lib/api/training';
import { userbaseApi, UserbaseHospitalDepartment, UserbaseUser } from '@/lib/api/userbase';

const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'bg-gray-100 text-gray-700',
  SUBMITTED: 'bg-yellow-100 text-yellow-800',
  APPROVED: 'bg-green-100 text-green-800',
  ACTIVE: 'bg-blue-100 text-blue-800',
  COMPLETED: 'bg-slate-100 text-slate-700',
  RETURNED: 'bg-orange-100 text-orange-700',
  REJECTED: 'bg-red-100 text-red-700',
};

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

function RotationStatusBadge({ status }: { status: string }) {
  const cls = STATUS_COLORS[status] || 'bg-gray-100 text-gray-600';
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{status}</span>;
}

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
    ? 'bg-green-600 hover:bg-green-700'
    : 'bg-indigo-600 hover:bg-indigo-700';

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5">
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
        <RotationStatusBadge status={rotation.status} />
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
            className={`px-4 py-2 text-white rounded-lg text-sm font-medium disabled:opacity-50 ${actionClassName}`}
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
  const [trainingRecords, setTrainingRecords] = useState<ResidentTrainingRecordListItem[]>([]);
  const [placements, setPlacements] = useState<UserbaseHospitalDepartment[]>([]);
  const [rotations, setRotations] = useState<RotationAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [savingRotation, setSavingRotation] = useState(false);
  const [actingRotationId, setActingRotationId] = useState<number | null>(null);
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
        ])
        : Promise.resolve<[ResidentTrainingRecordListItem[], UserbaseHospitalDepartment[], RotationAssignment[]]>([
          [],
          [],
          [],
        ]);

      const [hospitals, departments, users, [records, matrix, rotationRows]] = await Promise.all([
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

  const draftRotations = rotations.filter((item) => item.status === 'DRAFT');
  const submittedRotations = rotations.filter((item) => item.status === 'SUBMITTED');
  const approvedRotations = rotations.filter((item) => item.status === 'APPROVED');
  const activeRotations = rotations.filter((item) => item.status === 'ACTIVE');
  const returnedRotations = rotations.filter((item) => item.status === 'RETURNED');
  const rejectedRotations = rotations.filter((item) => item.status === 'REJECTED');
  const completedRotations = rotations.filter((item) => item.status === 'COMPLETED').slice(0, 5);

  const cards = [
    { label: 'Hospitals', value: stats.hospitals },
    { label: 'Departments', value: stats.departments },
    { label: 'Total Users', value: stats.users },
    { label: 'Supervisors', value: stats.supervisors },
    { label: 'Residents / PGs', value: stats.residents },
  ];

  if (loading) {
    return <p className="text-gray-500">Loading...</p>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">UTRMC Overview</h1>
        {error && <div className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}
        {message && <div className="mb-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4">{message}</div>}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {cards.map((card) => (
            <div key={card.label} className="bg-white border border-gray-200 rounded-lg p-4">
              <p className="text-3xl font-bold text-indigo-600">{card.value}</p>
              <p className="text-sm text-gray-600 mt-1">{card.label}</p>
            </div>
          ))}
        </div>
      </div>

      <section className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Rotation Operations</h2>
          <p className="text-sm text-gray-500 mt-1">
            Active-scope lifecycle: create draft, resident submits, supervisor approves, UTRMC activates and completes.
          </p>
        </div>

        {!canManageRotations ? (
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-sm text-blue-800">
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
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
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
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
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
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
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
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
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
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                  placeholder="Optional scheduling notes or handoff context"
                />
              </div>

              <button
                type="submit"
                disabled={savingRotation}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
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
