'use client';

import { useEffect, useMemo, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { reportsApi, ReportCatalogItem } from '@/lib/api/reports';

export default function AdminReportsPage() {
  const [catalog, setCatalog] = useState<ReportCatalogItem[]>([]);
  const [selected, setSelected] = useState<string>('');
  const [rows, setRows] = useState<Array<Record<string, unknown>>>([]);
  const [filters, setFilters] = useState({ department_id: '', year: '' });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    reportsApi
      .getCatalog()
      .then((items) => {
        setCatalog(items);
        if (items.length) setSelected(items[0].key);
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : 'Failed to load report catalog.'));
  }, []);

  const columns = useMemo(() => (rows.length ? Object.keys(rows[0]) : []), [rows]);

  const runReport = async () => {
    try {
      const response = await reportsApi.run(selected, filters);
      setRows(response.rows);
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to run report.');
    }
  };

  const exportReport = async (format: 'xlsx' | 'csv') => {
    try {
      const blob = await reportsApi.export(selected, format, filters);
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
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <h1 className="text-3xl font-bold text-gray-900">Admin Reports</h1>
          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          <SectionCard title="Run Report">
            <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
              <select value={selected} onChange={(e) => setSelected(e.target.value)} className="rounded border px-3 py-2 text-sm">
                {catalog.map((item) => (
                  <option key={item.key} value={item.key}>
                    {item.title}
                  </option>
                ))}
              </select>
              <input
                placeholder="Department ID (optional)"
                value={filters.department_id}
                onChange={(e) => setFilters((prev) => ({ ...prev, department_id: e.target.value }))}
                className="rounded border px-3 py-2 text-sm"
              />
              <input
                placeholder="Year (optional)"
                value={filters.year}
                onChange={(e) => setFilters((prev) => ({ ...prev, year: e.target.value }))}
                className="rounded border px-3 py-2 text-sm"
              />
              <div className="space-x-2">
                <button onClick={runReport} className="rounded bg-indigo-600 px-3 py-2 text-sm text-white">
                  Run
                </button>
                <button onClick={() => exportReport('xlsx')} className="rounded border px-3 py-2 text-sm">
                  XLSX
                </button>
                <button onClick={() => exportReport('csv')} className="rounded border px-3 py-2 text-sm">
                  CSV
                </button>
              </div>
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
                  {rows.slice(0, 100).map((row, idx) => (
                    <tr key={idx}>
                      {columns.map((column) => (
                        <td key={column} className="border-b px-2 py-1">
                          {String(row[column] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              {!rows.length && <p className="text-sm text-gray-600">No rows to preview.</p>}
            </div>
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
