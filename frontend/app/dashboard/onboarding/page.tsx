'use client';

import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

const LINKS = [
  { href: '/dashboard/onboarding/residents', label: 'Resident Onboarding', body: 'Upload Excel/CSV, map columns, preview rows, import residents, and generate login IDs.' },
  { href: '/dashboard/onboarding/login-sheet', label: 'Login Sheet', body: 'Export, issue, and reset resident login credentials.' },
  { href: '/dashboard/onboarding/batches', label: 'Imported Batches', body: 'Review prior imports and batch-level outcomes.' },
  { href: '/dashboard/onboarding/incomplete-profiles', label: 'Incomplete Profiles', body: 'Finish first-login profile setup and export the outstanding list.' },
];

export default function OnboardingHomePage() {
  return (
    <ProtectedRoute allowedRoles={['admin', 'utrmc_admin']}>
      <div className="space-y-6">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-semibold text-slate-900">Onboarding</h1>
          <p className="mt-1 text-sm text-slate-500">Simple resident onboarding tools exposed through the UI.</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {LINKS.map((item) => (
            <Link key={item.href} href={item.href} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-indigo-200 hover:bg-indigo-50/30">
              <div className="text-lg font-semibold text-slate-900">{item.label}</div>
              <p className="mt-2 text-sm leading-6 text-slate-600">{item.body}</p>
            </Link>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
