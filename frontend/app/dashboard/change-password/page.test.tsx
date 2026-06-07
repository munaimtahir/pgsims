import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChangePasswordPage from './page';
import authApi from '@/lib/api/auth';

jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    changePassword: jest.fn(),
  },
}));

const mockedChangePassword = authApi.changePassword as jest.MockedFunction<
  typeof authApi.changePassword
>;

describe('ChangePasswordPage', () => {
  beforeEach(() => {
    mockedChangePassword.mockReset();
  });

  it('renders fields and handles success flow', async () => {
    mockedChangePassword.mockResolvedValueOnce({ message: 'Password changed successfully' });
    const user = userEvent.setup();

    render(<ChangePasswordPage />);

    expect(screen.getByLabelText(/^current password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^new password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^confirm new password$/i)).toBeInTheDocument();

    await user.type(screen.getByLabelText(/^current password$/i), 'OldPassword123!');
    await user.type(screen.getByLabelText(/^new password$/i), 'NewPassword123!');
    await user.type(screen.getByLabelText(/^confirm new password$/i), 'NewPassword123!');

    await user.click(screen.getByRole('button', { name: /update password/i }));

    await waitFor(() => {
      expect(mockedChangePassword).toHaveBeenCalledWith({
        old_password: 'OldPassword123!',
        new_password: 'NewPassword123!',
        new_password2: 'NewPassword123!',
      });
    });

    expect(await screen.findByText('Your password has been changed successfully.')).toBeInTheDocument();
  });

  it('shows error when new passwords do not match', async () => {
    const user = userEvent.setup();

    render(<ChangePasswordPage />);

    await user.type(screen.getByLabelText(/^current password$/i), 'OldPassword123!');
    await user.type(screen.getByLabelText(/^new password$/i), 'NewPassword123!');
    await user.type(screen.getByLabelText(/^confirm new password$/i), 'DifferentPassword123!');

    await user.click(screen.getByRole('button', { name: /update password/i }));

    expect(await screen.findByText('New passwords do not match.')).toBeInTheDocument();
    expect(mockedChangePassword).not.toHaveBeenCalled();
  });

  it('shows error when new password is too short', async () => {
    const user = userEvent.setup();

    render(<ChangePasswordPage />);

    await user.type(screen.getByLabelText(/^current password$/i), 'OldPassword123!');
    await user.type(screen.getByLabelText(/^new password$/i), 'short');
    await user.type(screen.getByLabelText(/^confirm new password$/i), 'short');

    await user.click(screen.getByRole('button', { name: /update password/i }));

    expect(await screen.findByText('New password must be at least 8 characters long.')).toBeInTheDocument();
    expect(mockedChangePassword).not.toHaveBeenCalled();
  });

  it('shows API error message when password change fails', async () => {
    mockedChangePassword.mockRejectedValueOnce({
      response: { data: { error: 'Current password is incorrect' } },
    });
    const user = userEvent.setup();

    render(<ChangePasswordPage />);

    await user.type(screen.getByLabelText(/^current password$/i), 'WrongOldPassword!');
    await user.type(screen.getByLabelText(/^new password$/i), 'NewPassword123!');
    await user.type(screen.getByLabelText(/^confirm new password$/i), 'NewPassword123!');

    await user.click(screen.getByRole('button', { name: /update password/i }));

    expect(await screen.findByText('Current password is incorrect')).toBeInTheDocument();
  });
});
