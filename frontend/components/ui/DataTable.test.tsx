import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DataTable from './DataTable';

describe('DataTable', () => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'date', label: 'Date' },
  ];
  const data = [
    { id: 1, name: 'Item 1', date: '2026-04-23' },
    { id: 2, name: 'Item 2', date: '2026-04-24' },
  ];

  it('renders data correctly', () => {
    render(<DataTable columns={columns} data={data} />);
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
    // Date formatting check
    expect(screen.getByText('Apr 23, 2026')).toBeInTheDocument();
  });

  it('renders empty message when no data', () => {
    render(<DataTable columns={columns} data={[]} emptyMessage="Nothing found" />);
    expect(screen.getByText('Nothing found')).toBeInTheDocument();
  });

  it('handles row click', () => {
    const onRowClick = jest.fn();
    render(<DataTable columns={columns} data={data} onRowClick={onRowClick} />);
    
    fireEvent.click(screen.getByText('Item 1'));
    expect(onRowClick).toHaveBeenCalledWith(data[0]);
  });

  it('uses custom render function', () => {
    const customColumns = [
      { 
        key: 'action', 
        label: 'Action', 
        render: (item: { id: number }) => <button>Delete {item.id}</button> 
      },
    ];
    render(<DataTable columns={customColumns} data={data} />);
    expect(screen.getByRole('button', { name: /Delete 1/i })).toBeInTheDocument();
  });
});
