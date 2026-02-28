'use client';

import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api/auth';
import Sidebar from './Sidebar';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, clearAuth } = useAuthStore();
  const router = useRouter();

  const handleLogout = async () => {
    await authApi.logout();
    clearAuth();
    router.push('/login');
  };

  const userName = user?.full_name || user?.email || '';

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar role={user?.role ?? ''} userName={userName} onLogout={handleLogout} />
      <main className="flex-1 overflow-y-auto">
        <div className="px-6 py-6 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
