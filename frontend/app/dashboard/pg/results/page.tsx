'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { resultsApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import { format } from 'date-fns';

interface ExamScore {
  id: number;
  exam: number | { title?: string; date?: string; max_marks?: number };
  marks_obtained: number;
  percentage?: number;
  grade?: string;
  is_passing: boolean;
  created_at?: string;
}

export default function PGResultsPage() {
  const [scores, setScores] = useState<ExamScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadScores();
  }, []);

  async function loadScores() {
    try {
      setLoading(true);
      setError(null);
      const data = await resultsApi.scores.getMyScores();
      setScores(Array.isArray(data) ? data : []);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load exam results';
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  const columns: Column<ExamScore>[] = [
    {
      key: 'exam',
      label: 'Exam',
      render: (item) => {
        if (typeof item.exam === 'object' && item.exam?.title) {
          return item.exam.title;
        }
        if (typeof item.exam === 'number') {
          return String(item.exam);
        }
        return '-';
      },
    },
    {
      key: 'created_at',
      label: 'Date',
      render: (item) => {
        try {
          if (typeof item.exam === 'object' && item.exam?.date) {
            return format(new Date(item.exam.date), 'MMM dd, yyyy');
          }
          if (item.created_at) {
            return format(new Date(item.created_at), 'MMM dd, yyyy');
          }
          return '-';
        } catch {
          return '-';
        }
      },
    },
    {
      key: 'marks_obtained',
      label: 'Score',
      render: (item) => {
        const marks = item.marks_obtained;
        const maxMarks = typeof item.exam === 'object' ? item.exam?.max_marks : undefined;
        if (marks !== undefined && maxMarks !== undefined) {
          return `${marks} / ${maxMarks}`;
        }
        return marks !== undefined ? marks.toString() : '-';
      },
    },
    {
      key: 'percentage',
      label: 'Percentage',
      render: (item) => {
        if (item.percentage !== undefined) {
          return `${item.percentage.toFixed(1)}%`;
        }
        return '-';
      },
    },
    {
      key: 'grade',
      label: 'Grade',
      render: (item) => (
        <span className={`px-2 py-1 text-xs rounded-full ${
          item.is_passing ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {item.grade || (item.is_passing ? 'Pass' : 'Fail')}
        </span>
      ),
    },
    {
      key: 'is_passing',
      label: 'Status',
      render: (item) => (
        <span className={`px-2 py-1 text-xs rounded-full ${
          item.is_passing ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {item.is_passing ? 'Pass' : 'Fail'}
        </span>
      ),
    },
  ];

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Exam Results</h1>
            <p className="mt-2 text-gray-600">View your exam scores and grades</p>
          </div>

          {error && <ErrorBanner message={error} />}

          <SectionCard title="My Exam Scores">
            {loading ? (
              <TableSkeleton rows={10} cols={6} />
            ) : (
              <DataTable
                columns={columns}
                data={scores}
                emptyMessage="No exam results available"
              />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
