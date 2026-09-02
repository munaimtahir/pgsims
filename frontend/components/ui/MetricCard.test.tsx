import React from 'react';
import { render, screen } from '@testing-library/react';
import MetricCard from './MetricCard';

describe('MetricCard', () => {
  it('renders label and value', () => {
    render(<MetricCard label="Total PGs" value={42} />);
    expect(screen.getByText('Total PGs')).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
  });

  it('renders hint if provided', () => {
    render(<MetricCard label="Test" value="10" hint="Important hint" />);
    expect(screen.getByText('Important hint')).toBeInTheDocument();
  });

  it('applies correct tone class', () => {
    const { container } = render(<MetricCard label="Test" value="10" tone="success" />);
    expect(container.firstChild).toHaveClass('border-green-200');
  });
});
