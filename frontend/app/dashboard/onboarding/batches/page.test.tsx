import React from 'react';
import { render, screen } from '@testing-library/react';
import ImportedBatchesPage from './page';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

jest.mock('@/components/onboarding/ImportedBatchesPanel', () => ({
  __esModule: true,
  default: () => <div>Imported Batches Panel</div>,
}));

describe('ImportedBatchesPage', () => {
  it('renders the imported batches panel', () => {
    render(<ImportedBatchesPage />);

    expect(screen.getByText('Imported Batches Panel')).toBeInTheDocument();
  });
});
