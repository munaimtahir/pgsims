/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import { fetchAuth } from "@/lib/auth/fetch";
import BackupList from "@/components/backup/BackupList";
import CreateBackupModal from "@/components/backup/CreateBackupModal";
import RestoreModal from "@/components/backup/RestoreModal";
import GoogleDrivePanel from "@/components/backup/GoogleDrivePanel";
import { RefreshCw } from "lucide-react";
import ErrorBanner from "@/components/ui/ErrorBanner";
import SuccessBanner from "@/components/ui/SuccessBanner";
import MetricCard from "@/components/ui/MetricCard";
import SectionCard from "@/components/ui/SectionCard";
import useAuthStore from "@/store/authStore";

export default function BackupCenterPage() {
  const user = useAuthStore((s) => s.user);
  const isAllowedAdmin = user?.role === "ADMIN";
  const canRestore = user?.role === "ADMIN";
  const [backups, setBackups] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [restores, setRestores] = useState<any[]>([]);
  const [driveCopies, setDriveCopies] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [createDefaultKind, setCreateDefaultKind] = useState<"routine_application_data" | "disaster_recovery">("routine_application_data");
  const [isRestoreModalOpen, setIsRestoreModalOpen] = useState(false);
  const [initialRestoreJobId, setInitialRestoreJobId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const normalizeList = useCallback((data: any) => {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.results)) return data.results;
    return [];
  }, []);

  const loadBackups = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetchAuth("/api/backup_center/backups/");
      if (response.ok) {
        const data = await response.json();
        setBackups(normalizeList(data));
      } else {
        setError("Failed to load backups");
      }
    } catch (error) {
      console.error(error);
      setError("An error occurred while loading backups");
    } finally {
      setIsLoading(false);
    }
  }, [normalizeList]);

  const loadAuditLogs = useCallback(async () => {
    try {
      const response = await fetchAuth("/api/backup_center/audit-logs/");
      if (!response.ok) return;
      const data = await response.json();
      setAuditLogs(normalizeList(data));
    } catch (error) {
      console.error(error);
    }
  }, [normalizeList]);

  const loadRestores = useCallback(async () => {
    try {
      const response = await fetchAuth("/api/backup_center/restores/");
      if (!response.ok) return;
      const data = await response.json();
      setRestores(normalizeList(data));
    } catch (error) {
      console.error(error);
    }
  }, [normalizeList]);

  const loadDriveCopies = useCallback(async () => {
    if (user?.role !== "ADMIN") {
      setDriveCopies([]);
      return;
    }
    try {
      const response = await fetchAuth("/api/backup_center/google-drive/list/");
      if (!response.ok) return;
      const data = await response.json();
      setDriveCopies(normalizeList(data));
    } catch (e) {
      console.error(e);
    }
  }, [normalizeList, user?.role]);

  useEffect(() => {
    loadBackups();
    loadAuditLogs();
    loadRestores();
    loadDriveCopies();
  }, [loadAuditLogs, loadBackups, loadRestores, loadDriveCopies]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const params = new URLSearchParams(window.location.search);
    const drive = params.get("googleDrive");
    if (drive === "connected") {
      setSuccess("Google Drive connected successfully.");
    } else if (drive === "error") {
      setError("Google Drive connection failed. Please check settings and try again.");
    }
  }, []);

  const lastRoutine = backups.find((b) => b.backup_kind === "routine_application_data" && b.status === "completed");
  const lastDisaster = backups.find((b) => b.backup_kind === "disaster_recovery" && b.status === "completed");
  const lastRestore = restores[0];
  const totalBackups = backups.length;
  const completedBackups = backups.filter((b) => b.status === "completed");

  const latestDriveCopyByBackupId = useMemo(() => {
    const map: Record<number, any> = {};
    for (const c of driveCopies || []) {
      const id = c?.backup_record_id;
      if (typeof id !== "number") continue;
      if (!map[id]) {
        map[id] = c;
        continue;
      }
      const currTs = map[id]?.created_at ? new Date(map[id].created_at).getTime() : 0;
      const nextTs = c?.created_at ? new Date(c.created_at).getTime() : 0;
      if (nextTs >= currTs) map[id] = c;
    }
    return map;
  }, [driveCopies]);

  if (!user) {
    return <div className="py-10 text-center text-gray-500">Loading user profile...</div>;
  }

  if (!isAllowedAdmin) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" data-testid="access-denied">
        <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          <p className="font-semibold">Access Denied</p>
          <p className="mt-1">You do not have permission to access the Backup Center. Only administrative staff may view this page.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
      {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

      <div>
        <div className="flex items-start justify-between gap-3 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:tracking-tight">Backup Center</h2>
            <p className="mt-2 text-sm text-gray-500">Regular backups protect user accounts, records, and uploaded documents.</p>
          </div>
          <button
            type="button"
            onClick={() => {
              loadBackups();
              loadAuditLogs();
              loadRestores();
              loadDriveCopies();
            }}
            className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            <RefreshCw className="-ml-0.5 mr-1.5 h-4 w-4 text-gray-400" />
            Refresh
          </button>
        </div>

        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          <MetricCard
            label="Last Regular System Backup"
            value={lastRoutine?.created_at ? new Date(lastRoutine.created_at).toLocaleString() : "None yet"}
          />
          <MetricCard
            label="Last Full Server Recovery Backup"
            value={lastDisaster?.created_at ? new Date(lastDisaster.created_at).toLocaleString() : "None yet"}
          />
          <MetricCard label="Backup Health" value={lastRoutine ? "OK" : "Needs first backup"} tone={lastRoutine ? "success" : "warning"} />
          <MetricCard label="Last Restore" value={lastRestore?.started_at ? new Date(lastRestore.started_at).toLocaleString() : "None"} />
          <MetricCard label="Total Backups" value={totalBackups} />
        </div>
      </div>

      <SectionCard
        title="Create Backup"
        actions={
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => {
                setCreateDefaultKind("routine_application_data");
                setIsCreateModalOpen(true);
              }}
              className="pg-btn-primary"
            >
              Create Regular System Backup
            </button>
            {canRestore && (
              <button
                type="button"
                onClick={() => {
                  setCreateDefaultKind("disaster_recovery");
                  setIsCreateModalOpen(true);
                }}
                className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              >
                Create Full Server Recovery Backup
              </button>
            )}
          </div>
        }
      >
        <div className={`grid grid-cols-1 ${canRestore ? 'md:grid-cols-2' : ''} gap-4 text-sm text-gray-700`}>
          <div className="rounded-md border border-gray-200 bg-gray-50 p-4">
            <p className="font-semibold text-gray-900">Regular System Backup</p>
            <p className="mt-1 text-gray-600">
              Use this before importing data, making bulk changes, or as a daily backup. It saves users, passwords, profiles, records, logbooks, approvals, and uploaded files.
            </p>
          </div>
          {canRestore && (
            <div className="rounded-md border border-gray-200 bg-gray-50 p-4">
              <p className="font-semibold text-gray-900">Full Server Recovery Backup</p>
              <p className="mt-1 text-gray-600">
                Use this after major milestones or before server migration. It includes system data plus recovery instructions for setting up PGSIMS on a new server.
              </p>
            </div>
          )}
        </div>
      </SectionCard>

      <GoogleDrivePanel
        canManage={user?.role === "ADMIN"}
        completedBackups={completedBackups}
        onRestoreReady={(restoreJobId) => {
          setInitialRestoreJobId(restoreJobId);
          setIsRestoreModalOpen(true);
          setSuccess("Drive backup downloaded and prepared for restore.");
          loadRestores();
          loadDriveCopies();
        }}
      />

      <SectionCard title="Backup History">
        {isLoading ? (
          <div className="py-10 text-center text-gray-500">Loading backups...</div>
        ) : (
          <BackupList
            backups={backups}
            driveCopyByBackupId={latestDriveCopyByBackupId}
            onDriveRestoreReady={(restoreJobId) => {
              setInitialRestoreJobId(restoreJobId);
              setIsRestoreModalOpen(true);
              setSuccess("Drive backup downloaded and prepared for restore.");
              loadRestores();
              loadDriveCopies();
            }}
            onRefresh={() => { loadBackups(); loadAuditLogs(); loadDriveCopies(); }}
          />
        )}
      </SectionCard>

      {canRestore && (
        <SectionCard title="Restore Wizard" actions={
          <button
            type="button"
            onClick={() => setIsRestoreModalOpen(true)}
            className="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500"
          >
            Start Restore Wizard
          </button>
        }>
          <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800">
            <p className="font-semibold">Warning</p>
            <p className="mt-1">
              Restoring a backup will replace the current PGSIMS data. Before restore, the system will automatically create a protection backup of the current data.
              Continue only if you are sure this is the correct backup file.
            </p>
          </div>
        </SectionCard>
      )}

      <SectionCard title="Audit Log">
        {auditLogs.length === 0 ? (
          <div className="text-sm text-gray-500">No backup/restore actions recorded yet.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200" aria-label="Audit Log">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Date</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Action</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Actor</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-100">
                {auditLogs.slice(0, 20).map((log) => (
                  <tr key={log.id}>
                    <td className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">{new Date(log.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{log.action}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">{log.actor_username || 'System'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </SectionCard>

      <CreateBackupModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={() => {
          setIsCreateModalOpen(false);
          setSuccess("Backup started. When complete, download and store the file safely.");
          loadBackups();
          loadAuditLogs();
          loadDriveCopies();
        }}
        defaultKind={createDefaultKind}
      />

      <RestoreModal
        isOpen={isRestoreModalOpen}
        initialRestoreJobId={initialRestoreJobId}
        onClose={() => {
          setIsRestoreModalOpen(false);
          setInitialRestoreJobId(null);
        }}
        onSuccess={() => {
          setIsRestoreModalOpen(false);
          setInitialRestoreJobId(null);
          setSuccess("Restore completed successfully. A protection backup was created before restore.");
          loadBackups();
          loadAuditLogs();
          loadRestores();
        }}
      />
    </div>
  );
}
