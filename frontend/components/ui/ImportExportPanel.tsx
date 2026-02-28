'use client';

/**
 * Reusable import/export panel component for Data Admin pages.
 * Supports dry-run preview, apply import, and CSV export.
 */

import { useState, useRef } from 'react';
import apiClient from '@/lib/api/client';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import SectionCard from '@/components/ui/SectionCard';

interface RowError {
  row: string | number;
  error: string;
}

interface ImportResult {
  operation?: string;
  status?: string;
  success_count: number;
  failure_count: number;
  details?: {
    successes?: unknown[];
    failures?: RowError[];
  };
  dry_run?: boolean;
}

interface ImportExportPanelProps {
  /** Entity key used in API: e.g. "hospitals", "matrix", "residents" */
  entity: string;
  /** Human-readable label */
  label: string;
  /** Template CSV download path (relative to /templates/) */
  templateFile: string;
  /** Export resource key (for /api/bulk/exports/<resource>/) */
  exportResource?: string;
}

export default function ImportExportPanel({
  entity,
  label,
  templateFile,
  exportResource,
}: ImportExportPanelProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [result, setResult] = useState<ImportResult | null>(null);
  const [exporting, setExporting] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const reset = () => {
    setError(null);
    setSuccess(null);
    setResult(null);
  };

  const runImport = async (action: 'dry-run' | 'apply') => {
    if (!file) {
      setError('Please select a CSV file');
      return;
    }
    reset();
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const resp = await apiClient.post<ImportResult>(
        `/api/bulk/import/${entity}/${action}/`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResult(resp.data);
      const failures = resp.data.failure_count ?? 0;
      const label_action = action === 'dry-run' ? 'Dry-run' : 'Import';
      setSuccess(
        `${label_action} complete: ${resp.data.success_count} rows OK, ${failures} errors.`
      );
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        (err instanceof Error ? err.message : 'Request failed');
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: 'csv' | 'xlsx') => {
    setExporting(true);
    setError(null);
    try {
      const resource = exportResource ?? entity;
      const resp = await apiClient.get(`/api/bulk/exports/${resource}/`, {
        params: { file_format: format },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `${resource}_export.${format}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err: unknown) {
      setError('Export failed. Check console.');
      console.error(err);
    } finally {
      setExporting(false);
    }
  };

  const failures = result?.details?.failures ?? [];

  return (
    <div className="space-y-4">
      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
      {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

      {/* Import panel */}
      <SectionCard title={`Import ${label}`}>
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <input
              ref={fileRef}
              type="file"
              accept=".csv,.xlsx"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="block text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            {file && (
              <span className="text-xs text-gray-500">{file.name}</span>
            )}
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              disabled={loading || !file}
              onClick={() => runImport('dry-run')}
              className="px-4 py-2 rounded bg-yellow-100 text-yellow-800 text-sm font-medium hover:bg-yellow-200 disabled:opacity-50"
            >
              {loading ? 'Running…' : '🔍 Dry Run (validate only)'}
            </button>
            <button
              disabled={loading || !file}
              onClick={() => {
                if (confirm(`Apply import for ${label}? This will write to the database.`)) {
                  runImport('apply');
                }
              }}
              className="px-4 py-2 rounded bg-green-600 text-white text-sm font-medium hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Importing…' : '✅ Apply Import'}
            </button>
            <a
              href={`/templates/${templateFile}`}
              download
              className="px-4 py-2 rounded bg-gray-100 text-gray-700 text-sm font-medium hover:bg-gray-200"
            >
              ⬇ Download Template
            </a>
          </div>
        </div>
      </SectionCard>

      {/* Results */}
      {result && (
        <SectionCard title="Import Results">
          <div className="space-y-2">
            <p className="text-sm">
              <span className="font-medium">Mode:</span>{' '}
              {result.dry_run ? 'Dry Run' : 'Applied'}
            </p>
            <p className="text-sm">
              <span className="font-medium">Success rows:</span>{' '}
              <span className="text-green-700">{result.success_count}</span>
            </p>
            <p className="text-sm">
              <span className="font-medium">Failed rows:</span>{' '}
              <span className={result.failure_count > 0 ? 'text-red-600' : 'text-gray-600'}>
                {result.failure_count}
              </span>
            </p>
            {failures.length > 0 && (
              <div className="mt-2">
                <p className="text-sm font-medium text-red-600 mb-1">Row errors:</p>
                <ul className="text-xs text-red-600 list-disc list-inside space-y-0.5 max-h-48 overflow-y-auto bg-red-50 rounded p-2">
                  {failures.slice(0, 50).map((f, i) => (
                    <li key={i}>
                      Row {f.row}: {typeof f.error === 'string' ? f.error : JSON.stringify(f.error)}
                    </li>
                  ))}
                  {failures.length > 50 && (
                    <li>… and {failures.length - 50} more</li>
                  )}
                </ul>
              </div>
            )}
          </div>
        </SectionCard>
      )}

      {/* Export panel */}
      {exportResource !== undefined && (
        <SectionCard title={`Export ${label}`}>
          <div className="flex gap-3">
            <button
              disabled={exporting}
              onClick={() => handleExport('csv')}
              className="px-4 py-2 rounded bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {exporting ? 'Exporting…' : '⬇ Export CSV'}
            </button>
            <button
              disabled={exporting}
              onClick={() => handleExport('xlsx')}
              className="px-4 py-2 rounded bg-indigo-100 text-indigo-700 text-sm font-medium hover:bg-indigo-200 disabled:opacity-50"
            >
              {exporting ? 'Exporting…' : '⬇ Export Excel'}
            </button>
          </div>
        </SectionCard>
      )}
    </div>
  );
}
