'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { auditApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import { format } from 'date-fns';
import { ActivityLog } from '@/lib/api/audit';

interface AuditLogFilters {
  action?: string;
  start_date?: string;
  end_date?: string;
  ordering?: string;
}

export default function AdminAuditLogsPage() {
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    action: '',
    start_date: '',
    end_date: '',
  });

  const loadLogs = async () => {
    try {
      setLoading(true);
      setError(null);
      const params: AuditLogFilters = {};
      if (filters.action) params.action = filters.action;
      if (filters.start_date) params.start_date = filters.start_date;
      if (filters.end_date) params.end_date = filters.end_date;
      params.ordering = '-created_at';

      const response = await auditApi.getActivityLogs(params);
      setLogs(response.results || []);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load audit logs';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleApplyFilters = () => {
    loadLogs();
  };

  const columns: Column<ActivityLog>[] = [
    {
      key: 'created_at',
      label: 'Timestamp',
      render: (item) => {
        try {
          return format(new Date(item.created_at), 'MMM dd, yyyy HH:mm');
        } catch {
          return item.created_at || '-';
        }
      },
    },
    {
      key: 'user',
      label: 'Actor',
      render: (item) => {
        if (typeof item.user === 'object' && item.user?.username) {
          return item.user.username;
        }
        if (typeof item.user === 'number') {
          return String(item.user);
        }
        return '-';
      },
    },
    { key: 'action', label: 'Action' },
    {
      key: 'details',
      label: 'Details',
      render: (item) => {
        if (item.details && typeof item.details === 'object') {
          return JSON.stringify(item.details).substring(0, 50) + '...';
        }
        return item.details || '-';
      },
    },
  ];

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Audit Logs</h1>
            <p className="mt-2 text-gray-600">View system activity and audit logs</p>
          </div>

          {error && <ErrorBanner message={error} />}

          <SectionCard
            title="Filters"
            actions={
              <button
                onClick={handleApplyFilters}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Apply Filters
              </button>
            }
          >
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Action</label>
                <input
                  type="text"
                  value={filters.action}
                  onChange={(e) => handleFilterChange('action', e.target.value)}
                  placeholder="Search action..."
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Start Date</label>
                <input
                  type="date"
                  value={filters.start_date}
                  onChange={(e) => handleFilterChange('start_date', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">End Date</label>
                <input
                  type="date"
                  value={filters.end_date}
                  onChange={(e) => handleFilterChange('end_date', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Activity Logs">
            {loading ? (
              <TableSkeleton rows={10} cols={4} />
            ) : (
              <DataTable
                columns={columns}
                data={logs}
                emptyMessage="No audit logs found"
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
