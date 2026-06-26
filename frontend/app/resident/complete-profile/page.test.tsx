import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResidentCompleteProfilePage from './page';
import { authApi } from '@/lib/api/auth';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/auth', () => ({
  authApi: {
    getProfileCompletionStatus: jest.fn(),
    completeProfile: jest.fn(),
  },
}));

describe('ResidentCompleteProfilePage', () => {
  const mockPush = jest.fn();
  const mockSetUser = jest.fn();

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      user: {
        role: 'resident',
        email: 'resident@example.com',
        phone_number: '03001234567',
        cnic: '12345-1234567-1',
      },
      setUser: mockSetUser,
      hasHydrated: true,
      isAuthenticated: true,
    });
    (authApi.getProfileCompletionStatus as jest.Mock).mockResolvedValue({
      profile_completed: false,
      force_password_change: true,
      needs_completion: true,
      program: 'FCPS',
      training_year: '1',
      joining_date: '2026-01-01',
    });
    (authApi.completeProfile as jest.Mock).mockResolvedValue({
      detail: 'Profile completed.',
      redirect_to: '/dashboard/resident',
    });
  });

  it('renders the completion form', async () => {
    render(<ResidentCompleteProfilePage />);

    expect(await screen.findByRole('heading', { name: 'Complete Profile' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('New Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Complete Profile' })).toBeInTheDocument();
  });

  it('submits the completion form', async () => {
    render(<ResidentCompleteProfilePage />);

    await screen.findByRole('heading', { name: 'Complete Profile' });

    fireEvent.change(screen.getByPlaceholderText('New Password'), { target: { value: 'NewPass123!' } });
    fireEvent.change(screen.getByPlaceholderText('Confirm New Password'), { target: { value: 'NewPass123!' } });
    fireEvent.change(screen.getByPlaceholderText('Mobile Number'), { target: { value: '03009998888' } });
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'resident.updated@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('CNIC'), { target: { value: '12345-7654321-2' } });
    fireEvent.change(screen.getByPlaceholderText('Program'), { target: { value: 'FCPS' } });
    fireEvent.change(screen.getByPlaceholderText('Training Year'), { target: { value: '2' } });

    fireEvent.click(screen.getByRole('button', { name: 'Complete Profile' }));

    await waitFor(() => {
      expect(authApi.completeProfile).toHaveBeenCalled();
      expect(mockSetUser).toHaveBeenCalled();
      expect(mockPush).toHaveBeenCalledWith('/dashboard/resident');
    });
  });
});
