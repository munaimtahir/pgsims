'use client';

import { useEffect, useMemo, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { reportsApi, ReportCatalogItem } from '@/lib/api/reports';

export default function UTRMCReportsPage() {
  const [catalog, setCatalog] = useState<ReportCatalogItem[]>([]);
  const [selected, setSelected] = useState<string>('');
  const [rows, setRows] = useState<Array<Record<string, unknown>>>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    reportsApi
      .getCatalog()
      .then((items) => {
        setCatalog(items);
        if (items.length) setSelected(items[0].key);
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : 'Failed to load reports.'));
  }, []);

  const columns = useMemo(() => (rows.length ? Object.keys(rows[0]) : []), [rows]);

  const runReport = async () => {
    if (!selected) return;
    try {
      setLoading(true);
      setError(null);
      const response = await reportsApi.run(selected);
      setRows(response.rows);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to run report.');
    } finally {
      setLoading(false);
    }
  };

  const exportReport = async (format: 'xlsx' | 'csv') => {
    if (!selected) return;
    try {
      const blob = await reportsApi.export(selected, format);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${selected}.${format}`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to export report.');
    }
  };

  return (
    <ProtectedRoute allowedRoles={['utrmc_user', 'utrmc_admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <h1 className="text-3xl font-bold text-gray-900">UTRMC Reports</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          <SectionCard title="Report Catalog">
            <div className="flex flex-wrap gap-3">
              <select
                value={selected}
                onChange={(e) => setSelected(e.target.value)}
                className="rounded border px-3 py-2 text-sm"
              >
                {catalog.map((item) => (
                  <option key={item.key} value={item.key}>
                    {item.title}
                  </option>
                ))}
              </select>
              <button onClick={runReport} className="rounded bg-indigo-600 px-3 py-2 text-sm text-white">
                {loading ? 'Running…' : 'Run'}
              </button>
              <button onClick={() => exportReport('xlsx')} className="rounded border px-3 py-2 text-sm">
                XLSX
              </button>
              <button onClick={() => exportReport('csv')} className="rounded border px-3 py-2 text-sm">
                CSV
              </button>
            </div>
          </SectionCard>
          <SectionCard title="Preview">
            <div className="overflow-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr>
                    {columns.map((column) => (
                      <th key={column} className="border-b px-2 py-1 text-left">
                        {column}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.slice(0, 100).map((row, index) => (
                    <tr key={index}>
                      {columns.map((column) => (
                        <td key={column} className="border-b px-2 py-1">
                          {String(row[column] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              {!rows.length && <p className="text-sm text-gray-600">Run a report to preview rows.</p>}
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
