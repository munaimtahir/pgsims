import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ImportExportPanel from './ImportExportPanel';
import apiClient from '@/lib/api/client';

jest.mock('@/lib/api/client', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
    post: jest.fn(),
  },
}));

describe('ImportExportPanel', () => {
  const defaultProps = {
    entity: 'residents',
    label: 'Residents',
    exportResource: 'residents',
    expectedColumns: [
      { name: 'username', required: true },
      { name: 'email', required: true },
    ],
    onSuccess: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly', () => {
    render(<ImportExportPanel {...defaultProps} />);
    expect(screen.getByText(/Import Residents/i)).toBeInTheDocument();
    expect(screen.getByText(/Download Template/i)).toBeInTheDocument();
    expect(screen.getByText(/username/i)).toBeInTheDocument();
  });

  it('handles template download', async () => {
    (apiClient.get as jest.Mock).mockResolvedValue({ data: new Blob() });
    
    // Mock window.URL.createObjectURL
    window.URL.createObjectURL = jest.fn().mockReturnValue('blob:url');
    window.URL.revokeObjectURL = jest.fn();

    render(<ImportExportPanel {...defaultProps} />);
    fireEvent.click(screen.getByText(/Download Template/i));

    await waitFor(() => {
      expect(apiClient.get).toHaveBeenCalledWith(expect.stringContaining('/api/bulk/templates/residents/'), expect.any(Object));
    });
  });

  it('handles file selection and dry run', async () => {
    const { container } = render(<ImportExportPanel {...defaultProps} />);
    
    const file = new File(['col1,col2'], 'test.csv', { type: 'text/csv' });
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });
    
    expect(screen.getByText('test.csv')).toBeInTheDocument();
    
    (apiClient.post as jest.Mock).mockResolvedValue({
      data: {
        status: 'completed',
        success_count: 5,
        failure_count: 0,
        details: { successes: [], failures: [] }
      }
    });

    fireEvent.click(screen.getByText(/Dry Run/i));

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith(expect.stringContaining('/api/bulk/import/residents/dry-run/'), expect.any(FormData), expect.any(Object));
      expect(screen.getByText(/Dry-run complete: 5 rows OK/i)).toBeInTheDocument();
    });
  });
});
