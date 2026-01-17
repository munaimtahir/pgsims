'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuthStore } from '@/store/authStore';
import { logbookApi } from '@/lib/api';
import { notificationsApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import SuccessBanner from '@/components/ui/SuccessBanner';
import Link from 'next/link';
import { format } from 'date-fns';

interface PendingLogbookEntry {
  id: number;
  user: { full_name?: string; username?: string } | number;
  case_title?: string;
  date: string;
  status?: string;
}

export default function SupervisorDashboardPage() {
  const { user } = useAuthStore();
  const [pendingEntries, setPendingEntries] = useState<PendingLogbookEntry[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [verifyingId, setVerifyingId] = useState<number | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      setError(null);

      const [pendingData, unreadData] = await Promise.all([
        logbookApi.getPending().catch(() => ({ count: 0, results: [] })),
        notificationsApi.getUnreadCount().catch(() => ({ count: 0 })),
      ]);

      if (pendingData) {
        setPendingEntries(pendingData.results || []);
      }
      if (unreadData) {
        setUnreadCount(unreadData.count || 0);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load dashboard data';
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
      loadData(); // Reload data
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to verify entry';
      setError(message);
    } finally {
      setVerifyingId(null);
    }
  };

  const columns: Column<PendingLogbookEntry>[] = [
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
          item.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
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
          <button
            onClick={() => handleVerify(item.id)}
            disabled={verifyingId === item.id}
            className="text-sm text-indigo-600 hover:text-indigo-900 disabled:opacity-50"
          >
            {verifyingId === item.id ? 'Verifying...' : 'Verify'}
          </button>
        </div>
      ),
    },
  ];

  return (
    <ProtectedRoute allowedRoles={['supervisor']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Supervisor Dashboard</h1>
            <p className="mt-2 text-gray-600">Welcome, {user?.first_name}. Review pending logbook entries.</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

          {/* Notifications Widget */}
          <SectionCard
            title="Notifications"
            actions={
              <Link
                href="/dashboard/pg/notifications"
                className="text-sm text-indigo-600 hover:text-indigo-900"
              >
                View All
              </Link>
            }
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-2xl font-semibold text-gray-900">{unreadCount}</p>
                <p className="text-sm text-gray-500">Unread notifications</p>
              </div>
            </div>
          </SectionCard>

          {/* Pending Logbook Verifications */}
          <SectionCard
            title="Pending Logbook Verifications"
            actions={
              <Link
                href="/dashboard/supervisor/logbooks"
                className="text-sm text-indigo-600 hover:text-indigo-900"
              >
                View All
              </Link>
            }
          >
            {loading ? (
              <TableSkeleton rows={5} cols={6} />
            ) : (
              <DataTable
                columns={columns}
                data={pendingEntries}
                emptyMessage="No pending logbook verifications"
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
