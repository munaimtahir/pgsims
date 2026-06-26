'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import ResidentOnboardingWizard from '@/components/onboarding/ResidentOnboardingWizard';

export default function ResidentOnboardingPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <ResidentOnboardingWizard />
    </ProtectedRoute>
  );
}
