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
    role: 'RESIDENT',
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
    expect(screen.getByText('My Training')).toBeInTheDocument();
    expect(screen.getByText('My Supervisor')).toBeInTheDocument();
    expect(screen.getByText('My Academic Summary')).toBeInTheDocument();
  });

  it('renders supervisor specific items', () => {
    render(<Sidebar {...defaultProps} role="SUPERVISOR" />);
    expect(screen.getByText('My Residents')).toBeInTheDocument();
    expect(screen.getByText('Supervision Ledger')).toBeInTheDocument();
    expect(screen.getByText('Academic Review Queue')).toBeInTheDocument();
  });

  it('renders utrmc admin specific items', () => {
    render(<Sidebar {...defaultProps} role="ADMIN" />);
    expect(screen.getByText('Residents')).toBeInTheDocument();
    expect(screen.getByText('Supervisors')).toBeInTheDocument();
    expect(screen.getByText('Masters')).toBeInTheDocument();
  });
});
