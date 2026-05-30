import React from 'react';
import { format } from 'date-fns';
import { ArrowDownTrayIcon, ClockIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-hot-toast';

export default function BackupList({ backups }: { backups: Record<string, unknown>[] }) {
  const handleDownload = async (backupId: number, filename: string) => {
    try {
      const response = await fetch(`/api/backup_center/jobs/${backupId}/download/`, {
        method: 'GET',
        // In a real app with JWT auth we might need to handle this differently if it's protected
        // For simplicity, assuming the endpoint handles standard session auth or we use fetchAuth approach
        // if using next-auth or custom fetchAuth that adds headers, we need a Blob.
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}` // simple example
        }
      });
      
      if (!response.ok) {
        toast.error('Download failed or not authorized');
        return;
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || `backup_${backupId}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (error) {
      console.error(error);
      toast.error('An error occurred during download');
    }
  };

  if (!backups || backups.length === 0) {
    return (
      <div className="p-10 text-center">
        <ClockIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-semibold text-gray-900">No backups</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new system backup.</p>
      </div>
    );
  }

  const formatSize = (bytes: number) => {
    if (!bytes) return 'Unknown size';
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)).toString());
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <ul role="list" className="divide-y divide-gray-100">
      {backups.map((backup) => (
        <li key={backup.id} className="flex items-center justify-between gap-x-6 py-5 px-6 hover:bg-gray-50">
          <div className="min-w-0">
            <div className="flex items-start gap-x-3">
              <p className="text-sm font-semibold leading-6 text-gray-900">{backup.file_name || 'In Progress...'}</p>
              <p className={`rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset ${
                backup.status === 'completed' ? 'bg-green-50 text-green-700 ring-green-600/20' : 
                backup.status === 'failed' ? 'bg-red-50 text-red-700 ring-red-600/20' : 
                'bg-yellow-50 text-yellow-800 ring-yellow-600/20'
              }`}>
                {backup.status.toUpperCase()}
              </p>
            </div>
            <div className="mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500">
              <p className="whitespace-nowrap">
                Created {format(new Date(backup.created_at), 'PPP p')}
              </p>
              <svg viewBox="0 0 2 2" className="h-0.5 w-0.5 fill-current">
                <circle cx={1} cy={1} r={1} />
              </svg>
              <p className="truncate">{formatSize(backup.file_size)}</p>
              {backup.manifest_json && typeof backup.manifest_json === 'object' && 'notes' in backup.manifest_json && (
                <>
                  <svg viewBox="0 0 2 2" className="h-0.5 w-0.5 fill-current">
                    <circle cx={1} cy={1} r={1} />
                  </svg>
                  <p className="truncate text-gray-700">{String(backup.manifest_json.notes)}</p>
                </>
              )}
            </div>
          </div>
          <div className="flex flex-none items-center gap-x-4">
            {backup.status === 'completed' && backup.file_name && (
              <button
                onClick={() => handleDownload(backup.id, backup.file_name)}
                className="hidden rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:block"
              >
                Download
              </button>
            )}
            {backup.status === 'completed' && backup.file_name && (
                <button
                onClick={() => handleDownload(backup.id, backup.file_name)}
                className="rounded-md bg-white p-1 text-gray-400 hover:text-gray-500 sm:hidden"
              >
                <ArrowDownTrayIcon className="h-5 w-5" aria-hidden="true" />
              </button>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
