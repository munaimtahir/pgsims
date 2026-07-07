'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DeferredWorkflowNotice from '@/components/ui/DeferredWorkflowNotice';

export default function ResidentResearchPage() {
  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'RESIDENT']}>
      <DeferredWorkflowNotice
        title="Research"
        description="Synopsis and research submission workflows are deferred from the current active release surface."
      />
    </ProtectedRoute>
  );
}
