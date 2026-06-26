import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoginPage from './page';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/lib/api/auth';
import { useRouter } from 'next/navigation';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/auth', () => ({
  authApi: {
    login: jest.fn(),
  },
}));

describe('LoginPage', () => {
  const mockPush = jest.fn();
  const mockSetAuth = jest.fn();

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      setAuth: mockSetAuth,
      isAuthenticated: false,
    });
  });

  it('renders login form', () => {
    render(<LoginPage />);
    expect(screen.getByPlaceholderText(/Enter your username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter your password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in/i })).toBeInTheDocument();
  });

  it('handles successful login', async () => {
    const user = { id: 1, role: 'resident', profile_completed: true, force_password_change: false };
    (authApi.login as jest.Mock).mockResolvedValue({
      user,
      access: 'access-token',
      refresh: 'refresh-token',
    });

    render(<LoginPage />);
    
    fireEvent.change(screen.getByPlaceholderText(/Enter your username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Enter your password/i), {
      target: { value: 'password123' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Sign in/i }));

    await waitFor(() => {
      expect(authApi.login).toHaveBeenCalledWith({ username: 'testuser', password: 'password123' });
      expect(mockSetAuth).toHaveBeenCalledWith(user, 'access-token', 'refresh-token');
      expect(mockPush).toHaveBeenCalledWith('/dashboard/resident');
    });
  });

  it('redirects residents needing profile completion to the completion page', async () => {
    const user = { id: 1, role: 'resident', profile_completed: false, force_password_change: true };
    (authApi.login as jest.Mock).mockResolvedValue({
      user,
      access: 'access-token',
      refresh: 'refresh-token',
    });

    render(<LoginPage />);

    fireEvent.change(screen.getByPlaceholderText(/Enter your username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Enter your password/i), {
      target: { value: 'password123' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Sign in/i }));

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/resident/complete-profile');
    });
  });

  it('handles login failure', async () => {
    (authApi.login as jest.Mock).mockRejectedValue(new Error('Invalid credentials'));

    render(<LoginPage />);
    
    fireEvent.change(screen.getByPlaceholderText(/Enter your username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Enter your password/i), {
      target: { value: 'wrong' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/Login failed/i)).toBeInTheDocument();
    });
  });
});
