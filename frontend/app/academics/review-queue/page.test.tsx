import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import ReviewQueuePage from './page';
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
    listReviewQueue: jest.fn(),
    getOptions: jest.fn(),
    listTrainingRecords: jest.fn(),
    createReviewQueueItem: jest.fn(),
    updateReviewQueueItem: jest.fn(),
  },
}));

const mockedAcademicsApi = academicsApi as unknown as {
  listReviewQueue: jest.Mock;
  getOptions: jest.Mock;
  listTrainingRecords: jest.Mock;
  createReviewQueueItem: jest.Mock;
  updateReviewQueueItem: jest.Mock;
};

describe('ReviewQueuePage', () => {
  beforeEach(() => {
    mockedAcademicsApi.listReviewQueue.mockResolvedValue([
      { id: 7, resident: 1, resident_name: 'Dr Resident', supervisor: 2, supervisor_name: 'Prof Supervisor', training_record: 11, queue_type: 'TRAINING_RECORD_REVIEW', status: 'PENDING', due_date: null, notes: '' },
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
    mockedAcademicsApi.listTrainingRecords.mockResolvedValue([]);
  });

  it('renders the academic review queue route', async () => {
    render(<ReviewQueuePage />);
    await waitFor(() => expect(screen.getByText('Academic Review Queue')).toBeInTheDocument());
    expect(screen.getByText('Dr Resident')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'View Resident' })).toHaveAttribute('href', '/residents/1');
  });
});
