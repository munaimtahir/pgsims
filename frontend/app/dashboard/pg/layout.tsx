'use client';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function PGLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute allowedRoles={['RESIDENT', 'RESIDENT', 'ADMIN']}>
      {children}
    </ProtectedRoute>
  );
}
