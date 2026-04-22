'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DeferredWorkflowNotice from '@/components/ui/DeferredWorkflowNotice';

export default function SupervisorResearchApprovalsPage() {
  return (
    <ProtectedRoute allowedRoles={['supervisor', 'faculty', 'admin', 'utrmc_admin']}>
      <DeferredWorkflowNotice
        title="Research Approvals"
        description="Supervisor synopsis/research approvals are deferred from the current active release surface."
      />
    </ProtectedRoute>
  );
}
