import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import UsersPage from './page';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    users: {
      list: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockApi = userbaseApi as unknown as {
  users: { list: jest.Mock; create: jest.Mock; update: jest.Mock };
};

describe('UTRMC Users Page', () => {
  const mockUsers = [
    {
      id: 1,
      username: 'admin_user',
      full_name: 'Admin User',
      email: 'admin@example.com',
      role: 'ADMIN',
      is_active: true,
      first_name: 'Admin',
      last_name: 'User',
    },
    {
      id: 2,
      username: 'resident_user',
      full_name: 'Resident User',
      email: 'resident@example.com',
      role: 'RESIDENT',
      is_active: false,
      first_name: 'Resident',
      last_name: 'User',
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    mockAuth.mockReturnValue({ user: { role: 'ADMIN' } });
    mockApi.users.list.mockResolvedValue(mockUsers);
    mockApi.users.create.mockResolvedValue({ id: 3 });
    mockApi.users.update.mockResolvedValue({ id: 1 });
  });

  it('renders user list and handles search filtering', async () => {
    render(<UsersPage />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('admin_user')).toBeInTheDocument();
      expect(screen.getByText('resident_user')).toBeInTheDocument();
    });

    const searchInput = screen.getByLabelText(/search users/i);
    await userEvent.type(searchInput, 'ADMIN');

    expect(screen.getByText('admin_user')).toBeInTheDocument();
    expect(screen.queryByText('resident_user')).not.toBeInTheDocument();
  });

  it('allows UTRMC admin to add a new user with password', async () => {
    const user = userEvent.setup();
    render(<UsersPage />);

    await waitFor(() => expect(screen.getByText('admin_user')).toBeInTheDocument());

    await user.click(screen.getByRole('button', { name: /\+ Add User/i }));

    expect(screen.getByRole('heading', { name: /add user/i })).toBeInTheDocument();

    await user.type(screen.getByLabelText(/^Username/i), 'new_guy');
    await user.type(screen.getByLabelText(/^Email/i), 'new_guy@example.com');
    await user.type(screen.getByLabelText(/^First Name/i), 'New');
    await user.type(screen.getByLabelText(/^Last Name/i), 'Guy');
    await user.type(screen.getByLabelText(/^Password/i), 'SecretPassword123!');
    await user.selectOptions(screen.getByLabelText(/role/i), 'RESIDENT');

    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.users.create).toHaveBeenCalledWith({
        username: 'new_guy',
        email: 'new_guy@example.com',
        first_name: 'New',
        last_name: 'Guy',
        password: 'SecretPassword123!',
        role: 'RESIDENT',
        is_active: true,
      });
    });
  });

  it('allows UTRMC admin to edit user and change password optionally', async () => {
    const user = userEvent.setup();
    render(<UsersPage />);

    await waitFor(() => expect(screen.getAllByText('Edit').length).toBeGreaterThan(0));

    // Click Edit on the first user (admin_user)
    const editButtons = screen.getAllByText('Edit');
    await user.click(editButtons[0]);

    expect(screen.getByRole('heading', { name: /edit user/i })).toBeInTheDocument();

    // Verify initial values
    expect(screen.getByLabelText(/^Username/i)).toHaveValue('admin_user');

    // Change first name and leave password blank
    await user.clear(screen.getByLabelText(/^First Name/i));
    await user.type(screen.getByLabelText(/^First Name/i), 'ModifiedAdmin');

    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.users.update).toHaveBeenCalledWith(1, {
        username: 'admin_user',
        email: 'admin@example.com',
        first_name: 'ModifiedAdmin',
        last_name: 'User',
        role: 'ADMIN',
        is_active: true,
      });
    });

    // Open edit again and update password
    await user.click(editButtons[0]);
    await user.type(screen.getByLabelText(/new password/i), 'NewCoolPass987!');
    await user.click(screen.getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(mockApi.users.update).toHaveBeenLastCalledWith(1, {
        username: 'admin_user',
        email: 'admin@example.com',
        first_name: 'Admin',
        last_name: 'User',
        role: 'ADMIN',
        is_active: true,
        password: 'NewCoolPass987!',
      });
    });
  });

  it('shows read-only view and hides add/edit controls for read-only UTRMC user', async () => {
    mockAuth.mockReturnValue({ user: { role: 'SUPPORT_STAFF' } });
    render(<UsersPage />);

    await waitFor(() => expect(screen.getByText('admin_user')).toBeInTheDocument());

    expect(screen.queryByRole('button', { name: /\+ Add User/i })).not.toBeInTheDocument();
    expect(screen.getAllByText('View only')[0]).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Edit' })).not.toBeInTheDocument();
  });
});
