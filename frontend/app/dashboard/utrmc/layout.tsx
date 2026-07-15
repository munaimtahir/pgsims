'use client';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function UTRMCLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute allowedRoles={['ADMIN', 'SUPPORT_STAFF']}>
      {children}
    </ProtectedRoute>
  );
}
