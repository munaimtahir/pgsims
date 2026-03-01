'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';

const NAV = [
  { label: 'Overview', href: '/dashboard/utrmc' },
  { label: 'Hospitals', href: '/dashboard/utrmc/hospitals' },
  { label: 'Departments', href: '/dashboard/utrmc/departments' },
  { label: 'Hospital-Dept Matrix', href: '/dashboard/utrmc/matrix' },
  { label: 'Users', href: '/dashboard/utrmc/users' },
  { label: 'Supervision Links', href: '/dashboard/utrmc/supervision' },
  { label: 'HOD Assignments', href: '/dashboard/utrmc/hod' },
];

export default function UTRMCLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin', 'utrmc_user']}>
      <DashboardLayout>
        <div className="flex gap-6">
          <nav className="w-48 shrink-0">
            <ul className="space-y-1">
              {NAV.map((n) => (
                <li key={n.href}>
                  <Link
                    href={n.href}
                    className={`block px-3 py-2 rounded text-sm font-medium ${
                      pathname === n.href
                        ? 'bg-indigo-600 text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {n.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
          <div className="flex-1 min-w-0">{children}</div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
