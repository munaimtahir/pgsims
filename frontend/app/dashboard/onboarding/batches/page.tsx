'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import ImportedBatchesPanel from '@/components/onboarding/ImportedBatchesPanel';

export default function ImportedBatchesPage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <ImportedBatchesPanel />
    </ProtectedRoute>
  );
}
