'use client';

import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api/auth';
import Sidebar from './Sidebar';
import { Bell, ChevronDown, Search } from 'lucide-react';
import { useState, useMemo, useEffect } from 'react';
import { getNavForRole, NavSubItem } from '@/lib/navRegistry';
import { notificationsApi } from '@/lib/api/notifications';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, clearAuth } = useAuthStore();
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [unread, setUnread] = useState<number | null>(null);

  const handleLogout = async () => {
    await authApi.logout();
    clearAuth();
    router.push('/login');
  };

  const userName = user?.full_name || user?.email || '';
  const suggestions = useMemo<NavSubItem[]>(() => getNavForRole(user?.role ?? '').flatMap((section) => section.items.flatMap((item) => item.subItems || (item.href ? [{ label: item.label, href: item.href }] : []))).filter((item) => item.label.toLowerCase().includes(query.toLowerCase())).slice(0, 5), [query, user?.role]);

  useEffect(() => {
    notificationsApi.getUnreadCount().then((result) => setUnread(result.count)).catch(() => setUnread(null));
  }, []);

  const submitSearch = (event: React.FormEvent) => {
    event.preventDefault();
    const match = suggestions[0];
    if (match?.href) router.push(match.href);
  };

  return (
    <div className="pg-app flex min-h-screen overflow-hidden">
      <Sidebar role={user?.role ?? ''} userName={userName} onLogout={handleLogout} />
      <main className="min-w-0 flex-1 overflow-y-auto">
        <header className="pg-topbar">
          <form onSubmit={submitSearch} className="relative hidden max-w-md flex-1 md:block">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" aria-hidden="true" />
            <input aria-label="Search navigation" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search modules..." className="pg-search-input" />
            {query && suggestions.length > 0 && <div className="absolute left-0 right-0 top-12 z-30 rounded-xl border border-slate-200 bg-white p-1 shadow-xl">{suggestions.map((item) => <button type="button" key={item.href} onClick={() => { setQuery(''); router.push(item.href); }} className="block w-full rounded-lg px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50">{item.label}</button>)}</div>}
          </form>
          <div className="ml-auto flex items-center gap-3">
            <button type="button" aria-label={unread === null ? 'Notifications unavailable' : `${unread} unread notifications`} className="pg-topbar-icon"><Bell className="h-5 w-5" />{unread !== null && unread > 0 && <span className="pg-notification-dot">{unread > 9 ? '9+' : unread}</span>}</button>
            <button type="button" onClick={() => router.push('/profile')} aria-label={`Open account for ${userName || 'account'}`} className="flex items-center gap-2 rounded-xl px-2 py-1.5 text-left hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"><span className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-blue-700">{userName?.charAt(0).toUpperCase() || 'U'}</span><span className="hidden sm:block"><span className="block text-sm font-semibold text-slate-800">Account</span><span className="block text-xs text-slate-500">{user?.role?.replace('_', ' ')}</span></span><ChevronDown className="hidden h-4 w-4 text-slate-400 sm:block" /></button>
          </div>
        </header>
        <div className="mx-auto w-full max-w-[1440px] px-4 py-6 sm:px-6 lg:px-10">
          {children}
        </div>
      </main>
    </div>
  );
}
