'use client';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function UTRMCLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
      {children}
    </ProtectedRoute>
  );
}
