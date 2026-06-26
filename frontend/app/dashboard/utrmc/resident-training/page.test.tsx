import type { ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import ResidentTrainingPage from './page';
import { trainingApi } from '@/lib/api/training';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    listPrograms: jest.fn(),
    listResidentTrainingRecords: jest.fn(),
    createResidentTrainingRecord: jest.fn(),
    updateResidentTrainingRecord: jest.fn(),
    deleteResidentTrainingRecord: jest.fn(),
  },
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    users: {
      list: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockTrainingApi = trainingApi as unknown as {
  listPrograms: jest.Mock;
  listResidentTrainingRecords: jest.Mock;
  createResidentTrainingRecord: jest.Mock;
  updateResidentTrainingRecord: jest.Mock;
  deleteResidentTrainingRecord: jest.Mock;
};
const mockUserbaseApi = userbaseApi as unknown as {
  users: { list: jest.Mock };
};

describe('ResidentTrainingPage', () => {
  beforeEach(() => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_admin' } });
    mockTrainingApi.listPrograms.mockResolvedValue([
      { id: 1, code: 'FCPS-URO', name: 'FCPS Urology', degree_type: 'FCPS', degree_type_display: 'FCPS', department: null, duration_months: 60, is_active: true, notes: '' },
    ]);
    mockTrainingApi.listResidentTrainingRecords.mockResolvedValue([
      {
        id: 11,
        resident_user: 21,
        resident_name: 'Resident One',
        program: 1,
        program_name: 'FCPS Urology',
        program_code: 'FCPS-URO',
        start_date: '2026-01-01',
        expected_end_date: '2031-01-01',
        current_level: 'y1',
        active: true,
        created_by: 1,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      },
    ]);
    mockTrainingApi.createResidentTrainingRecord.mockResolvedValue({});
    mockTrainingApi.updateResidentTrainingRecord.mockResolvedValue({});
    mockTrainingApi.deleteResidentTrainingRecord.mockResolvedValue(undefined);
    mockUserbaseApi.users.list.mockResolvedValue([
      { id: 21, username: 'resident.one', full_name: 'Resident One', first_name: 'Resident', last_name: 'One', role: 'resident', is_active: true },
    ]);
  });

  it('renders the resident programme assignment workflow', async () => {
    const user = userEvent.setup();
    render(<ResidentTrainingPage />);

    expect(await screen.findByText('Resident Programme Assignment')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '+ Add Assignment' })).toBeInTheDocument();
    expect(await screen.findByText('Resident One', { selector: 'td' }, { timeout: 3000 })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: '+ Add Assignment' }));
    await user.selectOptions(screen.getByLabelText(/^Resident$/i), '21');
    await user.selectOptions(screen.getByLabelText(/programme \/ course/i), '1');
    fireEvent.change(screen.getByLabelText(/start date/i), { target: { value: '2026-06-01' } });
    fireEvent.change(screen.getByLabelText(/expected end date/i), { target: { value: '2031-06-01' } });
    await user.selectOptions(screen.getByLabelText(/current level/i), 'y2');
    await user.click(screen.getByRole('button', { name: 'Save Assignment' }));

    await waitFor(() => {
      expect(mockTrainingApi.createResidentTrainingRecord).toHaveBeenCalled();
    });
  });
});
