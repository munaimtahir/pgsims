/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import SectionCard from "@/components/ui/SectionCard";
import { fetchAuth } from "@/lib/auth/fetch";

type DriveStatus = {
  enabled: boolean;
  status: "not_connected" | "connected" | "disconnected" | "failed";
  connected_account: string | null;
  backup_folder: { id?: string | null; name?: string | null } | null;
  token_expiry?: string | null;
  last_health_check_at?: string | null;
  last_error?: string | null;
  updated_at?: string | null;
};

export default function GoogleDrivePanel({
  canManage,
  completedBackups,
  onRestoreReady,
}: {
  canManage: boolean;
  completedBackups: any[];
  onRestoreReady: (restoreJobId: number) => void;
}) {
  const [status, setStatus] = useState<DriveStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [selectedBackupId, setSelectedBackupId] = useState<number | null>(null);

  const selectedBackup = useMemo(() => {
    if (!selectedBackupId) return null;
    return completedBackups.find((b) => b.id === selectedBackupId) || null;
  }, [completedBackups, selectedBackupId]);

  const loadStatus = useCallback(async () => {
    setError(null);
    try {
      const response = await fetchAuth("/api/backup_center/google-drive/status/");
      if (!response.ok) {
        setError("Failed to load Google Drive status");
        return;
      }
      const data = await response.json();
      setStatus(data);
    } catch (e) {
      console.error(e);
      setError("Failed to load Google Drive status");
    }
  }, []);

  useEffect(() => {
    loadStatus();
  }, [loadStatus]);

  useEffect(() => {
    if (!selectedBackupId && completedBackups.length > 0) {
      setSelectedBackupId(completedBackups[0].id);
    }
  }, [completedBackups, selectedBackupId]);

  const doAction = async (name: string, fn: () => Promise<void>) => {
    setBusy(name);
    setError(null);
    try {
      await fn();
      await loadStatus();
    } catch (e: any) {
      console.error(e);
      setError(e?.message || "Action failed");
    } finally {
      setBusy(null);
    }
  };

  const connect = async () => {
    const response = await fetchAuth("/api/backup_center/google-drive/connect/");
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Failed to start Google Drive connection");
    if (!data.authorization_url) throw new Error("Missing authorization_url");
    window.location.href = data.authorization_url;
  };

  const disconnect = async () => {
    const response = await fetchAuth("/api/backup_center/google-drive/disconnect/", { method: "POST" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Failed to disconnect");
  };

  const healthCheck = async () => {
    const response = await fetchAuth("/api/backup_center/google-drive/health-check/", { method: "POST" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Health check failed");
  };

  const createFolder = async () => {
    const response = await fetchAuth("/api/backup_center/google-drive/create-folder/", { method: "POST" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Failed to create/use backup folder");
  };

  const uploadSelected = async () => {
    if (!selectedBackup) throw new Error("Select a completed backup first");
    const response = await fetchAuth(`/api/backup_center/backups/${selectedBackup.id}/google-drive/upload/`, { method: "POST" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Upload failed");
  };

  const verifySelected = async () => {
    if (!selectedBackup) throw new Error("Select a completed backup first");
    const response = await fetchAuth(`/api/backup_center/backups/${selectedBackup.id}/google-drive/verify/`, { method: "POST" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Verify failed");
  };

  const downloadSelected = async () => {
    if (!selectedBackup) throw new Error("Select a completed backup first");
    const response = await fetchAuth(`/api/backup_center/backups/${selectedBackup.id}/google-drive/download/`, { method: "POST" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data?.error || "Download failed");
    if (typeof data.restore_job_id !== "number") throw new Error("Missing restore_job_id");
    onRestoreReady(data.restore_job_id);
  };

  const statusLine = useMemo(() => {
    if (!status) return "Loading…";
    if (!status.enabled) return "Disabled (GOOGLE_DRIVE_BACKUP_ENABLED=false)";
    if (status.status === "connected") return "Connected";
    if (status.status === "failed") return "Failed";
    if (status.status === "disconnected") return "Disconnected";
    return "Not connected";
  }, [status]);

  return (
    <SectionCard
      title="Google Drive Backup"
      actions={
        canManage ? (
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => doAction("connect", connect)}
              className="pg-btn-primary"
              disabled={!!busy || status?.status === "connected"}
            >
              {busy === "connect" ? "Connecting…" : "Connect Google Drive"}
            </button>
            <button
              type="button"
              onClick={() => doAction("disconnect", disconnect)}
              className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              disabled={!!busy || status?.status !== "connected"}
            >
              Disconnect
            </button>
            <button
              type="button"
              onClick={() => doAction("health", healthCheck)}
              className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              disabled={!!busy || status?.status !== "connected"}
            >
              Check Connection
            </button>
          </div>
        ) : (
          <div className="text-xs text-gray-500">Super Admin only</div>
        )
      }
    >
      <div className="space-y-3 text-sm">
        {error && <div className="rounded-md border border-red-200 bg-red-50 p-3 text-red-800">{error}</div>}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
            <div className="text-xs text-gray-500">Status</div>
            <div className="font-semibold text-gray-900">{statusLine}</div>
            {status?.connected_account && <div className="mt-1 text-xs text-gray-600">Account: {status.connected_account}</div>}
          </div>
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
            <div className="text-xs text-gray-500">Backup folder</div>
            <div className="font-semibold text-gray-900">{status?.backup_folder?.name || "Not set"}</div>
            {status?.backup_folder?.id && <div className="mt-1 text-xs text-gray-600">Folder ID: {status.backup_folder.id}</div>}
          </div>
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
            <div className="text-xs text-gray-500">Last error</div>
            <div className="text-gray-800">{status?.last_error || "None"}</div>
          </div>
        </div>

        {canManage && (
          <div className="rounded-md border border-gray-200 p-3">
            <div className="flex flex-col md:flex-row md:items-end gap-3">
              <div className="flex-1">
                <label className="block text-xs font-semibold text-gray-700">Backup record</label>
                <select
                  className="mt-1 block w-full rounded-md border-gray-300 text-sm"
                  value={selectedBackupId || ""}
                  onChange={(e) => setSelectedBackupId(e.target.value ? Number(e.target.value) : null)}
                  disabled={!!busy}
                >
                  {completedBackups.length === 0 ? (
                    <option value="">No completed backups yet</option>
                  ) : (
                    completedBackups.map((b) => (
                      <option key={b.id} value={b.id}>
                        #{b.id} · {b.backup_kind} · {b.created_at ? new Date(b.created_at).toLocaleString() : ""}
                      </option>
                    ))
                  )}
                </select>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => doAction("folder", createFolder)}
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  disabled={!!busy || status?.status !== "connected"}
                >
                  Create/Use Backup Folder
                </button>
                <button
                  type="button"
                  onClick={() => doAction("upload", uploadSelected)}
                  className="pg-btn-primary"
                  disabled={!!busy || status?.status !== "connected" || !selectedBackup}
                >
                  {busy === "upload" ? "Uploading…" : "Upload Backup to Drive"}
                </button>
                <button
                  type="button"
                  onClick={() => doAction("verify", verifySelected)}
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  disabled={!!busy || status?.status !== "connected" || !selectedBackup}
                >
                  Verify Drive Copy
                </button>
                <button
                  type="button"
                  onClick={() => doAction("download", downloadSelected)}
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  disabled={!!busy || status?.status !== "connected" || !selectedBackup}
                >
                  {busy === "download" ? "Downloading…" : "Download from Drive"}
                </button>
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Uploads are encrypted locally before they are sent to Google Drive.
            </div>
          </div>
        )}
      </div>
    </SectionCard>
  );
}

