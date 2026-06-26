import React from 'react';
import { render, screen } from '@testing-library/react';
import LoginSheetPage from './page';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

jest.mock('@/components/onboarding/LoginSheetPanel', () => ({
  __esModule: true,
  default: () => <div>Login Sheet Panel</div>,
}));

describe('LoginSheetPage', () => {
  it('renders the login sheet panel', () => {
    render(<LoginSheetPage />);

    expect(screen.getByText('Login Sheet Panel')).toBeInTheDocument();
  });
});
