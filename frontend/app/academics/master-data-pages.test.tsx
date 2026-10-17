import type { ReactNode } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import AcademicPeriodsPage from './periods/page';
import RotationTemplatesPage from './rotation-templates/page';
import EvaluationTemplatesPage from './evaluation-templates/page';
import LogbookCategoriesPage from './logbook-categories/page';

import { academicsApi } from '@/lib/api/academics';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));
jest.mock('@/store/authStore', () => ({ useAuthStore: jest.fn() }));
jest.mock('@/lib/api/academics', () => ({
  academicsApi: {
    listPeriods: jest.fn(), createPeriod: jest.fn(), listRotationTemplates: jest.fn(),
    createRotationTemplate: jest.fn(), listEvaluationTemplates: jest.fn(),
    createEvaluationTemplate: jest.fn(), listLogbookCategories: jest.fn(),
    createLogbookCategory: jest.fn(), getOptions: jest.fn(),
  },
}));
const { useAuthStore } = jest.requireMock('@/store/authStore') as { useAuthStore: jest.Mock };
const api = academicsApi as unknown as Record<string, jest.Mock>;
const options = {
  residents: [], supervisors: [], programs: [{ id: 4, name: 'Medicine' }],
  academic_sessions: [{ id: 3, name: '2026–27' }], training_sites: [],
  departments: [{ id: 5, name: 'Internal Medicine' }], periods: [],
};

beforeEach(() => {
  jest.clearAllMocks();
  useAuthStore.mockReturnValue({ user: { role: 'ADMIN' } });
  api.getOptions.mockResolvedValue(options);
  api.listPeriods.mockResolvedValue([{ id: 1, name: 'Academic year', code: 'AY26', period_type: 'YEAR', start_date: '2026-01-01', end_date: '2026-12-31' }]);
  api.listRotationTemplates.mockResolvedValue([{ id: 2, name: 'Medicine ward', code: 'MW', program_name: 'Medicine', department_name: 'Internal Medicine' }]);
  api.createPeriod.mockResolvedValue({ id: 3 });
  api.createRotationTemplate.mockResolvedValue({ id: 4 });
  api.listEvaluationTemplates.mockResolvedValue([{ id: 5, name: 'Mini-CEX', code: 'MCEX', form_type: 'MINI_CEX', program_name: 'Medicine' }]);
  api.createEvaluationTemplate.mockResolvedValue({ id: 6 });
  api.listLogbookCategories.mockResolvedValue([{ id: 7, name: 'Procedures', code: 'PROC', category_type: 'PROCEDURE', program_name: 'Medicine' }]);
  api.createLogbookCategory.mockResolvedValue({ id: 8 });
});

describe('academic master-data pages', () => {
  it('lists and creates an academic period with normalized option values', async () => {
    render(<AcademicPeriodsPage />);
    await screen.findByText('Academic year');
    expect(screen.getByText('AY26 · YEAR · 2026-01-01 to 2026-12-31')).toBeInTheDocument();
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: 'Term one' } });
    fireEvent.change(inputs[1], { target: { value: 'TERM1' } });
    fireEvent.change(screen.getByDisplayValue('Academic Session'), { target: { value: '3' } });
    const dates = document.querySelectorAll<HTMLInputElement>('input[type="date"]');
    fireEvent.change(dates[0], { target: { value: '2026-01-01' } });
    fireEvent.change(dates[1], { target: { value: '2026-03-30' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create Period' }));
    await waitFor(() => expect(api.createPeriod).toHaveBeenCalledWith({ name: 'Term one', code: 'TERM1', academic_session: 3, start_date: '2026-01-01', end_date: '2026-03-30', period_type: 'CUSTOM', sort_order: 2 }));
    expect(api.listPeriods).toHaveBeenCalledTimes(2);
  });

  it('sends null optional rotation scope and re-loads the template list', async () => {
    render(<RotationTemplatesPage />);
    await screen.findByText('Medicine ward');
    expect(screen.getByText('Medicine · Internal Medicine')).toBeInTheDocument();
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'ICU' } });
    fireEvent.change(screen.getByPlaceholderText('Code'), { target: { value: 'ICU1' } });
    fireEvent.change(screen.getByDisplayValue('Program'), { target: { value: '4' } });
    fireEvent.change(screen.getByDisplayValue('Department'), { target: { value: '5' } });
    fireEvent.change(screen.getByPlaceholderText('Training year'), { target: { value: '2' } });
    fireEvent.change(screen.getByPlaceholderText('Duration weeks'), { target: { value: '8' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create Rotation Template' }));
    await waitFor(() => expect(api.createRotationTemplate).toHaveBeenCalledWith({ name: 'ICU', code: 'ICU1', program: 4, department: 5, training_year: 2, duration_weeks: 8, description: 'Scaffold only. Resident rotation scheduling will be added later.' }));
    expect(api.listRotationTemplates).toHaveBeenCalledTimes(2);
  });

  it('hides create forms for non-admins and clears failed initial loads', async () => {
    useAuthStore.mockReturnValue({ user: { role: 'RESIDENT' } });
    api.listPeriods.mockRejectedValue(new Error('offline'));
    api.getOptions.mockRejectedValue(new Error('offline'));
    render(<AcademicPeriodsPage />);
    await waitFor(() => expect(api.getOptions).toHaveBeenCalled());
    expect(screen.queryByRole('button', { name: 'Create Period' })).not.toBeInTheDocument();
    expect(screen.queryByText('Academic year')).not.toBeInTheDocument();
  });

  it('creates an evaluation template with explicit schema and scope defaults', async () => {
    render(<EvaluationTemplatesPage />);
    await screen.findByText('Mini-CEX');
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'DOPS' } });
    fireEvent.change(screen.getByPlaceholderText('Code'), { target: { value: 'DOPS1' } });
    fireEvent.change(screen.getByDisplayValue('SUPERVISOR_REVIEW'), { target: { value: 'DOPS' } });
    fireEvent.change(screen.getByDisplayValue('Program'), { target: { value: '4' } });
    fireEvent.change(screen.getByDisplayValue('Department'), { target: { value: '5' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create Evaluation Template' }));
    await waitFor(() => expect(api.createEvaluationTemplate).toHaveBeenCalledWith({ name: 'DOPS', code: 'DOPS1', form_type: 'DOPS', program: 4, department: 5, schema: {}, description: 'Template registry only. Evaluation submissions will be added later.' }));
    expect(api.listEvaluationTemplates).toHaveBeenCalledTimes(2);
  });

  it('creates a logbook category and keeps the category vocabulary intact', async () => {
    render(<LogbookCategoriesPage />);
    await screen.findByText('Procedures');
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Cases' } });
    fireEvent.change(screen.getByPlaceholderText('Code'), { target: { value: 'CASE1' } });
    fireEvent.change(screen.getByDisplayValue('CASE_LOG'), { target: { value: 'RESEARCH' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create Logbook Category' }));
    await waitFor(() => expect(api.createLogbookCategory).toHaveBeenCalledWith({ name: 'Cases', code: 'CASE1', category_type: 'RESEARCH', program: null, department: null, description: 'Category registry only. Logbook entries will be added later.' }));
    expect(api.listLogbookCategories).toHaveBeenCalledTimes(2);
  });
});
