'use client';

import { useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { bulkApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import SectionCard from '@/components/ui/SectionCard';
import { BulkImportResult } from '@/lib/api/bulk';

type ImportType = 'trainees' | 'supervisors' | 'residents' | 'generic';

export default function AdminBulkImportPage() {
  const [importType, setImportType] = useState<ImportType>('trainees');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [importResult, setImportResult] = useState<BulkImportResult | null>(null);
  const [reviewData, setReviewData] = useState<unknown>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(null);
      setImportResult(null);

      let result;
      switch (importType) {
        case 'trainees':
          result = await bulkApi.importTrainees(file);
          break;
        case 'supervisors':
          result = await bulkApi.importSupervisors(file);
          break;
        case 'residents':
          result = await bulkApi.importResidents(file);
          break;
        case 'generic':
          result = await bulkApi.import(file, 'generic');
          break;
      }

      setImportResult(result);
      setSuccess(`Import completed: ${result.success_count} successful, ${result.error_count || 0} errors`);

      // Try to load review data if import ID is available
      if (result.import_id) {
        try {
          const review = await bulkApi.review(result.import_id);
          setReviewData(review);
        } catch {
          // Review endpoint may not be available
        }
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to import file';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleReviewLatest = async () => {
    if (!importResult?.import_id) return;
    try {
      const review = await bulkApi.review(importResult.import_id);
      setReviewData(review);
    } catch {
      setError('Failed to load review data');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Bulk Import</h1>
            <p className="mt-2 text-gray-600">Import users and data in bulk via CSV</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

          <SectionCard title="Import Data">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <div className="flex justify-between items-center">
                  <label className="block text-sm font-medium text-gray-700">Import Type</label>
                  <a
                    href={`/templates/${importType}_template.csv`}
                    download
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    Download {importType.charAt(0).toUpperCase() + importType.slice(1)} Template CSV
                  </a>
                </div>
                <select
                  value={importType}
                  onChange={(e) => setImportType(e.target.value as ImportType)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="trainees">Trainees</option>
                  <option value="supervisors">Supervisors</option>
                  <option value="residents">Residents</option>
                  <option value="generic">Generic</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">CSV File</label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading || !file}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Importing...' : 'Import'}
              </button>
            </form>
          </SectionCard>

          {importResult && (
            <SectionCard
              title="Import Results"
              actions={
                importResult.import_id && (
                  <button
                    onClick={handleReviewLatest}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm"
                  >
                    Review Latest Import
                  </button>
                )
              }
            >
              <div className="space-y-2">
                <div>
                  <span className="font-medium">Success Count:</span> {importResult.success_count || 0}
                </div>
                <div>
                  <span className="font-medium">Error Count:</span> {importResult.error_count || 0}
                </div>
                {importResult.errors && importResult.errors.length > 0 && (
                  <div>
                    <span className="font-medium">Errors:</span>
                    <ul className="list-disc list-inside mt-2 text-sm text-red-600">
                      {importResult.errors.slice(0, 10).map((err: string, idx: number) => (
                        <li key={idx}>{err}</li>
                      ))}
                      {importResult.errors.length > 10 && (
                        <li>... and {importResult.errors.length - 10} more errors</li>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            </SectionCard>
          )}

          {reviewData !== null && (
            <SectionCard title="Review Data">
              <pre className="text-xs bg-gray-100 p-4 rounded overflow-auto">
                {JSON.stringify(reviewData, null, 2)}
              </pre>
            </SectionCard>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
