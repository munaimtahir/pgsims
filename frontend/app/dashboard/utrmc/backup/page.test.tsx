import { afterEach } from '@jest/globals';
import type { ReactNode } from 'react';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import BackupCenterPage from './page';
import { fetchAuth } from '@/lib/auth/fetch';
import useAuthStore from '@/store/authStore';

jest.mock('@/lib/auth/fetch', () => ({ fetchAuth: jest.fn() }));
jest.mock('@/components/backup/BackupList', () => ({ __esModule: true, default: ({ backups, onRefresh, onDriveRestoreReady }: any) => <><div data-testid="backup-list">{backups.map((item: any) => item.id).join(',')}</div><button onClick={onRefresh}>Refresh list</button><button onClick={() => onDriveRestoreReady?.(99)}>Drive restore ready</button></> }));
jest.mock('@/components/backup/GoogleDrivePanel', () => ({ __esModule: true, default: ({ completedBackups, onRestoreReady }: any) => <><span>Drive backups: {completedBackups.length}</span><button onClick={() => onRestoreReady(88)}>Prepare drive restore</button></> }));
jest.mock('@/components/backup/CreateBackupModal', () => ({ __esModule: true, default: ({ isOpen, defaultKind, onSuccess }: any) => isOpen ? <div>create:{defaultKind}<button onClick={onSuccess}>Created</button></div> : null }));
jest.mock('@/components/backup/RestoreModal', () => ({ __esModule: true, default: ({ isOpen, initialRestoreJobId, onSuccess }: any) => isOpen ? <div>restore:{initialRestoreJobId}<button onClick={onSuccess}>Restored</button></div> : null }));

const mockedFetch = fetchAuth as jest.Mock;
const response = (data: unknown, ok = true) => ({ ok, json: jest.fn().mockResolvedValue(data) });

beforeEach(() => {
  jest.clearAllMocks();
  window.history.replaceState({}, '', '/dashboard/utrmc/backup');
  useAuthStore.setState({ user: { id: 1, role: 'ADMIN' } as any });
  mockedFetch.mockImplementation((url: string) => {
    if (url.includes('audit-logs')) return Promise.resolve(response([{ id: 5, action: 'BACKUP_CREATED', actor_username: 'admin', created_at: '2026-01-01T00:00:00Z' }]));
    if (url.includes('restores')) return Promise.resolve(response([{ id: 7, started_at: '2026-01-02T00:00:00Z' }]));
    if (url.includes('google-drive/list')) return Promise.resolve(response([{ backup_record_id: 1, created_at: '2026-01-03T00:00:00Z' }, { backup_record_id: 1, created_at: '2026-01-04T00:00:00Z' }]));
    return Promise.resolve(response({ results: [{ id: 1, backup_kind: 'routine_application_data', status: 'completed', created_at: '2026-01-01T00:00:00Z' }, { id: 2, backup_kind: 'disaster_recovery', status: 'failed', created_at: '2026-01-02T00:00:00Z' }] }));
  });
});

afterEach(cleanup);

describe('BackupCenterPage', () => {
  it('blocks non-admin roles and does not request Google Drive records', () => {
    useAuthStore.setState({ user: { role: 'RESIDENT' } as any });
    render(<BackupCenterPage />);
    expect(screen.getByTestId('access-denied')).toHaveTextContent('Only administrative staff may view this page.');
    expect(mockedFetch).toHaveBeenCalledTimes(3);
    expect(mockedFetch.mock.calls.flat()).not.toContain('/api/backup_center/google-drive/list/');
  });

  it('loads paginated data, renders management controls, and refreshes all sources', async () => {
    render(<BackupCenterPage />);
    await screen.findByTestId('backup-list');
    expect(screen.getByTestId('backup-list')).toHaveTextContent('1,2');
    expect(screen.getByText('Drive backups: 1')).toBeInTheDocument();
    expect(screen.getByText('BACKUP_CREATED')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Create Full Server Recovery Backup' })).toBeInTheDocument();
    const before = mockedFetch.mock.calls.length;
    fireEvent.click(screen.getByRole('button', { name: 'Refresh' }));
    await waitFor(() => expect(mockedFetch.mock.calls.length).toBe(before + 4));
  });

  it('opens the correct backup and restore workflows, then reports their success', async () => {
    render(<BackupCenterPage />);
    await screen.findByTestId('backup-list');
    fireEvent.click(screen.getByRole('button', { name: 'Create Regular System Backup' }));
    expect(screen.getByText('create:routine_application_data')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Created'));
    await screen.findByText('Backup started. When complete, download and store the file safely.');
    fireEvent.click(screen.getByRole('button', { name: 'Create Full Server Recovery Backup' }));
    expect(screen.getByText('create:disaster_recovery')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Start Restore Wizard' }));
    expect(screen.getByRole('button', { name: 'Restored' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Prepare drive restore' }));
    expect(screen.getByText('restore:88')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Restored'));
    await screen.findByText('Restore completed successfully. A protection backup was created before restore.');
  });

  it('surfaces load failures and clears drive records for staff', async () => {
    useAuthStore.setState({ user: { role: 'SUPPORT_STAFF' } as any });
    mockedFetch.mockResolvedValue(response({}, false));
    render(<BackupCenterPage />);
    await screen.findByText('Access Denied');
    expect(mockedFetch).toHaveBeenCalledTimes(3);
    useAuthStore.setState({ user: { role: 'ADMIN' } as any });
    mockedFetch.mockRejectedValueOnce(new Error('network'));
    render(<BackupCenterPage />);
    await screen.findByText('An error occurred while loading backups');
  });
});
