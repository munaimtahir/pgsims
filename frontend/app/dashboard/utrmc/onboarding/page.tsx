'use client';

import Link from 'next/link';

import BulkSetupWorkspace from '@/components/utrmc/BulkSetupWorkspace';
import PageHeader from '@/components/ui/PageHeader';

export default function UtrmcOnboardingPage() {
  return (
    <div className="pg-page">
      <PageHeader
        title="Onboarding & Import Tools"
        description="Guided onboarding and import tools will be available here."
        actions={(
          <Link href="/dashboard/utrmc" className="pg-btn-primary inline-flex items-center">
            Back to UTRMC Dashboard
          </Link>
        )}
      />

      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm leading-6 text-slate-700">
        Upload residents, supervisors, departments, matrix links, and program data in a safer, guided order.
        Start with the overview card first, then use the import panels below when you are ready.
      </div>

      <div className="mt-6">
        <BulkSetupWorkspace />
      </div>
    </div>
  );
}
