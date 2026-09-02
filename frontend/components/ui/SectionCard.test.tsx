import React from 'react';
import { render, screen } from '@testing-library/react';
import SectionCard from './SectionCard';

describe('SectionCard', () => {
  it('renders title and children', () => {
    render(
      <SectionCard title="My Section">
        <p>Content goes here</p>
      </SectionCard>
    );
    expect(screen.getByText('My Section')).toBeInTheDocument();
    expect(screen.getByText('Content goes here')).toBeInTheDocument();
  });

  it('renders actions if provided', () => {
    render(
      <SectionCard title="Test" actions={<button>Edit</button>}>
        <p>Content</p>
      </SectionCard>
    );
    expect(screen.getByRole('button', { name: /Edit/i })).toBeInTheDocument();
  });
});
