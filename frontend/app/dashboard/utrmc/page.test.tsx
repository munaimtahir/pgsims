import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import UTRMCOverviewPage from './page';
import { trainingApi } from '@/lib/api/training';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    listResidentTrainingRecords: jest.fn(),
    getUTRMCOperationalDashboard: jest.fn(),
  },
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    hospitals: { list: jest.fn() },
    departments: { list: jest.fn() },
    users: { list: jest.fn() },
    matrix: { list: jest.fn() },
    hodAssignments: { list: jest.fn() },
    dataQuality: { summary: jest.fn() },
  },
}));

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

const mockedTrainingApi = trainingApi as unknown as {
  listResidentTrainingRecords: jest.Mock;
  getUTRMCOperationalDashboard: jest.Mock;
};
const mockedUserbaseApi = userbaseApi as unknown as {
  departments: { list: jest.Mock };
  users: { list: jest.Mock };
  matrix: { list: jest.Mock };
  hodAssignments: { list: jest.Mock };
  dataQuality: { summary: jest.Mock };
};

describe('UTRMCOverviewPage', () => {
  beforeEach(() => {
    (useAuthStore as unknown as jest.Mock).mockReturnValue({ user: { role: 'admin' } });
    mockedUserbaseApi.departments.list.mockResolvedValue([
      { id: 1, name: 'Medicine', code: 'MED', active: true, created_at: '2026-01-01' },
    ]);
    mockedUserbaseApi.users.list.mockResolvedValue([
      { id: 1, username: 'resident', first_name: 'Resident', last_name: 'One', role: 'resident', is_active: true },
    ]);
    mockedUserbaseApi.matrix.list.mockResolvedValue([
      { id: 1, hospital: { id: 1, name: 'FMU', active: true }, department: { id: 1, name: 'Medicine', code: 'MED', active: true }, active: true, created_at: '2026-01-01' },
    ]);
    mockedUserbaseApi.hodAssignments.list.mockResolvedValue([
      { id: 1, department: { id: 1, name: 'Medicine', code: 'MED' }, hod_user: { id: 2, username: 'hod', full_name: 'Dr HOD' }, start_date: '2026-01-01', active: true },
    ]);
    mockedUserbaseApi.dataQuality.summary.mockResolvedValue({ incomplete_profiles: 0 });
    mockedTrainingApi.listResidentTrainingRecords.mockResolvedValue([
      {
        id: 1,
        resident_user: 1,
        resident_name: 'Resident One',
        program: 3,
        program_name: 'FCPS Medicine',
        program_code: 'FCPS-MED',
        start_date: '2026-01-01',
        expected_end_date: null,
        current_level: 'y1',
        active: true,
        created_by: 1,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      },
    ]);
    mockedTrainingApi.getUTRMCOperationalDashboard.mockResolvedValue({
      cross_department_overview: { active_residents: 1, program_count: 1, pending_logbook_reviews: 0 },
      pending_synopsis_reviews: 2,
      pending_thesis_reviews: 1,
      pending_rotation_completion_verifications: 3,
      resident_milestone_readiness: [],
      readiness_summary: { fully_ready_count: 0, total_rows: 0 },
    });
  });

  it('renders the monitoring dashboard with quick links and summary cards', async () => {
    render(<UTRMCOverviewPage />);

    await waitFor(() => {
      expect(screen.getByText('UTRMC Dashboard')).toBeInTheDocument();
    });

    expect(screen.getByText('Active Residents')).toBeInTheDocument();
    expect(screen.getByText('Residents Without Programme')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /resident programme assignment/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /resident onboarding/i })).toBeInTheDocument();
    expect(screen.queryByText('Bulk Setup & Import/Export')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /create rotation/i })).not.toBeInTheDocument();
  });
});
