import type { ReactNode } from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import ResidentSchedulePage from './page';
import { trainingApi } from '@/lib/api/training';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('@/lib/api/training', () => ({
  trainingApi: {
    getResidentSummary: jest.fn(),
    listMyLeaves: jest.fn(),
    listMyRotations: jest.fn(),
    createLeave: jest.fn(),
    submitLeave: jest.fn(),
  },
}));

const mockedTrainingApi = trainingApi as unknown as {
  getResidentSummary: jest.Mock;
  listMyLeaves: jest.Mock;
  listMyRotations: jest.Mock;
  createLeave: jest.Mock;
  submitLeave: jest.Mock;
};

describe('ResidentSchedulePage', () => {
  beforeEach(() => {
    mockedTrainingApi.getResidentSummary.mockResolvedValue({
      training_record: { 
        id: 1, 
        program_name: 'Med', 
        start_date: '2026-01-01', 
        current_month_index: 4 
      },
    });
    mockedTrainingApi.listMyLeaves.mockResolvedValue({ results: [] });
    mockedTrainingApi.listMyRotations.mockResolvedValue({ results: [] });
  });

  it('renders and allows leave draft creation', async () => {
    render(<ResidentSchedulePage />);
    
    // Wait for spinner to disappear
    await waitFor(() => expect(screen.queryByRole('status')).not.toBeInTheDocument(), { timeout: 4000 });
    // Or just wait for some text
    await waitFor(() => expect(screen.getByText('Request Leave')).toBeInTheDocument());
    
    expect(screen.getByText('My Schedule')).toBeInTheDocument();
    
    // Fill form
    fireEvent.change(screen.getByLabelText(/Start Date/i), { target: { value: '2026-05-01' } });
    fireEvent.change(screen.getByLabelText(/End Date/i), { target: { value: '2026-05-05' } });
    fireEvent.change(screen.getByPlaceholderText(/Reason for leave/i), { target: { value: 'Vacation' } });
    
    mockedTrainingApi.createLeave.mockResolvedValue({});
    fireEvent.click(screen.getByText('Save Draft'));
    
    await waitFor(() => {
      expect(mockedTrainingApi.createLeave).toHaveBeenCalled();
    });
  });

  it('handles leave submission', async () => {
    mockedTrainingApi.listMyLeaves.mockResolvedValue({
      results: [
        { id: 10, leave_type: 'annual', start_date: '2026-06-01', end_date: '2026-06-05', status: 'DRAFT' }
      ]
    });
    
    render(<ResidentSchedulePage />);
    await waitFor(() => expect(screen.getByText('Submit for Review')).toBeInTheDocument());
    
    const submitBtn = screen.getByText('Submit for Review');
    mockedTrainingApi.submitLeave.mockResolvedValue({});
    fireEvent.click(submitBtn);
    
    await waitFor(() => {
      expect(mockedTrainingApi.submitLeave).toHaveBeenCalledWith(10);
    });
  });
});
