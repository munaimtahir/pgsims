/* eslint-disable @typescript-eslint/no-explicit-any */
import { render, screen, waitFor } from '@testing-library/react';
import BackupCenterPage from './page';
import { fetchAuth } from '../../../../lib/auth/fetch';
import { useAuthStore } from '../../../../store/authStore';

jest.mock('../../../../lib/auth/fetch');

jest.mock('../../../../components/backup/BackupList', () => ({
  __esModule: true,
  default: ({ backups }: any) => (
    <div data-testid="backup-list">
      {backups.map((b: any) => <div key={b.id}>{b.file_name}</div>)}
    </div>
  )
}));

jest.mock('../../../../components/backup/CreateBackupModal', () => ({
  __esModule: true,
  default: () => <div data-testid="create-modal" />
}));

jest.mock('../../../../components/backup/RestoreModal', () => ({
  __esModule: true,
  default: () => <div data-testid="restore-modal" />
}));

describe('BackupCenterPage', () => {
  const mockBackups = [
    {
      id: 1,
      file_name: 'test1.pgsimsbak',
      status: 'completed',
      created_at: new Date().toISOString(),
      backup_kind: 'routine_application_data',
      file_size: 1024,
    },
  ];

  const mockAuditLogs = [
    {
      id: 1,
      action: 'routine_backup_completed',
      created_at: new Date().toISOString(),
      actor_username: 'admin',
    },
  ];

  beforeEach(() => {
    useAuthStore.setState({
      user: { id: 1, username: 'admin', role: 'admin' } as any,
      accessToken: 't',
      refreshToken: 'r',
      isAuthenticated: true,
      isLoading: false,
      hasHydrated: true,
    });

    (fetchAuth as jest.Mock).mockImplementation(async (url: string) => {
      if (url.includes('/api/backup_center/backups/')) {
        return { ok: true, json: async () => ({ results: mockBackups }) };
      }
      if (url.includes('/api/backup_center/audit-logs/')) {
        return { ok: true, json: async () => ({ results: mockAuditLogs }) };
      }
      if (url.includes('/api/backup_center/restores/')) {
        return { ok: true, json: async () => ({ results: [] }) };
      }
      return { ok: true, json: async () => ({ results: [] }) };
    });
  });

  it('renders key sections and actions', async () => {
    render(<BackupCenterPage />);

    expect(screen.getByText('Backup Center')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Backup History')).toBeInTheDocument();
    });

    expect(screen.getByText('Create Regular System Backup')).toBeInTheDocument();
    expect(screen.getByText('Create Full Server Recovery Backup')).toBeInTheDocument();
    
    // Backup list is a ul, not a table
    await waitFor(() => {
      expect(screen.queryByText(/Loading backups/)).not.toBeInTheDocument();
      expect(screen.getByText(/test1\.pgsimsbak/i)).toBeInTheDocument();
    }, { timeout: 3000 });

    expect(screen.getByText('Restore Wizard')).toBeInTheDocument();
    expect(screen.getByText('Start Restore Wizard')).toBeInTheDocument();
    expect(screen.getByText('Audit Log')).toBeInTheDocument();
    expect(screen.getByRole('table', { name: 'Audit Log' })).toBeInTheDocument();
  });

  it('shows access denied to restricted roles', async () => {
    useAuthStore.setState({ user: { id: 2, username: 'pg1', role: 'pg' } as any });
    render(<BackupCenterPage />);

    await waitFor(() => {
      expect(screen.getByTestId('access-denied')).toBeInTheDocument();
    });

    expect(screen.queryByText('Backup Center')).not.toBeInTheDocument();
    expect(screen.queryByText('Restore Wizard')).not.toBeInTheDocument();
  });

  it('allows other admins to view page and create routine backup, but hides restore/disaster controls', async () => {
    useAuthStore.setState({ user: { id: 3, username: 'utrmc_admin1', role: 'utrmc_admin' } as any });
    render(<BackupCenterPage />);

    await waitFor(() => {
      expect(screen.getByText('Backup Center')).toBeInTheDocument();
    });

    expect(screen.getByText('Create Regular System Backup')).toBeInTheDocument();
    expect(screen.queryByText('Create Full Server Recovery Backup')).not.toBeInTheDocument();
    expect(screen.queryByText('Restore Wizard')).not.toBeInTheDocument();
  });
});
