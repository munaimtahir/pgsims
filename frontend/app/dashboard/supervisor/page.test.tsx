import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import SupervisorHomePage from './page';
import { trainingApi } from '@/lib/api/training';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    getSupervisorSummary: jest.fn(),
    getSupervisorOperationalDashboard: jest.fn(),
    getSupervisorPendingLeaves: jest.fn(),
    getLogbookReviewQueue: jest.fn(),
  },
}));

const mockedTrainingApi = trainingApi as unknown as {
  getSupervisorSummary: jest.Mock;
  getSupervisorOperationalDashboard: jest.Mock;
  getSupervisorPendingLeaves: jest.Mock;
  getLogbookReviewQueue: jest.Mock;
};

describe('SupervisorHomePage', () => {
  beforeEach(() => {
    mockedTrainingApi.getSupervisorSummary.mockResolvedValue({
      residents: [],
      pending: { leave_approvals: 0 },
    });
    mockedTrainingApi.getSupervisorOperationalDashboard.mockResolvedValue({
      assigned_residents: 0,
      pending_logbook_reviews: 0,
      returned_logbook_queue: 0,
      is_hod: false,
    });
    mockedTrainingApi.getSupervisorPendingLeaves.mockResolvedValue([]);
    mockedTrainingApi.getLogbookReviewQueue.mockResolvedValue({ count: 0, results: [] });
  });

  it('renders the supervisor dashboard', async () => {
    render(<SupervisorHomePage />);
    
    // Wait for header to be visible
    await waitFor(() => expect(screen.getByText('Supervisor Dashboard')).toBeInTheDocument());
    
    await waitFor(() => expect(screen.getByRole('heading', { name: /today’s attention/i })).toBeInTheDocument());
    expect(screen.getByRole('heading', { name: /my residents/i })).toBeInTheDocument();
  });
});
