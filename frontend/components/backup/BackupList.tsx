/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useMemo, useState } from 'react';
import { format } from 'date-fns';
import { Download, Clock, Trash2, ShieldCheck, FileSearch } from 'lucide-react';
import { fetchAuth } from '@/lib/auth/fetch';

export default function BackupList({ backups, onRefresh }: { backups: any[], onRefresh: () => void }) {
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [lastValidationById, setLastValidationById] = useState<Record<number, any>>({});

  const sortedBackups = useMemo(() => {
    const arr = Array.isArray(backups) ? [...backups] : [];
    arr.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    return arr;
  }, [backups]);

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

  const handleValidate = async (backupId: number) => {
    try {
      const response = await fetchAuth(`/api/backup_center/backups/${backupId}/validate/`, {
        method: 'POST',
      });
      const data = await response.json();
      setLastValidationById((prev) => ({ ...prev, [backupId]: data }));
      if (data.valid) {
        alert('Backup file checked successfully. It is ready for restore.');
      } else {
        alert('This does not look like a valid PGSIMS backup file. Please use another backup file.');
      }
    } catch (error) {
      console.error(error);
      alert('An error occurred while checking the backup file.');
    }
  };

  if (!sortedBackups || sortedBackups.length === 0) {
    return (
      <div className="p-10 text-center">
        <Clock className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-semibold text-gray-900">No backups</h3>
        <p className="mt-1 text-sm text-gray-500">No backups have been created yet. Create your first Regular System Backup before importing real data.</p>
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
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200" aria-label="Backup History">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Date</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Type</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Created By</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Size</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Status</th>
            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-100">
          {sortedBackups.map((backup) => {
            const isExpanded = expandedId === backup.id;
            const kindLabel = backup.backup_kind === 'disaster_recovery' ? 'Full Server Recovery Backup' : 'Regular System Backup';
            const validation = lastValidationById[backup.id];
            return (
              <React.Fragment key={backup.id}>
                <tr className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">{format(new Date(backup.created_at), 'PPP p')}</td>
                  <td className="px-4 py-3 text-sm text-gray-700">{kindLabel}</td>
                  <td className="px-4 py-3 text-sm text-gray-700">{backup.created_by_username || 'System'}</td>
                  <td className="px-4 py-3 text-sm text-gray-700">{formatSize(backup.file_size)}</td>
                  <td className="px-4 py-3 text-sm">
                    <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-semibold ring-1 ring-inset ${
                      backup.status === 'completed' ? 'bg-green-50 text-green-700 ring-green-600/20' :
                      backup.status === 'failed' ? 'bg-red-50 text-red-700 ring-red-600/20' :
                      'bg-yellow-50 text-yellow-800 ring-yellow-600/20'
                    }`}>
                      {String(backup.status || '').toUpperCase()}
                    </span>
                    {validation?.valid ? (
                      <span className="ml-2 inline-flex items-center text-xs text-green-700">
                        <ShieldCheck className="h-3.5 w-3.5 mr-1" /> Checked
                      </span>
                    ) : null}
                  </td>
                  <td className="px-4 py-3 text-right space-x-2">
                    {backup.status === 'completed' && backup.file_name ? (
                      <>
                        <button
                          onClick={() => handleDownload(backup.id, backup.file_name)}
                          className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                        >
                          <Download className="h-3.5 w-3.5 inline-block mr-1" />
                          Download
                        </button>
                        <button
                          onClick={() => handleValidate(backup.id)}
                          className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                        >
                          <FileSearch className="h-3.5 w-3.5 inline-block mr-1" />
                          Check File
                        </button>
                      </>
                    ) : null}
                    <button
                      onClick={() => setExpandedId(isExpanded ? null : backup.id)}
                      className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                    >
                      View Details
                    </button>
                    {backup.status !== 'running' ? (
                      <button
                        onClick={() => handleDelete(backup.id)}
                        className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-red-700 shadow-sm ring-1 ring-inset ring-red-300 hover:bg-red-50"
                        aria-label="Delete backup"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    ) : null}
                  </td>
                </tr>
                {isExpanded ? (
                  <tr>
                    <td colSpan={6} className="px-4 pb-4">
                      <div className="mt-2 rounded-md border border-gray-200 bg-gray-50 p-3 text-xs text-gray-700 space-y-2">
                        <div className="flex flex-wrap gap-x-6 gap-y-1">
                          <span><strong>Backup Record:</strong> #{backup.id}</span>
                          <span><strong>File:</strong> {backup.file_name || '—'}</span>
                          <span><strong>Includes uploads:</strong> {backup.media_included ? 'Yes' : 'No'}</span>
                        </div>
                        <details>
                          <summary className="cursor-pointer select-none font-semibold text-gray-800">Technical Details</summary>
                          <div className="mt-2 space-y-1 text-gray-700">
                            <div><strong>Database:</strong> {backup.database_engine || '—'}</div>
                            <div><strong>App version:</strong> {backup.app_version || '—'}</div>
                            <div><strong>Commit:</strong> {backup.commit_hash || '—'}</div>
                          </div>
                        </details>
                        {backup.notes ? <div className="text-gray-600 italic"><strong>Notes:</strong> {backup.notes}</div> : null}
                      </div>
                    </td>
                  </tr>
                ) : null}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
