import React from 'react';
import { render, screen } from '@testing-library/react';
import OnboardingHomePage from './page';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

describe('OnboardingHomePage', () => {
  it('renders the onboarding hub links', () => {
    render(<OnboardingHomePage />);

    expect(screen.getByText('Onboarding')).toBeInTheDocument();
    expect(screen.getByText('Resident Onboarding')).toBeInTheDocument();
    expect(screen.getByText('Login Sheet')).toBeInTheDocument();
    expect(screen.getByText('Imported Batches')).toBeInTheDocument();
    expect(screen.getByText('Incomplete Profiles')).toBeInTheDocument();
  });
});
