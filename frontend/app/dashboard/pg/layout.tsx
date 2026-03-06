'use client';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function PGLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute allowedRoles={['pg', 'resident', 'admin']}>
      {children}
    </ProtectedRoute>
  );
}
