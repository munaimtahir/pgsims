'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import IncompleteProfilesPanel from '@/components/onboarding/IncompleteProfilesPanel';

export default function IncompleteProfilesPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <IncompleteProfilesPanel />
    </ProtectedRoute>
  );
}
