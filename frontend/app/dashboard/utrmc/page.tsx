'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi } from '@/lib/api/userbase';
import { academicsApi, AcademicOverview } from '@/lib/api/academics';
import { supervisionApi, SupervisionDataQuality } from '@/lib/api/supervision';

type AdminStats = {
  users: number;
  residents: number;
  supervisors: number;
  supportStaff: number;
};

const adminQuickLinks = [
  { label: 'Users', href: '/users' },
  { label: 'Residents', href: '/residents' },
  { label: 'Supervisors', href: '/supervisors' },
  { label: 'Support Staff', href: '/support-staff' },
  { label: 'Admins', href: '/admins' },
  { label: 'Masters', href: '/masters' },
  { label: 'Supervision', href: '/supervision' },
  { label: 'Academics', href: '/academics' },
];

export default function UTRMCOverviewPage() {
  const { user } = useAuthStore();
  const isSupportStaff = user?.role === 'SUPPORT_STAFF';
  const [stats, setStats] = useState<AdminStats>({ users: 0, residents: 0, supervisors: 0, supportStaff: 0 });
  const [academicOverview, setAcademicOverview] = useState<AcademicOverview | null>(null);
  const [supervisionDataQuality, setSupervisionDataQuality] = useState<SupervisionDataQuality | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    const load = async () => {
      try {
        if (isSupportStaff) {
          if (active) {
            setLoading(false);
          }
          return;
        }

        const [users, academics, supervisionQuality] = await Promise.all([
          userbaseApi.users.list(),
          academicsApi.getOverview().catch(() => null),
          supervisionApi.getSupervisionDataQuality().catch(() => null),
        ]);

        if (!active) {
          return;
        }

        setStats({
          users: users.length,
          residents: users.filter((row) => row.role === 'RESIDENT').length,
          supervisors: users.filter((row) => row.role === 'SUPERVISOR').length,
          supportStaff: users.filter((row) => row.role === 'SUPPORT_STAFF').length,
        });
        setAcademicOverview(academics);
        setSupervisionDataQuality(supervisionQuality);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    load();

    return () => {
      active = false;
    };
  }, [isSupportStaff]);

  if (isSupportStaff) {
    return (
      <ProtectedRoute allowedRoles={['ADMIN', 'SUPPORT_STAFF']}>
        <div className="pg-page space-y-6">
          <PageHeader
            title="Support Staff Dashboard"
            description="Restricted support-staff shell. Administrative setup and canonical mutation modules remain hidden."
          />
          <div className="grid gap-4 md:grid-cols-2">
            <div className="pg-card">
              <h2 className="pg-section-title">My Access</h2>
              <p className="mt-3 text-sm text-slate-600">This role is limited to profile completion and read-only operational support.</p>
            </div>
            <div className="pg-card">
              <h2 className="pg-section-title">Available Actions</h2>
              <div className="mt-3 flex flex-wrap gap-3">
                <Link href="/complete-profile" className="pg-btn-primary">Complete Profile</Link>
                <Link href="/change-password" className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700">
                  Change Password
                </Link>
              </div>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPPORT_STAFF']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Admin Dashboard"
          description="Canonical PGMS administration shell for users, masters, supervision, academics, and data quality."
        />

        {loading ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-500">
            Loading administrative overview...
          </div>
        ) : (
          <>
            <div className="grid gap-4 md:grid-cols-4">
              <MetricCard label="Users" value={stats.users} />
              <MetricCard label="Residents" value={stats.residents} />
              <MetricCard label="Supervisors" value={stats.supervisors} />
              <MetricCard label="Support Staff" value={stats.supportStaff} />
            </div>

            <div className="grid gap-4 md:grid-cols-4">
              <MetricCard label="Training Records" value={academicOverview?.cards?.active_training_records || 0} />
              <MetricCard label="Review Queue Items" value={academicOverview?.cards?.pending_review_queue_items || 0} />
              <MetricCard label="Residents Without Training Record" value={academicOverview?.cards?.residents_without_training_record || 0} tone="warning" />
              <MetricCard label="Supervision Warnings" value={supervisionDataQuality ? Object.values(supervisionDataQuality).reduce((count, rows) => count + rows.length, 0) : 0} tone="warning" />
            </div>

            <section className="pg-card">
              <h2 className="pg-section-title">Canonical Modules</h2>
              <div className="mt-4 flex flex-wrap gap-3">
                {adminQuickLinks.map((item) => (
                  <Link key={item.href} href={item.href} className="pg-btn-primary">
                    {item.label}
                  </Link>
                ))}
              </div>
            </section>
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
