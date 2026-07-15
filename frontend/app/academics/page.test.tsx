import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

import AcademicsHomePage from './page';
import { academicsApi } from '@/lib/api/academics';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ href, children }: { href: string; children: ReactNode }) => <a href={href}>{children}</a>,
}));

jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    getOverview: jest.fn(),
  },
}));

const mockedAcademicsApi = academicsApi as unknown as {
  getOverview: jest.Mock;
};

describe('AcademicsHomePage', () => {
  beforeEach(() => {
    mockedAcademicsApi.getOverview.mockResolvedValue({
      cards: {
        active_training_records: 2,
        residents_without_training_record: 1,
      },
    });
  });

  it('renders the academics dashboard route family entry point', async () => {
    render(<AcademicsHomePage />);
    await waitFor(() => expect(screen.getByText('Academic Workflow Foundation')).toBeInTheDocument());
    expect(screen.getByRole('link', { name: 'Training Records' })).toHaveAttribute('href', '/academics/training-records');
    expect(screen.getByRole('link', { name: 'Review Queue' })).toHaveAttribute('href', '/academics/review-queue');
  });
});
