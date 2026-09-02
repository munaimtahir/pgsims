import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import ProtectedRoute from './ProtectedRoute';
import { useRouter, usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import authApi from '@/lib/api/auth';
import { afterEach } from '@jest/globals';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  usePathname: jest.fn(),
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    me: jest.fn(),
  },
}));

describe('ProtectedRoute', () => {
  const mockPush = jest.fn();

  beforeEach(() => {
    mockPush.mockReset();
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
    (usePathname as jest.Mock).mockReturnValue('/dashboard/resident');
    (authApi.me as jest.Mock).mockResolvedValue({ allowed_next_route: '/dashboard/resident' });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state when not hydrated', () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      user: null,
      hasHydrated: false,
    });

    render(<ProtectedRoute>Content</ProtectedRoute>);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('redirects to /login when not authenticated', () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      user: null,
      hasHydrated: true,
    });

    render(<ProtectedRoute>Content</ProtectedRoute>);
    expect(mockPush).toHaveBeenCalledWith('/login');
  });

  it('renders children when authenticated and role is allowed', async () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'RESIDENT' },
      hasHydrated: true,
    });

    render(<ProtectedRoute allowedRoles={['RESIDENT']}>Content</ProtectedRoute>);
    await waitFor(() => expect(screen.getByText('Content')).toBeInTheDocument());
  });

  it('redirects to /change-password when the backend says onboarding is incomplete', async () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'RESIDENT' },
      hasHydrated: true,
    });
    (authApi.me as jest.Mock).mockResolvedValue({ allowed_next_route: '/change-password' });

    render(<ProtectedRoute allowedRoles={['RESIDENT']}>Content</ProtectedRoute>);
    await waitFor(() => expect(mockPush).toHaveBeenCalledWith('/change-password'));
  });

  it('redirects to role dashboard when role is not allowed', () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'SUPERVISOR' },
      hasHydrated: true,
    });

    render(<ProtectedRoute allowedRoles={['RESIDENT']}>Content</ProtectedRoute>);
    expect(mockPush).toHaveBeenCalledWith('/dashboard/supervisor');
  });

  it('allows admin role even if not in allowedRoles', async () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'ADMIN' },
      hasHydrated: true,
    });

    render(<ProtectedRoute allowedRoles={['RESIDENT']}>Content</ProtectedRoute>);
    await waitFor(() => expect(screen.getByText('Content')).toBeInTheDocument());
  });
});
