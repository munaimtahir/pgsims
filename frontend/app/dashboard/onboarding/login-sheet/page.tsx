'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import LoginSheetPanel from '@/components/onboarding/LoginSheetPanel';

export default function LoginSheetPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <LoginSheetPanel />
    </ProtectedRoute>
  );
}
