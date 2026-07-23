import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import UTRMCOverviewPage from './page';
import { academicsApi } from '@/lib/api/academics';
import { supervisionApi } from '@/lib/api/supervision';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    getOverview: jest.fn(),
  },
}));

jest.mock('@/lib/api/supervision', () => ({
  supervisionApi: {
    getSupervisionDataQuality: jest.fn(),
  },
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    users: { list: jest.fn() },
  },
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

const mockedAcademicsApi = academicsApi as unknown as {
  getOverview: jest.Mock;
};
const mockedSupervisionApi = supervisionApi as unknown as {
  getSupervisionDataQuality: jest.Mock;
};
const mockedUserbaseApi = userbaseApi as unknown as {
  users: { list: jest.Mock };
};

describe('UTRMCOverviewPage', () => {
  beforeEach(() => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({ user: { role: 'ADMIN' } });
    mockedUserbaseApi.users.list.mockResolvedValue([
      { role: 'ADMIN' },
      { role: 'RESIDENT' },
      { role: 'SUPERVISOR' },
      { role: 'SUPPORT_STAFF' },
    ]);
    mockedAcademicsApi.getOverview.mockResolvedValue({
      cards: {
        active_training_records: 4,
        pending_review_queue_items: 3,
        residents_without_training_record: 1,
      },
    } as never);
    mockedSupervisionApi.getSupervisionDataQuality.mockResolvedValue({
      residents_without_primary_supervisor: [{ resident_id: 9 }],
    } as never);
  });

  it('renders the canonical admin dashboard shell', async () => {
    render(<UTRMCOverviewPage />);

    expect(screen.getByText('Admin Dashboard')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('Canonical Modules')).toBeInTheDocument());
    expect(screen.getByRole('link', { name: 'Users' })).toHaveAttribute('href', '/users');
    expect(screen.getByRole('link', { name: 'Supervision' })).toHaveAttribute('href', '/supervision');
    expect(screen.getByRole('link', { name: 'Academics' })).toHaveAttribute('href', '/academics');
  });
});
