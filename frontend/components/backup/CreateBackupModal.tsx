import React, { useState, Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { ShieldCheckIcon, BeakerIcon } from '@heroicons/react/24/outline';
import { fetchAuth } from '@/lib/auth/fetch';
import { toast } from 'react-hot-toast';

export default function CreateBackupModal({ isOpen, onClose, onSuccess }: { isOpen: boolean, onClose: () => void, onSuccess: () => void }) {
  const [notes, setNotes] = useState('');
  const [kind, setKind] = useState<'routine_application_data' | 'disaster_recovery'>('routine_application_data');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const endpoint = kind === 'routine_application_data' 
      ? '/api/backup_center/backups/create-routine/' 
      : '/api/backup_center/backups/create-disaster/';

    try {
      const response = await fetchAuth(endpoint, {
        method: 'POST',
        body: JSON.stringify({ notes }),
      });
      
      if (response.ok) {
        toast.success(`${kind === 'routine_application_data' ? 'Routine' : 'Disaster'} backup initiated`);
        setNotes('');
        onSuccess();
      } else {
        const error = await response.json();
        toast.error(`Failed: ${error.error || 'Unknown error'}`);
      }
    } catch (err) {
      console.error(err);
      toast.error('An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-md sm:p-6">
                <form onSubmit={handleCreate}>
                  <div>
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
                      <ShieldCheckIcon className="h-6 w-6 text-indigo-600" aria-hidden="true" />
                    </div>
                    <div className="mt-3 text-center sm:mt-5">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                        Create System Backup
                      </Dialog.Title>
                      
                      <div className="mt-4 text-left space-y-4">
                        <div>
                          <label className="text-sm font-medium text-gray-900">Backup Pathway</label>
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
                                  Routine Data
                                </label>
                              </div>
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
                                  Disaster Recovery
                                </label>
                              </div>
                            </div>
                          </fieldset>
                        </div>

                        <div className="bg-blue-50 p-3 rounded-md">
                          <p className="text-xs text-blue-700">
                            {kind === 'routine_application_data' 
                              ? "Includes full database + media. Best for routine updates and data safety."
                              : "Includes routine backup + deployment metadata + env templates. Best for full server recovery."}
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
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}

