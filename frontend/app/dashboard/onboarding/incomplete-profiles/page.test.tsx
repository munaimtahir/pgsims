import React from 'react';
import { render, screen } from '@testing-library/react';
import IncompleteProfilesPage from './page';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

jest.mock('@/components/onboarding/IncompleteProfilesPanel', () => ({
  __esModule: true,
  default: () => <div>Incomplete Profiles Panel</div>,
}));

describe('IncompleteProfilesPage', () => {
  it('renders the incomplete profiles panel', () => {
    render(<IncompleteProfilesPage />);

    expect(screen.getByText('Incomplete Profiles Panel')).toBeInTheDocument();
  });
});
