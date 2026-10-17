import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import SupervisionHomePage from './page';
import supervisionApi from '@/lib/api/supervision';

jest.mock('@/components/auth/ProtectedRoute', () => ({ __esModule: true, default: ({ children }: { children: ReactNode }) => <>{children}</> }));
jest.mock('@/lib/api/supervision', () => ({ __esModule: true, default: { listAssignments: jest.fn(), getSupervisionDataQuality: jest.fn() } }));
const api = supervisionApi as unknown as Record<string, jest.Mock>;

describe('SupervisionHomePage', () => {
  beforeEach(() => jest.clearAllMocks());

  it('summarizes active primary and co-supervisor assignments with data issues', async () => {
    api.listAssignments.mockResolvedValue([
      { id: 1, status: 'ACTIVE', assignment_type: 'PRIMARY' },
      { id: 2, status: 'ACTIVE', assignment_type: 'CO_SUPERVISOR' },
      { id: 3, status: 'ENDED', assignment_type: 'PRIMARY' },
    ]);
    api.getSupervisionDataQuality.mockResolvedValue({ missing_supervisor: [{ id: 5 }], duplicate: [{ id: 6 }, { id: 7 }] });
    render(<SupervisionHomePage />);
    expect(screen.getByText('Loading supervision overview...')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('3')).toBeInTheDocument());
    expect(screen.getByText('2 Active')).toBeInTheDocument();
    expect(screen.getByText('Add Assignment')).toHaveAttribute('href', '/supervision/assignments/new');
  });

  it('continues with empty data quality when that optional request fails', async () => {
    api.listAssignments.mockResolvedValue([]);
    api.getSupervisionDataQuality.mockRejectedValue(new Error('unavailable'));
    render(<SupervisionHomePage />);
    await waitFor(() => expect(screen.queryByText('Loading supervision overview...')).not.toBeInTheDocument());
    expect(screen.getByText('0 Active')).toBeInTheDocument();
  });

  it('reports required assignment loading failures', async () => {
    api.listAssignments.mockRejectedValue(new Error('offline'));
    api.getSupervisionDataQuality.mockResolvedValue({});
    render(<SupervisionHomePage />);
    expect(await screen.findByText('Unable to load supervision overview.')).toBeInTheDocument();
  });
});
