import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import SupervisorHomePage from './page';
import { academicsApi } from '@/lib/api/academics';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    getMySupervisorSummary: jest.fn(),
  },
}));

const mockedAcademicsApi = academicsApi as unknown as {
  getMySupervisorSummary: jest.Mock;
};

describe('SupervisorHomePage', () => {
  beforeEach(() => {
    mockedAcademicsApi.getMySupervisorSummary.mockResolvedValue({
      supervisor: {
        id: 11,
        name: 'Prof Supervisor',
      },
      summary: {
        assigned_residents: 3,
        active_training_records: 2,
        residents_missing_training_records: 1,
        pending_review_queue_items: 4,
      },
      assigned_residents: [
        {
          resident_id: 101,
          name: 'Dr Resident',
          program: 'FCPS Medicine',
          training_year: 1,
          status: 'ACTIVE',
        },
      ],
      review_queue: {
        pending_count: 4,
        items: [],
      },
    } as never);
  });

  it('renders the canonical supervisor dashboard summary', async () => {
    render(<SupervisorHomePage />);

    await waitFor(() => expect(screen.getByText('Supervisor Dashboard')).toBeInTheDocument());
    expect(screen.getByText('My Residents')).toBeInTheDocument();
    expect(screen.getByText('Academic Review Queue')).toBeInTheDocument();
    expect(screen.getByText('Dr Resident')).toBeInTheDocument();
  });
});
