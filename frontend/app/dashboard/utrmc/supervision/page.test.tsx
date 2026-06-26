import type { ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import SupervisionPage from './page';
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
    supervisionLinks: {
      list: jest.fn(),
      create: jest.fn(),
    },
    users: {
      list: jest.fn(),
    },
    departments: {
      list: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockApi = userbaseApi as unknown as {
  supervisionLinks: { list: jest.Mock; create: jest.Mock };
  users: { list: jest.Mock };
  departments: { list: jest.Mock };
};

describe('UTRMC Supervision links page', () => {
  beforeEach(() => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_admin' } });
    mockApi.supervisionLinks.list.mockResolvedValue([
      {
        id: 1,
        supervisor_user: { id: 2, username: 'sup', full_name: 'Dr Sup' },
        resident_user: { id: 3, username: 'res', full_name: 'Dr Res' },
        department: { id: 4, name: 'Urology' },
        start_date: '2026-01-01',
        active: true,
      },
    ]);
    mockApi.users.list.mockResolvedValue([
      { id: 2, username: 'sup', full_name: 'Dr Sup', role: 'supervisor', is_active: true },
      { id: 3, username: 'res', full_name: 'Dr Res', role: 'resident', is_active: true },
    ]);
    mockApi.departments.list.mockResolvedValue([{ id: 4, name: 'Urology', code: 'URO', active: true, created_at: '2026-01-01' }]);
    mockApi.supervisionLinks.create.mockResolvedValue({ id: 2 });
  });

  it('renders supervision rows and exposes department selection', async () => {
    const user = userEvent.setup();
    render(<SupervisionPage />);

    expect(await screen.findByText('Dr Sup')).toBeInTheDocument();
    expect(screen.getByText('Urology')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: '+ Add Link' }));
    expect(screen.getByLabelText(/department/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/resident \/ pg/i)).toBeInTheDocument();

    await user.selectOptions(screen.getByLabelText(/supervisor/i), '2');
    await user.selectOptions(screen.getByLabelText(/resident \/ pg/i), '3');
    await user.selectOptions(screen.getByLabelText(/department/i), '4');
    fireEvent.change(screen.getByLabelText(/start date/i), { target: { value: '2026-06-01' } });
    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.supervisionLinks.create).toHaveBeenCalledWith(expect.objectContaining({
        supervisor_user_id: 2,
        resident_user_id: 3,
        department_id: 4,
        start_date: '2026-06-01',
        active: true,
      }));
    });
  });
});
