'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { analyticsApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import LoadingSkeleton, { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';

type TabType = 'trends' | 'performance' | 'compliance';

export default function AdminAnalyticsPage() {
  const [activeTab, setActiveTab] = useState<TabType>('trends');
  const [trendsData, setTrendsData] = useState<any[]>([]);
  const [performanceData, setPerformanceData] = useState<any>(null);
  const [complianceData, setComplianceData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTabData();
  }, [activeTab]);

  async function loadTabData() {
    try {
      setLoading(true);
      setError(null);

      switch (activeTab) {
        case 'trends':
          const trends = await analyticsApi.getTrends();
          setTrendsData(Array.isArray(trends) ? trends : []);
          break;
        case 'performance':
          const performance = await analyticsApi.getPerformance();
          setPerformanceData(performance);
          break;
        case 'compliance':
          const compliance = await analyticsApi.getCompliance();
          setComplianceData(compliance);
          break;
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  }

  const trendsColumns: Column<any>[] = [
    { key: 'period', label: 'Period' },
    { key: 'label', label: 'Label' },
    { key: 'value', label: 'Value', render: (item) => item.value?.toLocaleString() || '-' },
  ];

  return (
    <ProtectedRoute allowedRoles={['admin']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
            <p className="mt-2 text-gray-600">View system analytics and metrics</p>
          </div>

          {error && <ErrorBanner message={error} />}

          {/* Tabs */}
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {(['trends', 'performance', 'compliance'] as TabType[]).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`${
                    activeTab === tab
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm capitalize`}
                >
                  {tab}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          {loading ? (
            <TableSkeleton rows={5} cols={3} />
          ) : (
            <>
              {activeTab === 'trends' && (
                <SectionCard title="Trends">
                  {trendsData.length > 0 ? (
                    <DataTable columns={trendsColumns} data={trendsData} />
                  ) : (
                    <div className="text-center py-8 text-gray-500">No trends data available</div>
                  )}
                </SectionCard>
              )}

              {activeTab === 'performance' && (
                <SectionCard title="Performance Metrics">
                  {performanceData ? (
                    <div className="space-y-4">
                      {performanceData.average_scores !== undefined && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Average Scores</dt>
                          <dd className="mt-1 text-2xl font-semibold text-gray-900">
                            {performanceData.average_scores.toFixed(2)}
                          </dd>
                        </div>
                      )}
                      {performanceData.pass_rate !== undefined && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Pass Rate</dt>
                          <dd className="mt-1 text-2xl font-semibold text-gray-900">
                            {(performanceData.pass_rate * 100).toFixed(1)}%
                          </dd>
                        </div>
                      )}
                      {performanceData.completion_rate !== undefined && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Completion Rate</dt>
                          <dd className="mt-1 text-2xl font-semibold text-gray-900">
                            {(performanceData.completion_rate * 100).toFixed(1)}%
                          </dd>
                        </div>
                      )}
                      {process.env.NODE_ENV === 'development' && (
                        <details className="text-xs mt-4">
                          <summary className="cursor-pointer text-gray-600">Debug: Raw Data</summary>
                          <pre className="mt-2 p-4 bg-gray-100 rounded overflow-auto">
                            {JSON.stringify(performanceData, null, 2)}
                          </pre>
                        </details>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">No performance data available</div>
                  )}
                </SectionCard>
              )}

              {activeTab === 'compliance' && (
                <SectionCard title="Compliance Metrics">
                  {complianceData ? (
                    <div className="space-y-4">
                      {complianceData.logbook_compliance !== undefined && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Logbook Compliance</dt>
                          <dd className="mt-1 text-2xl font-semibold text-gray-900">
                            {(complianceData.logbook_compliance * 100).toFixed(1)}%
                          </dd>
                        </div>
                      )}
                      {complianceData.certificate_compliance !== undefined && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Certificate Compliance</dt>
                          <dd className="mt-1 text-2xl font-semibold text-gray-900">
                            {(complianceData.certificate_compliance * 100).toFixed(1)}%
                          </dd>
                        </div>
                      )}
                      {complianceData.overall_compliance !== undefined && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Overall Compliance</dt>
                          <dd className="mt-1 text-2xl font-semibold text-gray-900">
                            {(complianceData.overall_compliance * 100).toFixed(1)}%
                          </dd>
                        </div>
                      )}
                      {process.env.NODE_ENV === 'development' && (
                        <details className="text-xs mt-4">
                          <summary className="cursor-pointer text-gray-600">Debug: Raw Data</summary>
                          <pre className="mt-2 p-4 bg-gray-100 rounded overflow-auto">
                            {JSON.stringify(complianceData, null, 2)}
                          </pre>
                        </details>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">No compliance data available</div>
                  )}
                </SectionCard>
              )}
            </>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
