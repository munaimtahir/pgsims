import React, { useState, Fragment, useRef } from 'react';
import { format } from 'date-fns';
import { Dialog, Transition } from '@headlessui/react';
import { ExclamationTriangleIcon, CloudArrowUpIcon, XCircleIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { fetchAuth } from '@/lib/auth/fetch';
import { toast } from 'react-hot-toast';

export default function RestoreModal({ isOpen, onClose, onSuccess }: { isOpen: boolean, onClose: () => void, onSuccess: () => void }) {
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1); // 1: upload, 2: validate/details, 3: dry-run, 4: confirm
  const [file, setFile] = useState<File | null>(null);
  const [restoreJobId, setRestoreJobId] = useState<number | null>(null);
  const [validationResult, setValidationResult] = useState<any | null>(null);
  const [dryRunResult, setDryRunResult] = useState<any | null>(null);
  const [password, setPassword] = useState('');
  const [typedConfirmation, setTypedConfirmation] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDryRunSuccess, setIsDryRunSuccess] = useState(false);

  const resetState = () => {
    setStep(1);
    setFile(null);
    setRestoreJobId(null);
    setValidationResult(null);
    setDryRunResult(null);
    setPassword('');
    setTypedConfirmation('');
    setIsProcessing(false);
    setIsDryRunSuccess(false);
  };

  const handleClose = () => {
    if (isProcessing && step === 4) {
      toast.error('Restore in progress, please do not close.');
      return;
    }
    resetState();
    onClose();
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsProcessing(true);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetchAuth('/api/backup_center/restores/upload/', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const data = await response.json();
        setRestoreJobId(data.id);
        await validateBackup(data.id);
      } else {
        const error = await response.json();
        toast.error(`Upload failed: ${error.error || 'Unknown error'}`);
        setIsProcessing(false);
      }
    } catch (err) {
      console.error(err);
      toast.error('An error occurred during upload');
      setIsProcessing(false);
    }
  };

  const validateBackup = async (jobId: number) => {
    try {
      const response = await fetchAuth(`/api/backup_center/restores/${jobId}/validate/`, {
        method: 'POST',
      });
      
      const data = await response.json();
      setValidationResult(data);
      if (data.valid) {
        setStep(2);
      } else {
        toast.error('Validation failed');
        setStep(2); // show errors
      }
    } catch (err) {
      console.error(err);
      toast.error('An error occurred during validation');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDryRun = async () => {
    if (!restoreJobId) return;
    setIsProcessing(true);
    try {
      const response = await fetchAuth(`/api/backup_center/restores/${restoreJobId}/dry-run/`, {
        method: 'POST',
      });
      
      const data = await response.json();
      setDryRunResult(data);
      if (data.status === 'validation_passed') {
        setIsDryRunSuccess(true);
        toast.success('Dry-run successful!');
        setStep(4);
      } else {
        toast.error(`Dry-run failed: ${data.error_message}`);
      }
    } catch (err) {
      console.error(err);
      toast.error('An error occurred during dry-run');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRestore = async () => {
    if (typedConfirmation !== 'RESTORE') {
      toast.error('You must type RESTORE to confirm');
      return;
    }
    if (!password) {
      toast.error('Admin password required');
      return;
    }
    
    setIsProcessing(true);
    try {
      const response = await fetchAuth(`/api/backup_center/restores/${restoreJobId}/confirm/`, {
        method: 'POST',
        body: JSON.stringify({ 
          password,
          typed_confirmation: typedConfirmation
        }),
      });
      
      if (response.ok) {
        toast.success('System restored successfully!');
        resetState();
        onSuccess();
      } else {
        const error = await response.json();
        toast.error(`Restore failed: ${error.error || 'Unknown error'}`);
      }
    } catch (err) {
      console.error(err);
      toast.error('An error occurred during restore');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={handleClose}>
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
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
                
                {step === 1 && (
                  <div>
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                      <ExclamationTriangleIcon className="h-6 w-6 text-red-600" aria-hidden="true" />
                    </div>
                    <div className="mt-3 text-center sm:mt-5">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                        Restore Application Data
                      </Dialog.Title>
                      <div className="mt-2 text-left">
                        <p className="text-sm text-gray-500">
                          <strong>Warning:</strong> Restore will replace current PGSIMS application data. External services like DNS/SSL are not affected.
                        </p>
                        <div className="mt-4 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                          <div className="text-center">
                            <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
                            <div className="mt-4 flex text-sm leading-6 text-gray-600 justify-center">
                              <label
                                htmlFor="file-upload"
                                className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
                              >
                                <span>Upload a backup file</span>
                                <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".pgsimsbak,.pgsimsdr" onChange={(e) => {
                                  if (e.target.files && e.target.files[0]) {
                                    setFile(e.target.files[0]);
                                  }
                                }} />
                              </label>
                            </div>
                            <p className="text-xs leading-5 text-gray-600 mt-2">
                              {file ? file.name : ".pgsimsbak or .pgsimsdr files"}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                      <button
                        type="button"
                        disabled={!file || isProcessing}
                        className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:col-start-2 disabled:opacity-50"
                        onClick={handleUpload}
                      >
                        {isProcessing ? 'Uploading...' : 'Upload & Validate'}
                      </button>
                      <button
                        type="button"
                        className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
                        onClick={handleClose}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

                {step === 2 && validationResult && (
                  <div>
                    <div className={`mx-auto flex h-12 w-12 items-center justify-center rounded-full ${validationResult.valid ? 'bg-green-100' : 'bg-red-100'}`}>
                      {validationResult.valid ? <CheckCircleIcon className="h-6 w-6 text-green-600" aria-hidden="true" /> : <XCircleIcon className="h-6 w-6 text-red-600" aria-hidden="true" />}
                    </div>
                    <div className="mt-3 text-center sm:mt-5">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                        {validationResult.valid ? 'Backup Validated' : 'Validation Failed'}
                      </Dialog.Title>
                      
                      {validationResult.valid ? (
                        <div className="mt-4 text-left space-y-4">
                          <div className="bg-gray-50 p-4 rounded-md">
                            <h4 className="text-sm font-medium text-gray-900">Details from Manifest:</h4>
                            <ul className="mt-2 text-xs text-gray-600 space-y-1">
                                <li><strong>Kind:</strong> {validationResult.backup_kind}</li>
                                <li><strong>App Version:</strong> {validationResult.manifest.app_version}</li>
                                <li><strong>Database:</strong> {validationResult.manifest.database_engine}</li>
                                <li><strong>Created:</strong> {format(new Date(validationResult.manifest.created_at), 'PPP p')}</li>
                                <li><strong>Tables:</strong> {Object.keys(validationResult.table_counts).length}</li>
                                <li><strong>Media:</strong> {validationResult.media_summary.file_count} files</li>
                            </ul>
                          </div>
                          <p className="text-xs text-gray-500">
                            The backup is compatible and ready for a dry-run test.
                          </p>
                        </div>
                      ) : (
                        <div className="mt-2 text-left">
                          <ul className="list-disc pl-5 text-sm text-red-600">
                            {(validationResult.errors as string[]).map((err: string, i: number) => (
                              <li key={i}>{err}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                    <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                      {validationResult.valid ? (
                        <button
                          type="button"
                          disabled={isProcessing}
                          className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 sm:col-start-2 disabled:opacity-50"
                          onClick={handleDryRun}
                        >
                          {isProcessing ? 'Running Dry-Run...' : 'Dry-Run Test'}
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-span-2"
                          onClick={() => setStep(1)}
                        >
                          Try another file
                        </button>
                      )}
                      {validationResult.valid && (
                        <button
                          type="button"
                          className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
                          onClick={handleClose}
                        >
                          Cancel
                        </button>
                      )}
                    </div>
                  </div>
                )}

                {step === 4 && isDryRunSuccess && (
                  <div>
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-yellow-100">
                      <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600" aria-hidden="true" />
                    </div>
                    <div className="mt-3 text-center sm:mt-5">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                        Final Restore Confirmation
                      </Dialog.Title>
                      <div className="mt-2 text-left space-y-4">
                        <div className="bg-red-50 border-l-4 border-red-400 p-4">
                          <div className="flex">
                            <div className="ml-3">
                              <p className="text-sm text-red-700 font-bold">
                                DESTRUCTIVE ACTION
                              </p>
                              <p className="text-xs text-red-600 mt-1">
                                This will replace all current data. A safety backup will be created automatically.
                              </p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <label htmlFor="pass" className="block text-sm font-medium leading-6 text-gray-900">
                            Your Admin Password
                          </label>
                          <div className="mt-2">
                            <input
                              type="password"
                              id="pass"
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-red-600 sm:text-sm sm:leading-6"
                              value={password}
                              onChange={(e) => setPassword(e.target.value)}
                            />
                          </div>
                        </div>

                        <div>
                          <label htmlFor="confirm" className="block text-sm font-medium leading-6 text-gray-900">
                            Type <strong className="text-red-600">RESTORE</strong> to confirm
                          </label>
                          <div className="mt-2">
                            <input
                              type="text"
                              id="confirm"
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-red-300 focus:ring-2 focus:ring-inset focus:ring-red-600 sm:text-sm sm:leading-6"
                              placeholder="RESTORE"
                              value={typedConfirmation}
                              onChange={(e) => setTypedConfirmation(e.target.value)}
                            />
                          </div>
                        </div>
                        
                        <div className="flex items-center">
                            <input
                                id="check"
                                type="checkbox"
                                className="h-4 w-4 rounded border-gray-300 text-red-600 focus:ring-red-600"
                                required
                            />
                            <label htmlFor="check" className="ml-2 block text-xs text-gray-900">
                                I understand this will replace current application data.
                            </label>
                        </div>
                      </div>
                    </div>
                    <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                      <button
                        type="button"
                        disabled={typedConfirmation !== 'RESTORE' || !password || isProcessing}
                        className="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600 sm:col-start-2 disabled:opacity-50"
                        onClick={handleRestore}
                      >
                        {isProcessing ? 'Restoring...' : 'Finalize Restore'}
                      </button>
                      <button
                        type="button"
                        disabled={isProcessing}
                        className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0 disabled:opacity-50"
                        onClick={handleClose}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}

