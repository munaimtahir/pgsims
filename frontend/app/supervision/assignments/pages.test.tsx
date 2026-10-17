import type { ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import SupervisionAssignmentsPage from './page';
import NewSupervisionAssignmentPage from './new/page';
import SupervisionDataQualityPage from '../data-quality/page';
import supervisionApi from '@/lib/api/supervision';

jest.mock('@/components/auth/ProtectedRoute', () => ({ __esModule: true, default: ({ children }: { children: ReactNode }) => <>{children}</> }));
jest.mock('@/lib/api/supervision', () => ({ __esModule: true, default: { listAssignments: jest.fn(), getSupervisionDataQuality: jest.fn(), getSupervisionOptions: jest.fn(), createAssignment: jest.fn() } }));
const api = supervisionApi as unknown as Record<string, jest.Mock>;

describe('supervision assignment pages', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    api.listAssignments.mockResolvedValue([]);
    api.getSupervisionDataQuality.mockResolvedValue({});
    api.getSupervisionOptions.mockResolvedValue({ residents: [], supervisors: [] });
  });

  it('renders assignment details, links, and missing start dates', async () => {
    api.listAssignments.mockResolvedValue([{ id: 12, resident: { name: 'Resident One' }, supervisor: { name: 'Dr One' }, assignment_type: 'PRIMARY', status: 'ACTIVE', start_date: null }]);
    render(<SupervisionAssignmentsPage />);
    expect(screen.getByText('Loading assignments...')).toBeInTheDocument();
    expect(await screen.findByText('Resident One')).toBeInTheDocument();
    expect(screen.getByText('Dr One')).toBeInTheDocument();
    expect(screen.getByText('—')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open' })).toHaveAttribute('href', '/supervision/assignments/12');
  });

  it('displays an assignment retrieval failure', async () => {
    api.listAssignments.mockRejectedValue(new Error('offline'));
    render(<SupervisionAssignmentsPage />);
    expect(await screen.findByText('Unable to load assignments.')).toBeInTheDocument();
  });

  it('counts and labels every data-quality category', async () => {
    api.getSupervisionDataQuality.mockResolvedValue({ residents_no_primary: [{ id: 1 }], hospital_mismatch: [{ id: 2 }], department_mismatch: [{ id: 3 }, { id: 4 }] });
    render(<SupervisionDataQualityPage />);
    await waitFor(() => expect(screen.getByText('residents no primary')).toBeInTheDocument());
    expect(screen.getByText('hospital mismatch')).toBeInTheDocument();
    expect(screen.getByText('department mismatch')).toBeInTheDocument();
    expect(screen.getByText('2 record(s)')).toBeInTheDocument();
  });

  it('displays a data-quality retrieval failure', async () => {
    api.getSupervisionDataQuality.mockRejectedValue(new Error('offline'));
    render(<SupervisionDataQualityPage />);
    expect(await screen.findByText('Unable to load supervision data quality.')).toBeInTheDocument();
  });

  it('creates a selected assignment and resets the form', async () => {
    api.getSupervisionOptions.mockResolvedValue({ residents: [{ id: 1, name: 'Resident One', username: 'pgr001' }], supervisors: [{ id: 2, name: 'Dr One', username: 'sup001' }] });
    api.createAssignment.mockResolvedValue({ id: 44 });
    render(<NewSupervisionAssignmentPage />);
    await screen.findByRole('option', { name: 'Resident One (pgr001)' });
    fireEvent.change(screen.getByLabelText('Resident'), { target: { value: '1' } });
    fireEvent.change(screen.getByLabelText('Supervisor'), { target: { value: '2' } });
    fireEvent.change(screen.getByLabelText('Assignment Type'), { target: { value: 'CO_SUPERVISOR' } });
    fireEvent.change(screen.getByLabelText('Start Date'), { target: { value: '2026-09-01' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create Assignment' }));
    await waitFor(() => expect(api.createAssignment).toHaveBeenCalledWith({ resident_id: 1, supervisor_id: 2, assignment_type: 'CO_SUPERVISOR', start_date: '2026-09-01' }));
    expect(await screen.findByText('Created assignment #44.')).toBeInTheDocument();
    expect(screen.getByLabelText('Resident')).toHaveValue('');
  });

  it('reports option retrieval failures', async () => {
    api.getSupervisionOptions.mockRejectedValueOnce(new Error('options unavailable'));
    render(<NewSupervisionAssignmentPage />);
    expect(await screen.findByText('Unable to load supervision options.')).toBeInTheDocument();
  });
});
