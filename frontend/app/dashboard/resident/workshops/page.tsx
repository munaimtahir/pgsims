'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DeferredWorkflowNotice from '@/components/ui/DeferredWorkflowNotice';

export default function ResidentWorkshopsPage() {
  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'RESIDENT']}>
      <DeferredWorkflowNotice
        title="Workshops"
        description="Workshop recording is deferred from the current active release surface."
      />
    </ProtectedRoute>
  );
}
