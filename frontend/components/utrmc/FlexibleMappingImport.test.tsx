import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import FlexibleMappingImport from './FlexibleMappingImport';
import apiClient from '@/lib/api/client';

jest.mock('@/lib/api/client', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
    post: jest.fn(),
    delete: jest.fn(),
  },
}));

describe('FlexibleMappingImport', () => {
  const mockSchemas = {
    residents: {
      label: 'Residents',
      fields: [
        { name: 'email', label: 'Email', required: true, type: 'email' },
        { name: 'full_name', label: 'Full Name', required: true, type: 'string' },
        { name: 'phone_number', label: 'Phone Number', required: false, type: 'string' },
      ],
    },
    supervisors: {
      label: 'Supervisors',
      fields: [
        { name: 'email', label: 'Email', required: true, type: 'email' },
        { name: 'full_name', label: 'Full Name', required: true, type: 'string' },
      ],
    },
  };

  const mockPresets = {
    results: [
      {
        id: 10,
        name: 'Resident Google Form',
        entity: 'residents',
        mapping: { email: 'CustomEmail', full_name: 'CustomName' },
        created_at: '2026-05-30T00:00:00Z',
        last_used_at: null,
      },
    ],
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (apiClient.get as jest.Mock).mockImplementation((url: string) => {
      if (url.includes('/api/bulk/flexible/schemas/')) {
        return Promise.resolve({ data: mockSchemas });
      }
      if (url.includes('/api/bulk/flexible/presets/')) {
        return Promise.resolve({ data: mockPresets });
      }
      return Promise.reject(new Error('Unknown url'));
    });
    (apiClient.post as jest.Mock).mockImplementation((url: string) => {
      if (url.includes('/api/bulk/flexible/detect-headers/')) {
        return Promise.resolve({
          data: {
            headers: ['CustomEmail', 'CustomName', 'UnrelatedCol'],
            sample_rows: [{ CustomEmail: 'trainee@example.com', CustomName: 'Trainee A' }],
            total_rows: 15,
            sheets: [],
          },
        });
      }
      if (url.includes('/api/bulk/flexible/validate-mapping/')) {
        return Promise.resolve({
          data: {
            ready: true,
            missing_required: [],
            duplicate_mappings: {},
            required_fields: ['email', 'full_name'],
            optional_fields: ['phone_number'],
          },
        });
      }
      return Promise.reject(new Error('Unknown url'));
    });
  });

  it('renders target selector and upload dropzone on load', async () => {
    render(<FlexibleMappingImport />);
    
    await waitFor(() => {
      expect(screen.getByText('Select Import Target')).toBeInTheDocument();
    });
    
    expect(screen.getByRole('combobox')).toHaveValue('residents');
    expect(screen.getByText('Click to upload or drag & drop CSV/Excel file')).toBeInTheDocument();
  });

  it('handles target entity selection changes', async () => {
    render(<FlexibleMappingImport />);
    
    await waitFor(() => {
      expect(screen.getByRole('combobox')).toHaveValue('residents');
    });

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'supervisors' } });
    
    await waitFor(() => {
      expect(apiClient.get).toHaveBeenLastCalledWith(expect.stringContaining('/api/bulk/flexible/presets/?entity=supervisors'));
    });
  });

  it('handles file upload and header detection with auto-mapping', async () => {
    const { container } = render(<FlexibleMappingImport />);
    
    await waitFor(() => {
      expect(screen.getByText('Select Import Target')).toBeInTheDocument();
    });

    const file = new File(['CustomEmail,CustomName,UnrelatedCol\ntrainee@example.com,Trainee A,XYZ'], 'custom_trainees.csv', { type: 'text/csv' });
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/api/bulk/flexible/detect-headers/', expect.any(FormData), expect.any(Object));
      expect(screen.getByText(/File "custom_trainees.csv" successfully parsed/i)).toBeInTheDocument();
    });

    // Advance to Step 2: Mapping
    fireEvent.click(screen.getByRole('button', { name: /Continue to Mapping/i }));

    // Verify mapping headers table is displayed
    expect(screen.getByText('PGSIMS Field')).toBeInTheDocument();
    expect(screen.getByText('Source Column from Uploaded File')).toBeInTheDocument();
  });
});
