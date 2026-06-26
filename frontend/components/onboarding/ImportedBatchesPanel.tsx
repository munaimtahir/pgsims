'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { downloadFile } from '@/lib/utils';
import { onboardingApi, OnboardingBatchDetail, OnboardingBatchRow, LoginSheetRow } from '@/lib/api/onboarding';

export default function ImportedBatchesPanel() {
  const [batches, setBatches] = useState<OnboardingBatchRow[]>([]);
  const [selectedBatch, setSelectedBatch] = useState<OnboardingBatchDetail | null>(null);
  const [importedResidents, setImportedResidents] = useState<LoginSheetRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const selectedBatchRef = useRef<OnboardingBatchDetail | null>(null);

  const openBatch = useCallback(async (batchId: number) => {
    setBusy(true);
    setError('');
    try {
      const [detail, residents] = await Promise.all([
        onboardingApi.getBatch(batchId),
        onboardingApi.listBatchResidents(batchId),
      ]);
      setSelectedBatch(detail);
      setImportedResidents(residents);
      selectedBatchRef.current = detail;
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to open batch.');
    } finally {
      setBusy(false);
    }
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await onboardingApi.listBatches();
      setBatches(data);
      if (data.length > 0 && !selectedBatchRef.current) {
        await openBatch(data[0].id);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load batches.');
    } finally {
      setLoading(false);
    }
  }, [openBatch]);

  useEffect(() => {
    void load();
  }, [load]);

  const generateMissing = async () => {
    if (!selectedBatch) return;
    setBusy(true);
    setError('');
    try {
      const response = await onboardingApi.generateBatchLogins(selectedBatch.id);
      setMessage(`Generated ${response.generated} login ID(s) for batch ${selectedBatch.id}.`);
      await openBatch(selectedBatch.id);
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate logins.');
    } finally {
      setBusy(false);
    }
  };

  const exportBatch = async () => {
    if (!selectedBatch) return;
    const blob = await onboardingApi.exportBatchLoginSheet(selectedBatch.id);
    downloadFile(blob, `resident_login_sheet_batch_${selectedBatch.id}.xlsx`);
  };

  const downloadErrors = async () => {
    if (!selectedBatch) return;
    const blob = await onboardingApi.downloadBatchErrorReport(selectedBatch.id);
    downloadFile(blob, `resident_batch_${selectedBatch.id}_errors.csv`);
  };

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Imported Batches</h2>
        <p className="mt-1 text-sm text-slate-500">Review past resident imports, open batch details, and export or regenerate login sheets.</p>
      </div>

      {(message || error) && (
        <div className={`rounded-xl border px-4 py-3 text-sm ${error ? 'border-red-200 bg-red-50 text-red-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
          {error || message}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-[1.2fr_1.8fr]">
        <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
          <table className="min-w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-3 py-2">Batch ID</th>
                <th className="px-3 py-2">File Name</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Imported</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {batches.map((batch) => (
                <tr key={batch.id} className="border-t border-slate-100">
                  <td className="px-3 py-2 font-medium text-slate-900">{batch.id}</td>
                  <td className="px-3 py-2">{batch.file_name}</td>
                  <td className="px-3 py-2">{batch.status}</td>
                  <td className="px-3 py-2">{batch.imported_rows}</td>
                  <td className="px-3 py-2">
                    <button onClick={() => openBatch(batch.id)} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50" disabled={busy}>
                      Open Batch
                    </button>
                  </td>
                </tr>
              ))}
              {batches.length === 0 && !loading && (
                <tr>
                  <td colSpan={5} className="px-3 py-8 text-center text-sm text-slate-500">No batches found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          {selectedBatch ? (
            <>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900">Batch #{selectedBatch.id}</h3>
                  <p className="text-sm text-slate-500">{selectedBatch.file_name}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button onClick={generateMissing} className="pg-btn-primary" disabled={busy}>Generate Missing Logins</button>
                  <button onClick={exportBatch} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" disabled={busy}>Export Batch Login Sheet</button>
                  <button onClick={downloadErrors} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" disabled={busy}>Download Error Report</button>
                </div>
              </div>

              <div className="grid gap-3 sm:grid-cols-3">
                {[
                  ['Total Rows', selectedBatch.total_rows],
                  ['Ready Rows', selectedBatch.ready_rows],
                  ['Error Rows', selectedBatch.error_rows],
                  ['Duplicate Rows', selectedBatch.duplicate_rows],
                  ['Imported Rows', selectedBatch.imported_rows],
                  ['Logins Generated', selectedBatch.logins_generated],
                ].map(([label, value]) => (
                  <div key={label as string} className="rounded-xl border border-slate-200 bg-slate-50 p-3">
                    <div className="text-xs uppercase tracking-wide text-slate-500">{label as string}</div>
                    <div className="mt-1 text-lg font-semibold text-slate-900">{value as number}</div>
                  </div>
                ))}
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-slate-900">Mapping used</h4>
                <pre className="overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-100">{JSON.stringify(selectedBatch.mapping, null, 2)}</pre>
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-slate-900">Imported Residents</h4>
                <div className="overflow-x-auto rounded-xl border border-slate-200">
                  <table className="min-w-full text-left text-xs">
                    <thead className="bg-slate-50 text-slate-500">
                      <tr>
                        <th className="px-3 py-2">Resident Name</th>
                        <th className="px-3 py-2">Department</th>
                        <th className="px-3 py-2">Username</th>
                        <th className="px-3 py-2">Profile</th>
                        <th className="px-3 py-2">Issued</th>
                      </tr>
                    </thead>
                    <tbody>
                      {importedResidents.map((resident) => (
                        <tr key={resident.resident_id} className="border-t border-slate-100">
                          <td className="px-3 py-2">{resident.resident_name}</td>
                          <td className="px-3 py-2">{resident.department || '—'}</td>
                          <td className="px-3 py-2">{resident.username || '—'}</td>
                          <td className="px-3 py-2">{resident.profile_completed ? 'Complete' : 'Incomplete'}</td>
                          <td className="px-3 py-2">{resident.login_issued ? 'Yes' : 'No'}</td>
                        </tr>
                      ))}
                      {importedResidents.length === 0 && (
                        <tr>
                          <td colSpan={5} className="px-3 py-8 text-center text-sm text-slate-500">No residents in this batch.</td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-slate-900">Skipped / Error Rows</h4>
                <div className="overflow-x-auto rounded-xl border border-slate-200">
                  <table className="min-w-full text-left text-xs">
                    <thead className="bg-slate-50 text-slate-500">
                      <tr>
                        <th className="px-3 py-2">Row</th>
                        <th className="px-3 py-2">Resident</th>
                        <th className="px-3 py-2">Status</th>
                        <th className="px-3 py-2">Remarks</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(selectedBatch.preview_rows || []).filter((row) => row.status !== 'Ready').map((row) => (
                        <tr key={row.row_number} className="border-t border-slate-100">
                          <td className="px-3 py-2">{row.row_number}</td>
                          <td className="px-3 py-2">{row.resident_name || '—'}</td>
                          <td className="px-3 py-2">{row.status}</td>
                          <td className="px-3 py-2">{row.remarks || '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          ) : (
            <div className="rounded-xl border border-dashed border-slate-200 p-8 text-sm text-slate-500">Select a batch to see details.</div>
          )}
        </div>
      </div>
    </div>
  );
}
