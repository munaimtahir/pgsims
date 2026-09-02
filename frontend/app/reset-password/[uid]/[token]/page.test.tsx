import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ResetPasswordConfirmPage from './page';
import authApi from '@/lib/api/auth';

jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    passwordResetConfirm: jest.fn(),
  },
}));

jest.mock('next/navigation', () => ({
  useParams: () => ({ uid: 'encoded_uid', token: 'some_token' }),
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

const mockedPasswordResetConfirm = authApi.passwordResetConfirm as jest.MockedFunction<
  typeof authApi.passwordResetConfirm
>;

describe('ResetPasswordConfirmPage', () => {
  beforeEach(() => {
    mockedPasswordResetConfirm.mockReset();
  });

  it('renders fields and handles success flow', async () => {
    mockedPasswordResetConfirm.mockResolvedValueOnce({ message: 'Password reset successful' });
    const user = userEvent.setup();

    render(<ResetPasswordConfirmPage />);

    expect(screen.getByLabelText(/new password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();

    await user.type(screen.getByLabelText(/new password/i), 'NewPassword123!');
    await user.type(screen.getByLabelText(/confirm password/i), 'NewPassword123!');

    await user.click(screen.getByRole('button', { name: /set password/i }));

    await waitFor(() => {
      expect(mockedPasswordResetConfirm).toHaveBeenCalledWith({
        uid: 'encoded_uid',
        token: 'some_token',
        new_password: 'NewPassword123!',
        new_password2: 'NewPassword123!',
      });
    });

    expect(await screen.findByText('Password Set Successfully')).toBeInTheDocument();
  });

  it('shows error when passwords do not match', async () => {
    const user = userEvent.setup();

    render(<ResetPasswordConfirmPage />);

    await user.type(screen.getByLabelText(/new password/i), 'NewPassword123!');
    await user.type(screen.getByLabelText(/confirm password/i), 'DifferentPassword123!');

    await user.click(screen.getByRole('button', { name: /set password/i }));

    expect(await screen.findByText('Passwords do not match.')).toBeInTheDocument();
    expect(mockedPasswordResetConfirm).not.toHaveBeenCalled();
  });

  it('shows error when password is too short', async () => {
    const user = userEvent.setup();

    render(<ResetPasswordConfirmPage />);

    await user.type(screen.getByLabelText(/new password/i), 'short');
    await user.type(screen.getByLabelText(/confirm password/i), 'short');

    await user.click(screen.getByRole('button', { name: /set password/i }));

    expect(await screen.findByText('Password must be at least 8 characters long.')).toBeInTheDocument();
    expect(mockedPasswordResetConfirm).not.toHaveBeenCalled();
  });

  it('shows API error message when setting password fails', async () => {
    mockedPasswordResetConfirm.mockRejectedValueOnce({
      isAxiosError: true,
      response: { data: { error: 'Reset token is invalid or has expired.' } },
    });
    const user = userEvent.setup();

    render(<ResetPasswordConfirmPage />);

    await user.type(screen.getByLabelText(/new password/i), 'NewPassword123!');
    await user.type(screen.getByLabelText(/confirm password/i), 'NewPassword123!');

    await user.click(screen.getByRole('button', { name: /set password/i }));

    expect(await screen.findByText('Reset token is invalid or has expired.')).toBeInTheDocument();
  });
});
