'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { notificationsApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import LoadingSkeleton, { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { format } from 'date-fns';

type TabType = 'all' | 'unread';

export default function PGNotificationsPage() {
  const [activeTab, setActiveTab] = useState<TabType>('all');
  const [notifications, setNotifications] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [markingRead, setMarkingRead] = useState<number | null>(null);

  useEffect(() => {
    loadNotifications();
  }, [activeTab]);

  async function loadNotifications() {
    try {
      setLoading(true);
      setError(null);

      const [allData, unreadData, countData] = await Promise.all([
        activeTab === 'all' 
          ? notificationsApi.list().catch(() => ({ results: [], count: 0 }))
          : Promise.resolve({ results: [], count: 0 }),
        activeTab === 'unread'
          ? notificationsApi.getUnread().catch(() => ({ results: [], count: 0 }))
          : Promise.resolve({ results: [], count: 0 }),
        notificationsApi.getUnreadCount().catch(() => ({ count: 0 })),
      ]);

      if (activeTab === 'all' && allData) {
        setNotifications(allData.results || []);
      } else if (activeTab === 'unread' && unreadData) {
        setNotifications(unreadData.results || []);
      }

      if (countData) {
        setUnreadCount(countData.count || 0);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to load notifications');
    } finally {
      setLoading(false);
    }
  }

  const handleMarkRead = async (id: number) => {
    try {
      setMarkingRead(id);
      setError(null);
      await notificationsApi.markRead(id);
      setSuccess('Notification marked as read');
      loadNotifications();
    } catch (err: any) {
      setError(err?.message || 'Failed to mark notification as read');
    } finally {
      setMarkingRead(null);
    }
  };

  const handleMarkAllRead = async () => {
    const unreadNotifications = notifications.filter((n) => !n.is_read);
    try {
      setError(null);
      for (const notification of unreadNotifications) {
        await notificationsApi.markRead(notification.id);
      }
      setSuccess('All notifications marked as read');
      loadNotifications();
    } catch (err: any) {
      setError(err?.message || 'Failed to mark all notifications as read');
    }
  };

  const columns: Column<any>[] = [
    {
      key: 'title',
      label: 'Title',
    },
    {
      key: 'body',
      label: 'Message',
      render: (item) => (
        <div className="max-w-md truncate">{item.body || '-'}</div>
      ),
    },
    {
      key: 'created_at',
      label: 'Date',
      render: (item) => {
        try {
          return format(new Date(item.created_at), 'MMM dd, yyyy HH:mm');
        } catch {
          return item.created_at || '-';
        }
      },
    },
    {
      key: 'is_read',
      label: 'Status',
      render: (item) => (
        <span className={`px-2 py-1 text-xs rounded-full ${
          item.is_read ? 'bg-gray-100 text-gray-800' : 'bg-blue-100 text-blue-800'
        }`}>
          {item.is_read ? 'Read' : 'Unread'}
        </span>
      ),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (item) => (
        !item.is_read && (
          <button
            onClick={() => handleMarkRead(item.id)}
            disabled={markingRead === item.id}
            className="text-sm text-indigo-600 hover:text-indigo-900 disabled:opacity-50"
          >
            {markingRead === item.id ? 'Marking...' : 'Mark Read'}
          </button>
        )
      ),
    },
  ];

  const hasUnread = notifications.some((n) => !n.is_read);

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
            <p className="mt-2 text-gray-600">View and manage your notifications</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

          {/* Tabs */}
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {(['all', 'unread'] as TabType[]).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`${
                    activeTab === tab
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm capitalize`}
                >
                  {tab} {tab === 'unread' && unreadCount > 0 && `(${unreadCount})`}
                </button>
              ))}
            </nav>
          </div>

          <SectionCard
            title="Notifications"
            actions={
              hasUnread && (
                <button
                  onClick={handleMarkAllRead}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm"
                >
                  Mark All Read
                </button>
              )
            }
          >
            {loading ? (
              <TableSkeleton rows={10} cols={5} />
            ) : (
              <DataTable
                columns={columns}
                data={notifications}
                emptyMessage="No notifications found"
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
