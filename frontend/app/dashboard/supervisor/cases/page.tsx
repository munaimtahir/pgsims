'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { casesApi, ClinicalCase } from '@/lib/api/cases';

export default function SupervisorCasesPage() {
  const [items, setItems] = useState<ClinicalCase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await casesApi.getPendingCases();
      setItems(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load pending cases');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const review = async (id: number, action: 'approved' | 'needs_revision' | 'rejected') => {
    const feedback = window.prompt('Feedback', action === 'approved' ? 'Reviewed and approved.' : '') || '';
    try {
      await casesApi.reviewCase(id, { status: action, overall_feedback: feedback });
      setSuccess(`Case ${action.replace('_', ' ')}.`);
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Review failed');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['supervisor', 'admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <h1 className="text-3xl font-bold text-gray-900">Cases Review</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}
          <SectionCard title="Pending Cases">
            {loading ? (
              <p>Loading...</p>
            ) : (
              <div className="space-y-2">
                {items.map((item) => (
                  <div key={item.id} className="flex items-center justify-between rounded border p-3">
                    <div>
                      <p className="font-medium">{item.case_title}</p>
                      <p className="text-sm text-gray-600">{item.pg_name || 'PG'} • {item.status}</p>
                    </div>
                    <div className="flex gap-2">
                      <button className="text-green-700 text-sm" onClick={() => review(item.id, 'approved')}>Approve</button>
                      <button className="text-amber-700 text-sm" onClick={() => review(item.id, 'needs_revision')}>Needs revision</button>
                      <button className="text-red-700 text-sm" onClick={() => review(item.id, 'rejected')}>Reject</button>
                    </div>
                  </div>
                ))}
                {!items.length && <p className="text-sm text-gray-600">No pending cases.</p>}
              </div>
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
