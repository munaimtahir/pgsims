import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import ResidentHomePage from './page';
import { academicsApi } from '@/lib/api/academics';

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ href, children, ...props }: { href: string; children: ReactNode }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    getMyResidentSummary: jest.fn(),
  },
}));

const mockedAcademicsApi = academicsApi as unknown as {
  getMyResidentSummary: jest.Mock;
};

describe('ResidentHomePage', () => {
  beforeEach(() => {
    mockedAcademicsApi.getMyResidentSummary.mockResolvedValue({
      resident: {
        id: 7,
        name: 'Dr Resident',
        username: 'resident001',
        department: 'Medicine',
        program: 'FCPS Medicine',
        academic_session: 'Session 2026',
      },
      training_record: {
        id: 17,
        status: 'ACTIVE',
        training_year: 1,
        start_date: '2026-07-01',
        expected_end_date: '2027-06-30',
      },
      supervision: {
        primary_supervisor: {
          supervisor: {
            name: 'Prof Supervisor',
            designation: 'Professor',
            department: 'Medicine',
            start_date: '2026-07-01',
            email: 'sup@example.com',
            phone: '03001234567',
          },
        },
        co_supervisors: [{ name: 'Dr Co Supervisor' }],
      },
      review_queue: {
        pending_count: 2,
        items: [],
      },
      readiness: {
        has_active_training_record: true,
        has_primary_supervisor: true,
        missing_items: [],
      },
    } as never);
  });

  it('renders the canonical resident dashboard summary', async () => {
    render(<ResidentHomePage />);

    await waitFor(() => expect(screen.getByText('Resident Dashboard')).toBeInTheDocument());
    expect(screen.getByText('My Training')).toBeInTheDocument();
    expect(screen.getByText('My Supervisor')).toBeInTheDocument();
    expect(screen.getByText('My Academic Summary')).toBeInTheDocument();
    expect(screen.getByText('Prof Supervisor')).toBeInTheDocument();
    expect(screen.queryByRole('link', { name: /View Schedule/i })).not.toBeInTheDocument();
  });
});
