/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState } from 'react';
import { format } from 'date-fns';
import { TriangleAlert, CloudUpload, XCircle, CheckCircle } from 'lucide-react';
import { fetchAuth } from '@/lib/auth/fetch';
import Modal from '@/components/ui/Modal';

export default function RestoreModal({
  isOpen,
  onClose,
  onSuccess,
  initialRestoreJobId,
}: {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  initialRestoreJobId?: number | null;
}) {
  const [step, setStep] = useState<1 | 2 | 3 | 4 | 5>(1); // 1: upload, 2: check, 3: details, 4: confirm, 5: result
  const [file, setFile] = useState<File | null>(null);
  const [restoreJobId, setRestoreJobId] = useState<number | null>(null);
  const [validationResult, setValidationResult] = useState<any | null>(null);
  const [password, setPassword] = useState('');
  const [typedConfirmation, setTypedConfirmation] = useState('');
  const [confirmChecked, setConfirmChecked] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDryRunSuccess, setIsDryRunSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const resetState = () => {
    setStep(1);
    setFile(null);
    setRestoreJobId(null);
    setValidationResult(null);
    setPassword('');
    setTypedConfirmation('');
    setConfirmChecked(false);
    setIsProcessing(false);
    setIsDryRunSuccess(false);
    setError(null);
  };

  useEffect(() => {
    if (!isOpen) return;
    if (!initialRestoreJobId) return;
    if (restoreJobId) return;
    setIsProcessing(true);
    setRestoreJobId(initialRestoreJobId);
    // Begin at validation step for a server-prepared restore upload.
    // validateBackup will transition the UI to step 2.
    void validateBackup(initialRestoreJobId);
  }, [isOpen, initialRestoreJobId, restoreJobId]);

  const handleClose = () => {
    if (isProcessing && step === 4) {
      setError('Restore in progress, please do not close.');
      return;
    }
    resetState();
    onClose();
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsProcessing(true);
    setError(null);
    
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
        const errData = await response.json();
        const rawErr = errData.error || '';
        let uploadError = 'This does not look like a valid PGSIMS backup file.';
        if (rawErr.toLowerCase().includes('extension') || rawErr.toLowerCase().includes('invalid')) {
          uploadError = 'This does not look like a valid PGSIMS backup file.';
        }
        setError(uploadError);
        setStep(2);
        setIsProcessing(false);
      }
    } catch (err) {
      console.error(err);
      setError('This does not look like a valid PGSIMS backup file.');
      setStep(2);
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
        setError(null);
        setStep(2);
      } else {
        const errors = data.errors || [];
        const isChecksumError = errors.some((e: string) => 
          e.toLowerCase().includes('checksum') || e.toLowerCase().includes('integrity') || e.toLowerCase().includes('damage')
        );
        const isManifestError = errors.some((e: string) => 
          e.toLowerCase().includes('manifest') || e.toLowerCase().includes('zip')
        );
        
        if (isChecksumError) {
          setError('This backup file may be damaged or changed after creation. Please use another backup file.');
        } else if (isManifestError) {
          setError('This does not look like a valid PGSIMS backup file.');
        } else {
          setError(errors[0] || 'This does not look like a valid PGSIMS backup file.');
        }
        setStep(2);
      }
    } catch (err) {
      console.error(err);
      setError('This does not look like a valid PGSIMS backup file.');
      setStep(2);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDryRun = async () => {
    if (!restoreJobId) return;
    setIsProcessing(true);
    setError(null);
    try {
      const response = await fetchAuth(`/api/backup_center/restores/${restoreJobId}/dry-run/`, {
        method: 'POST',
      });
      
      const data = await response.json();
      if (data.status === 'validation_passed') {
        setIsDryRunSuccess(true);
        setStep(4);
      } else {
        setError(`Dry-run failed: ${data.error_message}`);
      }
    } catch (err) {
      console.error(err);
      setError('An error occurred during dry-run');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRestore = async () => {
    if (typedConfirmation !== 'RESTORE') {
      setError('You must type RESTORE to confirm');
      return;
    }
    if (!password) {
      setError('Admin password required');
      return;
    }
    if (!confirmChecked) {
      setError('You must confirm you understand this will replace current data.');
      return;
    }
    
    setIsProcessing(true);
    setError(null);
    try {
      const response = await fetchAuth(`/api/backup_center/restores/${restoreJobId}/confirm/`, {
        method: 'POST',
        body: JSON.stringify({ 
          password,
          typed_confirmation: typedConfirmation
        }),
      });
      
      if (response.ok) {
        setStep(5);
      } else {
        const errData = await response.json();
        const rawErr = errData.error || '';
        if (rawErr.toLowerCase().includes('password')) {
          setError('Invalid admin password.');
        } else {
          setError('Restore could not be completed. Your current data has not been replaced. Please contact the technical administrator and keep the automatic protection backup.');
        }
        setStep(5);
      }
    } catch (err) {
      console.error(err);
      setError('Restore could not be completed. Your current data has not been replaced. Please contact the technical administrator and keep the automatic protection backup.');
      setStep(5);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFinish = () => {
    if (!error) {
      onSuccess();
    }
    resetState();
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Restore Application Data"
      maxWidth="max-w-lg"
    >
      {error && step !== 2 && step !== 5 && (
        <div className="mb-4 bg-red-50 p-2 rounded text-xs text-red-600">
          {error}
        </div>
      )}

      {step === 1 && (
        <div>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
            <TriangleAlert className="h-6 w-6 text-red-600" aria-hidden="true" />
          </div>
          <div className="mt-3 text-center sm:mt-5">
            <h3 className="text-base font-semibold leading-6 text-gray-900">
              Step 1: Upload Backup File
            </h3>
            <div className="mt-2 text-left space-y-4">
              <p className="text-sm text-gray-600">
                Restore will replace current PGSIMS application data. A safety backup will be created first.
              </p>
              <div className="mt-4 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                <div className="text-center">
                  <CloudUpload className="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
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
              {isProcessing ? 'Uploading & Checking...' : 'Upload & Validate'}
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

      {step === 2 && (
        <div>
          <div className={`mx-auto flex h-12 w-12 items-center justify-center rounded-full ${!error ? 'bg-green-100' : 'bg-red-100'}`}>
            {!error ? <CheckCircle className="h-6 w-6 text-green-600" aria-hidden="true" /> : <XCircle className="h-6 w-6 text-red-600" aria-hidden="true" />}
          </div>
          <div className="mt-3 text-center sm:mt-5">
            <h3 className="text-base font-semibold leading-6 text-gray-900">
              Step 2: Check Backup File
            </h3>
            
            {!error ? (
              <div className="mt-4 text-left space-y-4">
                <div className="rounded-md bg-green-50 p-4 border border-green-200">
                  <p className="text-sm font-semibold text-green-800">
                    Backup file checked successfully. It is ready for restore.
                  </p>
                </div>
              </div>
            ) : (
              <div className="mt-4 text-left space-y-4">
                <div className="rounded-md bg-red-50 p-4 border border-red-200">
                  <p className="text-sm font-semibold text-red-800">
                    {error}
                  </p>
                </div>
              </div>
            )}
          </div>
          <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
            {!error ? (
              <button
                type="button"
                className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 sm:col-start-2"
                onClick={() => { setError(null); setStep(3); }}
              >
                Review Backup Details
              </button>
            ) : (
              <button
                type="button"
                className="inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-span-2"
                onClick={() => { resetState(); setStep(1); }}
              >
                Try another file
              </button>
            )}
            {!error && (
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

      {step === 3 && validationResult && (
        <div>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
            <CheckCircle className="h-6 w-6 text-indigo-600" aria-hidden="true" />
          </div>
          <div className="mt-3 text-center sm:mt-5">
            <h3 className="text-base font-semibold leading-6 text-gray-900">
              Step 3: Review Backup Details
            </h3>
            
            <div className="mt-4 text-left space-y-3">
              <div className="flex flex-wrap gap-x-6 gap-y-1 font-semibold text-gray-900 border-b border-gray-200 pb-2 text-xs">
                <span>Backup Record: #{restoreJobId}</span>
                <span>Type: {validationResult.backup_kind === 'disaster_recovery' ? 'Full Server Recovery Backup' : 'Regular System Backup'}</span>
              </div>

              <div className="space-y-2 text-xs">
                <details className="group border border-gray-200 rounded-md bg-white p-2">
                  <summary className="cursor-pointer select-none font-semibold text-gray-800 focus:outline-none">
                    Backup Contents
                  </summary>
                  <div className="mt-2 pl-2 space-y-1 text-gray-600 border-t border-gray-100 pt-2">
                    <div><strong>Created At:</strong> {validationResult.manifest?.created_at ? format(new Date(validationResult.manifest.created_at), 'PPP p') : '—'}</div>
                    <div><strong>Uploaded Documents:</strong> {validationResult.media_summary?.file_count ?? 0} files ({validationResult.manifest?.media_included ? 'Included' : 'Not Included'})</div>
                    <div><strong>Data Scope:</strong> Users, passwords, profiles, training records, logbooks, approvals, and verification history.</div>
                  </div>
                </details>

                <details className="group border border-gray-200 rounded-md bg-white p-2">
                  <summary className="cursor-pointer select-none font-semibold text-gray-800 focus:outline-none">
                    File Integrity Details
                  </summary>
                  <div className="mt-2 pl-2 space-y-1 text-gray-600 border-t border-gray-100 pt-2">
                    <div><strong>File Name:</strong> {validationResult.manifest?.file_name || file?.name || '—'}</div>
                    <div><strong>File Integrity Check:</strong> SHA-256 Verified</div>
                  </div>
                </details>

                {validationResult.backup_kind === 'disaster_recovery' && (
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
                    <div><strong>Database Engine:</strong> {validationResult.manifest?.database_engine || '—'}</div>
                    <div><strong>Application Version:</strong> {validationResult.manifest?.app_version || '—'}</div>
                    <div><strong>Git Commit Hash:</strong> {validationResult.manifest?.commit_hash || '—'}</div>
                  </div>
                </details>
              </div>
            </div>
          </div>
          <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
            <button
              type="button"
              disabled={isProcessing}
              className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 sm:col-start-2 disabled:opacity-50"
              onClick={handleDryRun}
            >
              {isProcessing ? 'Running Dry-Run...' : 'Dry-Run Test'}
            </button>
            <button
              type="button"
              disabled={isProcessing}
              className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
              onClick={handleClose}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {step === 4 && isDryRunSuccess && (
        <div>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-yellow-100">
            <TriangleAlert className="h-6 w-6 text-yellow-600" aria-hidden="true" />
          </div>
          <div className="mt-3 text-center sm:mt-5">
            <h3 className="text-base font-semibold leading-6 text-gray-900">
              Step 4: Confirm Restore
            </h3>
            <div className="mt-2 text-left space-y-4">
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-xs text-red-800 font-semibold uppercase">
                  Safety Warning
                </p>
                <p className="text-xs text-red-700 mt-1">
                  Restoring a backup will replace the current PGSIMS data. Before restore, the system will automatically create a protection backup of the current data. Continue only if you are sure this is the correct backup file.
                </p>
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
              
              <div className="flex items-start">
                <div className="flex h-6 items-center">
                  <input
                    id="check"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-red-600 focus:ring-red-600"
                    checked={confirmChecked}
                    onChange={(e) => setConfirmChecked(e.target.checked)}
                  />
                </div>
                <div className="ml-3 text-xs leading-6">
                  <label htmlFor="check" className="font-medium text-gray-900">
                    I understand this will replace current application data.
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
            <button
              type="button"
              disabled={typedConfirmation !== 'RESTORE' || !password || !confirmChecked || isProcessing}
              className="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600 sm:col-start-2 disabled:opacity-50"
              onClick={handleRestore}
            >
              {isProcessing ? 'Restoring...' : 'Finalize Restore'}
            </button>
            <button
              type="button"
              disabled={isProcessing}
              className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
              onClick={handleClose}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {step === 5 && (
        <div>
          <div className={`mx-auto flex h-12 w-12 items-center justify-center rounded-full ${!error ? 'bg-green-100' : 'bg-red-100'}`}>
            {!error ? <CheckCircle className="h-6 w-6 text-green-600" aria-hidden="true" /> : <XCircle className="h-6 w-6 text-red-600" aria-hidden="true" />}
          </div>
          <div className="mt-3 text-center sm:mt-5">
            <h3 className="text-base font-semibold leading-6 text-gray-900">
              Step 5: Restore Result
            </h3>
            <div className="mt-4 text-left space-y-4">
              {!error ? (
                <div className="rounded-md bg-green-50 p-4 border border-green-200 text-sm text-green-800">
                  <p className="font-semibold">Restore completed successfully.</p>
                  <p className="mt-1">PGSIMS has been returned to the selected backup state.</p>
                </div>
              ) : (
                <div className="rounded-md bg-red-50 p-4 border border-red-200 text-sm text-red-800">
                  <p className="font-semibold">Restore Failed</p>
                  <p className="mt-1">{error}</p>
                </div>
              )}
            </div>
          </div>
          <div className="mt-5 sm:mt-6">
            <button
              type="button"
              className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
              onClick={handleFinish}
            >
              {!error ? 'Finish' : 'Close'}
            </button>
          </div>
        </div>
      )}
    </Modal>
  );
}
