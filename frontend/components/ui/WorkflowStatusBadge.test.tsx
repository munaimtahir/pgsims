import React from 'react';
import { render, screen } from '@testing-library/react';
import WorkflowStatusBadge from './WorkflowStatusBadge';

describe('WorkflowStatusBadge', () => {
  it('renders status label', () => {
    render(<WorkflowStatusBadge status="APPROVED" />);
    expect(screen.getByText('APPROVED')).toBeInTheDocument();
  });

  it('renders custom label if provided', () => {
    render(<WorkflowStatusBadge status="APPROVED" label="Completed" />);
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('renders placeholder for null status', () => {
    render(<WorkflowStatusBadge status={null} />);
    expect(screen.getByText('—')).toBeInTheDocument();
  });

  it('normalizes status string', () => {
    render(<WorkflowStatusBadge status="under-review" />);
    expect(screen.getByText('UNDER REVIEW')).toBeInTheDocument();
  });

  it('applies correct status colors', () => {
    const { container } = render(<WorkflowStatusBadge status="ELIGIBLE" />);
    expect(container.firstChild).toHaveClass('bg-green-100');
  });

  it('applies default colors for unknown status', () => {
    const { container } = render(<WorkflowStatusBadge status="UNKNOWN_XYZ" />);
    expect(container.firstChild).toHaveClass('bg-slate-100');
  });
});
