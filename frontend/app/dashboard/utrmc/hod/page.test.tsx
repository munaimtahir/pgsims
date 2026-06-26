import type { ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import HodPage from './page';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    hodAssignments: {
      list: jest.fn(),
      create: jest.fn(),
    },
    departments: {
      list: jest.fn(),
    },
    users: {
      list: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockApi = userbaseApi as unknown as {
  hodAssignments: { list: jest.Mock; create: jest.Mock };
  departments: { list: jest.Mock };
  users: { list: jest.Mock };
};

describe('UTRMC HOD assignments page', () => {
  beforeEach(() => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_admin' } });
    mockApi.hodAssignments.list.mockResolvedValue([
      {
        id: 40,
        department: { id: 10, name: 'Medicine' },
        hod_user: { id: 20, username: 'hod_user', full_name: 'Dr HOD' },
        start_date: '2026-04-01',
        active: true,
      },
    ]);
    mockApi.departments.list.mockResolvedValue([{ id: 10, name: 'Medicine', code: 'MED', active: true }]);
    mockApi.users.list.mockResolvedValue([
      { id: 20, username: 'hod_user', full_name: 'Dr HOD', role: 'supervisor', is_active: true },
      { id: 21, username: 'resident_user', full_name: 'Resident', role: 'resident', is_active: true },
    ]);
    mockApi.hodAssignments.create.mockResolvedValue({ id: 41 });
  });

  it('lets UTRMC admin exercise the Add HOD CTA and submit a valid assignment', async () => {
    const user = userEvent.setup();
    render(<HodPage />);

    await waitFor(() => expect(screen.getByText('Dr HOD')).toBeInTheDocument());

    await user.click(screen.getByRole('button', { name: '+ Add HOD' }));
    const [departmentSelect, hodSelect] = screen.getAllByRole('combobox');
    await user.selectOptions(departmentSelect, '10');
    await user.selectOptions(hodSelect, '20');
    fireEvent.change(screen.getByLabelText(/start date/i), { target: { value: '2026-05-01' } });
    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() =>
      expect(mockApi.hodAssignments.create).toHaveBeenCalledWith({
        department_id: 10,
        hod_user_id: 20,
        start_date: '2026-05-01',
        active: true,
      })
    );
  });

  it('shows read-only state without exposing the Add HOD CTA to UTRMC user', async () => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_user' } });

    render(<HodPage />);

    await waitFor(() => expect(screen.getByText('Dr HOD')).toBeInTheDocument());

    expect(screen.getByText(/read-only/i)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '+ Add HOD' })).not.toBeInTheDocument();
  });
});
