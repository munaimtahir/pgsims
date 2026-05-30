import React, { useEffect, useState } from 'react';
import { ShieldCheck } from 'lucide-react';
import { fetchAuth } from '@/lib/auth/fetch';
import Modal from '@/components/ui/Modal';
import useAuthStore from '@/store/authStore';

type BackupKind = 'routine_application_data' | 'disaster_recovery';

export default function CreateBackupModal({
  isOpen,
  onClose,
  onSuccess,
  defaultKind,
}: {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  defaultKind?: BackupKind;
}) {
  const user = useAuthStore((s) => s.user);
  const isSuperAdmin = user?.role === 'admin';
  const [notes, setNotes] = useState('');
  const [kind, setKind] = useState<BackupKind>('routine_application_data');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isOpen) return;
    if (defaultKind) {
      if (defaultKind === 'disaster_recovery' && !isSuperAdmin) {
        setKind('routine_application_data');
      } else {
        setKind(defaultKind);
      }
    }
  }, [defaultKind, isOpen, isSuperAdmin]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    
    const endpoint = kind === 'routine_application_data' 
      ? '/api/backup_center/backups/create-routine/' 
      : '/api/backup_center/backups/create-disaster/';

    try {
      const response = await fetchAuth(endpoint, {
        method: 'POST',
        body: JSON.stringify({ notes }),
      });
      
      if (response.ok) {
        setNotes('');
        onSuccess();
      } else {
        const errData = await response.json();
        setError(`Failed: ${errData.error || 'Unknown error'}`);
      }
    } catch (err) {
      console.error(err);
      setError('An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Create System Backup"
      maxWidth="max-w-md"
    >
      <form onSubmit={handleCreate}>
        <div>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
            <ShieldCheck className="h-6 w-6 text-indigo-600" aria-hidden="true" />
          </div>
          <div className="mt-3 text-center sm:mt-5">
            {error && (
              <div className="mb-4 bg-red-50 p-2 rounded text-xs text-red-600">
                {error}
              </div>
            )}
            
            <div className="mt-4 text-left space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-900">Backup Type</label>
                <fieldset className="mt-2">
                  <div className="space-y-4 sm:flex sm:items-center sm:space-x-10 sm:space-y-0">
                    <div className="flex items-center">
                      <input
                        id="routine"
                        name="backup-kind"
                        type="radio"
                        checked={kind === 'routine_application_data'}
                        onChange={() => setKind('routine_application_data')}
                        className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      />
                      <label htmlFor="routine" className="ml-3 block text-sm font-medium leading-6 text-gray-900">
                        Regular System Backup
                      </label>
                    </div>
                    {isSuperAdmin && (
                      <div className="flex items-center">
                        <input
                          id="disaster"
                          name="backup-kind"
                          type="radio"
                          checked={kind === 'disaster_recovery'}
                          onChange={() => setKind('disaster_recovery')}
                          className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                        />
                        <label htmlFor="disaster" className="ml-3 block text-sm font-medium leading-6 text-gray-900">
                          Full Server Recovery Backup
                        </label>
                      </div>
                    )}
                  </div>
                </fieldset>
              </div>

              <div className="bg-blue-50 p-3 rounded-md">
                <p className="text-xs text-blue-700">
                  {kind === 'routine_application_data' 
                    ? "Use this before importing data, making bulk changes, or as a daily backup. It saves users, passwords, profiles, records, logbooks, approvals, and uploaded files."
                    : "Use this after major milestones or before server migration. It includes system data plus recovery instructions for setting up PGSIMS on a new server."}
                </p>
              </div>

              <div>
                <label htmlFor="notes" className="block text-sm font-medium leading-6 text-gray-900">
                  Notes (Optional)
                </label>
                <div className="mt-2">
                  <textarea
                    id="notes"
                    name="notes"
                    rows={3}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    placeholder="e.g. Before pilot data import"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
          <button
            type="submit"
            disabled={isSubmitting}
            className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:col-start-2 disabled:opacity-50"
          >
            {isSubmitting ? 'Starting...' : 'Initiate Backup'}
          </button>
          <button
            type="button"
            className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
            onClick={onClose}
          >
            Cancel
          </button>
        </div>
      </form>
    </Modal>
  );
}
