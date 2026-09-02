import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import TrainingRecordsPage from './page';
import { academicsApi } from '@/lib/api/academics';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ href, children }: { href: string; children: ReactNode }) => <a href={href}>{children}</a>,
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: () => ({ user: { role: 'ADMIN' } }),
}));

jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    listTrainingRecords: jest.fn(),
    getOptions: jest.fn(),
    createTrainingRecord: jest.fn(),
  },
}));

const mockedAcademicsApi = academicsApi as unknown as {
  listTrainingRecords: jest.Mock;
  getOptions: jest.Mock;
  createTrainingRecord: jest.Mock;
};

describe('TrainingRecordsPage', () => {
  beforeEach(() => {
    mockedAcademicsApi.listTrainingRecords.mockResolvedValue([
      { id: 1, resident_name: 'Dr Resident', program_name: 'FCPS Medicine', academic_session_name: 'Session 2026', training_year: 1, status: 'ACTIVE' },
    ]);
    mockedAcademicsApi.getOptions.mockResolvedValue({
      residents: [],
      supervisors: [],
      programs: [],
      academic_sessions: [],
      training_sites: [],
      departments: [],
      periods: [],
    });
  });

  it('renders the training records route', async () => {
    render(<TrainingRecordsPage />);
    await waitFor(() => expect(screen.getByText('Training Records')).toBeInTheDocument());
    expect(screen.getByText('Create Training Record')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open' })).toHaveAttribute('href', '/academics/training-records/1');
  });
});
