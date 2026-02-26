'use client';

import { useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { bulkApi } from '@/lib/api';

const DATASETS: Array<{ key: 'residents' | 'supervisors' | 'departments'; label: string }> = [
  { key: 'residents', label: 'Residents' },
  { key: 'supervisors', label: 'Supervisors' },
  { key: 'departments', label: 'Departments' },
];

export default function AdminExportsPage() {
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const download = async (resource: 'residents' | 'supervisors' | 'departments', format: 'xlsx' | 'csv') => {
    try {
      setLoading(`${resource}-${format}`);
      setError(null);
      const blob = await bulkApi.exportDataset(resource, format);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${resource}_export.${format}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      setSuccess(`${resource} ${format.toUpperCase()} export downloaded.`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to export dataset.');
    } finally {
      setLoading(null);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <h1 className="text-3xl font-bold text-gray-900">Data Exports</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}
          <SectionCard title="Export Master Data">
            <div className="space-y-4">
              {DATASETS.map((dataset) => (
                <div key={dataset.key} className="flex items-center justify-between rounded border p-3">
                  <span className="font-medium">{dataset.label}</span>
                  <div className="space-x-2">
                    <button
                      onClick={() => download(dataset.key, 'xlsx')}
                      disabled={loading !== null}
                      className="rounded bg-indigo-600 px-3 py-2 text-sm text-white hover:bg-indigo-700 disabled:opacity-50"
                    >
                      {loading === `${dataset.key}-xlsx` ? 'Exporting…' : 'Download XLSX'}
                    </button>
                    <button
                      onClick={() => download(dataset.key, 'csv')}
                      disabled={loading !== null}
                      className="rounded border border-indigo-600 px-3 py-2 text-sm text-indigo-700 hover:bg-indigo-50 disabled:opacity-50"
                    >
                      {loading === `${dataset.key}-csv` ? 'Exporting…' : 'Download CSV'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
