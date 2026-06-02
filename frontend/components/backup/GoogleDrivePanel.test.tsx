/* eslint-disable @typescript-eslint/no-explicit-any */
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import GoogleDrivePanel from "./GoogleDrivePanel";
import { fetchAuth } from "@/lib/auth/fetch";

jest.mock("@/lib/auth/fetch");

describe("GoogleDrivePanel", () => {
  beforeEach(() => {
    (fetchAuth as jest.Mock).mockReset();
  });

  it("renders connected state and shows admin actions", async () => {
    (fetchAuth as jest.Mock).mockImplementation(async (url: string) => {
      if (url.endsWith("/api/backup_center/google-drive/status/")) {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            enabled: true,
            status: "connected",
            connected_account: "admin@example.com",
            backup_folder: { id: "folder123", name: "PGSIMS Backups" },
            token_expiry: new Date(Date.now() + 60_000).toISOString(),
            last_error: null,
          }),
        };
      }
      if (url.endsWith("/api/backup_center/google-drive/list/")) {
        return { ok: true, status: 200, json: async () => ({ results: [] }) };
      }
      return { ok: true, status: 200, json: async () => ({}) };
    });

    render(<GoogleDrivePanel canManage={true} completedBackups={[]} onRestoreReady={() => {}} />);

    await screen.findByText("Google Drive Backup");
    await screen.findByText("Connected");
    expect(screen.getByText(/Account: admin@example\.com/i)).toBeInTheDocument();
    expect(screen.getByText("Connect Google Drive")).toBeInTheDocument();
    expect(screen.getByText("Disconnect")).toBeInTheDocument();
    expect(screen.getByText("Check Connection")).toBeInTheDocument();
  });

  it("renders not configured when disabled", async () => {
    (fetchAuth as jest.Mock).mockImplementation(async (url: string) => {
      if (url.endsWith("/api/backup_center/google-drive/status/")) {
        return { ok: true, status: 200, json: async () => ({ enabled: false, status: "not_connected" }) };
      }
      if (url.endsWith("/api/backup_center/google-drive/list/")) {
        return { ok: true, status: 200, json: async () => ({ results: [] }) };
      }
      return { ok: true, status: 200, json: async () => ({}) };
    });

    render(<GoogleDrivePanel canManage={true} completedBackups={[]} onRestoreReady={() => {}} />);
    await screen.findByText("Not configured");
    expect(screen.getByText("Connect Google Drive")).toBeDisabled();
  });

  it("shows Super Admin only without surfacing a 403 error banner", async () => {
    (fetchAuth as jest.Mock).mockImplementation(async (url: string) => {
      if (url.endsWith("/api/backup_center/google-drive/status/")) {
        return { ok: false, status: 403, json: async () => ({}) };
      }
      if (url.endsWith("/api/backup_center/google-drive/list/")) {
        return { ok: false, status: 403, json: async () => ({}) };
      }
      return { ok: true, status: 200, json: async () => ({}) };
    });

    render(<GoogleDrivePanel canManage={false} completedBackups={[]} onRestoreReady={() => {}} />);
    await screen.findByText(/Super Admin only/i);
    expect(screen.queryByText("Action failed")).not.toBeInTheDocument();
  });

  it("requires confirmation to disconnect", async () => {
    (fetchAuth as jest.Mock).mockImplementation(async (url: string, options?: any) => {
      if (url.endsWith("/api/backup_center/google-drive/status/")) {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            enabled: true,
            status: "connected",
            connected_account: null,
            backup_folder: null,
            token_expiry: new Date(Date.now() + 60_000).toISOString(),
            last_error: null,
          }),
        };
      }
      if (url.endsWith("/api/backup_center/google-drive/list/")) {
        return { ok: true, status: 200, json: async () => ({ results: [] }) };
      }
      if (url.endsWith("/api/backup_center/google-drive/disconnect/") && options?.method === "POST") {
        return { ok: true, status: 200, json: async () => ({ status: "disconnected" }) };
      }
      return { ok: true, status: 200, json: async () => ({}) };
    });

    render(<GoogleDrivePanel canManage={true} completedBackups={[]} onRestoreReady={() => {}} />);
    await screen.findByText("Connected");

    fireEvent.click(screen.getByText("Disconnect"));
    expect(screen.getByText("Disconnect Google Drive?")).toBeInTheDocument();
    fireEvent.click(screen.getAllByText("Disconnect")[1]);

    await waitFor(() =>
      expect((fetchAuth as jest.Mock).mock.calls.some((c: any[]) => String(c[0]).includes("/google-drive/disconnect/"))).toBe(true)
    );
  });
});
