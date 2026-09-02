'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { userbaseApi, UserbaseUser } from '@/lib/api/userbase';

export default function SupportStaffDetailPage() {
  const params = useParams();
  const [user, setUser] = useState<UserbaseUser | null>(null);

  useEffect(() => {
    const id = Number(params.id);
    if (!id) return;
    userbaseApi.users.get(id).then(setUser).catch(() => setUser(null));
  }, [params.id]);

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Support Staff Detail"
          description="Canonical support-staff identity detail."
        />
        <div className="pg-card">
          <p className="font-semibold text-slate-900">{user?.full_name || user?.username || 'Support staff'}</p>
          <p className="mt-2 text-sm text-slate-600">Role: {user?.role || 'SUPPORT_STAFF'}</p>
          <p className="text-sm text-slate-600">Email: {user?.email || 'Not set'}</p>
          <p className="text-sm text-slate-600">Phone: {user?.phone_number || 'Not set'}</p>
        </div>
      </div>
    </ProtectedRoute>
  );
}
