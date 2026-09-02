import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import ForgotPasswordPage from './page';
import authApi from '@/lib/api/auth';

jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    passwordReset: jest.fn(),
  },
}));

const mockedPasswordReset = authApi.passwordReset as jest.MockedFunction<typeof authApi.passwordReset>;

describe('ForgotPasswordPage', () => {
  beforeEach(() => {
    mockedPasswordReset.mockReset();
  });

  it('submits email to password reset API and shows success message', async () => {
    mockedPasswordReset.mockResolvedValueOnce({ message: 'Password reset email sent' });
    const user = userEvent.setup();

    render(<ForgotPasswordPage />);

    await user.type(screen.getByLabelText(/email address/i), 'resident@example.com');
    await user.click(screen.getByRole('button', { name: /send reset link/i }));

    await waitFor(() => {
      expect(mockedPasswordReset).toHaveBeenCalledWith('resident@example.com');
    });
    expect(await screen.findByText('Password reset email sent')).toBeInTheDocument();
  });

  it('shows API error message when reset request fails', async () => {
    mockedPasswordReset.mockRejectedValueOnce({
      isAxiosError: true,
      response: { data: { error: 'Failed to send reset email' } },
    });
    const user = userEvent.setup();

    render(<ForgotPasswordPage />);

    await user.type(screen.getByLabelText(/email address/i), 'resident@example.com');
    await user.click(screen.getByRole('button', { name: /send reset link/i }));

    expect(await screen.findByText('Failed to send reset email')).toBeInTheDocument();
  });
});
