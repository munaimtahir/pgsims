'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import { academicsApi, AcademicDataQuality } from '@/lib/api/academics';

export default function AcademicDataQualityPage() {
  const [payload, setPayload] = useState<AcademicDataQuality | null>(null);
  useEffect(() => {
    academicsApi.getDataQuality().then(setPayload).catch(() => setPayload({ summary: {}, sections: [] }));
  }, []);
  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader title="Academic Data Quality" description="Readiness gaps across training records, supervision, and review queue." />
        <div className="pg-kpi-grid md:grid-cols-4">
          {Object.entries(payload?.summary || {}).slice(0, 8).map(([key, value]) => (
            <div key={key} className="pg-card">
              <p className="text-xs uppercase tracking-wider text-slate-500">{key.replaceAll('_', ' ')}</p>
              <p className="mt-2 text-2xl font-semibold text-slate-900">{value}</p>
            </div>
          ))}
        </div>
        <div className="space-y-4">
          {(payload?.sections || []).map((section) => (
            <div key={section.key} className="pg-card">
              <div className="flex items-center justify-between gap-3">
                <h2 className="text-lg font-semibold text-slate-900">{section.label}</h2>
                <span className="rounded-full bg-amber-50 px-3 py-1 text-sm font-medium text-amber-700">{section.count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
