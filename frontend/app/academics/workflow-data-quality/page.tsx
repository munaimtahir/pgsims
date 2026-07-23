'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import MetricCard from '@/components/ui/MetricCard';
import { academicsApi } from '@/lib/api/academics';

interface DataQualityItem {
  resident_name?: string;
  name?: string;
  issue_details?: string;
  notes?: string;
}

interface DataQualitySectionRow {
  key: string;
  label: string;
  count: number;
  items?: DataQualityItem[];
}

interface DataQualityData {
  summary?: Record<string, number>;
  sections?: DataQualitySectionRow[];
}

export default function WorkflowDataQualityPage() {
  const [dq, setDq] = useState<DataQualityData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    academicsApi
      .getAcademicWorkflowDataQuality()
      .then((data) => setDq(data as unknown as DataQualityData))
      .catch(() => setDq(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading && !dq) {
    return <div className="text-center py-6 text-sm text-slate-500">Loading data quality metrics...</div>;
  }

  const summary = dq?.summary || {};
  const sections = dq?.sections || [];

  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Workflow Data Quality & Audits"
          description="Identify discrepancies, missing rotation evaluations, inactive or orphan training records, and logbook threshold warnings."
        />

        <div className="pg-kpi-grid md:grid-cols-4">
          <MetricCard
            label="No Evaluation Submissions"
            value={summary.residents_with_active_record_no_evaluations || 0}
            tone={summary.residents_with_active_record_no_evaluations > 0 ? 'warning' : 'default'}
          />
          <MetricCard
            label="No Logbook Procedures"
            value={summary.residents_with_active_record_no_logbooks || 0}
            tone={summary.residents_with_active_record_no_logbooks > 0 ? 'warning' : 'default'}
          />
          <MetricCard
            label="Pending Review Queue Items"
            value={summary.pending_review_queue_items || 0}
            tone={summary.pending_review_queue_items > 0 ? 'info' : 'default'}
          />
          <MetricCard
            label="Unassigned Supervisors"
            value={summary.active_residents_without_primary_supervisor || 0}
            tone={summary.active_residents_without_primary_supervisor > 0 ? 'warning' : 'default'}
          />
        </div>

        {/* Dynamic Warning Sections */}
        <div className="space-y-6">
          {sections.map((section) => (
            <div key={section.key} className="pg-card space-y-3">
              <div className="flex justify-between items-center border-b border-slate-100 pb-2">
                <h3 className="text-base font-semibold text-slate-900">{section.label}</h3>
                <span className="rounded bg-red-100 text-red-750 text-xs font-semibold px-2 py-0.5">
                  {section.count} Issues
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-50 text-xs text-slate-500 uppercase">
                    <tr>
                      <th className="px-3 py-2 text-left">Resident</th>
                      <th className="px-3 py-2 text-left">Details</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {section.items?.map((item, idx) => (
                      <tr key={idx}>
                        <td className="px-3 py-2 font-medium text-slate-800">
                          {item.resident_name || item.name || 'Unknown'}
                        </td>
                        <td className="px-3 py-2 text-slate-600 text-xs">
                          {item.issue_details || item.notes || 'Missing registry fields or training spine data.'}
                        </td>
                      </tr>
                    ))}
                    {(!section.items || section.items.length === 0) && (
                      <tr>
                        <td className="px-3 py-4 text-center text-slate-500 text-xs" colSpan={2}>
                          No quality warnings in this category. Clean record!
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
