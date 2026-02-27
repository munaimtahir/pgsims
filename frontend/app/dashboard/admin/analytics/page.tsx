'use client';

import { useEffect, useMemo, useState } from 'react';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import { analyticsApi, AnalyticsTabPayload } from '@/lib/api/analytics';

type AnalyticsTab =
  | 'overview'
  | 'adoption'
  | 'logbook'
  | 'review-sla'
  | 'departments'
  | 'rotations'
  | 'research'
  | 'data-ops'
  | 'system'
  | 'security'
  | 'live';

const TAB_CONFIG: Array<{ key: AnalyticsTab; label: string }> = [
  { key: 'overview', label: 'Overview' },
  { key: 'adoption', label: 'Adoption' },
  { key: 'logbook', label: 'Logbook' },
  { key: 'review-sla', label: 'Review / SLA' },
  { key: 'departments', label: 'Departments' },
  { key: 'rotations', label: 'Rotations' },
  { key: 'research', label: 'Research' },
  { key: 'data-ops', label: 'Data Ops' },
  { key: 'system', label: 'System' },
  { key: 'security', label: 'Security' },
  { key: 'live', label: 'Live' },
];

const formatDate = (value: Date) => value.toISOString().slice(0, 10);

export default function AdminAnalyticsPage() {
  const end = new Date();
  const start = new Date(end);
  start.setDate(end.getDate() - 13);

  const [activeTab, setActiveTab] = useState<AnalyticsTab>('overview');
  const [startDate, setStartDate] = useState(formatDate(start));
  const [endDate, setEndDate] = useState(formatDate(end));
  const [departmentId, setDepartmentId] = useState<string>('');
  const [role, setRole] = useState<string>('');
  const [options, setOptions] = useState<{ departments: Array<{ id: number; name: string }>; roles: string[] }>({
    departments: [],
    roles: [],
  });
  const [tabData, setTabData] = useState<AnalyticsTabPayload | null>(null);
  const [liveCursor, setLiveCursor] = useState<string | undefined>(undefined);
  const [liveRows, setLiveRows] = useState<Array<Record<string, unknown>>>([]);
  const [eventTypePrefix, setEventTypePrefix] = useState('');
  const [entityType, setEntityType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const queryParams = useMemo(
    () => ({
      start_date: startDate,
      end_date: endDate,
      department_id: departmentId ? Number(departmentId) : '',
      role,
    }),
    [startDate, endDate, departmentId, role]
  );

  const loadTab = async (tab: AnalyticsTab) => {
    setLoading(true);
    try {
      const payload = await analyticsApi.getTab(tab, queryParams);
      setTabData(payload);
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load analytics data.');
    } finally {
      setLoading(false);
    }
  };

  const pollLive = async (isInitial = false) => {
    setLoading(isInitial);
    try {
      const payload = await analyticsApi.getLiveEvents({
        ...queryParams,
        limit: 200,
        cursor: isInitial ? undefined : liveCursor,
        event_type_prefix: eventTypePrefix || undefined,
        entity_type: entityType || undefined,
      });
      setLiveCursor(payload.cursor || liveCursor);
      setLiveRows((previousRows) => {
        const incoming = (payload.events || []) as Array<Record<string, unknown>>;
        const combined = isInitial ? incoming : [...incoming, ...previousRows];
        const seen = new Set<string>();
        const deduped = combined.filter((row) => {
          const id = String(row.id ?? '');
          if (!id || seen.has(id)) return false;
          seen.add(id);
          return true;
        });
        return deduped.slice(0, 200);
      });
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load live feed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyticsApi
      .getFilters()
      .then((payload) => setOptions({ departments: payload.departments, roles: payload.roles }))
      .catch(() => setOptions({ departments: [], roles: [] }));
  }, []);

  useEffect(() => {
    void analyticsApi.ingestUIEvent({
      event_type: 'page.view',
      metadata: { source: 'admin_analytics_page', tab: activeTab },
      event_key: 'admin-analytics-page-view',
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    void analyticsApi.ingestUIEvent({
      event_type: 'feature.used',
      metadata: { source: 'admin_analytics_tab', tab: activeTab },
      event_key: `admin-analytics-tab-${activeTab}`,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]);

  useEffect(() => {
    if (activeTab !== 'live') {
      void loadTab(activeTab);
      return;
    }
    setLiveCursor(undefined);
    setLiveRows([]);
    void pollLive(true);
    const timer = setInterval(() => {
      void pollLive(false);
    }, 7000);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, queryParams, eventTypePrefix, entityType]);

  useEffect(() => {
    if (activeTab !== 'live') return;
    setTabData({
      title: 'Live',
      date_range: { start_date: startDate, end_date: endDate },
      cards: [{ key: 'live_events', title: 'Events (Latest Window)', value: liveRows.length }],
      table: {
        columns: ['occurred_at', 'event_type', 'actor_role', 'department_id', 'hospital_id', 'entity_id'],
        rows: liveRows,
      },
      series: [],
    });
  }, [activeTab, liveRows, startDate, endDate]);

  const handleExport = async () => {
    try {
      const blob = await analyticsApi.exportTabCsv(activeTab, queryParams);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `analytics-${activeTab}-${startDate}-${endDate}.csv`;
      anchor.click();
      URL.revokeObjectURL(url);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to export CSV.');
    }
  };

  const tableColumns: Column<Record<string, unknown>>[] = useMemo(() => {
    const columns = tabData?.table?.columns || [];
    return columns.map((column) => ({
      key: column,
      label: column.replace(/_/g, ' '),
      render: (row) => {
        const value = row[column];
        if (column === 'entity_id' && typeof row.drilldown_url === 'string' && row.drilldown_url) {
          return (
            <a className="text-indigo-600 hover:text-indigo-800 underline" href={String(row.drilldown_url)}>
              {value === null || value === undefined || value === '' ? 'Open' : String(value)}
            </a>
          );
        }
        if (typeof value === 'number') return value.toLocaleString();
        return value === null || value === undefined || value === '' ? '-' : String(value);
      },
    }));
  }, [tabData]);

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6" data-testid="admin-analytics-page">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
            <p className="mt-2 text-gray-600">Operational analytics dashboard</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

          <SectionCard title="Global Filters">
            <div className="grid grid-cols-1 gap-3 md:grid-cols-5">
              <label className="text-sm text-gray-700">
                Start date
                <input
                  data-testid="analytics-filter-start-date"
                  type="date"
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
              </label>
              <label className="text-sm text-gray-700">
                End date
                <input
                  data-testid="analytics-filter-end-date"
                  type="date"
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </label>
              <label className="text-sm text-gray-700">
                Department
                <select
                  data-testid="analytics-filter-department"
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  value={departmentId}
                  onChange={(e) => setDepartmentId(e.target.value)}
                >
                  <option value="">All departments</option>
                  {options.departments.map((department) => (
                    <option key={department.id} value={department.id}>
                      {department.name}
                    </option>
                  ))}
                </select>
              </label>
              <label className="text-sm text-gray-700">
                Role
                <select
                  data-testid="analytics-filter-role"
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                >
                  <option value="">All roles</option>
                  {options.roles.map((roleOption) => (
                    <option key={roleOption} value={roleOption}>
                      {roleOption}
                    </option>
                  ))}
                </select>
              </label>
              <div className="flex items-end">
                <button
                  type="button"
                  onClick={handleExport}
                  data-testid="analytics-export-csv"
                  className="rounded border px-3 py-2 text-sm hover:bg-gray-50"
                >
                  Export CSV
                </button>
              </div>
            </div>
            {activeTab === 'live' ? (
              <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-3">
                <label className="text-sm text-gray-700">
                  Event type prefix
                  <input
                    data-testid="analytics-live-filter-event-prefix"
                    type="text"
                    className="mt-1 w-full rounded border px-3 py-2 text-sm"
                    placeholder="logbook.case"
                    value={eventTypePrefix}
                    onChange={(e) => setEventTypePrefix(e.target.value)}
                  />
                </label>
                <label className="text-sm text-gray-700">
                  Entity type
                  <input
                    data-testid="analytics-live-filter-entity-type"
                    type="text"
                    className="mt-1 w-full rounded border px-3 py-2 text-sm"
                    placeholder="logbook_entry"
                    value={entityType}
                    onChange={(e) => setEntityType(e.target.value)}
                  />
                </label>
              </div>
            ) : null}
          </SectionCard>

          <div className="overflow-x-auto border-b border-gray-200">
            <nav className="-mb-px flex space-x-6">
              {TAB_CONFIG.map((tab) => (
                <button
                  key={tab.key}
                  type="button"
                  data-testid={`analytics-tab-${tab.key}`}
                  onClick={() => setActiveTab(tab.key)}
                  className={`whitespace-nowrap border-b-2 px-1 py-3 text-sm font-medium ${
                    activeTab === tab.key
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {loading ? (
            <TableSkeleton rows={6} cols={4} />
          ) : (
            <>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
                {(tabData?.cards || []).map((card) => (
                  <div key={card.key} className="rounded-lg border bg-white p-4">
                    <p className="text-sm text-gray-500">{card.title}</p>
                    <p className="mt-2 text-2xl font-semibold text-gray-900">{Number(card.value).toLocaleString()}</p>
                  </div>
                ))}
              </div>

              <SectionCard title={tabData?.title || 'Analytics'}>
                {tabData && tabData.table.rows.length > 0 ? (
                  <DataTable columns={tableColumns} data={tabData.table.rows} />
                ) : (
                  <div data-testid="analytics-empty-state" className="py-8 text-center text-gray-500">
                    No data yet for the selected filters.
                  </div>
                )}
              </SectionCard>
            </>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
