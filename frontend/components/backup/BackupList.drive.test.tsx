/* eslint-disable @typescript-eslint/no-explicit-any */
import { render, screen } from "@testing-library/react";
import BackupList from "./BackupList";
import { useAuthStore } from "@/store/authStore";

describe("BackupList (Google Drive integration)", () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: { id: 1, username: "ADMIN", role: "ADMIN" } as any,
      isAuthenticated: true,
      isLoading: false,
      hasHydrated: true,
    } as any);
  });

  it("shows Google Drive status label per backup", () => {
    const backups = [
      {
        id: 1,
        created_at: new Date().toISOString(),
        backup_kind: "routine_application_data",
        status: "completed",
        file_name: "b1.pgsimsbak",
        file_size: 10,
      },
    ];
    const driveCopyByBackupId = {
      1: { upload_status: "uploaded", verification_status: "verified", download_status: "not_uploaded" },
    };

    render(
      <BackupList
        backups={backups}
        driveCopyByBackupId={driveCopyByBackupId}
        onRefresh={() => {}}
      />
    );

    expect(screen.getByText(/Google Drive: Verified/i)).toBeInTheDocument();
  });
});

