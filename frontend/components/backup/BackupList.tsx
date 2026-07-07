/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useMemo, useState } from 'react';
import { format } from 'date-fns';
import { Download, Clock, Trash2, ShieldCheck, FileSearch } from 'lucide-react';
import { fetchAuth } from '@/lib/auth/fetch';
import useAuthStore from '@/store/authStore';

export default function BackupList({
  backups,
  driveCopyByBackupId,
  onDriveRestoreReady,
  onRefresh,
}: {
  backups: any[];
  driveCopyByBackupId?: Record<number, any>;
  onDriveRestoreReady?: (restoreJobId: number) => void;
  onRefresh: () => void;
}) {
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [lastValidationById, setLastValidationById] = useState<Record<number, any>>({});
  const [driveActionBusyById, setDriveActionBusyById] = useState<Record<number, string | null>>({});
  const user = useAuthStore((s) => s.user);
  const canRestore = user?.role === 'ADMIN';

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
        const hasIntegrityError = data.errors && data.errors.some((e: string) => 
          e.toLowerCase().includes('checksum') || e.toLowerCase().includes('integrity') || e.toLowerCase().includes('damage')
        );
        if (hasIntegrityError) {
          alert('This backup file may be damaged or changed after creation. Please use another backup file.');
        } else {
          alert('This does not look like a valid PGSIMS backup file.');
        }
      }
    } catch (error) {
      console.error(error);
      alert('An error occurred while checking the backup file.');
    }
  };

  const handleRestoreClick = (fileName: string) => {
    alert(
      `To restore this backup:\n\n` +
      `1. Click the 'Download' button next to "${fileName}" to save the backup file to your computer.\n` +
      `2. Click the 'Start Restore Wizard' button below the table.\n` +
      `3. Upload the downloaded backup file in Step 1 of the wizard.`
    );
  };

  const driveStatusLabel = (backupId: number) => {
    const copy = driveCopyByBackupId?.[backupId];
    if (!copy) return 'Not uploaded';
    if (copy.download_status === 'restore_ready') return 'Restore-ready';
    if (copy.verification_status === 'verified') return 'Verified';
    if (copy.verification_status === 'verification_failed') return 'Failed';
    if (copy.upload_status === 'uploaded') return 'Uploaded';
    if (copy.upload_status === 'upload_failed') return 'Failed';
    if (copy.upload_status === 'uploading') return 'Uploading';
    if (copy.verification_status === 'verifying') return 'Verifying';
    if (copy.download_status === 'downloading') return 'Downloading';
    if (copy.download_status === 'download_failed') return 'Failed';
    return 'Not uploaded';
  };

  const runDriveAction = async (backupId: number, action: 'upload' | 'verify' | 'download') => {
    if (!canRestore) return;
    setDriveActionBusyById((p) => ({ ...p, [backupId]: action }));
    try {
      const endpoint =
        action === 'upload'
          ? `/api/backup_center/backups/${backupId}/google-drive/upload/`
          : action === 'verify'
            ? `/api/backup_center/backups/${backupId}/google-drive/verify/`
            : `/api/backup_center/backups/${backupId}/google-drive/download/`;

      const response = await fetchAuth(endpoint, { method: 'POST' });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        alert(data?.error || 'Google Drive action failed.');
        return;
      }

      if (action === 'download' && typeof data?.restore_job_id === 'number') {
        alert('Backup downloaded and prepared for restore. Open Restore Wizard to continue.');
        onDriveRestoreReady?.(data.restore_job_id);
      } else if (action === 'upload') {
        alert('Uploaded to Google Drive.');
      } else {
        alert('Google Drive copy verified.');
      }
      onRefresh();
    } catch (e) {
      console.error(e);
      alert('Google Drive action failed.');
    } finally {
      setDriveActionBusyById((p) => ({ ...p, [backupId]: null }));
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
	            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Google Drive</th>
	            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-600">Actions</th>
	          </tr>
	        </thead>
        <tbody className="bg-white divide-y divide-gray-100">
	          {sortedBackups.map((backup) => {
	            const isExpanded = expandedId === backup.id;
	            const kindLabel = backup.backup_kind === 'disaster_recovery' ? 'Full Server Recovery Backup' : 'Regular System Backup';
	            const validation = lastValidationById[backup.id];
	            const driveCopy = driveCopyByBackupId?.[backup.id];
	            const canUploadToDrive = canRestore && backup.status === 'completed' && !!backup.file_name;
	            const canVerifyDrive = canRestore && !!driveCopy && driveCopy.upload_status === 'uploaded' && driveCopy.verification_status !== 'verified';
	            const canDownloadDrive = canRestore && !!driveCopy && driveCopy.verification_status === 'verified';
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
	                  <td className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">
	                    <span className="text-xs text-gray-700">Google Drive: {driveStatusLabel(backup.id)}</span>
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
                        {canRestore && (
                          <button
                            onClick={() => handleRestoreClick(backup.file_name)}
                            className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                          >
                            Restore
                          </button>
                        )}
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
	                    <td colSpan={7} className="px-4 pb-4">
	                      <div className="mt-2 rounded-md border border-gray-200 bg-gray-50 p-4 text-xs text-gray-700 space-y-3">
                        <div className="flex flex-wrap gap-x-6 gap-y-1 font-semibold text-gray-900 border-b border-gray-200 pb-2">
                          <span>Backup Record: #{backup.id}</span>
                          <span>Type: {backup.backup_kind === 'disaster_recovery' ? 'Full Server Recovery Backup' : 'Regular System Backup'}</span>
                        </div>
                        
	                        <div className="space-y-2">
                          <details className="group border border-gray-200 rounded-md bg-white p-2">
                            <summary className="cursor-pointer select-none font-semibold text-gray-800 focus:outline-none">
                              Backup Contents
                            </summary>
                            <div className="mt-2 pl-2 space-y-1 text-gray-600 border-t border-gray-100 pt-2">
                              <div><strong>Uploaded Documents:</strong> {backup.media_included ? 'Included' : 'Not Included'}</div>
                              <div><strong>Data Scope:</strong> Users, passwords, profiles, training records, logbooks, approvals, and verification history.</div>
                            </div>
                          </details>

                          <details className="group border border-gray-200 rounded-md bg-white p-2">
                            <summary className="cursor-pointer select-none font-semibold text-gray-800 focus:outline-none">
                              File Integrity Details
                            </summary>
                            <div className="mt-2 pl-2 space-y-1 text-gray-600 border-t border-gray-100 pt-2">
                              <div><strong>File Name:</strong> {backup.file_name || '—'}</div>
                              <div><strong>File Integrity Check:</strong> {validation?.valid ? 'Checked (SHA-256 Verified)' : 'Not Checked / Pending'}</div>
                            </div>
                          </details>

                          {backup.backup_kind === 'disaster_recovery' && (
                            <details className="group border border-gray-200 rounded-md bg-white p-2">
                              <summary className="cursor-pointer select-none font-semibold text-gray-800 focus:outline-none">
                                Server Recovery Notes
                              </summary>
                              <div className="mt-2 pl-2 space-y-1 text-gray-600 border-t border-gray-100 pt-2">
                                <div>Includes full application settings, database dump, and recovery scripts for setting up PGSIMS on a new server. Does not restore DNS or external dashboard provider configurations.</div>
                              </div>
                            </details>
                          )}

                          <details className="group border border-gray-200 rounded-md bg-white p-2">
                            <summary className="cursor-pointer select-none font-semibold text-gray-800 focus:outline-none">
                              Technical Details
                            </summary>
                            <div className="mt-2 pl-2 space-y-1 text-gray-600 border-t border-gray-100 pt-2">
                              <div><strong>Database Engine:</strong> {backup.database_engine || '—'}</div>
                              <div><strong>Application Version:</strong> {backup.app_version || '—'}</div>
                              <div><strong>Git Commit Hash:</strong> {backup.commit_hash || '—'}</div>
                            </div>
                          </details>
	                        </div>
	                        {canRestore && (
	                          <div className="pt-2 border-t border-gray-200 flex flex-wrap items-center gap-2">
	                            <span className="font-semibold text-gray-900">Google Drive</span>
	                            <span className="text-gray-700">Google Drive: {driveStatusLabel(backup.id)}</span>
	                            <div className="ml-auto flex flex-wrap gap-2">
	                              <button
	                                type="button"
	                                onClick={() => runDriveAction(backup.id, 'upload')}
	                                className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:opacity-50"
	                                disabled={!!driveActionBusyById[backup.id] || !canUploadToDrive}
	                              >
	                                {driveActionBusyById[backup.id] === 'upload' ? 'Uploading…' : 'Upload to Drive'}
	                              </button>
	                              <button
	                                type="button"
	                                onClick={() => runDriveAction(backup.id, 'verify')}
	                                className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:opacity-50"
	                                disabled={!!driveActionBusyById[backup.id] || !canVerifyDrive}
	                              >
	                                {driveActionBusyById[backup.id] === 'verify' ? 'Verifying…' : 'Verify Drive Copy'}
	                              </button>
	                              <button
	                                type="button"
	                                onClick={() => runDriveAction(backup.id, 'download')}
	                                className="rounded-md bg-white px-2.5 py-1.5 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:opacity-50"
	                                disabled={!!driveActionBusyById[backup.id] || !canDownloadDrive}
	                              >
	                                {driveActionBusyById[backup.id] === 'download' ? 'Downloading…' : 'Download from Drive'}
	                              </button>
	                            </div>
	                          </div>
	                        )}
	                        {backup.notes ? <div className="text-gray-600 italic mt-2"><strong>Notes:</strong> {backup.notes}</div> : null}
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
