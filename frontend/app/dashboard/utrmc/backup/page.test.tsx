import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import BackupCenterPage from './page';
import { fetchAuth } from '../../../../lib/auth/fetch';
import { toast } from 'react-hot-toast';

// Mock the dependencies
jest.mock('../../../../lib/auth/fetch');
jest.mock('react-hot-toast');
jest.mock('../../../../components/backup/BackupList', () => ({
  __esModule: true,
  default: ({ backups }: any) => <div data-testid="backup-list">{backups?.length || 0} backups</div>,
}));

jest.mock('../../../../components/backup/CreateBackupModal', () => ({
  __esModule: true,
  default: ({ isOpen }: any) => isOpen ? <div>Backup Pathway</div> : null,
}));

jest.mock('../../../../components/backup/RestoreModal', () => ({
  __esModule: true,
  default: ({ isOpen }: any) => isOpen ? <div>Upload Backup</div> : null,
}));


describe('BackupCenterPage', () => {
  const mockBackups = [
    { id: 1, file_name: 'test1.pgsimsbak', status: 'completed', created_at: new Date().toISOString(), backup_kind: 'routine_application_data' },
  ];

  beforeEach(() => {
    (fetchAuth as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockBackups,
    });
  });

  it('renders the page and loads backups', async () => {
    render(<BackupCenterPage />);
    
    expect(screen.getByText('Backup & Restore Center')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByTestId('backup-list')).toHaveTextContent('1 backups');
    });
  });

  it('opens the create backup modal when button is clicked', async () => {
    render(<BackupCenterPage />);
    
    const createBtn = screen.getByText('Create Backup');
    fireEvent.click(createBtn);
    
    expect(screen.getByText('Backup Pathway')).toBeInTheDocument();
  });
});
