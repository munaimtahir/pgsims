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
    <div className="flex min-h-screen overflow-hidden bg-slate-50">
      <Sidebar role={user?.role ?? ''} userName={userName} onLogout={handleLogout} />
      <main className="flex-1 overflow-y-auto bg-gradient-to-b from-slate-50 to-slate-100/50">
        <div className="mx-auto w-full max-w-7xl px-4 py-5 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
}
