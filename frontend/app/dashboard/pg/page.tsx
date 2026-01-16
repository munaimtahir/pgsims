'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/lib/api';
import { notificationsApi } from '@/lib/api';
import { attendanceApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import LoadingSkeleton, { CardSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import Link from 'next/link';

export default function PGDashboardPage() {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState<any>(null);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [attendanceSummary, setAttendanceSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      setError(null);

      // Get current date range for attendance (last month)
      const endDate = new Date();
      const startDate = new Date();
      startDate.setMonth(startDate.getMonth() - 1);

      const [profileData, unreadData, attendanceData] = await Promise.all([
        authApi.getCurrentUser().catch(() => null),
        notificationsApi.getUnreadCount().catch(() => ({ count: 0 })),
        attendanceApi.getSummary({
          period: 'monthly',
          start_date: startDate.toISOString().split('T')[0],
          end_date: endDate.toISOString().split('T')[0],
        }).catch(() => null),
      ]);

      if (profileData) {
        setProfile(profileData);
      }
      if (unreadData) {
        setUnreadCount(unreadData.count || 0);
      }
      if (attendanceData) {
        setAttendanceSummary(attendanceData);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  }

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">PG Dashboard</h1>
            <p className="mt-2 text-gray-600">
              Welcome, {user?.first_name || profile?.first_name}. View your progress and activities.
            </p>
          </div>

          {error && <ErrorBanner message={error} />}

          {loading ? (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <CardSkeleton />
              <CardSkeleton />
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {/* Profile Summary */}
              <SectionCard title="Profile Summary">
                {profile ? (
                  <div className="space-y-2">
                    <div>
                      <span className="text-sm font-medium text-gray-500">Name:</span>
                      <span className="ml-2 text-sm text-gray-900">
                        {profile.full_name || `${profile.first_name} ${profile.last_name}`}
                      </span>
                    </div>
                    {profile.specialty && (
                      <div>
                        <span className="text-sm font-medium text-gray-500">Specialty:</span>
                        <span className="ml-2 text-sm text-gray-900">{profile.specialty}</span>
                      </div>
                    )}
                    {profile.year && (
                      <div>
                        <span className="text-sm font-medium text-gray-500">Year:</span>
                        <span className="ml-2 text-sm text-gray-900">{profile.year}</span>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Profile information not available</p>
                )}
              </SectionCard>

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

              {/* Attendance Summary */}
              {attendanceSummary && (
                <SectionCard title="Attendance Summary">
                  <div className="space-y-2">
                    <div>
                      <span className="text-sm font-medium text-gray-500">Attendance Percentage:</span>
                      <span className="ml-2 text-sm text-gray-900">
                        {attendanceSummary.attendance_percentage?.toFixed(1) || 0}%
                      </span>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-500">Attended:</span>
                      <span className="ml-2 text-sm text-gray-900">{attendanceSummary.attended || 0}</span>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-500">Total Sessions:</span>
                      <span className="ml-2 text-sm text-gray-900">{attendanceSummary.total_sessions || 0}</span>
                    </div>
                  </div>
                </SectionCard>
              )}

              {/* Quick Links */}
              <SectionCard title="Quick Links">
                <div className="grid grid-cols-2 gap-4">
                  <Link
                    href="/dashboard/pg/results"
                    className="p-3 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition text-center"
                  >
                    <div className="font-medium text-gray-900">Results</div>
                    <div className="text-xs text-gray-500 mt-1">View exam scores</div>
                  </Link>
                  <Link
                    href="/dashboard/pg/logbook"
                    className="p-3 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition text-center"
                  >
                    <div className="font-medium text-gray-900">Logbook</div>
                    <div className="text-xs text-gray-500 mt-1">Manage entries</div>
                  </Link>
                  <Link
                    href="/dashboard/pg/rotations"
                    className="p-3 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition text-center"
                  >
                    <div className="font-medium text-gray-900">Rotations</div>
                    <div className="text-xs text-gray-500 mt-1">View schedule</div>
                  </Link>
                  <Link
                    href="/dashboard/pg/certificates"
                    className="p-3 border border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition text-center"
                  >
                    <div className="font-medium text-gray-900">Certificates</div>
                    <div className="text-xs text-gray-500 mt-1">View certificates</div>
                  </Link>
                </div>
              </SectionCard>
            </div>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
