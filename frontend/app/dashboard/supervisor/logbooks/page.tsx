'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { logbookApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { format } from 'date-fns';

interface LogbookEntry {
  id: number;
  user: { full_name?: string; username?: string } | number;
  case_title?: string;
  date: string;
  status?: string;
}

export default function SupervisorLogbooksPage() {
  const [entries, setEntries] = useState<LogbookEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [verifyingId, setVerifyingId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    loadEntries();
  }, []);

  async function loadEntries() {
    try {
      setLoading(true);
      setError(null);
      const data = await logbookApi.getPending();
      setEntries(data.results || []);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load logbook entries';
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  const handleVerify = async (id: number) => {
    if (!confirm('Are you sure you want to verify this logbook entry?')) {
      return;
    }

    try {
      setVerifyingId(id);
      setError(null);
      await logbookApi.verify(id);
      setSuccess('Logbook entry verified successfully');
      loadEntries(); // Reload data
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to verify entry';
      setError(message);
    } finally {
      setVerifyingId(null);
    }
  };

  const filteredEntries = entries.filter((entry) => {
    const matchesSearch = !searchTerm ||
      entry.case_title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (typeof entry.user === 'object' && entry.user?.full_name?.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = statusFilter === 'all' || entry.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const columns: Column<LogbookEntry>[] = [
    {
      key: 'id',
      label: 'ID',
    },
    {
      key: 'user',
      label: 'PG Name',
      render: (item) => {
        if (typeof item.user === 'object' && item.user?.full_name) {
          return item.user.full_name;
        }
        if (typeof item.user === 'object' && item.user?.username) {
          return item.user.username;
        }
        if (typeof item.user === 'number') {
          return String(item.user);
        }
        return '-';
      },
    },
    {
      key: 'case_title',
      label: 'Procedure/Case',
    },
    {
      key: 'date',
      label: 'Date',
      render: (item) => {
        try {
          return format(new Date(item.date), 'MMM dd, yyyy');
        } catch {
          return item.date || '-';
        }
      },
    },
    {
      key: 'status',
      label: 'Status',
      render: (item) => (
        <span className={`px-2 py-1 text-xs rounded-full ${
          item.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
          item.status === 'approved' ? 'bg-green-100 text-green-800' : 
          'bg-gray-100 text-gray-800'
        }`}>
          {item.status || 'pending'}
        </span>
      ),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (item) => (
        <div className="flex space-x-2">
          {item.status === 'pending' && (
            <button
              onClick={() => handleVerify(item.id)}
              disabled={verifyingId === item.id}
              className="text-sm text-indigo-600 hover:text-indigo-900 disabled:opacity-50"
            >
              {verifyingId === item.id ? 'Verifying...' : 'Verify'}
            </button>
          )}
        </div>
      ),
    },
  ];

  return (
    <ProtectedRoute allowedRoles={['supervisor']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Logbook Review</h1>
            <p className="mt-2 text-gray-600">Review and verify logbook entries</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

          <SectionCard title="Filters">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-gray-700">Search</label>
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search by case title or PG name..."
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="all">All</option>
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Logbook Entries">
            {loading ? (
              <TableSkeleton rows={10} cols={6} />
            ) : (
              <DataTable
                columns={columns}
                data={filteredEntries}
                emptyMessage="No logbook entries found"
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
