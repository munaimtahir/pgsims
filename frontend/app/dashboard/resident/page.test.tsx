import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import ResidentHomePage from './page';
import { trainingApi } from '@/lib/api/training';

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

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    getResidentSummary: jest.fn(),
    getResidentOperationalDashboard: jest.fn(),
  },
}));

const mockedTrainingApi = trainingApi as unknown as {
  getResidentSummary: jest.Mock;
  getResidentOperationalDashboard: jest.Mock;
};

describe('ResidentHomePage', () => {
  beforeEach(() => {
    mockedTrainingApi.getResidentSummary.mockResolvedValue({
      training_record: {
        id: 17,
        program_name: 'Internal Medicine',
        current_month_index: 8,
        degree_type: 'fcps',
        start_date: '2025-01-01',
      },
      rotation: {
        current: null,
        next: null,
      },
      research: {
        status: 'DRAFT',
        supervisor_name: null,
      },
      thesis: {
        status: 'DRAFT',
        submitted_at: null,
      },
      workshops: {
        total_completed: 0,
        required_for_imm: 2,
        required_for_final: 4,
      },
      eligibility: {
        IMM: { status: 'NOT_READY', reasons: [] },
        FINAL: { status: 'NOT_READY', reasons: [] },
      },
      leaves: { pending_count: 0 },
      postings: { pending_count: 0 },
    } as never);
    mockedTrainingApi.getResidentOperationalDashboard.mockResolvedValue(null as never);
  });

  it('keeps the dashboard as a summary surface instead of a launcher for inactive subflows', async () => {
    render(<ResidentHomePage />);

    await waitFor(() => expect(screen.getByText('My Training Dashboard')).toBeInTheDocument());

    expect(screen.getByRole('link', { name: 'View Schedule' })).toHaveAttribute(
      'href',
      '/dashboard/resident/schedule'
    );
    expect(screen.getByRole('link', { name: 'Logbook & Readiness' })).toHaveAttribute(
      'href',
      '/dashboard/resident/progress'
    );

    expect(screen.queryByRole('link', { name: /Update Research/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('link', { name: /Upload Workshop/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('link', { name: /Apply for Leave/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('link', { name: /Manage/i })).not.toBeInTheDocument();
  });

  it('shows a calm empty state when no resident training record is linked', async () => {
    mockedTrainingApi.getResidentSummary.mockResolvedValueOnce({
      training_record: null,
      rotation: { current: null, next: null },
      research: { status: null, supervisor_name: null, synopsis_uploaded: false, university_submitted: false },
      thesis: { status: 'DRAFT', submitted_at: null },
      workshops: { total_completed: 0, required_for_imm: 0, required_for_final: 0, completed_list: [] },
      eligibility: {
        IMM: { status: null, reasons: [] },
        FINAL: { status: null, reasons: [] },
      },
      leaves: { active_count: 0, pending_count: 0, list: [] },
      postings: { active_count: 0, pending_count: 0 },
    } as never);

    render(<ResidentHomePage />);

    await waitFor(() => {
      expect(screen.getByText('No active resident training record is linked yet.')).toBeInTheDocument();
    });
    expect(screen.getByRole('link', { name: 'View Schedule' })).toHaveAttribute(
      'href',
      '/dashboard/resident/schedule'
    );
  });
});
