import React from 'react';
import { render, screen } from '@testing-library/react';
import ProtectedRoute from './ProtectedRoute';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { afterEach } from '@jest/globals';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

describe('ProtectedRoute', () => {
  const mockPush = jest.fn();

  beforeEach(() => {
    mockPush.mockReset();
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
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

  it('renders children when authenticated and role is allowed', () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'resident' },
      hasHydrated: true,
    });

    render(<ProtectedRoute allowedRoles={['resident']}>Content</ProtectedRoute>);
    expect(screen.getByText('Content')).toBeInTheDocument();
  });

  it('redirects to role dashboard when role is not allowed', () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'supervisor' },
      hasHydrated: true,
    });

    render(<ProtectedRoute allowedRoles={['resident']}>Content</ProtectedRoute>);
    expect(mockPush).toHaveBeenCalledWith('/dashboard/supervisor');
  });

  it('allows admin role even if not in allowedRoles', () => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { role: 'admin' },
      hasHydrated: true,
    });

    render(<ProtectedRoute allowedRoles={['resident']}>Content</ProtectedRoute>);
    expect(screen.getByText('Content')).toBeInTheDocument();
  });
});
