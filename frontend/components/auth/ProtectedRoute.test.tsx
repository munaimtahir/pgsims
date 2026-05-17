import React from 'react';
import { render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import ProtectedRoute from './ProtectedRoute';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

describe('ProtectedRoute', () => {
  const mockPush = jest.fn();

  beforeEach(() => {
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
    expect(screen.getByText('Loading...')).toBeTruthy();
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
    expect(screen.getByText('Content')).toBeTruthy();
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
    expect(screen.getByText('Content')).toBeTruthy();
  });
});
