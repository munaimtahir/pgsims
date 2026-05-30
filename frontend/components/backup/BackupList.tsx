/* eslint-disable @typescript-eslint/no-explicit-any */
import React from 'react';
import { format } from 'date-fns';
import { Download, Clock, Trash2 } from 'lucide-react';
import { fetchAuth } from '@/lib/auth/fetch';

export default function BackupList({ backups, onRefresh }: { backups: any[], onRefresh: () => void }) {
  const handleDownload = async (backupId: number, filename: string) => {
    try {
      const response = await fetchAuth(`/api/backup_center/backups/${backupId}/download/`, {
        method: 'GET',
      });
      
      if (!response.ok) {
        alert('Download failed or not authorized');
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
      alert('An error occurred during download');
    }
  };

  const handleDelete = async (backupId: number) => {
    if (!confirm('Are you sure you want to delete this backup? This cannot be undone.')) return;
    
    try {
      const response = await fetchAuth(`/api/backup_center/backups/${backupId}/delete/`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        alert('Backup deleted');
        onRefresh();
      } else {
        alert('Failed to delete backup');
      }
    } catch (error) {
      console.error(error);
      alert('An error occurred while deleting');
    }
  };

  if (!backups || backups.length === 0) {
    return (
      <div className="p-10 text-center">
        <Clock className="mx-auto h-12 w-12 text-gray-400" />
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
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-x-3">
              <p className="text-sm font-semibold leading-6 text-gray-900">{backup.file_name || 'Processing...'}</p>
              <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${
                backup.backup_kind === 'disaster_recovery' ? 'bg-purple-50 text-purple-700 ring-purple-700/10' : 'bg-blue-50 text-blue-700 ring-blue-700/10'
              }`}>
                {backup.backup_kind === 'disaster_recovery' ? 'Disaster' : 'Routine'}
              </span>
              <p className={`rounded-md whitespace-nowrap px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset ${
                backup.status === 'completed' ? 'bg-green-50 text-green-700 ring-green-600/20' : 
                backup.status === 'failed' ? 'bg-red-50 text-red-700 ring-red-600/20' : 
                'bg-yellow-50 text-yellow-800 ring-yellow-600/20'
              }`}>
                {backup.status.toUpperCase()}
              </p>
            </div>
            <div className="mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500">
              <p className="whitespace-nowrap">
                {format(new Date(backup.created_at), 'PPP p')}
              </p>
              <svg viewBox="0 0 2 2" className="h-0.5 w-0.5 fill-current">
                <circle cx={1} cy={1} r={1} />
              </svg>
              <p className="truncate">{formatSize(backup.file_size)}</p>
              <svg viewBox="0 0 2 2" className="h-0.5 w-0.5 fill-current">
                <circle cx={1} cy={1} r={1} />
              </svg>
              <p className="truncate">{backup.database_engine}</p>
              {backup.created_by_username && (
                <>
                  <svg viewBox="0 0 2 2" className="h-0.5 w-0.5 fill-current">
                    <circle cx={1} cy={1} r={1} />
                  </svg>
                  <p className="truncate">by {backup.created_by_username}</p>
                </>
              )}
            </div>
            {backup.notes && (
               <p className="mt-1 text-xs text-gray-400 italic truncate max-w-md">{backup.notes}</p>
            )}
          </div>
          <div className="flex flex-none items-center gap-x-2">
            {backup.status === 'completed' && backup.file_name && (
              <button
                onClick={() => handleDownload(backup.id, backup.file_name)}
                className="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              >
                <Download className="h-4 w-4 inline-block mr-1" />
                Download
              </button>
            )}
            {backup.status !== 'running' && (
               <button
               onClick={() => handleDelete(backup.id)}
               className="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-red-600 shadow-sm ring-1 ring-inset ring-red-300 hover:bg-red-50"
             >
               <Trash2 className="h-4 w-4" />
             </button>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}

