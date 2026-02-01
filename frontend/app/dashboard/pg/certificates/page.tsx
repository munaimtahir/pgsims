'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Download } from 'lucide-react';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import SectionCard from '@/components/ui/SectionCard';
import EmptyState from '@/components/ui/EmptyState';
import { DataTable, ColumnDef } from '@/components/ui/DataTable';
import LoadingSkeleton from '@/components/ui/LoadingSkeleton';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { certificatesApi, CertificateSummary } from '@/lib/api/certificates';
import { format } from 'date-fns';

const getStatusClasses = (status: string) => {
  switch (status.toLowerCase()) {
    case 'approved':
      return 'bg-green-100 text-green-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'rejected':
      return 'bg-red-100 text-red-800';
    case 'expired':
      return 'bg-gray-100 text-gray-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function PGCertificatesPage() {
  const [downloading, setDownloading] = useState<number | null>(null);
  const [downloadSuccess, setDownloadSuccess] = useState<string | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const { data: certificates, isLoading, isError, error } = useQuery({
    queryKey: ['my-certificates'],
    queryFn: certificatesApi.getMyCertificates,
  });

  const handleDownload = async (cert: CertificateSummary) => {
    if (!cert.has_file) return;

    setDownloading(cert.id);
    setDownloadError(null);
    setDownloadSuccess(null);

    try {
      const success = await certificatesApi.downloadCertificate(cert.id, cert.file_name || `${cert.title}.pdf`);
      if (success) {
        setDownloadSuccess(`Successfully downloaded ${cert.file_name}.`);
      } else {
        throw new Error('Download failed unexpectedly.');
      }
    } catch (e: any) {
      setDownloadError(`Failed to download ${cert.file_name}. Please try again.`);
      console.error(e);
    } finally {
      setDownloading(null);
    }
  };

  const columns: ColumnDef<CertificateSummary>[] = [
    {
      accessorKey: 'title',
      header: 'Certificate Title',
      cell: ({ row }) => <span className="font-medium">{row.original.title}</span>,
    },
    {
      accessorKey: 'certificate_type_name',
      header: 'Type',
    },
    {
      accessorKey: 'issue_date',
      header: 'Issue Date',
      cell: ({ row }) => format(new Date(row.original.issue_date), 'dd MMM yyyy'),
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => (
        <span
          className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClasses(
            row.original.status
          )}`}
        >
          {row.original.status}
        </span>
      ),
    },
    {
      id: 'actions',
      header: 'Actions',
      cell: ({ row }) => {
        const cert = row.original;
        const isDownloading = downloading === cert.id;
        return (
          <button
            onClick={() => handleDownload(cert)}
            disabled={!cert.has_file || isDownloading}
            className="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Download className="mr-2 h-4 w-4" />
            {isDownloading ? 'Downloading...' : 'Download'}
          </button>
        );
      },
    },
  ];

  const renderContent = () => {
    if (isLoading) {
      return <LoadingSkeleton count={5} />;
    }

    if (isError) {
      return <ErrorBanner title="Failed to load certificates" message={error.message} />;
    }

    if (!certificates || certificates.length === 0) {
      return (
        <EmptyState
          title="No Certificates Found"
          description="You have not uploaded any certificates yet."
        />
      );
    }

    return <DataTable columns={columns} data={certificates} />;
  };

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Certificates</h1>
            <p className="mt-2 text-gray-600">View and download your uploaded certificates.</p>
          </div>
          
          {downloadSuccess && <SuccessBanner title="Download Complete" message={downloadSuccess} />}
          {downloadError && <ErrorBanner title="Download Failed" message={downloadError} />}

          <SectionCard>
            {renderContent()}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
