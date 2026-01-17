'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuthStore } from '@/store/authStore';
import Link from 'next/link';
import { analyticsApi } from '@/lib/api';
import { notificationsApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { CardSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import { DashboardOverview } from '@/lib/api/analytics';

export default function AdminDashboardPage() {
  const { user } = useAuthStore();
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError(null);
        
        const [overviewData, unreadData] = await Promise.all([
          analyticsApi.getDashboardOverview().catch(() => null),
          notificationsApi.getUnreadCount().catch(() => ({ count: 0 })),
        ]);

        if (overviewData) {
          setOverview(overviewData);
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

    loadData();
  }, []);

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="mt-2 text-gray-600">
              Welcome, {user?.first_name}. Manage the system and view analytics.
            </p>
          </div>

          {error && <ErrorBanner message={error} />}

          {loading ? (
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <CardSkeleton key={i} />
              ))}
            </div>
          ) : (
            <>
              {/* Quick Stats */}
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {overview?.total_pgs !== undefined && (
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">Total PGs</dt>
                            <dd className="text-lg font-semibold text-gray-900">{overview.total_pgs}</dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {overview?.total_supervisors !== undefined && (
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">Supervisors</dt>
                            <dd className="text-lg font-semibold text-gray-900">{overview.total_supervisors}</dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {overview?.pending_reviews !== undefined && (
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                        <div className="ml-5 w-0 flex-1">
                          <dl>
                            <dt className="text-sm font-medium text-gray-500 truncate">Pending Reviews</dt>
                            <dd className="text-lg font-semibold text-gray-900">{overview.pending_reviews}</dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Unread Notifications</dt>
                          <dd className="text-lg font-semibold text-gray-900">{unreadCount}</dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Debug Panel (Admin Only) */}
              {overview && process.env.NODE_ENV === 'development' && (
                <SectionCard title="Debug (Admin Only)">
                  <details className="text-xs">
                    <summary className="cursor-pointer text-gray-600 hover:text-gray-900">View Raw Overview Data</summary>
                    <pre className="mt-2 p-4 bg-gray-100 rounded overflow-auto">
                      {JSON.stringify(overview, null, 2)}
                    </pre>
                  </details>
                </SectionCard>
              )}

              {/* Quick Links */}
              <div className="bg-white shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <Link
                      href="/dashboard/admin/users"
                      className="p-4 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition"
                    >
                      <h4 className="font-medium text-gray-900">Manage Users</h4>
                      <p className="mt-1 text-sm text-gray-500">View and manage all users</p>
                    </Link>
                    <Link
                      href="/dashboard/admin/analytics"
                      className="p-4 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition"
                    >
                      <h4 className="font-medium text-gray-900">Analytics</h4>
                      <p className="mt-1 text-sm text-gray-500">View system analytics</p>
                    </Link>
                    <Link
                      href="/dashboard/admin/bulk-import"
                      className="p-4 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition"
                    >
                      <h4 className="font-medium text-gray-900">Bulk Import</h4>
                      <p className="mt-1 text-sm text-gray-500">Import users in bulk</p>
                    </Link>
                    <Link
                      href="/dashboard/admin/audit-logs"
                      className="p-4 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition"
                    >
                      <h4 className="font-medium text-gray-900">Audit Logs</h4>
                      <p className="mt-1 text-sm text-gray-500">View system audit logs</p>
                    </Link>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
