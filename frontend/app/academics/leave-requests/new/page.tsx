'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { leaveApi, LEAVE_TYPE_OPTIONS } from '@/lib/api/leave';
import { rotationsApi, TrainingResidentTrainingRecord } from '@/lib/api/rotations';

export default function NewLeaveRequestPage() {
  const router = useRouter();
  const [records, setRecords] = useState<TrainingResidentTrainingRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const [residentTraining, setResidentTraining] = useState('');
  const [leaveType, setLeaveType] = useState('annual');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [reason, setReason] = useState('');

  useEffect(() => {
    rotationsApi
      .listResidentTrainingRecords()
      .then((recs) => {
        setRecords(recs);
        if (recs.length === 1) {
          setResidentTraining(String(recs[0].id));
        }
      })
      .catch(() => setError('Unable to load your training record'))
      .finally(() => setLoading(false));
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!residentTraining || !startDate || !endDate) {
      setError('Training record, start date, and end date are required.');
      return;
    }
    setSaving(true);
    setError('');
    try {
      const created = await leaveApi.create({
        resident_training: Number(residentTraining),
        leave_type: leaveType,
        start_date: startDate,
        end_date: endDate,
        reason,
      });
      router.push(`/academics/leave-requests/${created.id}`);
    } catch (err: unknown) {
      const message =
        typeof err === 'object' && err !== null && 'response' in err
          ? JSON.stringify((err as { response?: { data?: unknown } }).response?.data)
          : 'Unable to create leave request';
      setError(message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'ADMIN']}>
      <div className="pg-page max-w-2xl space-y-6">
        <PageHeader
          title="New Leave Request"
          description="Request leave for your current training record. Starts as DRAFT."
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
                Training Record
              </label>
              <select
                className="pg-form-input w-full"
                value={residentTraining}
                onChange={(e) => setResidentTraining(e.target.value)}
              >
                <option value="">Select training record...</option>
                {records.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.resident_name} — {r.program_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Leave Type</label>
              <select
                className="pg-form-input w-full"
                value={leaveType}
                onChange={(e) => setLeaveType(e.target.value)}
              >
                {LEAVE_TYPE_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
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
              <label className="block text-sm font-medium text-slate-700 mb-1">Reason</label>
              <textarea
                className="pg-form-input w-full"
                rows={3}
                value={reason}
                onChange={(e) => setReason(e.target.value)}
              />
            </div>

            <button type="submit" disabled={saving} className="pg-btn-primary">
              {saving ? 'Saving...' : 'Create Leave Request (DRAFT)'}
            </button>
          </form>
        )}
      </div>
    </ProtectedRoute>
  );
}
