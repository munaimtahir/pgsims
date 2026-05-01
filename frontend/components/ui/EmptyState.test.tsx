import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EmptyState from './EmptyState';

describe('EmptyState', () => {
  it('renders title and description', () => {
    render(<EmptyState title="No data" description="Try searching for something else" />);
    expect(screen.getByText('No data')).toBeInTheDocument();
    expect(screen.getByText('Try searching for something else')).toBeInTheDocument();
  });

  it('renders action button and handles click', () => {
    const onClick = jest.fn();
    render(<EmptyState title="No data" action={{ label: 'Add new', onClick }} />);
    
    const button = screen.getByRole('button', { name: /Add new/i });
    fireEvent.click(button);
    
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
