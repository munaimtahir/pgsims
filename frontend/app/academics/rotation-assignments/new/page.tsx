'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import {
  rotationsApi,
  TrainingResidentTrainingRecord,
  HospitalDepartmentOption,
  TrainingProgramOption,
} from '@/lib/api/rotations';
import { academicsApi, AcademicOptionRow } from '@/lib/api/academics';

export default function NewRotationAssignmentPage() {
  const router = useRouter();
  const [records, setRecords] = useState<TrainingResidentTrainingRecord[]>([]);
  const [hospitalDepartments, setHospitalDepartments] = useState<HospitalDepartmentOption[]>([]);
  const [residents, setResidents] = useState<AcademicOptionRow[]>([]);
  const [programs, setPrograms] = useState<TrainingProgramOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const [residentTraining, setResidentTraining] = useState('');
  const [hospitalDepartment, setHospitalDepartment] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [notes, setNotes] = useState('');

  const [showCreateRecord, setShowCreateRecord] = useState(false);
  const [newRecordResident, setNewRecordResident] = useState('');
  const [newRecordProgram, setNewRecordProgram] = useState('');
  const [newRecordStart, setNewRecordStart] = useState('');
  const [creatingRecord, setCreatingRecord] = useState(false);

  const loadAll = () => {
    setLoading(true);
    Promise.all([
      rotationsApi.listResidentTrainingRecords(),
      rotationsApi.listHospitalDepartments(),
      rotationsApi.listTrainingPrograms(),
      academicsApi.getOptions(),
    ])
      .then(([recs, hds, progs, options]) => {
        setRecords(recs);
        setHospitalDepartments(hds.filter((hd) => hd.active));
        setPrograms(progs);
        setResidents(options.residents);
      })
      .catch(() => setError('Unable to load form data'))
      .finally(() => setLoading(false));
  };

  useEffect(loadAll, []);

  const createTrainingRecord = async () => {
    if (!newRecordResident || !newRecordProgram || !newRecordStart) {
      setError('Resident, program, and start date are required to create a training record.');
      return;
    }
    setCreatingRecord(true);
    setError('');
    try {
      const created = await rotationsApi.createResidentTrainingRecord({
        resident_user: Number(newRecordResident),
        program: Number(newRecordProgram),
        start_date: newRecordStart,
        current_level: 'y1',
      });
      setRecords((prev) => [...prev, created]);
      setResidentTraining(String(created.id));
      setShowCreateRecord(false);
    } catch (err: unknown) {
      const message =
        typeof err === 'object' && err !== null && 'response' in err
          ? JSON.stringify((err as { response?: { data?: unknown } }).response?.data)
          : 'Unable to create training record';
      setError(message);
    } finally {
      setCreatingRecord(false);
    }
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!residentTraining || !hospitalDepartment || !startDate || !endDate) {
      setError('All fields except notes are required.');
      return;
    }
    setSaving(true);
    setError('');
    try {
      const created = await rotationsApi.create({
        resident_training: Number(residentTraining),
        hospital_department: Number(hospitalDepartment),
        start_date: startDate,
        end_date: endDate,
        notes,
      });
      router.push(`/academics/rotation-assignments/${created.id}`);
    } catch (err: unknown) {
      const message =
        typeof err === 'object' && err !== null && 'response' in err
          ? JSON.stringify((err as { response?: { data?: unknown } }).response?.data)
          : 'Unable to create rotation assignment';
      setError(message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page max-w-2xl space-y-6">
        <PageHeader
          title="New Rotation Assignment"
          description="Place a resident into a hospital/department rotation. Starts as DRAFT."
        />

        {loading ? (
          <div className="text-center py-6 text-sm text-slate-500">Loading...</div>
        ) : (
          <form onSubmit={submit} className="pg-card space-y-4">
            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Resident Training Record
              </label>
              <select
                className="pg-form-input w-full"
                value={residentTraining}
                onChange={(e) => setResidentTraining(e.target.value)}
              >
                <option value="">Select resident training record...</option>
                {records.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.resident_name} — {r.program_name}
                  </option>
                ))}
              </select>
              <button
                type="button"
                onClick={() => setShowCreateRecord((v) => !v)}
                className="mt-1 text-xs font-medium text-indigo-600 hover:underline"
              >
                {showCreateRecord ? 'Cancel' : "Resident not listed? Create their training record"}
              </button>
            </div>

            {showCreateRecord && (
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 space-y-3">
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Resident</label>
                  <select
                    className="pg-form-input w-full"
                    value={newRecordResident}
                    onChange={(e) => setNewRecordResident(e.target.value)}
                  >
                    <option value="">Select resident...</option>
                    {residents.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Program</label>
                  <select
                    className="pg-form-input w-full"
                    value={newRecordProgram}
                    onChange={(e) => setNewRecordProgram(e.target.value)}
                  >
                    <option value="">Select program...</option>
                    {programs.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Start Date</label>
                  <input
                    type="date"
                    className="pg-form-input w-full"
                    value={newRecordStart}
                    onChange={(e) => setNewRecordStart(e.target.value)}
                  />
                </div>
                <button
                  type="button"
                  onClick={createTrainingRecord}
                  disabled={creatingRecord}
                  className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                >
                  {creatingRecord ? 'Creating...' : 'Create Training Record'}
                </button>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Hospital / Department
              </label>
              <select
                className="pg-form-input w-full"
                value={hospitalDepartment}
                onChange={(e) => setHospitalDepartment(e.target.value)}
              >
                <option value="">Select hospital/department...</option>
                {hospitalDepartments.map((hd) => (
                  <option key={hd.id} value={hd.id}>
                    {hd.hospital.name} — {hd.department.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Start Date</label>
                <input
                  type="date"
                  className="pg-form-input w-full"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">End Date</label>
                <input
                  type="date"
                  className="pg-form-input w-full"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Notes</label>
              <textarea
                className="pg-form-input w-full"
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </div>

            <button type="submit" disabled={saving} className="pg-btn-primary">
              {saving ? 'Saving...' : 'Create Assignment (DRAFT)'}
            </button>
          </form>
        )}
      </div>
    </ProtectedRoute>
  );
}
