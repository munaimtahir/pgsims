'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi, AcademicOverview } from '@/lib/api/academics';

export default function AcademicsHomePage() {
  const [overview, setOverview] = useState<AcademicOverview | null>(null);

  useEffect(() => {
    academicsApi.getOverview().then(setOverview).catch(() => setOverview({ cards: {} }));
  }, []);

  const cards = overview?.cards || {};

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Academic Workflow Foundation"
          description="Brick 8 academic container for training records, registries, review queue, and readiness checks."
        />

        <div className="pg-kpi-grid md:grid-cols-4">
          <MetricCard label="Active Training Records" value={cards.active_training_records || 0} />
          <MetricCard label="Residents without Record" value={cards.residents_without_training_record || 0} tone="warning" />
          <MetricCard label="No Primary Supervisor" value={cards.residents_without_primary_supervisor || 0} tone="warning" />
          <MetricCard label="Pending Review Queue" value={cards.pending_review_queue_items || 0} tone="info" />
          <MetricCard label="Academic Periods" value={cards.active_academic_periods || 0} />
          <MetricCard label="Evaluation Templates" value={cards.active_evaluation_templates || 0} />
          <MetricCard label="Logbook Categories" value={cards.active_logbook_categories || 0} />
          <MetricCard label="Warnings" value={cards.data_quality_warnings || 0} tone="warning" />
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {[
            ['Training Records', '/academics/training-records'],
            ['Academic Periods', '/academics/periods'],
            ['Rotation Templates', '/academics/rotation-templates'],
            ['Evaluation Templates', '/academics/evaluation-templates'],
            ['Logbook Categories', '/academics/logbook-categories'],
            ['Review Queue', '/academics/review-queue'],
            ['Academic Data Quality', '/academics/data-quality'],
          ].map(([label, href]) => (
            <Link key={href} href={href} className="pg-card transition hover:border-indigo-300">
              <h2 className="text-lg font-semibold text-slate-900">{label}</h2>
              <p className="mt-2 text-sm text-slate-600">Open {label.toLowerCase()}.</p>
            </Link>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
