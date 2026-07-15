'use client';

import { FormEvent, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import supervisionApi from '@/lib/api/supervision';

export default function SupervisionImportPage() {
  const [file, setFile] = useState<File | null>(null);
  const [dryRun, setDryRun] = useState(true);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError('Select a CSV file first.');
      return;
    }
    setLoading(true);
    setMessage('');
    setError('');
    try {
      const result = await supervisionApi.importSupervisionCsv(file, dryRun);
      setMessage(`Import ${result.dry_run ? 'dry run' : 'apply'} complete. Successes: ${result.successes.length}, Failures: ${result.failures.length}.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to import CSV.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page max-w-3xl">
        <PageHeader
          title="Import Supervision CSV"
          description="Dry-run or apply supervision assignments from a CSV file."
          actions={<Link href="/supervision" className="pg-btn-primary">Back</Link>}
        />
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-700">{message}</div>}

        <form onSubmit={submit} className="pg-card space-y-4">
          <div>
            <label className="pg-form-label" htmlFor="file">CSV File</label>
            <input id="file" type="file" accept=".csv,text/csv" className="pg-form-input bg-white" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          </div>
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" checked={dryRun} onChange={(event) => setDryRun(event.target.checked)} />
            Dry run only
          </label>
          <button type="submit" disabled={loading} className="pg-btn-primary">
            {loading ? 'Processing...' : 'Run Import'}
          </button>
        </form>
      </div>
    </ProtectedRoute>
  );
}
