'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DeferredWorkflowNotice from '@/components/ui/DeferredWorkflowNotice';

export default function ResidentThesisPage() {
  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'RESIDENT']}>
      <DeferredWorkflowNotice
        title="Thesis"
        description="Thesis submission is deferred from the current active release surface."
      />
    </ProtectedRoute>
  );
}
