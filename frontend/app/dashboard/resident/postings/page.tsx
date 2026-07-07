'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DeferredWorkflowNotice from '@/components/ui/DeferredWorkflowNotice';

export default function ResidentPostingsPage() {
  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'RESIDENT']}>
      <DeferredWorkflowNotice
        title="Postings"
        description="Deputation postings are deferred from the current active release surface."
      />
    </ProtectedRoute>
  );
}
