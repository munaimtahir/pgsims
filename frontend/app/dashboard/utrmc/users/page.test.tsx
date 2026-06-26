import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import UsersPage from './page';
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
  },
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    users: {
      list: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      resetPassword: jest.fn(),
      deactivate: jest.fn(),
      delete: jest.fn(),
    },
    departments: {
      list: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockTrainingApi = trainingApi as unknown as {
  listPrograms: jest.Mock;
  listResidentTrainingRecords: jest.Mock;
};
const mockApi = userbaseApi as unknown as {
  users: {
    list: jest.Mock;
    create: jest.Mock;
    update: jest.Mock;
    resetPassword: jest.Mock;
    deactivate: jest.Mock;
    delete: jest.Mock;
  };
  departments: { list: jest.Mock };
};

describe('UTRMC Users Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockAuth.mockReturnValue({ user: { role: 'utrmc_admin' } });
    mockApi.departments.list.mockResolvedValue([
      { id: 1, name: 'Medicine', code: 'MED', active: true, created_at: '2026-01-01T00:00:00Z' },
      { id: 2, name: 'Urology', code: 'URO', active: true, created_at: '2026-01-01T00:00:00Z' },
    ]);
    mockApi.users.list.mockResolvedValue([
      {
        id: 1,
        username: 'admin_user',
        full_name: 'Admin User',
        email: 'admin@example.com',
        role: 'admin',
        is_active: true,
        first_name: 'Admin',
        last_name: 'User',
        departments: [{ id: 1, name: 'Medicine', code: 'MED', member_type: 'supervisor', is_primary: true }],
      },
      {
        id: 2,
        username: 'resident_user',
        full_name: 'Resident User',
        email: 'resident@example.com',
        role: 'resident',
        is_active: false,
        first_name: 'Resident',
        last_name: 'User',
        departments: [{ id: 2, name: 'Urology', code: 'URO', member_type: 'resident', is_primary: true }],
        supervisor: 1,
      },
    ]);
    mockTrainingApi.listPrograms.mockResolvedValue([
      { id: 10, code: 'FCPS-URO', name: 'FCPS Urology', degree_type: 'FCPS', degree_type_display: 'FCPS', department: null, duration_months: 60, is_active: true, notes: '' },
    ]);
    mockTrainingApi.listResidentTrainingRecords.mockResolvedValue([
      {
        id: 3,
        resident_user: 2,
        resident_name: 'Resident User',
        program: 10,
        program_name: 'FCPS Urology',
        program_code: 'FCPS-URO',
        start_date: '2026-01-01',
        expected_end_date: null,
        current_level: 'y1',
        active: true,
        created_by: 1,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      },
    ]);
    mockApi.users.create.mockResolvedValue({ id: 3 });
    mockApi.users.update.mockResolvedValue({ id: 1 });
    mockApi.users.resetPassword.mockResolvedValue({ detail: 'ok' });
    mockApi.users.deactivate.mockResolvedValue({ id: 1 });
    mockApi.users.delete.mockResolvedValue({ detail: 'archived' });
  });

  it('renders filters and row actions', async () => {
    const user = userEvent.setup();
    render(<UsersPage />);

    expect(await screen.findByText('admin_user')).toBeInTheDocument();
    expect(screen.getByLabelText(/supervisor/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /resident programme assignment/i })).toBeInTheDocument();

    await user.selectOptions(screen.getByLabelText(/programme \/ course/i), '10');
    await user.selectOptions(screen.getByLabelText(/^role$/i, { selector: '#role-filter' }), 'resident');

    await waitFor(() => {
      expect(mockApi.users.list).toHaveBeenLastCalledWith(
        expect.objectContaining({
          role: 'resident',
          program: 10,
        })
      );
    });

    expect(screen.getByText('FCPS Urology')).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: /reset password/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('button', { name: /deactivate/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('button', { name: /delete/i }).length).toBeGreaterThan(0);
  });

  it('allows creating a user with role-aware fields', async () => {
    const user = userEvent.setup();
    render(<UsersPage />);

    await screen.findByText('admin_user');
    await user.click(screen.getByRole('button', { name: /\+ Add User/i }));

    await user.type(screen.getByLabelText(/^Username/i), 'new_supervisor');
    await user.type(screen.getByLabelText(/^Email/i), 'supervisor@example.com');
    await user.type(screen.getByLabelText(/^First Name/i), 'Super');
    await user.type(screen.getByLabelText(/^Last Name/i), 'Visor');
    await user.type(screen.getByLabelText(/^Password/i), 'SecretPass123!');
    await user.selectOptions(screen.getByLabelText(/^Specialty/i), 'medicine');
    await user.selectOptions(screen.getByLabelText(/^Role$/i, { selector: '#role' }), 'supervisor');
    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.users.create).toHaveBeenCalledWith(expect.objectContaining({
        username: 'new_supervisor',
        email: 'supervisor@example.com',
        first_name: 'Super',
        last_name: 'Visor',
        password: 'SecretPass123!',
        role: 'supervisor',
        specialty: 'medicine',
        is_active: true,
      }));
    });
  });
});
