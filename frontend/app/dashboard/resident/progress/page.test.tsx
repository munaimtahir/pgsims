import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import ResidentProgressPage from './page';
import { trainingApi } from '@/lib/api/training';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    getResidentOperationalDashboard: jest.fn(),
    listRotations: jest.fn(),
    listLogbook: jest.fn(),
    getMyLogbookThreshold: jest.fn(),
    getMyEligibility: jest.fn(),
  },
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

const mockedTrainingApi = trainingApi as unknown as {
  getResidentOperationalDashboard: jest.Mock;
  listRotations: jest.Mock;
  listLogbook: jest.Mock;
  getMyLogbookThreshold: jest.Mock;
  getMyEligibility: jest.Mock;
};

describe('ResidentProgressPage', () => {
  beforeEach(() => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({ user: { role: 'RESIDENT' } });
    
    mockedTrainingApi.getResidentOperationalDashboard.mockResolvedValue({
      logbook: { total: 0, draft: 0, submitted: 0, returned: 0, approved: 0, threshold: { overall_met: false, count: 0, items: [] } },
      readiness: { logbook_threshold_met: false },
      submissions: { synopsis: null, thesis: null },
      certificates: [],
      pending_actions: [],
    });
    mockedTrainingApi.listRotations.mockResolvedValue([]);
    mockedTrainingApi.listLogbook.mockResolvedValue({ count: 0, results: [] });
    mockedTrainingApi.getMyLogbookThreshold.mockResolvedValue({ count: 0, results: [], overall_met: false });
    mockedTrainingApi.getMyEligibility.mockResolvedValue([]);
  });

  it('renders the resident progress page', async () => {
    render(<ResidentProgressPage />);
    
    // Wait for "Loading..." to disappear
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    }, { timeout: 4000 });
    
    expect(screen.getByText(/Logbook Threshold Progress/i)).toBeInTheDocument();
    expect(screen.getByText(/Exam Eligibility/i)).toBeInTheDocument();
  });
});
