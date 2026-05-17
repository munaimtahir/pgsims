import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import UTRMCOverviewPage from './page';
import { trainingApi } from '@/lib/api/training';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/components/utrmc/BulkSetupWorkspace', () => ({
  __esModule: true,
  default: () => <div data-testid="bulk-setup">Bulk Setup</div>,
}));

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    listResidentTrainingRecords: jest.fn(),
    listRotations: jest.fn(),
    getUTRMCOperationalDashboard: jest.fn(),
    getSynopsisReviewQueue: jest.fn(),
    getThesisReviewQueue: jest.fn(),
    listRotationCompletions: jest.fn(),
  },
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    hospitals: { list: jest.fn() },
    departments: { list: jest.fn() },
    users: { list: jest.fn() },
    matrix: { list: jest.fn() },
    dataQuality: { summary: jest.fn() },
  },
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

const mockedTrainingApi = trainingApi as unknown as {
  listResidentTrainingRecords: jest.Mock;
  listRotations: jest.Mock;
  getUTRMCOperationalDashboard: jest.Mock;
  getSynopsisReviewQueue: jest.Mock;
  getThesisReviewQueue: jest.Mock;
  listRotationCompletions: jest.Mock;
};
const mockedUserbaseApi = userbaseApi as unknown as {
  hospitals: { list: jest.Mock };
  departments: { list: jest.Mock };
  users: { list: jest.Mock };
  matrix: { list: jest.Mock };
  dataQuality: { summary: jest.Mock };
};

describe('UTRMCOverviewPage', () => {
  beforeEach(() => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({ user: { role: 'admin' } });
    
    mockedUserbaseApi.hospitals.list.mockResolvedValue([]);
    mockedUserbaseApi.departments.list.mockResolvedValue([]);
    mockedUserbaseApi.users.list.mockResolvedValue([]);
    mockedUserbaseApi.matrix.list.mockResolvedValue([]);
    mockedUserbaseApi.dataQuality.summary.mockResolvedValue({ incomplete_profiles: 0 });
    
    mockedTrainingApi.listResidentTrainingRecords.mockResolvedValue([]);
    mockedTrainingApi.listRotations.mockResolvedValue([]);
    mockedTrainingApi.getUTRMCOperationalDashboard.mockResolvedValue({
      cross_department_overview: { active_residents: 0 },
      pending_synopsis_reviews: 0,
      pending_thesis_reviews: 0,
      pending_rotation_completion_verifications: 0,
    });
    mockedTrainingApi.getSynopsisReviewQueue.mockResolvedValue({ count: 0, results: [] });
    mockedTrainingApi.getThesisReviewQueue.mockResolvedValue({ count: 0, results: [] });
    mockedTrainingApi.listRotationCompletions.mockResolvedValue({ count: 0, results: [] });
  });

  it('renders the UTRMC dashboard', async () => {
    render(<UTRMCOverviewPage />);
    
    // Wait for "Loading..." to disappear and header to be visible
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    }, { timeout: 4000 });
    
    expect(screen.getByText('UTRMC Dashboard')).toBeInTheDocument();
    expect(screen.getAllByRole('link', { name: /open onboarding tools/i }).length).toBeGreaterThan(0);
    expect(screen.getByRole('heading', { name: /Rotation Operations/i })).toBeInTheDocument();
  });
});
