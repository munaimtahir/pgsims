'use client';

import { useEffect, useState } from 'react';
import { downloadFile } from '@/lib/utils';
import { onboardingApi, LoginSheetRow } from '@/lib/api/onboarding';

export default function LoginSheetPanel() {
  const [rows, setRows] = useState<LoginSheetRow[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const data = await onboardingApi.getLoginSheet();
      setRows(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load login sheet.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const toggle = (id: number) => {
    setSelectedIds((current) =>
      current.includes(id) ? current.filter((item) => item !== id) : [...current, id]
    );
  };

  const resetPasswords = async (residentIds: number[]) => {
    setBusy(true);
    setError('');
    try {
      await Promise.all(residentIds.map((id) => onboardingApi.resetPassword(id)));
      setMessage('Temporary password reset to pgfmu123.');
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Password reset failed.');
    } finally {
      setBusy(false);
    }
  };

  const markIssued = async (payload: { resident_ids?: number[]; mark_all?: boolean }) => {
    setBusy(true);
    setError('');
    try {
      await onboardingApi.markIssued(payload);
      setMessage('Login sheet marked as issued.');
      await load();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to mark issued.');
    } finally {
      setBusy(false);
    }
  };

  const exportExcel = async () => {
    const blob = await onboardingApi.exportLoginSheetExcel();
    downloadFile(blob, 'resident_login_sheet.xlsx');
  };

  const exportPdf = async () => {
    const blob = await onboardingApi.exportLoginSheetPdf();
    downloadFile(blob, 'resident_login_sheet.pdf');
  };

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Login Sheet</h2>
        <p className="mt-1 text-sm text-slate-500">View, export, and issue generated resident logins.</p>
      </div>

      {(message || error) && (
        <div className={`rounded-xl border px-4 py-3 text-sm ${error ? 'border-red-200 bg-red-50 text-red-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
          {error || message}
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        <button onClick={exportExcel} className="pg-btn-primary" disabled={busy || loading}>Export Excel Login Sheet</button>
        <button onClick={exportPdf} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" disabled={busy || loading}>Export PDF Login Sheet</button>
        <button onClick={() => markIssued({ resident_ids: selectedIds })} className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700 hover:bg-emerald-100" disabled={busy || loading || selectedIds.length === 0}>Mark Selected as Issued</button>
        <button onClick={() => markIssued({ mark_all: true })} className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700 hover:bg-emerald-100" disabled={busy || loading || rows.length === 0}>Mark All as Issued</button>
        <button onClick={() => resetPasswords(selectedIds.length > 0 ? selectedIds : rows.map((row) => row.resident_id))} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" disabled={busy || loading || rows.length === 0}>
          Reset Password to pgfmu123
        </button>
      </div>

      {loading ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-8 text-sm text-slate-500">Loading login sheet…</div>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
          <table className="min-w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-3 py-2">Select</th>
                <th className="px-3 py-2">Resident Name</th>
                <th className="px-3 py-2">Department</th>
                <th className="px-3 py-2">Program</th>
                <th className="px-3 py-2">Username</th>
                <th className="px-3 py-2">Temporary Password</th>
                <th className="px-3 py-2">Login URL</th>
                <th className="px-3 py-2">Login Generated</th>
                <th className="px-3 py-2">Issued</th>
                <th className="px-3 py-2">Issued At</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.resident_id} className="border-t border-slate-100">
                  <td className="px-3 py-2">
                    <input type="checkbox" checked={selectedIds.includes(row.resident_id)} onChange={() => toggle(row.resident_id)} />
                  </td>
                  <td className="px-3 py-2">{row.resident_name}</td>
                  <td className="px-3 py-2">{row.department || '—'}</td>
                  <td className="px-3 py-2">{row.program || '—'}</td>
                  <td className="px-3 py-2 font-medium text-slate-900">{row.username || '—'}</td>
                  <td className="px-3 py-2">{row.temporary_password || 'pgfmu123'}</td>
                  <td className="px-3 py-2">{row.login_url}</td>
                  <td className="px-3 py-2">{row.login_generated ? 'Yes' : 'No'}</td>
                  <td className="px-3 py-2">{row.login_issued ? 'Yes' : 'No'}</td>
                  <td className="px-3 py-2">{row.login_issued_at || '—'}</td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap gap-2">
                      <button onClick={() => resetPasswords([row.resident_id])} className="rounded-md border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50" disabled={busy}>
                        Reset Password to pgfmu123
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
