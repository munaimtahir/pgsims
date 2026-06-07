import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import RegisterPage from './page';
import authApi from '@/lib/api/auth';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    register: jest.fn(),
  },
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: () => ({
    setAuth: jest.fn(),
  }),
}));

const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

const mockedRegister = authApi.register as jest.MockedFunction<typeof authApi.register>;

describe('RegisterPage', () => {
  beforeEach(() => {
    mockedRegister.mockReset();
    mockPush.mockReset();
  });

  it('renders all fields and submits registration successfully', async () => {
    mockedRegister.mockResolvedValueOnce({
      user: {
        id: 101,
        username: 'testpg',
        email: 'testpg@example.com',
        first_name: 'Test',
        last_name: 'PG',
        role: 'pg',
      },
      tokens: {
        access: 'access_tok',
        refresh: 'refresh_tok',
      },
    });
    const user = userEvent.setup();

    render(<RegisterPage />);

    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^username$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^confirm password$/i)).toBeInTheDocument();

    await user.type(screen.getByLabelText(/first name/i), 'Test');
    await user.type(screen.getByLabelText(/last name/i), 'PG');
    await user.type(screen.getByLabelText(/^username$/i), 'testpg');
    await user.type(screen.getByLabelText(/email address/i), 'testpg@example.com');
    await user.type(screen.getByLabelText(/^password$/i), 'Password123!');
    await user.type(screen.getByLabelText(/^confirm password$/i), 'Password123!');

    await user.click(screen.getByRole('button', { name: /^register$/i }));

    await waitFor(() => {
      expect(mockedRegister).toHaveBeenCalledWith({
        first_name: 'Test',
        last_name: 'PG',
        username: 'testpg',
        email: 'testpg@example.com',
        password: 'Password123!',
        password2: 'Password123!',
        role: 'pg',
      });
    });

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard/resident');
    });
  });

  it('shows error when passwords do not match', async () => {
    const user = userEvent.setup();

    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/first name/i), 'Test');
    await user.type(screen.getByLabelText(/last name/i), 'PG');
    await user.type(screen.getByLabelText(/^username$/i), 'testpg');
    await user.type(screen.getByLabelText(/email address/i), 'testpg@example.com');
    await user.type(screen.getByLabelText(/^password$/i), 'Password123!');
    await user.type(screen.getByLabelText(/^confirm password$/i), 'DifferentPassword123!');

    await user.click(screen.getByRole('button', { name: /^register$/i }));

    expect(await screen.findByText('Passwords do not match.')).toBeInTheDocument();
    expect(mockedRegister).not.toHaveBeenCalled();
  });

  it('shows error when password is too short', async () => {
    const user = userEvent.setup();

    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/first name/i), 'Test');
    await user.type(screen.getByLabelText(/last name/i), 'PG');
    await user.type(screen.getByLabelText(/^username$/i), 'testpg');
    await user.type(screen.getByLabelText(/email address/i), 'testpg@example.com');
    await user.type(screen.getByLabelText(/^password$/i), 'short');
    await user.type(screen.getByLabelText(/^confirm password$/i), 'short');

    await user.click(screen.getByRole('button', { name: /^register$/i }));

    expect(await screen.findByText('Password must be at least 8 characters long.')).toBeInTheDocument();
    expect(mockedRegister).not.toHaveBeenCalled();
  });

  it('handles public registration disabled error (403)', async () => {
    mockedRegister.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 403, data: { error: 'Public registration is disabled.' } },
    });
    const user = userEvent.setup();

    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/first name/i), 'Test');
    await user.type(screen.getByLabelText(/last name/i), 'PG');
    await user.type(screen.getByLabelText(/^username$/i), 'testpg');
    await user.type(screen.getByLabelText(/email address/i), 'testpg@example.com');
    await user.type(screen.getByLabelText(/^password$/i), 'Password123!');
    await user.type(screen.getByLabelText(/^confirm password$/i), 'Password123!');

    await user.click(screen.getByRole('button', { name: /^register$/i }));

    expect(
      await screen.findByText(
        'Public registration is disabled. New accounts are provisioned by administrators only.'
      )
    ).toBeInTheDocument();
  });
});
