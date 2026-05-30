"use client";

import React, { useState, useEffect } from "react";
import { fetchAuth } from "@/lib/auth/fetch";
import BackupList from "@/components/backup/BackupList";
import CreateBackupModal from "@/components/backup/CreateBackupModal";
import RestoreModal from "@/components/backup/RestoreModal";
import { PlusIcon, ArrowPathIcon } from "@heroicons/react/24/outline";
import { toast } from "react-hot-toast";

export default function BackupCenterPage() {
  const [backups, setBackups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isRestoreModalOpen, setIsRestoreModalOpen] = useState(false);

  const loadBackups = async () => {
    setIsLoading(true);
    try {
      const response = await fetchAuth("/api/backup_center/jobs/");
      if (response.ok) {
        const data = await response.json();
        setBackups(data);
      } else {
        toast.error("Failed to load backups");
      }
    } catch (error) {
      console.error(error);
      toast.error("An error occurred while loading backups");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadBackups();
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="md:flex md:items-center md:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Backup & Restore Center
          </h2>
          <p className="mt-2 text-sm text-gray-500">
            Manage system backups and critical restore operations.
          </p>
        </div>
        <div className="mt-4 flex md:ml-4 md:mt-0 space-x-3">
          <button
            type="button"
            onClick={loadBackups}
            className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            <ArrowPathIcon className="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400" aria-hidden="true" />
            Refresh
          </button>
          <button
            type="button"
            onClick={() => setIsRestoreModalOpen(true)}
            className="inline-flex items-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
          >
            Upload & Restore
          </button>
          <button
            type="button"
            onClick={() => setIsCreateModalOpen(true)}
            className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            <PlusIcon className="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
            Create Backup
          </button>
        </div>
      </div>

      <div className="bg-white shadow sm:rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-base font-semibold leading-6 text-gray-900">System Backups</h3>
        </div>
        {isLoading ? (
          <div className="p-10 text-center text-gray-500">Loading backups...</div>
        ) : (
          <BackupList backups={backups} onRefresh={loadBackups} />
        )}
      </div>

      <CreateBackupModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={() => {
          setIsCreateModalOpen(false);
          loadBackups();
        }}
      />

      <RestoreModal
        isOpen={isRestoreModalOpen}
        onClose={() => setIsRestoreModalOpen(false)}
        onSuccess={() => {
          setIsRestoreModalOpen(false);
          toast.success("Restore completed successfully! A safety backup was created.");
        }}
      />
    </div>
  );
}
