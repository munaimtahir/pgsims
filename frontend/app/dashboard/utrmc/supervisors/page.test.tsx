import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import SupervisorsPage from './page';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    users: {
      list: jest.fn(),
      update: jest.fn(),
    },
    staff: {
      list: jest.fn(),
      update: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockApi = userbaseApi as unknown as {
  users: { list: jest.Mock; update: jest.Mock };
  staff: { list: jest.Mock; update: jest.Mock };
};

describe('UTRMC Supervisors page', () => {
  beforeEach(() => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_admin' } });
    mockApi.users.list.mockResolvedValue([
      {
        id: 20,
        username: 'supervisor_user',
        full_name: 'Dr Supervisor',
        role: 'supervisor',
        is_active: true,
        specialty: 'medicine',
        email: 'supervisor@example.com',
      },
    ]);
    mockApi.staff.list.mockResolvedValue([
      {
        id: 30,
        user: { id: 20, username: 'supervisor_user' },
        designation: 'Professor',
        phone: '1234567890',
        active: true,
      },
    ]);
    mockApi.users.update.mockResolvedValue({ id: 20 });
    mockApi.staff.update.mockResolvedValue({ id: 30 });
  });

  it('renders supervisor list and allows UTRMC admin to open edit modal and save', async () => {
    const user = userEvent.setup();
    render(<SupervisorsPage />);

    await waitFor(() => expect(screen.getByText('Dr Supervisor')).toBeInTheDocument());
    expect(screen.getByText('Professor')).toBeInTheDocument();
    expect(screen.getByText('1234567890')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Edit' }));
    
    const designationInput = screen.getByLabelText('Designation');
    expect(designationInput).toHaveValue('Professor');

    await user.clear(designationInput);
    await user.type(designationInput, 'Senior Professor');

    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.staff.update).toHaveBeenCalledWith(20, {
        designation: 'Senior Professor',
        phone: '1234567890',
        active: true,
      });
    });
  });

  it('allows UTRMC admin to edit supervisor profile and change password', async () => {
    const user = userEvent.setup();
    render(<SupervisorsPage />);

    await waitFor(() => expect(screen.getByText('Dr Supervisor')).toBeInTheDocument());

    await user.click(screen.getByRole('button', { name: 'Edit' }));

    const passwordInput = screen.getByLabelText(/new password/i);
    await user.type(passwordInput, 'NewSecret123!');

    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.users.update).toHaveBeenCalledWith(20, {
        email: 'supervisor@example.com',
        first_name: 'Dr',
        last_name: 'Supervisor',
        specialty: 'medicine',
        password: 'NewSecret123!',
      });
      expect(mockApi.staff.update).toHaveBeenCalledWith(20, {
        designation: 'Professor',
        phone: '1234567890',
        active: true,
      });
    });
  });

  it('shows read-only view and hides edit controls for read-only UTRMC user', async () => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_user' } });
    render(<SupervisorsPage />);

    await waitFor(() => expect(screen.getByText('Dr Supervisor')).toBeInTheDocument());
    expect(screen.getByText('View only')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Edit' })).not.toBeInTheDocument();
  });
});
