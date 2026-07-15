'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicSummary, AcademicTrainingRecord } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

export default function TrainingRecordDetailPage() {
  const params = useParams();
  const { user } = useAuthStore();
  const canManage = user?.role === 'ADMIN';
  const [record, setRecord] = useState<AcademicTrainingRecord | null>(null);
  const [summary, setSummary] = useState<AcademicSummary | null>(null);

  useEffect(() => {
    const id = Number(params.id);
    if (!id) return;
    academicsApi.getTrainingRecord(id).then((nextRecord) => {
      setRecord(nextRecord);
      academicsApi.getResidentSummary(nextRecord.resident).then(setSummary).catch(() => setSummary(null));
    }).catch(() => setRecord(null));
  }, [params.id]);

  const closeRecord = async () => {
    if (!record) return;
    await academicsApi.closeTrainingRecord(record.id, { status: 'COMPLETED', actual_end_date: record.expected_end_date, notes: 'Closed from Brick 8 detail page.' });
    setRecord(await academicsApi.getTrainingRecord(record.id));
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Training Record Detail"
          description="Resident identity, academic placement, and future workflow placeholders."
          actions={<Link href="/academics/training-records" className="text-sm font-medium text-indigo-600 hover:underline">Back to records</Link>}
        />

        {record && (
          <>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="pg-card space-y-2">
                <h2 className="pg-section-title">Resident Identity</h2>
                <p><span className="font-medium">Resident:</span> {record.resident_name}</p>
                <p><span className="font-medium">Program:</span> {record.program_name || '—'}</p>
                <p><span className="font-medium">Session:</span> {record.academic_session_name || '—'}</p>
                <p><span className="font-medium">Department:</span> {record.department_name || '—'}</p>
                <p><span className="font-medium">Training Site:</span> {record.training_site_name || '—'}</p>
              </div>
              <div className="pg-card space-y-2">
                <h2 className="pg-section-title">Training Window</h2>
                <p><span className="font-medium">Training Year:</span> {record.training_year || '—'}</p>
                <p><span className="font-medium">Start Date:</span> {record.start_date || '—'}</p>
                <p><span className="font-medium">Expected End:</span> {record.expected_end_date || '—'}</p>
                <p><span className="font-medium">Status:</span> {record.status}</p>
                {canManage && record.is_active && (
                  <button onClick={closeRecord} className="pg-btn-warning mt-3">Close Record</button>
                )}
              </div>
            </div>

            <div className="pg-card space-y-3">
              <h2 className="pg-section-title">Supervisor Summary</h2>
              <p className="text-sm text-slate-600">Future evaluations, logbook, and procedure workflows will attach here.</p>
              <p><span className="font-medium">Primary Supervisor:</span> {summary?.supervision?.primary_supervisor?.supervisor.name || 'Not assigned'}</p>
              <p><span className="font-medium">Pending Review Items:</span> {summary?.review_queue?.pending_count || 0}</p>
            </div>
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
