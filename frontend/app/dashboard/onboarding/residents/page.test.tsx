import React from 'react';
import { render, screen } from '@testing-library/react';
import ResidentOnboardingPage from './page';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

jest.mock('@/components/onboarding/ResidentOnboardingWizard', () => ({
  __esModule: true,
  default: () => <div>Resident Onboarding Wizard</div>,
}));

describe('ResidentOnboardingPage', () => {
  it('renders the resident onboarding wizard', () => {
    render(<ResidentOnboardingPage />);

    expect(screen.getByText('Resident Onboarding Wizard')).toBeInTheDocument();
  });
});
