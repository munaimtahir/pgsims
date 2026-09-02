/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import SectionCard from "@/components/ui/SectionCard";
import { fetchAuth } from "@/lib/auth/fetch";
import Modal from "@/components/ui/Modal";

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
  const [technicalError, setTechnicalError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [selectedBackupId, setSelectedBackupId] = useState<number | null>(null);
  const [driveCopies, setDriveCopies] = useState<any[]>([]);
  const [noAccess, setNoAccess] = useState(false);
  const [isDisconnectOpen, setIsDisconnectOpen] = useState(false);

  const selectedBackup = useMemo(() => {
    if (!selectedBackupId) return null;
    return completedBackups.find((b) => b.id === selectedBackupId) || null;
  }, [completedBackups, selectedBackupId]);

  const loadStatus = useCallback(async () => {
    setError(null);
    setTechnicalError(null);
    try {
      const response = await fetchAuth("/api/backup_center/google-drive/status/");
      if (response.status === 403) {
        setNoAccess(true);
        return;
      }
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

  const loadDriveCopies = useCallback(async () => {
    if (!canManage) {
      setDriveCopies([]);
      return;
    }
    try {
      const response = await fetchAuth("/api/backup_center/google-drive/list/");
      if (!response.ok) return;
      const data = await response.json();
      const list = Array.isArray(data?.results) ? data.results : [];
      setDriveCopies(list);
    } catch (e) {
      console.error(e);
    }
  }, [canManage]);

  useEffect(() => {
    loadStatus();
    loadDriveCopies();
  }, [loadStatus, loadDriveCopies]);

  useEffect(() => {
    if (!selectedBackupId && completedBackups.length > 0) {
      setSelectedBackupId(completedBackups[0].id);
    }
  }, [completedBackups, selectedBackupId]);

  const doAction = async (name: string, fn: () => Promise<void>) => {
    setBusy(name);
    setError(null);
    setTechnicalError(null);
    try {
      await fn();
      await loadStatus();
      await loadDriveCopies();
    } catch (e: any) {
      console.error(e);
      const msg = String(e?.message || "Action failed");
      if (msg.toLowerCase().includes("permission") || msg.toLowerCase().includes("403")) {
        setError("Permission denied.");
        setTechnicalError(msg);
      } else if (msg.toLowerCase().includes("not connected")) {
        setError("Google Drive is not connected. Please connect Google Drive first.");
        setTechnicalError(msg);
      } else if (msg.toLowerCase().includes("missing") && msg.toLowerCase().includes("oauth")) {
        setError("Google Drive is not configured on the server. Please contact the technical administrator.");
        setTechnicalError(msg);
      } else if (msg.toLowerCase().includes("encryption key")) {
        setError("Backup encryption is not configured on the server. Please contact the technical administrator.");
        setTechnicalError(msg);
      } else {
        setError("Google Drive action failed.");
        setTechnicalError(msg);
      }
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
    if (!status.enabled) return "Not configured";
    if (status.status === "connected") return "Connected";
    if (status.status === "failed") return "Failed";
    if (status.status === "disconnected") return "Disconnected";
    return "Not connected";
  }, [status]);

  const tokenExpired = useMemo(() => {
    if (!status?.token_expiry) return false;
    const ts = Date.parse(status.token_expiry);
    if (Number.isNaN(ts)) return false;
    return ts <= Date.now();
  }, [status?.token_expiry]);

  const lastUploadAt = useMemo(() => {
    const ts = (driveCopies || [])
      .map((c) => (c?.uploaded_at ? Date.parse(c.uploaded_at) : 0))
      .filter((n) => Number.isFinite(n) && n > 0)
      .sort((a, b) => b - a)[0];
    return ts ? new Date(ts).toLocaleString() : null;
  }, [driveCopies]);

  const lastVerifiedAt = useMemo(() => {
    const ts = (driveCopies || [])
      .map((c) => (c?.verified_at ? Date.parse(c.verified_at) : 0))
      .filter((n) => Number.isFinite(n) && n > 0)
      .sort((a, b) => b - a)[0];
    return ts ? new Date(ts).toLocaleString() : null;
  }, [driveCopies]);

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
              disabled={!!busy || status?.status === "connected" || status?.enabled === false}
            >
              {busy === "connect" ? "Connecting…" : "Connect Google Drive"}
            </button>
            <button
              type="button"
              onClick={() => setIsDisconnectOpen(true)}
              className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              disabled={!!busy || status?.status !== "connected"}
            >
              Disconnect
            </button>
            <button
              type="button"
              onClick={() => doAction("health", healthCheck)}
              className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              disabled={!!busy || status?.status !== "connected" || tokenExpired}
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
        {noAccess && (
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3 text-gray-700">
            Google Drive management is available to Super Admin only.
          </div>
        )}
        {error && !noAccess && (
          <div className="rounded-md border border-red-200 bg-red-50 p-3 text-red-800">
            <div className="font-semibold">Action failed</div>
            <div className="mt-1">{error}</div>
            {technicalError && (
              <details className="mt-2 text-xs">
                <summary className="cursor-pointer select-none">Technical details</summary>
                <div className="mt-1 whitespace-pre-wrap text-red-900/80">{technicalError}</div>
              </details>
            )}
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
            <div className="text-xs text-gray-500">Status</div>
            <div className="font-semibold text-gray-900">
              {tokenExpired ? "Token expired" : statusLine}
            </div>
            {status?.connected_account && <div className="mt-1 text-xs text-gray-600">Account: {status.connected_account}</div>}
          </div>
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
            <div className="text-xs text-gray-500">Backup folder</div>
            <div className="font-semibold text-gray-900">{status?.backup_folder?.name || "Not set"}</div>
            {status?.backup_folder?.id && (
              <details className="mt-1 text-xs text-gray-600">
                <summary className="cursor-pointer select-none">Technical details</summary>
                <div className="mt-1">Folder ID: {status.backup_folder.id}</div>
              </details>
            )}
          </div>
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3">
            <div className="text-xs text-gray-500">Recent activity</div>
            <div className="text-gray-800">
              <div><span className="font-semibold">Last upload:</span> {lastUploadAt || "No upload yet"}</div>
              <div className="mt-1"><span className="font-semibold">Last verification:</span> {lastVerifiedAt || "Not verified yet"}</div>
              <details className="mt-2 text-xs text-gray-600">
                <summary className="cursor-pointer select-none">Last error</summary>
                <div className="mt-1 whitespace-pre-wrap">{status?.last_error || "None"}</div>
              </details>
            </div>
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
                  disabled={!!busy || status?.status !== "connected" || tokenExpired}
                >
                  Create/Use Backup Folder
                </button>
                <button
                  type="button"
                  onClick={() => doAction("upload", uploadSelected)}
                  className="pg-btn-primary"
                  disabled={!!busy || status?.status !== "connected" || tokenExpired || !selectedBackup}
                >
                  {busy === "upload" ? "Uploading…" : "Upload Backup to Drive"}
                </button>
                <button
                  type="button"
                  onClick={() => doAction("verify", verifySelected)}
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  disabled={!!busy || status?.status !== "connected" || tokenExpired || !selectedBackup}
                >
                  Verify Drive Copy
                </button>
                <button
                  type="button"
                  onClick={() => doAction("download", downloadSelected)}
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  disabled={!!busy || status?.status !== "connected" || tokenExpired || !selectedBackup}
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

      <Modal
        isOpen={isDisconnectOpen}
        onClose={() => setIsDisconnectOpen(false)}
        title="Disconnect Google Drive?"
        maxWidth="max-w-lg"
      >
        <p className="text-sm text-gray-700">
          Disconnecting Google Drive stops new uploads from PGSIMS. It does not delete backup files already present in Google Drive.
        </p>
        <div className="mt-4 flex justify-end gap-2">
          <button
            type="button"
            onClick={() => setIsDisconnectOpen(false)}
            className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            disabled={!!busy}
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={() => doAction("disconnect", async () => { await disconnect(); setIsDisconnectOpen(false); })}
            className="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 disabled:opacity-50"
            disabled={!!busy || status?.status !== "connected"}
          >
            {busy === "disconnect" ? "Disconnecting…" : "Disconnect"}
          </button>
        </div>
      </Modal>
    </SectionCard>
  );
}
