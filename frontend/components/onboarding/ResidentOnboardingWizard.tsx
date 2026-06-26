'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { downloadFile } from '@/lib/utils';
import { onboardingApi, OnboardingPreviewRow } from '@/lib/api/onboarding';

const FIELDS = [
  { key: 'resident_name', label: 'Resident Name', required: true },
  { key: 'father_name', label: 'Father Name', required: false },
  { key: 'department', label: 'Department', required: true },
  { key: 'program_name', label: 'Program', required: false },
  { key: 'training_year', label: 'Training Year', required: false },
  { key: 'supervisor_name', label: 'Supervisor Name', required: false },
  { key: 'mobile_number', label: 'Mobile Number', required: false },
  { key: 'email', label: 'Email', required: false },
  { key: 'cnic', label: 'CNIC', required: false },
  { key: 'registration_number', label: 'PMDC / PMC Number', required: false },
  { key: 'joining_date', label: 'Joining Date', required: false },
] as const;

const DEFAULT_AUTO_MATCH: Record<string, string[]> = {
  resident_name: ['name', 'resident name', 'trainee name', 'full name'],
  father_name: ['father', 'father name', 's/o'],
  department: ['department', 'dept', 'unit'],
  program_name: ['program', 'degree', 'course', 'training program'],
  training_year: ['year', 'training year', 'year of training'],
  supervisor_name: ['supervisor', 'supervisor name'],
  mobile_number: ['mobile', 'phone', 'contact', 'cell'],
  email: ['email', 'email address'],
  cnic: ['cnic', 'nic'],
  registration_number: ['pmdc', 'pmc', 'registration no', 'registration number'],
  joining_date: ['joining', 'joining date', 'date of joining'],
};

function normalize(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]/g, '');
}

function autoMatchHeaders(headers: string[]) {
  const normalizedHeaders = headers.map((header) => [normalize(header), header] as const);
  const result: Record<string, string> = {};
  FIELDS.forEach((field) => {
    const aliases = DEFAULT_AUTO_MATCH[field.key] || [];
    const matched = normalizedHeaders.find(([normalized]) =>
      aliases.some((alias) => normalize(alias) === normalized)
    );
    if (matched) {
      result[field.key] = matched[1];
    }
  });
  return result;
}

function statusClass(status: string) {
  if (status === 'Ready') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  if (status === 'Error') return 'bg-red-50 text-red-700 border-red-200';
  return 'bg-amber-50 text-amber-700 border-amber-200';
}

export default function ResidentOnboardingWizard() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [batchId, setBatchId] = useState<number | null>(null);
  const [headers, setHeaders] = useState<string[]>([]);
  const [sampleRows, setSampleRows] = useState<Array<Record<string, string>>>([]);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [previewRows, setPreviewRows] = useState<OnboardingPreviewRow[]>([]);
  const [counts, setCounts] = useState({ total: 0, ready: 0, error: 0, duplicate: 0 });
  const [importedCount, setImportedCount] = useState(0);
  const [generatedCount, setGeneratedCount] = useState(0);

  const canPreview = Boolean(batchId && mapping.resident_name && mapping.department);
  const readyRows = useMemo(() => previewRows.filter((row) => row.status === 'Ready'), [previewRows]);

  useEffect(() => {
    if (headers.length > 0) {
      setMapping(autoMatchHeaders(headers));
    }
  }, [headers]);

  const handleUpload = async (uploadedFile: File) => {
    setLoading(true);
    setError('');
    setNotice('');
    try {
      const response = await onboardingApi.uploadPreview(uploadedFile);
      setFile(uploadedFile);
      setBatchId(response.batch_id);
      setHeaders(response.headers);
      setSampleRows(response.sample_rows);
      setMapping(response.suggested_mapping);
      setPreviewRows([]);
      setCounts({ total: response.total_rows, ready: 0, error: 0, duplicate: 0 });
      setStep(2);
      setNotice(`Loaded ${response.total_rows} rows from ${uploadedFile.name}.`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to upload file.');
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = async () => {
    if (!batchId) return;
    setLoading(true);
    setError('');
    try {
      const response = await onboardingApi.mapColumns(batchId, mapping);
      setPreviewRows(response.preview_rows);
      setCounts({
        total: response.total_rows,
        ready: response.ready_rows,
        error: response.error_rows,
        duplicate: response.duplicate_rows,
      });
      setStep(3);
      setNotice('Preview generated. Review statuses before importing.');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to preview data.');
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async () => {
    if (!batchId) return;
    setLoading(true);
    setError('');
    try {
      const response = await onboardingApi.importResidents(batchId);
      setImportedCount(response.imported_rows);
      setStep(4);
      setNotice(`Imported ${response.imported_rows} ready resident record(s).`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to import residents.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!batchId) return;
    setLoading(true);
    setError('');
    try {
      const response = await onboardingApi.generateBatchLogins(batchId);
      setGeneratedCount(response.generated);
      setStep(5);
      setNotice(`Generated ${response.generated} login ID(s).`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate logins.');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!batchId) return;
    setLoading(true);
    setError('');
    try {
      const blob = await onboardingApi.exportBatchLoginSheet(batchId);
      downloadFile(blob, `resident_login_sheet_batch_${batchId}.xlsx`);
      setStep(6);
      setNotice('Login sheet exported.');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to export login sheet.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadErrors = async () => {
    if (!batchId) return;
    const blob = await onboardingApi.downloadBatchErrorReport(batchId);
    downloadFile(blob, `resident_batch_${batchId}_errors.csv`);
  };

  const handleReset = () => {
    setStep(1);
    setLoading(false);
    setNotice('');
    setError('');
    setFile(null);
    setBatchId(null);
    setHeaders([]);
    setSampleRows([]);
    setMapping({});
    setPreviewRows([]);
    setCounts({ total: 0, ready: 0, error: 0, duplicate: 0 });
    setImportedCount(0);
    setGeneratedCount(0);
  };

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Resident Onboarding</h2>
            <p className="text-sm text-slate-500">Upload a roster, map the columns you want, preview the rows, import ready residents, then generate login IDs.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link href="/dashboard/onboarding/login-sheet" className="pg-btn-primary inline-flex items-center">Open Login Sheet</Link>
            <button onClick={handleReset} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Cancel Import
            </button>
          </div>
        </div>
      </div>

      {(error || notice) && (
        <div className={`rounded-xl border px-4 py-3 text-sm ${error ? 'border-red-200 bg-red-50 text-red-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
          {error || notice}
        </div>
      )}

      <div className="grid gap-3 md:grid-cols-6">
        {['Upload Excel', 'Match Columns', 'Preview Data', 'Import Residents', 'Generate Login IDs', 'Export Login Sheet'].map((label, index) => (
          <div
            key={label}
            className={`rounded-xl border px-3 py-3 text-sm font-medium ${step >= index + 1 ? 'border-indigo-200 bg-indigo-50 text-indigo-700' : 'border-slate-200 bg-white text-slate-500'}`}
          >
            <div className="text-xs uppercase tracking-wide">{index + 1}</div>
            <div>{label}</div>
          </div>
        ))}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-6">
        <section className="space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h3 className="text-lg font-semibold text-slate-900">Step 1: Upload Excel</h3>
            {file && <span className="text-xs text-slate-500">{file.name}</span>}
          </div>
          <label className="inline-flex cursor-pointer items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
            <input
              type="file"
              accept=".xlsx,.xls,.csv"
              className="hidden"
              onChange={(e) => {
                const next = e.target.files?.[0];
                if (next) {
                  void handleUpload(next);
                }
              }}
            />
            Upload File
          </label>
          <div className="text-xs text-slate-500">Supported: .xlsx, .xls, .csv</div>
        </section>

        {headers.length > 0 && (
          <section className="space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="text-lg font-semibold text-slate-900">Step 2: Match Columns</h3>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => setMapping(autoMatchHeaders(headers))}
                  className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                >
                  Auto Match Columns
                </button>
                <button
                  type="button"
                  onClick={() => setMapping({})}
                  className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                >
                  Reset Mapping
                </button>
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                >
                  Upload File
                </button>
              </div>
            </div>

            <div className="grid gap-4 lg:grid-cols-2">
              <div className="space-y-2">
                <div className="text-sm font-medium text-slate-700">PGSIMS resident field</div>
                <div className="space-y-2">
                  {FIELDS.map((field) => (
                    <div key={field.key} className="rounded-lg border border-slate-200 px-3 py-2 text-sm">
                      <div className="font-medium text-slate-900">{field.label}</div>
                      <div className="text-xs text-slate-500">{field.required ? 'Required' : 'Optional'}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <div className="text-sm font-medium text-slate-700">Excel column header</div>
                <div className="space-y-2">
                  {FIELDS.map((field) => (
                    <label key={field.key} className="block rounded-lg border border-slate-200 p-3 text-sm">
                      <div className="mb-1 font-medium text-slate-900">{field.label}</div>
                      <select
                        value={mapping[field.key] || ''}
                        onChange={(e) => setMapping((current) => ({ ...current, [field.key]: e.target.value }))}
                        className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                      >
                        <option value="">Unmapped</option>
                        {headers.map((header) => (
                          <option key={header} value={header}>{header}</option>
                        ))}
                      </select>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                disabled={loading || !canPreview}
                onClick={handlePreview}
                className="pg-btn-primary disabled:opacity-60"
              >
                Preview Data
              </button>
              <button
                type="button"
                disabled={loading}
                onClick={handleDownloadErrors}
                className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                Download Error Report
              </button>
            </div>
          </section>
        )}

        {sampleRows.length > 0 && (
          <section className="space-y-3">
            <h3 className="text-lg font-semibold text-slate-900">Uploaded File Sample</h3>
            <div className="overflow-x-auto rounded-xl border border-slate-200">
              <table className="min-w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500">
                  <tr>
                    {headers.slice(0, 8).map((header) => (
                      <th key={header} className="px-3 py-2 font-medium">{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {sampleRows.slice(0, 3).map((row, index) => (
                    <tr key={index} className="border-t border-slate-100">
                      {headers.slice(0, 8).map((header) => (
                        <td key={header} className="px-3 py-2 text-slate-600">{row[header] || '—'}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {previewRows.length > 0 && (
          <section className="space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="text-lg font-semibold text-slate-900">Step 3: Preview Data</h3>
              <div className="grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-1 text-emerald-700">Ready: {counts.ready}</span>
                <span className="rounded-full border border-red-200 bg-red-50 px-2 py-1 text-red-700">Error: {counts.error}</span>
                <span className="rounded-full border border-amber-200 bg-amber-50 px-2 py-1 text-amber-700">Possible Duplicate: {counts.duplicate}</span>
                <span className="rounded-full border border-slate-200 bg-slate-50 px-2 py-1 text-slate-700">Total: {counts.total}</span>
              </div>
            </div>

            <div className="overflow-x-auto rounded-xl border border-slate-200">
              <table className="min-w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500">
                  <tr>
                    <th className="px-3 py-2">Resident Name</th>
                    <th className="px-3 py-2">Father Name</th>
                    <th className="px-3 py-2">Department</th>
                    <th className="px-3 py-2">Program</th>
                    <th className="px-3 py-2">Training Year</th>
                    <th className="px-3 py-2">Supervisor Name</th>
                    <th className="px-3 py-2">Mobile Number</th>
                    <th className="px-3 py-2">Email</th>
                    <th className="px-3 py-2">CNIC</th>
                    <th className="px-3 py-2">PMDC / PMC Number</th>
                    <th className="px-3 py-2">Joining Date</th>
                    <th className="px-3 py-2">Status</th>
                    <th className="px-3 py-2">Remarks</th>
                  </tr>
                </thead>
                <tbody>
                  {previewRows.map((row) => (
                    <tr key={row.row_number} className="border-t border-slate-100">
                      <td className="px-3 py-2">{row.resident_name || '—'}</td>
                      <td className="px-3 py-2">{row.father_name || '—'}</td>
                      <td className="px-3 py-2">{row.department || '—'}</td>
                      <td className="px-3 py-2">{row.program_name || '—'}</td>
                      <td className="px-3 py-2">{row.training_year || '—'}</td>
                      <td className="px-3 py-2">{row.supervisor_name || '—'}</td>
                      <td className="px-3 py-2">{row.mobile_number || '—'}</td>
                      <td className="px-3 py-2">{row.email || '—'}</td>
                      <td className="px-3 py-2">{row.cnic || '—'}</td>
                      <td className="px-3 py-2">{row.registration_number || '—'}</td>
                      <td className="px-3 py-2">{row.joining_date || '—'}</td>
                      <td className="px-3 py-2">
                        <span className={`inline-flex rounded-full border px-2 py-1 font-medium ${statusClass(row.status)}`}>
                          {row.status}
                        </span>
                      </td>
                      <td className="px-3 py-2">{row.remarks || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                disabled={loading || readyRows.length === 0}
                onClick={handleImport}
                className="pg-btn-primary disabled:opacity-60"
              >
                Import Ready Records
              </button>
              <button
                type="button"
                disabled={loading}
                onClick={handleDownloadErrors}
                className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                Download Error Report
              </button>
            </div>
          </section>
        )}

        {importedCount > 0 && (
          <section className="space-y-3">
            <h3 className="text-lg font-semibold text-slate-900">Step 4: Import Residents</h3>
            <p className="text-sm text-slate-600">Imported {importedCount} resident record(s) from the ready rows.</p>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                disabled={loading}
                onClick={handleGenerate}
                className="pg-btn-primary disabled:opacity-60"
              >
                Generate Login IDs
              </button>
            </div>
          </section>
        )}

        {generatedCount > 0 && (
          <section className="space-y-3">
            <h3 className="text-lg font-semibold text-slate-900">Step 5: Generate Login IDs</h3>
            <p className="text-sm text-slate-600">Generated {generatedCount} sequential username(s) with the temporary password `pgfmu123`.</p>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                disabled={loading}
                onClick={handleExport}
                className="pg-btn-primary disabled:opacity-60"
              >
                Export Login Sheet
              </button>
              <Link href="/dashboard/onboarding/login-sheet" className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
                Open Login Sheet
              </Link>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
