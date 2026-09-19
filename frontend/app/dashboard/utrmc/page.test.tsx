import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import UTRMCOverviewPage from './page';
import { academicsApi } from '@/lib/api/academics';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    getAdminDashboardMonitoring: jest.fn(),
  },
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

const mockedAcademicsApi = academicsApi as unknown as {
  getAdminDashboardMonitoring: jest.Mock;
};

describe('UTRMCOverviewPage', () => {
  beforeEach(() => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({ user: { role: 'ADMIN' } });
    mockedAcademicsApi.getAdminDashboardMonitoring.mockResolvedValue({
      total_users: 12,
      active_residents: 4,
      supervisor_users: 3,
      pending_supervisor_reviews: 2,
      residents_without_primary_supervisor: 1,
      residents_without_training_record: 1,
      pending_supervisor_links: 1,
      data_quality_issue_count: 1,
      residents_with_training_record: 3,
      active_training_records: 3,
    } as never);
  });

  it('renders the canonical admin dashboard shell', async () => {
    render(<UTRMCOverviewPage />);

    expect(screen.getByText('Admin Dashboard')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('Programme health')).toBeInTheDocument());
    expect(screen.getByText('12')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Manage users' })).toHaveAttribute('href', '/users');
    expect(mockedAcademicsApi.getAdminDashboardMonitoring).toHaveBeenCalledTimes(1);
  });
});
