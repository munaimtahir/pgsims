import React from 'react';
import { render } from '@testing-library/react';
import LoadingSkeleton, { TableSkeleton, CardSkeleton } from './LoadingSkeleton';

describe('LoadingSkeleton components', () => {
  it('renders LoadingSkeleton with default lines', () => {
    const { container } = render(<LoadingSkeleton />);
    expect(container.querySelectorAll('.h-4').length).toBe(3);
  });

  it('renders TableSkeleton with specified rows and cols', () => {
    const { container } = render(<TableSkeleton rows={3} cols={2} />);
    // 3 rows * 2 cols + 1 header * 2 cols = 8 cells total
    expect(container.querySelectorAll('.flex-1').length).toBe(8);
  });

  it('renders CardSkeleton', () => {
    const { container } = render(<CardSkeleton />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
    expect(container.querySelectorAll('.h-4').length).toBe(3);
  });
});
