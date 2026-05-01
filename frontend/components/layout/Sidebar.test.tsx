import React, { ReactNode } from 'react';
import { render, screen } from '@testing-library/react';
import Sidebar from './Sidebar';

jest.mock('next/navigation', () => ({
  usePathname: () => '/dashboard',
}));

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ href, children }: { href: string; children: ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));

describe('Sidebar', () => {
  const defaultProps = {
    role: 'resident',
    userName: 'Test Resident',
    onLogout: jest.fn(),
  };

  it('renders common items for all roles', () => {
    render(<Sidebar {...defaultProps} />);
    expect(screen.getByText('My Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Test Resident')).toBeInTheDocument();
    expect(screen.getByText('Sign out')).toBeInTheDocument();
  });

  it('renders resident specific items', () => {
    render(<Sidebar {...defaultProps} />);
    expect(screen.getByText('My Schedule')).toBeInTheDocument();
    expect(screen.getByText('Logbook')).toBeInTheDocument();
  });

  it('renders supervisor specific items', () => {
    render(<Sidebar {...defaultProps} role="supervisor" />);
    expect(screen.getByText('Overview')).toBeInTheDocument();
    expect(screen.getByText('My Residents')).toBeInTheDocument();
  });

  it('renders utrmc admin specific items', () => {
    render(<Sidebar {...defaultProps} role="utrmc_admin" />);
    expect(screen.getByText('Hospitals')).toBeInTheDocument();
    expect(screen.getByText('Programmes')).toBeInTheDocument();
    expect(screen.getByText('Eligibility Monitor')).toBeInTheDocument();
  });
});
