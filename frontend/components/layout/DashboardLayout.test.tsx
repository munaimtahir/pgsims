import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DashboardLayout from './DashboardLayout';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api/auth';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  usePathname: () => '/dashboard',
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/auth', () => ({
  authApi: {
    logout: jest.fn(),
  },
}));

jest.mock('./Sidebar', () => ({
  __esModule: true,
  default: ({ role, userName, onLogout }: { role: string; userName: string; onLogout: () => void }) => (
    <div data-testid="sidebar">
      <span>{role}</span>
      <span>{userName}</span>
      <button onClick={onLogout}>Logout</button>
    </div>
  ),
}));

describe('DashboardLayout', () => {
  const mockPush = jest.fn();
  const mockClearAuth = jest.fn();

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
    (useAuthStore as unknown as jest.Mock).mockReturnValue({
      user: { full_name: 'Test User', role: 'RESIDENT' },
      clearAuth: mockClearAuth,
    });
    (authApi.logout as jest.Mock).mockResolvedValue({});
  });

  it('renders children and sidebar', () => {
    render(<DashboardLayout>Content</DashboardLayout>);
    expect(screen.getByTestId('sidebar')).toBeInTheDocument();
    expect(screen.getByText('Content')).toBeInTheDocument();
    expect(screen.getByText('Test User')).toBeInTheDocument();
  });

  it('handles logout', async () => {
    render(<DashboardLayout>Content</DashboardLayout>);
    fireEvent.click(screen.getByText('Logout'));
    
    await waitFor(() => {
      expect(authApi.logout).toHaveBeenCalled();
      expect(mockClearAuth).toHaveBeenCalled();
      expect(mockPush).toHaveBeenCalledWith('/login');
    });
  });
});
