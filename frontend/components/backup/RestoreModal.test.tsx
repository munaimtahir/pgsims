import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import RestoreModal from './RestoreModal';
import { fetchAuth } from '@/lib/auth/fetch';

jest.mock('@/lib/auth/fetch');

describe('RestoreModal', () => {
  beforeEach(() => {
    (fetchAuth as jest.Mock).mockImplementation(async (url: string) => {
      if (url.endsWith('/api/backup_center/restores/upload/')) {
        return { ok: true, json: async () => ({ id: 123 }) };
      }
      if (url.endsWith('/api/backup_center/restores/123/validate/')) {
        return {
          ok: true,
          json: async () => ({
            valid: true,
            backup_kind: 'routine_application_data',
            manifest: {
              app_version: '1.2',
              database_engine: 'django.db.backends.sqlite3',
              created_at: new Date().toISOString(),
            },
            table_counts: {},
            media_summary: { file_count: 0 },
            errors: [],
            warnings: [],
          }),
        };
      }
      if (url.endsWith('/api/backup_center/restores/123/dry-run/')) {
        return { ok: true, json: async () => ({ status: 'validation_passed' }) };
      }
      return { ok: true, json: async () => ({}) };
    });
  });

  it('disables final restore until password, typed RESTORE, and checkbox', async () => {
    render(<RestoreModal isOpen={true} onClose={() => {}} onSuccess={() => {}} />);

    const file = new File(['data'], 'backup.pgsimsbak', { type: 'application/zip' });
    const input = screen.getByLabelText('Upload a backup file', { selector: 'input' }) as HTMLInputElement;
    fireEvent.change(input, { target: { files: [file] } });

    fireEvent.click(screen.getByText('Upload & Validate'));

    await waitFor(() => {
      expect(screen.getByText('Dry-Run Test')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Dry-Run Test'));

    await waitFor(() => {
      expect(screen.getByText('Finalize Restore')).toBeInTheDocument();
    });

    const finalize = screen.getByText('Finalize Restore') as HTMLButtonElement;
    expect(finalize).toBeDisabled();

    fireEvent.change(screen.getByLabelText('Your Admin Password'), { target: { value: 'pw' } });
    expect(finalize).toBeDisabled();

    fireEvent.change(screen.getByLabelText(/Type RESTORE to confirm/i), { target: { value: 'RESTORE' } });
    expect(finalize).toBeDisabled();

    fireEvent.click(screen.getByLabelText('I understand this will replace current application data.'));
    expect(finalize).not.toBeDisabled();
  });
});

